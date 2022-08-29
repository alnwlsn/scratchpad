include <threads.scad>

z_layer				= 0.3;			// 3D print layer height (adjust if using different height !)

$fn					= 180;			// Polygons
draft				= 0.001;		// To make OpenSCAD's draft view look a bit nicer


r_bayonet_segments	= 23.6;			// Outer radius of the segments
r_bayonet_outer		= r_bayonet_segments+4;			// Outer radius of the bayonet base
z_bayonet_segments	= 2.3;			// Thickness of the segments
r_bayonet_inner		= 21.8;			// Inner radius of the segments
z_bayonet_base		= 4;			// Height of the bayonet base
z_flange_bayonet    = 3.2;          //from back of bayonet to flange face
funnel_thk          = 2;

z_topcap			= 4;			// Total height of the topcap
r_topcap_to_bayonet	= r_bayonet_segments-0.2; // Radius of the topcap part sinking into byonet tube

w_body				= 1;			// Bayonet tube wall thickness
z_bayonet_body		= 14-z_bayonet_base+z_topcap/2; // Height of the bayonet tube above bayonet base

r_slot				= r_bayonet_segments+1.1; // Spring lever slot radius
a_slot				= 45;			// Sping lever slot segment angle (degrees)
w_slot				= 0.3;			// Spring lever slot width

flgflg              = 28.674;       //flange to flange distance - 28.974 ideal
lcyex = 9;  //straight distance from lens side
scyex = 8;  //straight distance from sensor side
threadhole = 25.8;
threadh=scyex;


chamfer1_points=[
[r_bayonet_segments, 0],
[r_bayonet_inner-1, 1.5],
[r_bayonet_inner-1, 0],
];

funnel_points=[
[r_bayonet_segments,0],
[r_bayonet_segments, lcyex],
[threadhole/2,flgflg-scyex],
[threadhole/2,flgflg],
[(threadhole/2)+funnel_thk,flgflg],
[(threadhole/2)+funnel_thk,flgflg-scyex],
[r_bayonet_segments+funnel_thk,lcyex],
[r_bayonet_segments+funnel_thk,0]
];

union(){
    difference() {
        // Outer bayonet contour
        cylinder(r=r_bayonet_outer,h=z_bayonet_base);
        translate([0,0,-draft/2]) { // To make OpenSCAD's draft view look a bit nicer
            // Inner bayonet contour
            cylinder(r=r_bayonet_segments,h=z_bayonet_base+draft);
        }
    }
    difference(){
        union(){
            translate([0,0,z_flange_bayonet-z_bayonet_segments]) {
                rotate([0,0,35]) rotate_extrude(angle=50,convexity=2) translate([r_bayonet_inner+draft,0,0]) square([r_bayonet_segments-r_bayonet_inner+draft,z_bayonet_segments]);
                rotate([0,0,150]) rotate_extrude(angle=55,convexity=2) translate([r_bayonet_inner+draft,0,0]) square([r_bayonet_segments-r_bayonet_inner+draft,z_bayonet_segments]);
                rotate([0,0,265]) rotate_extrude(angle=55,convexity=2) translate([r_bayonet_inner+draft,0,0]) square([r_bayonet_segments-r_bayonet_inner+draft,z_bayonet_segments]);
            }
        }
        translate([0,0, z_flange_bayonet-z_bayonet_segments]) rotate_extrude() polygon(chamfer1_points);
    }
    translate([0,0, 0]) rotate_extrude() polygon(funnel_points);
    translate([0,0,flgflg-threadh])difference(){
      cylinder(d=threadhole,h=threadh);
      translate([0,0,-0.1])metric_thread (threadhole, 2, threadh+0.2, internal=true, leadin=2); 
    }
}



