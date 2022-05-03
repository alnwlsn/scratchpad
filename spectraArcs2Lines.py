#Alnwlsn 2021
#converts arcs (qarc) in spectra files output from topoR to line segments, so that Kicad can use them

inFilename = "main.ses" #input Spectra session file (output from TopoR)
outFilename = "out.ses" #output (modified) Spectra session file
segmentsPerRadian = 15 #use this many segments for each radian of arc
segmentsMinimum = 5 #use at least this many segments per arc

import re
import numpy as np

def circle3Point(tu): #not used, turns out that isn't how arcs in Spectra are specified
    # from 3 points, calculate a circle that passes through the 3 points
    # return the radius and center point
    # tuple ((x1,y1),(x2,y2),(x3,y3))
    # from the example here http://www.ambrsoft.com/TrigoCalc/Circle3D.htm
    a = (tu[0][0]*(tu[1][1]-tu[2][1]))-(tu[0][1]*(tu[1][0]-tu[2][0])) + \
        (tu[1][0]*tu[2][1])-(tu[2][0]*tu[1][1])
    b = (((tu[0][0]**2)+(tu[0][1]**2))*(tu[2][1]-tu[1][1]))+(((tu[1][0]**2)+(tu[1][1]**2))
                                                             * (tu[0][1]-tu[2][1]))+(((tu[2][0]**2)+(tu[2][1]**2))*(tu[1][1]-tu[0][1]))
    c = (((tu[0][0]**2)+(tu[0][1]**2))*(tu[1][0]-tu[2][0]))+(((tu[1][0]**2)+(tu[1][1]**2))
                                                             * (tu[2][0]-tu[0][0]))+(((tu[2][0]**2)+(tu[2][1]**2))*(tu[0][0]-tu[1][0]))
    d = (((tu[0][0]**2)+(tu[0][1]**2))*((tu[2][0]*tu[1][1])-(tu[1][0]*tu[2][1])))+(((tu[1][0]**2)+(tu[1][1]**2)) *
                                                                                   ((tu[0][0]*tu[2][1])-(tu[2][0]*tu[0][1])))+(((tu[2][0]**2)+(tu[2][1]**2))*((tu[1][0]*tu[0][1])-(tu[0][0]*tu[1][1])))
    r = np.sqrt(((b**2)+(c**2)-(4*a*d))/(4*(a**2)))
    cx = -b/(2*a)
    cy = -c/(2*a)
    return r, (cx, cy)


def paraCircle(tu):
    # gives x,y coords on circle given center point and radius, with t as angle (in radians)
    # https://en.wikipedia.org/wiki/Circle#Equations - parametric form
    # tuple (t,(r,(cx,cy)))
    x = tu[1][1][0] + tu[1][0]*np.cos(tu[0])
    y = tu[1][1][1] + tu[1][0]*np.sin(tu[0])
    return x, y


def paraAngle(tu):
    # returns the angle t from 0 radians to a point (x,y) on the circle (given radius and center)
    # tuple ((x,y),(r,(cx,cy))))
    # which is a greater distance, delta x or delta y?
    t = np.arctan2(tu[0][1]-tu[1][1][1], tu[0][0]-tu[1][1][0])
    return t

with open(inFilename) as f:  # read each line into a list
    content = f.readlines()
f.close()

g = open("out.ses", "w", newline="")

for l in content:
    m = re.search("            \(wire \(qarc", l)
    if m:
        # line with an arc
        # split line up on spaces (minus the first 12 characters, which are spaces)
        v = re.split("\s", l[12:])
        # now we have
        # print(v)
        layer = v[2]
        tracewidth = v[3]
        a = (int(v[4]), int(v[5]))  # first point
        c = (int(v[6]), int(v[7]))  # end point
        # trim the last 2 characters, which are "))""
        b = (int(v[8]), int(v[9][:-2])) #center of circle
        r = np.sqrt((((a[0]-b[0])**2)+((a[1]-b[1])**2))) #arc radius, as distance from start to center
        c1 = (r,b) #circle structure
        st = paraAngle((a, c1))  # arc start angle
        et = paraAngle((c, c1))  # arc end angle
        if(st>et): #ensure that the end is always greater 
            et+=2*np.pi
        
        # calculate number of steps
        dd = int(np.abs(st-et)*15 + 5) # lines for each radian + 5 lines minimum
        angs = np.linspace(st, et, dd)
        points = paraCircle((angs, c1))

        # linetxt = "            (wire (path "
        # linetxt += layer
        # linetxt += " "+tracewidth
        # linetxt += " "+str(a[0])
        # linetxt += " "+str(a[1])
        # linetxt += " "+str(b[0])
        # linetxt += " "+str(b[1])
        # linetxt += "))\r\n"
        # g.write(linetxt)

        for i in range(1, len(points[0])):
            linetxt = "            (wire (path "
            linetxt += layer
            linetxt += " "+tracewidth
            linetxt += " "+str(int(np.round(points[0][i-1])))
            linetxt += " "+str(int(np.round(points[1][i-1])))
            linetxt += " "+str(int(np.round(points[0][i])))
            linetxt += " "+str(int(np.round(points[1][i])))
            linetxt += "))\r\n"
            g.write(linetxt)

    else:
        g.write(l.strip('\n')+"\r\n")
        pass

g.close()
pass
