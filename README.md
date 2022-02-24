# pcbScripts
Scripts that I use to help design circuit boards (in KiCad)


## spectraArcs2Lines.py
I gave the topoR autorouter a try for my latest project for routing my traces, after designing the rest of my board in KiCad. To do this, you export a Spectra DSN file from KiCad, which you then import in topoR, do the autorouting, and then export a Spectra SES (session) file back to KiCad to put in all the traces.

I really like topoR's ability to route with arcs in addition to just line segments (mostly because it looks cooler), but it seems that KiCad does not like the arcs. I found that if I try importing the .ses file into KiCad after I'm done, all the trace segments show up, but the arcs are missing. TopoR allows you to "approximate arcs" on .ses export, but the results are quite low resolution, which ends up violating DRC and also looks pretty crappy, as bad as just using lines for autorouting in the first place. 

To get around this, I made this python script, which read in the exported .ses from topoR (with arcs) and converts them to a bunch of line segments (resolution adjustable) which KiCad can handle just fine.

## laserg ##
This is a quick hacky renderer for gcode that goes on my laser cutter (grbl). It will take a gcode file, and make an image of what would get cut.