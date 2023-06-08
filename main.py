import polyscope as ps
import numpy as np
import functions
import marching_squares as ms
import evaluation_grid as ev_grid
import function_visualization as func_visual
import sys # for printing max
import function_object as fob
import helper as helper

# some options
ps.set_program_name("first presentation main")
ps.set_verbosity(0)
ps.set_use_prefs_file(False)
ps.set_up_dir("z_up") 

ps.init()


helper.hlp.create_coordinate_axis()




# EXAMPLE LEVEL SETS START
center_x1 = 10
center_y1 = 10

unit_circle_SDF = functions.circle_SDF(center_x1+0,center_y1+0,1)
shifted_unit_circle_SDF = functions.circle_SDF(center_x1+0.8, center_y1+0.8, 0.8)
function1 = functions.union(unit_circle_SDF, shifted_unit_circle_SDF)


sidelength1 = 5
resolution1 = 0.01
resolution_step1 = 5

# isovalue 0
FOBfunction1a = fob.FOB(function1, 0, center_x1, center_y1, sidelength1, resolution1, resolution_step1)
name1a = "function1_a"
helper.hlp.ps_register_whole_FOB(FOBfunction1a, name1a)
# isovalue -0.5
FOBfunction1b = fob.FOB(function1, -0.5, center_x1, center_y1, sidelength1, resolution1, resolution_step1)
name1b = "function1_b"
helper.hlp.ps_register_whole_FOB(FOBfunction1b, name1b)
# isovalue 0.5
FOBfunction1c = fob.FOB(function1, 0.5, center_x1, center_y1, sidelength1, resolution1, resolution_step1)
name1c = "function1_c"
helper.hlp.ps_register_whole_FOB(FOBfunction1c, name1c)

# EXAMPLE LEVEL SETS END

"""
isocurve1 = ps.register_curve_network("isocurve1", FOBfunction1.isocurve_points, FOBfunction1.isocurve_edges)
FOBfunction1.compute_value_visuals()
value_mesh1 = ps.register_surface_mesh("value_mesh1", FOBfunction1.value_mesh_points, FOBfunction1.value_mesh_faces)
value_mesh1.add_color_quantity("value_mesh1_colors", FOBfunction1.value_mesh_colors, defined_on='faces', enabled=True)

value_plane1 = ps.register_surface_mesh("value_plane1", FOBfunction1.value_plane_points, FOBfunction1.value_mesh_faces)
value_plane1.add_color_quantity("value_plane1_colors", FOBfunction1.value_mesh_colors, defined_on='faces', enabled=True)
                                
"""
                                   






ps.show()