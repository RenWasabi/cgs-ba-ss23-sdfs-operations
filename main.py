import polyscope as ps
import numpy as np
import functions
import marching_squares as ms
import evaluation_grid as ev_grid
import function_visualization as func_visual
import sys # for printing max
import function_object as fob

# some options
ps.set_program_name("first presentation main")
ps.set_verbosity(0)
ps.set_use_prefs_file(False)
ps.set_up_dir("z_up") 

ps.init()

# create coordinate axis
axis_len = 1;
x_axis_nodes = np.array([[0,0,0], [axis_len,0,0]])
x_axis_edges = np.array([[0,1]])
x_axis_curve = ps.register_curve_network("x_axis", x_axis_nodes, x_axis_edges)

y_axis_nodes = np.array([[0,0,0], [0,axis_len,0]])
y_axis_edges = np.array([[0,1]])
y_axis_curve = ps.register_curve_network("y_axis", y_axis_nodes, y_axis_edges)

z_axis_nodes = np.array([[0,0,0], [0,0,axis_len]])
z_axis_edges = np.array([[0,1]])
z_axis_curve = ps.register_curve_network("z_axis", z_axis_nodes, z_axis_edges)






unit_circle = functions.circle_function(0,0,1)
shifted_unit_circle = functions.circle_function(0, 0.7, 1.25)

unit_circle_SDF = functions.circle_SDF(0,0,1)
shifted_unit_circle_SDF = functions.circle_SDF(0, 0.7, 1.25)

function1 = functions.intersection(unit_circle_SDF, shifted_unit_circle_SDF)
FOBfunction1 = fob.FOB(function1, 0, 0, 0, 4, 5)
isocurve1 = ps.register_curve_network("isocurve1", FOBfunction1.isocurve_points, FOBfunction1.isocurve_edges)
FOBfunction1.compute_value_visuals()
value_mesh1 = ps.register_surface_mesh("value_mesh1", FOBfunction1.value_mesh_points, FOBfunction1.value_mesh_faces)
value_mesh1.add_color_quantity("value_mesh1_colors", FOBfunction1.value_mesh_colors, defined_on='faces', enabled=True)
                                   
                                   






ps.show()