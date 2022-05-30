# takes a wav file, and generates a gcode toolpath for cartesian machines to cut a phonograph record

import matplotlib.pyplot as plt
from math import cos, sin, pi
from random import sample
import numpy as np
from scipy.io import wavfile


samplerate, data = wavfile.read('posthorn.wav')

drange = max(data) - min(data)
center = sum(data) / len(data)
data = (data-center) / (drange)  # map between -0.5 and 0.5

# User Vars

trackSpacing = 0.8
trackMaxWidth = 0.4
startDiam = 160
leadOutSpacing = 2
leadOutRotations = 1
leadInSpacing = 2
leadInRotations = 1

rpm = 78  # record rpm
spindleUp = 5
spindleDown = 0
spindleSpeed = 10000
spindleDelay = 5
feedRate = 50


###################

radsample = (2*pi*rpm)/(60*samplerate)  # radians per sample
radius = startDiam/2
x = []
y = []
rotation = 0
xp = 0
yp = 0
lRadius = radius
lRoation = rotation

# leadin groove
for revs in range(int((leadInRotations*(2*pi))/radsample)+1):
    rotation += radsample
    xp = (lRadius-(leadInSpacing*((rotation-lRoation)/(2*pi))))*cos(rotation)
    yp = (lRadius-(leadInSpacing*((rotation-lRoation)/(2*pi))))*sin(rotation)
    x.append(xp)
    y.append(yp)

lRadius = (lRadius-(leadInSpacing*((rotation-lRoation)/(2*pi))))
lRoation = rotation
for sample in data:
    rotation += radsample
    #print(sample, rotation)
    xp = (sample*trackMaxWidth+lRadius - (trackSpacing*((rotation-lRoation)/(2*pi))))*cos(rotation)
    yp = (sample*trackMaxWidth+lRadius - (trackSpacing*((rotation-lRoation)/(2*pi))))*sin(rotation)
    x.append(xp)
    y.append(yp)


# extra rev (leadout groove)
lRadius = (sample*trackMaxWidth+lRadius - (trackSpacing*((rotation-lRoation)/(2*pi))))
lRoation = rotation
for revs in range(int((leadOutRotations*(2*pi))/radsample)+1):
    rotation += radsample
    xp = (lRadius-(leadOutSpacing*((rotation-lRoation)/(2*pi))))*cos(rotation)
    yp = (lRadius-(leadOutSpacing*((rotation-lRoation)/(2*pi))))*sin(rotation)
    x.append(xp)
    y.append(yp)

# #stop groove
lRadius = (lRadius-(leadOutSpacing*((rotation-lRoation)/(2*pi))))
for revs in range(int((3*pi)/radsample)+1):
    rotation += radsample
    xp = lRadius*cos(rotation)
    yp = lRadius*sin(rotation)
    x.append(xp)
    y.append(yp)


f = open("record.nc", mode="w", newline='')
f.write("G0 Z{:.4f}\r\n".format(spindleUp))
f.write("G0 X{:.4f} Y{:.4f} S0\r\n".format(x[0], y[0]))  # go to start
f.write("M3 S{:.4f}\r\n".format(spindleSpeed))  # turn on spindle
f.write("G4 P"+str(spindleDelay)+"\r\n")  # wait for spindle
f.write("G1 Z{:.4f} F{:.4f}\r\n".format(spindleDown, feedRate))  # go down
for i in range(1, len(x)):
    f.write("G1 X{:.4f} Y{:.4f}\r\n".format(x[i], y[i]))  # cut sample
f.write("G0 Z{:.4f}\r\n".format(spindleUp))  # go up
f.write("M5\r\n")  # stop
f.close()

fig = plt.figure()
fig.patch.set_facecolor('black')
# plotting the points

fig.set_size_inches(4*3, 3*3)
ax = plt.gca()
linedata, = ax.plot(x, y)
ax.set_aspect('equal')
ax.set_facecolor("black")
ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white') 
ax.spines['right'].set_color('white')
ax.spines['left'].set_color('white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.tick_params(colors='white', which='both')  # 'both' refers to minor and major axes
plt.title('The whole thing', color='white')
plt.savefig('images/record-matplot.png', dpi=100)