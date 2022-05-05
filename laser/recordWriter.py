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

trackSpacing = 1
trackMaxWidth = 0.5
startDiam = 100

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
for sample in data:
    rotation += radsample
    #print(sample, rotation)
    xp = (sample*trackMaxWidth+radius -
          (trackSpacing*(rotation/(2*pi))))*cos(rotation)
    yp = (sample*trackMaxWidth+radius -
          (trackSpacing*(rotation/(2*pi))))*sin(rotation)
    x.append(xp)
    y.append(yp)


# extra rev (leadout groove)
for revs in range(int((2*pi)/radsample)+1):
    rotation += radsample
    xp = (radius-(trackSpacing*(rotation/(2*pi))))*cos(rotation)
    yp = (radius-(trackSpacing*(rotation/(2*pi))))*sin(rotation)
    x.append(xp)
    y.append(yp)

# #stop groove
lRoation = rotation
for revs in range(int((3*pi)/radsample)+1):
    rotation += radsample
    xp = (sample*trackMaxWidth+radius -
          (trackSpacing*(lRoation/(2*pi))))*cos(rotation)
    yp = (sample*trackMaxWidth+radius -
          (trackSpacing*(lRoation/(2*pi))))*sin(rotation)
    x.append(xp)
    y.append(yp)


f = open("record.nc", mode="w", newline='')
f.write("G0 Z{:.4f}\r\n".format(spindleUp))
f.write("G0 X{:.4f} Y{:.4f} S0\r\n".format(x[0], y[0]))  # go to start
f.write("M3\r\n")  # turn on spindle
f.write("G4 P"+str(spindleDelay)+"\r\n")  # wait for spindle
f.write("G1 Z{:.4f} F{:.4f}\r\n".format(spindleDown, feedRate))  # go down
for i in range(1, len(x)):
    f.write("G1 X{:.4f} Y{:.4f}\r\n".format(x[i], y[i]))  #cut sample
f.write("G0 Z{:.4f}\r\n".format(spindleUp)) #go up
f.write("M5\r\n") #stop
f.close()

# plotting the points
plt.plot(x, y)

# # naming the x axis
# plt.xlabel('x - axis')
# # naming the y axis
# plt.ylabel('y - axis')

# # giving a title to my graph
# plt.title('My first graph!')

# function to show the plot
plt.gca().set_aspect('equal')
plt.show()
