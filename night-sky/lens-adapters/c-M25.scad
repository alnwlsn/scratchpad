 use <threads.scad>

$fn = 40;


difference()
{
    union()
    {
        //flange edge
        translate([0,0,-5]) cylinder(d=32,h=5);
        // 1" diameter, 32tpi cs-mount adaptor
        english_thread(0.985, 32, 0.15, internal=false);
        
        //"M25-2" thread
        translate([0,0,-5-8]) metric_thread (25, 2, 8, internal=false); 
       
    }
    
    
    //center hole
    translate([0,0,-5-8]) cylinder(d=17,h=34,center=true);
    
    //grips around the edges
    pips = 67;
    translate([0,0,-5.1]) linear_extrude(5.2) union() {
        for(i = [0 : (pips-1)])
           rotate(i * (360/pips))
                translate([0, 32.5 / 2])
                    circle(d = 1);
    }
    
    //translate([0,0,-5+2]) cylinder(d=25,h=3);
    
}
