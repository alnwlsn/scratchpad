# gcode rasterizer for laser cutting
# makes gcode to send to laser cutter for burning
# Alnwlsn 2022-02-24

linesPerMM = 2
imageHeightMM = 30 #scale vertical size of image
headStart = 5 #extra mm to go back at beginning of line to get a running start (overscan)
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
    lastPixel = 0
    f.write("G1 X{:.4f}\r\n".format(round(centerX-(wMM/2),4)))
    for i in range(im2.size[0]):
        pixel = 255-pixels[i,j]
        skipFlag = False
        #peek next pixel to see if it is the same color:
        if(i+1<im2.size[0]):
            pixelF = 255-pixels[i+1,j]
            if(pixelF==pixel):
                skipFlag = True
        else:
            if(pixel == 0): #if last pixel is white
                skipFlag = True
        if(skipFlag==False):
            f.write("G1 X{:.4f} S{:d}\r\n".format(round(centerX-(wMM/2)+(i+1)/linesPerMM,4),pixel))
        # print(pixel)
    f.write("G1 X{:.4f} S0\r\n".format(round(centerX+(wMM/2)+tailStop,4)))

    # break

f.close()

import laserRender
laserRender