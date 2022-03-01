# gcode rasterizer for laser cutting
# makes gcode to send to laser cutter for burning
# targeted for my mostly-stock GRBL K40 conversion
# Alnwlsn 2022-02-27

from PIL import Image, ImageOps

# user settings ***************************

imageFilename = "in2.png"

linesPerMM = 3
imageHeightMM = 50  # scale vertical size of image
# extra mm to go back at beginning of line to get a running start (overscan)
headStart = 10
tailStop = 3  # extra mm to go after

# center of image in work coords - offet assuming the origin of the workspace is in the lower left corner; offset is up and to the right
centerX = 154  # also in mm
centerY = 117


laserMin = 250  # scaling for your laser's S parameter. Note that image values of white will still go as S0
laserMax = 600

feedRate = 900

blackAndWhite = True  # set to True for just 2 value. Black will be burned at laserMax
blackAndWhiteThresh = 128  # the value at which to divide pixels into black or white

# end settings ***************************

im = Image.open(imageFilename)
f = open("out.nc", mode="w", newline='')

f.write("M3\r\n")  # turn on laser
f.write("F"+str(feedRate)+"\r\n")  # turn on laser

w, h = im.size
aspect = w/h
sh = imageHeightMM * linesPerMM
sw = sh*aspect
im2 = im.resize((int(sw), int(sh))) #scale down the image, so one line of pixels = one laser line
im2 = ImageOps.grayscale(im2)
wMM = im2.size[0]/linesPerMM
hMM = im2.size[1]/linesPerMM
def ps(x): return 0 if(x == 0) else int(((x/255))*(laserMax-laserMin)+laserMin)


if(blackAndWhite):
    def fn(x): return 255 if x > blackAndWhiteThresh else 0
    im2 = im2.convert('L').point(fn, mode='1')

pixels = im2.load()

for j in range(im2.size[1]):
    skipWholeLine = False
    # search for the first burning pixel
    fp = 0
    while(fp < im2.size[0]):
        if(255-pixels[fp, j] > 0):
            break
        fp += 1
    if(fp == im2.size[0]):  # no need to do anything on the line if it is white
        skipWholeLine = True

    if(not skipWholeLine):
        # f.write("S0\r\n")
        # keep track of this; if we skip white with G0, we need to know where we skip from
        lastX = centerX-(wMM/2)+(fp)/linesPerMM
        f.write("G0 X{:.4f} Y{:.4f} S0\r\n".format(round(
            lastX-headStart, 4), round(((im2.size[1]-1-j)/linesPerMM)-(hMM/2)+centerY, 4)))
        f.write("G1 X{:.4f} S0\r\n".format(round(lastX, 4)))
        whiteSkipCount = 0
        firstG1Skip = True
        for i in range(fp-1, im2.size[0]):
            pixel = 255-pixels[i, j]

            # skipping - we don't need to write a gcode line again if the same laser power is being used
            skipFlag = False
            # peek next pixel to see if it is the same color:
            if(i+1 < im2.size[0]):  # make sure we aren't past the end
                pixelF = 255-pixels[i+1, j]
                if(pixelF == pixel):
                    skipFlag = True
            else:
                if(pixel == 0):  # if last pixel is white
                    skipFlag = True
            if(skipFlag == False):
                thisX = centerX-(wMM/2)+(i+1)/linesPerMM
                if(whiteSkipCount/linesPerMM >= headStart+(tailStop*2)):
                    f.write("G1 X{:.4f} S0\r\n".format(
                        round(lastX+tailStop, 4)))
                    f.write("G0 X{:.4f}\r\n".format(round(thisX-headStart, 4)))
                if(thisX > lastX):  # eliminates doubling of gcode at the beginning of the line
                    f.write("G1 X{:.4f} S{:d}\r\n".format(
                        round(thisX, 4), ps(pixel)))
                lastX = thisX
                whiteSkipCount = 0
            else:
                if(pixel == 0):
                    whiteSkipCount += 1
        f.write("G1 X{:.4f} S0\r\n".format(round(lastX+tailStop, 4)))

f.write("M5\r\n")  # turn off laser
f.close()

import laserRender #lazy way to run the renderer afterwards