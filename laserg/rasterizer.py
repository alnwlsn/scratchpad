# gcode rasterizer for laser cutting
# makes gcode to send to laser cutter for burning
# Alnwlsn 2022-02-27

linesPerMM = 2
imageHeightMM = 30 #scale vertical size of image
headStart = 2 #extra mm to go back at beginning of line to get a running start (overscan)
tailStop = 2 #extra mm to go after

#center of image in work coords - offet assuming the origin of the workspace is in the lower left corner; offset is up and to the right
centerX = 50 #also in mm
centerY = 35

laserMin = 0    #scaling for your laser's S parameter. Note that image values of white will still go as S0
laserMax = 4095

blackAndWhite = True #set to True for just 2 value. Black will be burned at laserMax
blackAndWhiteThresh = 128 #the value at which to divide pixels into black or white

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
ps = lambda x: 0 if(x == 0) else int(((x/255))*(laserMax-laserMin)+laserMin)

if(blackAndWhite):
    fn = lambda x : 255 if x > blackAndWhiteThresh else 0
    im2 = im2.convert('L').point(fn, mode='1')

pixels = im2.load()



for j in range(im2.size[1]):
    skipWholeLine = False
    #search for the first burning pixel
    fp = 0
    while(fp<im2.size[0]):
        if(255-pixels[fp,j]>0):
            break
        fp += 1
    if(fp==im2.size[0]): #no need to do anything on the line if it is white
        skipWholeLine = True

    if(not skipWholeLine):        
        # f.write("S0\r\n")
        lastX = centerX-(wMM/2)+(fp+1)/linesPerMM #keep track of this; if we skip white with G0, we need to know where we skip from
        f.write("G0 X{:.4f} Y{:.4f} S0\r\n".format(round(lastX-headStart,4),round(((im2.size[1]-1-j)/linesPerMM)-(hMM/2)+centerY,4)))
        f.write("G1 X{:.4f} S0\r\n".format(round(lastX,4))) 
        whiteSkipCount = 0
        
        for i in range(fp-1,im2.size[0]):
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
                    f.write("G1 X{:.4f} S0\r\n".format(round(lastX+tailStop,4)))
                    f.write("G0 X{:.4f}\r\n".format(round(thisX-headStart,4)))
                f.write("G1 X{:.4f} S{:d}\r\n".format(round(thisX,4),ps(pixel)))
                lastX = thisX
                whiteSkipCount = 0
            else:
                if(pixel==0):
                    whiteSkipCount += 1 
            # print(pixel)
        f.write("G1 X{:.4f} S0\r\n".format(round(lastX+tailStop,4)))

    # if(j==5):
    #     break

f.close()

import laserRender