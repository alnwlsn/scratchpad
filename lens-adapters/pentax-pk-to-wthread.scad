$fa=4;
$fs=0.4;

r_outer = 26;

include <mft.scad>
include <threads.scad>

// difference of systems relative to base plate
// https://de.wikipedia.org/wiki/Auflagema%C3%9F
// M4/3  19.25
// Pentax "K" 45.46
h_adapt = 45.46-19.25-h1; // 26.21-1

wthk = 2*1.6;

pk_r_cent = 48.5/2+0.1;
pk_r_snap = 45/2;
pk_r_outer = r_outer;
pk_r_inner = pk_r_outer - wthk;
pk_r_base = 58/2;

pk_h1 = 1;
pk_h2 = 3.6;  // 

pk_h_foot = 2.5;

aa = -360/113;
a1 =  1 *aa;
a1d = (20-1)*aa;
a2 =  40*aa;
a2d = (54-40)*aa;
a3 =  74*aa;
a3d = (95-74)*aa;

// anti-reflexion ring  
pk_rx = r_inner;
pk_hx = (pk_r_cent-pk_rx)/2;
pk_hr1 = 11;
pk_hr2 = pk_hr1+pk_hx;

flgflg = 27.6; //from flange to flange
lcyex = 10;  //straight distance from lens side
scyex = 8;  //straight distance from sensor side
threadhole = 25.8;
threadthk = 2*1.6;
threadh=scyex;


// shape of the MD part
pk_points=[
[pk_r_cent, 0],

// outer shape
[pk_r_base, 0],
[pk_r_base, pk_h_foot],
[pk_r_outer, pk_h_foot],
[pk_r_outer, lcyex],

[((threadthk+threadhole)/2), flgflg-scyex],
[((threadthk+threadhole)/2), flgflg],
[threadhole/2, flgflg],
[threadhole/2, flgflg],
[(threadhole)/2, flgflg-scyex],
[(threadthk+threadhole-wthk)/2, flgflg-scyex],



[pk_r_cent, lcyex],
[pk_r_cent, 0],
//[r_outer, h_adapt],
//
//// inner shape
//[r_inner, h_adapt],
//[pk_r_inner, h_adapt-(pk_r_inner-r_inner)/2],
//
//// anti-reflexion ring
//[pk_r_inner, pk_hr1+0.8],
//[pk_r_cent, pk_hr1+0.8],
//[r_inner, pk_hr2+0.4],
//[r_inner, pk_hr2],



//[pk_r_cent, h_adapt-(pk_r_cent-r_inner)/2],

];


pk_points_snap=[
[pk_r_cent+.1, pk_h2],
[pk_r_cent+.1, pk_h1+0.1],
[pk_r_snap, pk_h1+0.7],
[pk_r_snap, pk_h2],
];


module snap_shaper()
{
  translate([pk_r_cent-2.5,0,pk_h1+1.5])
    rotate([0,0,45])
      cube([3,3,3],center=true);
}

module snapper(ang)
{
  difference()
  {
    rotate_extrude(angle=ang)
    polygon(pk_points_snap);

    snap_shaper();

    rotate([0,0,ang])
      snap_shaper();
  }
}

module snappers()
{
  union()
  {
    rotate([0,0,a1+120])
      snapper(a1d);
    
    rotate([0,0,a2+120])
      snapper(a2d);
    
    rotate([0,0,a3+120])
      snapper(a3d);
  }

// bayonett turn limiter
  //rotate([0,0,a3+a3d])
  rotate([0,0,a1-a1d])
    translate([-pk_r_cent,0,pk_h2])
      cylinder(r=1.7,h=3);

 
}

module screw_hole()
{
    rotate([0,0,-88])
  translate([0,0,pk_h2+1.3])
      rotate([90,0,0])
        cylinder(r=1.3,h=30);
}

module screw_strenghener()
{
    rotate([0,0,-88])
  translate([0,-r_outer+0.5,pk_h2+1.3])
      rotate([90,0,0])
        cylinder(r=3,h=2.5);
}




module md()
{
  difference()
  {
    union()
    {
      // basic shape
      rotate_extrude()
        polygon(pk_points);
      
      // the 3 snappers
      snappers();      
      //screw_strenghener();
    }
      // red-dot-marker
      rotate([0,0,-55])
        translate([-pk_r_base,0,0])
          cylinder(r=2,h=pk_h_foot+1); 
    //screw_hole();
  }
}
// finally, put together telescope part and mft part

union()
{
//  translate([0,0,h_adapt])
//    mft();

  md();
  translate([0,0,flgflg-threadh])difference(){
      cylinder(d=threadhole,h=threadh);
      translate([0,0,-0.1])metric_thread (threadhole, 2, threadh+0.2, internal=true, leadin=2); 
  }
}


//snappers();