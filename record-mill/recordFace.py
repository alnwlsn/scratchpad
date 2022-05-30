# for facing the record surface to be cut before engraving (annular ring pocket, spiral cut)

import matplotlib.pyplot as plt
from math import cos, sin, pi

# User Vars

trackSpacing = 2
startDiam = 160
stopDiam = 30
surfaceDepth = -0.5

centerHoleDiam = 7.2-(3.18) #minus tool diameter
centerHoleDepth = -1

spindleUp = 5
spindleSpeed = 10000
spindleDelay = 5
feedRate = 300

radsample = 0.03  # radians per line segment


###################

f = open("recordFace.nc", mode="w", newline='')
f.write("G0 Z{:.4f}\r\n".format(spindleUp))
f.write("G0 X{:.4f} Y{:.4f} S0\r\n".format(0, 0))  # go to center
f.write("M3 S{:.4f}\r\n".format(spindleSpeed))  # turn on spindle
f.write("G4 P"+str(spindleDelay)+"\r\n")  # wait for spindle
f.write("G1 Z{:.4f} F{:.4f}\r\n".format(centerHoleDepth, feedRate))  # go down


radius = centerHoleDiam/2
x = []
y = []
rotation = 0
xp = 0
yp = 0

# center hole
for revs in range(int((2.1*pi)/radsample)+1):
    rotation += radsample
    xp = radius*cos(rotation)
    yp = radius*sin(rotation)
    x.append(xp)
    y.append(yp)

for i in range(1, len(x)):
    f.write("G1 X{:.4f} Y{:.4f}\r\n".format(x[i], y[i]))  # cut center hole
f.write("G1 X{:.4f} Y{:.4f}\r\n".format(0, 0))  # go to center
f.write("G0 Z{:.4f}\r\n".format(spindleUp)) #go up

radius = startDiam/2
x = []
y = []
rotation = 0
xp = 0
yp = 0

# start circle
lRoation = rotation
for revs in range(int((2.1*pi)/radsample)+1):
    rotation += radsample
    xp = radius*cos(rotation)
    yp = radius*sin(rotation)
    x.append(xp)
    y.append(yp)

#main surface
currentRadius = radius
stopRadius = stopDiam/2
lRoation = rotation
while currentRadius >= stopRadius:
    rotation += radsample
    #print(sample, rotation)
    currentRadius = radius - ((trackSpacing*((rotation-lRoation)/(2*pi))))
    xp = currentRadius*cos(rotation)
    yp = currentRadius*sin(rotation)
    x.append(xp)
    y.append(yp)

# end circle
lRoation = rotation
for revs in range(int((2.1*pi)/radsample)+1):
    rotation += radsample
    xp = stopRadius*cos(rotation)
    yp = stopRadius*sin(rotation)
    x.append(xp)
    y.append(yp)

f.write("G0 X{:.4f} Y{:.4f}\r\n".format(x[0], y[0]))  # go to start
f.write("G1 Z{:.4f} F{:.4f}\r\n".format(surfaceDepth, feedRate))  # go down
for i in range(1, len(x)):
    f.write("G1 X{:.4f} Y{:.4f}\r\n".format(x[i], y[i]))  # cut surface
f.write("G0 Z{:.4f}\r\n".format(spindleUp))  # go up
f.write("M5\r\n")  # stop
f.close()
