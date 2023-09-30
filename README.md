# scratchpad #
Files and small projects which are too tiny to have their own repo.

## spectraArcs2Lines.py
I gave the topoR autorouter a try for my latest project for routing my traces, after designing the rest of my board in KiCad. To do this, you export a Spectra DSN file from KiCad, which you then import in topoR, do the autorouting, and then export a Spectra SES (session) file back to KiCad to put in all the traces.

I really like topoR's ability to route with arcs in addition to just line segments (mostly because it looks cooler), but it seems that KiCad does not like the arcs. I found that if I try importing the .ses file into KiCad after I'm done, all the trace segments show up, but the arcs are missing. TopoR allows you to "approximate arcs" on .ses export, but the results are quite low resolution, which ends up violating DRC and also looks pretty crappy, as bad as just using lines for autorouting in the first place. 

To get around this, I made this python script, which read in the exported .ses from topoR (with arcs) and converts them to a bunch of line segments (resolution adjustable) which KiCad can handle just fine.

# laser #
Stuff for my laser engravers / cutter. Both run GRBL, and use the Spindle functions to control the lasers - M3/4 & M5 to turn laser on / off, and S to control the laser power.

## rasterizer.py ##
I was not satisfied with any of the rasterizer programs quickly accessible to the would-be laser enthusiast. I tried 2 - LaserWeb and LaserGRBL. I also know there's one for Inkscape - for which I didn't want to approach the learning curve. Not wanting to go for a commercial program, I decided to write one myself. It probably isn;t good for everything, but it does do these:

* Unidirectional engraving (left to right, in X only) - my laser seemed to have trouble going in both directions. LaserWeb doesn't do this.
* Uses G0 (rapid) on the retun stroke - saves time. LaserGRBL doesn't do this, it feeds back the same as the forwards direction (and also doen't seem to turn off the laser all the way?)
* Start moving before the laser cut, so the head can get up to speed. Aka "Overscan". LaserGRBL doesn't do this - it turns on the laser at the exact same time that the laser is supossed to be moving. Because the head is mechanical (and there is accelleration built into GRBL), it takes some time to get moving, especially if you don't want your steppers to skip steps. This otherwise leads to distorition along the starting edge of your image.
* Skip areas of the image that don't need to be cut with G0. LaserGRBL is supossed to do this, but it dson't implement any overscan.
* Compress the same colors within a line into one line of gcode. Example, if I have a line that is 50px of power S300, it will produce one line of gcode for the length of that line, instead of 50 lines for 50 small segments. I think most existing rasterizers already do this.

todo - add "burn white" or otherwise turn off the G0 white skip function

## laserRender.py ##
I needed a preview output for the gcode that the rasterizer program produces, so I could see what I was doing. Pretty uncomplicated, just reads a gcode file and draws on a blank image the Gcode moves as a laser would. Black/grey traces go where the laser would burn (at power), green lines are where there is a G1 move, but at S0 (otherwise it would draw a white line and possibly overwrite something), and red lines for G0 rapid moves.

## chatgpt.py ##
This is a simple interface to use chatGPT from a terminal. It doesn't use the API, instead, it uses Selenium and drives a chromium browser with the chat.openai.com site open, with you already logged in. Probably of little use to most people, but who knows. You'll need chromium, chromedriver, python and selenium.

## ttylynx ##
Bash script that forms a rudimentary command line interface to read and navigate web pages from a command line interface which has no cursor control. Optimized for a hard copy teletype, [like my converted Selectric II](https://www.youtube.com/watch?v=1kXnsvYfaF4), where printing things takes a long time. Uses lynx to render web pages, and wget / jp2a to view JPG images as ascii art. Works a bit like the original CERN LineModeBrowser

## trs804kb ##
This is a backlate for @jaycrutti's TRS-80 Model 4 keyboard [replacement](https://www.jaycrutti.com/hardware-projects/tandy-trs-80-model-4-replacement-keyboard) using modern mechanical keyswitches.
