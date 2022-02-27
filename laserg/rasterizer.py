# gcode rasterizer for laser cutting
# makes gcode to send to laser cutter for burning
# Alnwlsn 2022-02-24

linesPerMM = 2
imageHeightMM = 30 #scale vertical size of image
headStart = 2 #extra mm to go back at beginning of line to get a running start (overscan)
tailStop = 2 #extra mm to go after

#center of image - offet assuming the origin of the workspace is in the lower left corner; offset is up and to the right
centerX = 50 #also in mm
centerY = 35

from PIL import Image, ImageOps

im = Image.open("in2.png")
f = open("out.nc", mode="w", newline='')

f.write("M3\r\n") #turn on laser

w,h = im.size
aspect = w/h

sh = imageHeightMM * linesPerMM
sw = sh*aspect

im2 = im.resize((int(sw),int(sh)))
im2 = ImageOps.grayscale(im2)
wMM = im2.size[0]/linesPerMM
hMM = im2.size[1]/linesPerMM
pixels = im2.load()
for j in range(im2.size[1]):
    # f.write("S0\r\n")
    f.write("G0 X{:.4f} Y{:.4f} S0\r\n".format(round(centerX-(wMM/2)-headStart,4),round(((im2.size[1]-1-j)/linesPerMM)-(hMM/2)+centerY,4)))
    # f.write("G1 X{:.4f}\r\n".format(round(centerX-(wMM/2),4))) not actually needed
    whiteSkipCount = 0
    lastX = centerX-(wMM/2)-headStart #keep track of this; if we skip white with G0, we need to know where we skip from
    for i in range(im2.size[0]):
        pixel = 255-pixels[i,j]
        
        #skipping - we don't need to write a gcode line again if the same laser power is being used
        skipFlag = False
        #peek next pixel to see if it is the same color:
        if(i+1<im2.size[0]): #make sure we aren't past the end
            pixelF = 255-pixels[i+1,j]
            if(pixelF==pixel):
                skipFlag = True
        else:
            if(pixel == 0): #if last pixel is white
                skipFlag = True
        if(skipFlag==False):
            thisX = centerX-(wMM/2)+(i+1)/linesPerMM
            if(whiteSkipCount/linesPerMM>=headStart+(tailStop*2)):
                print(i, "skip possible", lastX, thisX)
                f.write("G1 X{:.4f} S0\r\n".format(round(lastX+tailStop,4)))
                f.write("G0 X{:.4f}\r\n".format(round(thisX-headStart,4)))
            f.write("G1 X{:.4f} S{:d}\r\n".format(round(thisX,4),pixel))
            lastX = thisX
            whiteSkipCount = 0
        else:
            if(pixel==0):
                whiteSkipCount += 1
        
        # print(pixel)
    f.write("G1 X{:.4f} S0\r\n".format(round(centerX+(wMM/2)+tailStop,4)))

    # break

f.close()

import laserRender