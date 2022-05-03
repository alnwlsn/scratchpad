# takes a wav file, and generates a gcode toolpath for cartesian machines to cut a phonograph record

import matplotlib.pyplot as plt
from math import cos, sin, pi
from random import sample
import numpy as np
from scipy.io import wavfile


samplerate, data = wavfile.read('posthorn.wav')

range = max(data) - min(data)
center = sum(data) / len(data)
data = (data-center) / (range)  # map between -0.5 and 0.5

trackSpacing = 1
trackMaxWidth = 0.2
startDiam = 100

rpm = 78  # record rpm
radsample = (2*pi*rpm)/(60*samplerate)
radius = startDiam/2
x = []
y = []

rotation = 0
for sample in data:
    rotation += radsample
    #print(sample, rotation)
    xp = (sample*trackMaxWidth+radius-(trackSpacing*(rotation/(2*pi))))*cos(rotation)
    yp = (sample*trackMaxWidth+radius-(trackSpacing*(rotation/(2*pi))))*sin(rotation)
    x.append(xp)
    y.append(yp)

# plotting the points
plt.plot(x, y)

# # naming the x axis
# plt.xlabel('x - axis')
# # naming the y axis
# plt.ylabel('y - axis')

# # giving a title to my graph
# plt.title('My first graph!')

# function to show the plot
plt.show()
