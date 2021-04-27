;set print bed temperature to 50 degrees celsius
M140 S50 
;wait for the print bed temp to reach 50 degrees
M190 S50
;set extruder temperature to 200 degrees celsius
M104 S200
;wait for extruder temp to reach desired temp
M109 S200
;start of print
;G1 = move to XYZ position and extrude E mm 
G1 F611.8 X112.2 Y111 E0.35256
G1 X112.2 Y100.4 E0.70511
G1 X122.8 Y100.4 E1.05767
G1 X122.8 Y111 E1.41023
;end of print
;set temperatures to 0 degrees 
M140 S0
M104 S0

