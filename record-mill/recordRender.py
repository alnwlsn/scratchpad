# Hacked laserRender.py for rendering the record cut toolpath

# gcode renderer for laser cutter gcode files
# makes an image of what the laser cutter would cut if sent to the laser cutter
# pays attention to GRBL G1 and G0 codes, in this format
#   Gn Xnnn Ynnn Snnn

# Alnwlsn 2022-02-23

# probably doesn't handle some edge cases, but whatever

from PIL import Image, ImageDraw, ImageOps

# define bed shape. Origin is always in lower left corner, inset by bedborder
bedx = 150  # units mm
bedy = 150
bedborder = 5  # extra space to draw around image, in mm
linewidthMM = 0.3

linewidthMoveMM = 0.05  # line size for moves

rapidColor = (255, 0, 0)  # g0 moves
offColor = (0, 255, 0)  # g1 moves with laser off

pixelsPerMM = 50

laserMin = 0  # scaling for your gcode S parameter.
laserMax = 255

# end settings

dimX = (bedx+(bedborder*2))*pixelsPerMM
dimY = (bedy+(bedborder*2))*pixelsPerMM

img = Image.new('RGB', (dimX, dimY), (0, 255, 255))
dr = ImageDraw.Draw(img)


xl = 0
yl = 0


def ps(x): return 0 if(x == 0) else int(255*((x-laserMin)/(laserMax-laserMin)))


# draws a line from the last point to x,y with intensity intn(0-255).
def drawLine(x, y, type, intn):
    global xl, yl

    lw = linewidthMM
    color = (0, 0, 0)

    if(type == 0):  # burn / draw move
        inti = int(255 - intn)  # intensity (255 = black)
        color = (inti, inti, inti)

    if(type == 1):  # rapid G0 move
        color = rapidColor
        lw = linewidthMoveMM

    if(type == 2):  # G1 with laser off
        color = offColor
        lw = linewidthMoveMM

    linewidthPx = int(pixelsPerMM*lw)

    x1 = (x+bedborder)*pixelsPerMM
    y1 = ((bedy+(bedborder*2)-y)-bedborder)*pixelsPerMM

    dr.line((x1, y1, xl, yl), width=linewidthPx, fill=color)
    radius = linewidthPx/2
    dr.ellipse((x1 - radius + 1, y1 - radius + 1, x1 + radius -
                1, y1 + radius - 1), fill=color, outline=None)
    dr.ellipse((xl - radius + 1, yl - radius + 1, xl + radius -
                1, yl + radius - 1), fill=color, outline=None)

    yl = y1
    xl = x1


dr.rectangle((0, 0, dimX, dimY), fill=(255, 255, 255))  # blank image
drawLine(0, 0, 1, 0)  # go to home


with open("record.nc") as file:
    lines = file.readlines()

xgo = 0
ygo = 0
sgo = 0  # S spindle - for the laser power
mstate = 0  # 1 for laser on, 0 if off (not the actual m code)

lineLockoutCount = 0
lineLockout = 4

for line in lines:
    segs = line.split()  # split on whitespace
    gen = 0  # don't do any moves until we are sure this is a g1 or g0
    for seg in segs:  # look at elements in line
        if(seg[0] == 'M'):
            # this is a mcode
            g = int(seg[1:])
            if(g == 3 or g == 4):  # spindle (laser) on
                mstate = 1
            elif(g == 5):  # off
                mstate = 0
        elif(seg[0] == 'G'):
            # this is a gcode
            g = int(seg[1:])
            if(g == 0 or g == 1):  # positioning command
                gen = g+1  # this is a g move command
                # hack - lock out the first few lines from drawing as cut
                if(lineLockoutCount < lineLockout):
                    lineLockoutCount += 1
                    if(lineLockoutCount >= lineLockout):
                        sgo = 255
        if(gen and seg[0] == 'X'):
            xgo = float(seg[1:])
        if(gen and seg[0] == 'Y'):
            ygo = float(seg[1:])
        # if(seg[0] == 'S'):
        #     sgo = float(seg[1:])
    if(gen == 1):  # G0 rapid move
        drawLine(xgo, ygo, 1, 0)
    if(gen == 2):  # draw of some kind
        if(sgo > 0 and mstate == 1):  # laser is on
            drawLine(xgo+(bedx/2), ygo+(bedy/2), 0, ps(sgo))
        else:  # laser is off
            drawLine(xgo+(bedx/2), ygo+(bedy/2), 2, 0)

img = ImageOps.invert(img)

img.save("record.png")
