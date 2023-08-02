import polyscope as ps
import numpy as np
import functions
import marching_squares as ms
import evaluation_grid as ev_grid
import function_visualization as func_visual
import sys # for printing max


# todo
# - implement linear interpolation for the marching squares cut
# - implement the marching squares situation in which there is two cuts in one square
# - improve marching squares performance
#
# - implement smooth version of math functions for Boolean operations (+ research)
# - fully implement batman function
# - currently I'm just using any implicit functions -> use signed distance functions
#
# - visualize SDF (function/distance) values
# - mesh coloring with LERP
# - use vectors for x y coordinates
#
# project isonlines to bottom plane instead of current one


# some options
ps.set_program_name("initial polyscope test")
ps.set_verbosity(0)
ps.set_use_prefs_file(False)
ps.set_up_dir("z_up") 

# Initialize polyscope, creating graphics contexts and constructing a window.
# Should be called exactly once.
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


# basic program flow:
# - create an evalutation grid to discretely evaluate an implicit function on
# - use marching squares on this evaluation grid with a specified function:
#   - retrieve an isocurve at the specified isovalue (points and edges -> curve)
#   - fill the evaluation_grid[.,.,!] with correct function values
# - visualize the function as a mesh using the evaluation grid
# - color this mesh based on whether the function values are positive or negative

# - one "object" works on
# - IN:
# - evaluation_grid
#   - center x, y coordinates
#   - sidelength
#   - resolution
# - function
# - isovalue
#
# - USE MARCHING SQUARES
#
# - OUT A: ISOCURVE
# - isocurve_points, isocurve_edges
#   (-> polyscope curve network)
# - OUT B: VALUE MESH
# - resolution step
# - value_mesh_points
# - value_mesh_edges
# - value_mesh_faces 
# - value_mesh_colors
#   (-> polyscope surface mesh)


# create the grid to discretely evaluate the function on
# format: [x_position, y_position, function_value]
vertice_grid = ev_grid.evaluation_grid().create_vertice_grid(0,0,4,0.01)




# use marching squares on a function

unit_circle = functions.circle_function(0,0,1)
shifted_unit_circle = functions.circle_function(0, 0.7, 1.25)
#squares_circles_subtract = ms.MS_Grid(vertice_grid, 0, functions.subtract(unit_circle, shifted_unit_circle))

unit_circle_SDF = functions.circle_SDF(0,0,1)
shifted_unit_circle_SDF = functions.circle_SDF(0, 0.7, 1.25)
#squares_circles_subtract = ms.MS_Grid(vertice_grid, 0, functions.subtract(unit_circle_SDF, shifted_unit_circle_SDF))
#squares_circles_union = ms.MS_Grid(vertice_grid, 0, functions.union(unit_circle_SDF, shifted_unit_circle_SDF))
squares_circles_intersection = ms.MS_Grid(vertice_grid, 0, functions.intersection(unit_circle_SDF, shifted_unit_circle_SDF))





#shape_points, shape_edges = squares_circles_intersection.full_run()
#shape_points, shape_edges = squares_circles_subtract.full_run()
#shape_points, shape_edges = squares_circles_union.full_run()
#shape = ps.register_curve_network("circles_subtract", shape_points, shape_edges)

rectangle = functions.rectangle_function(0,0,1.5,1)
#squares_rectangle = ms.MS_Grid(vertice_grid,0,rectangle)
squares_rectangle = ms.MS_Grid(vertice_grid,0,functions.subtract(rectangle, shifted_unit_circle_SDF))

rectangle_points, rectangle_edges = squares_rectangle.full_run()
shape_rectangle = ps.register_curve_network("rectangle", rectangle_points, rectangle_edges)



# visualizing functions as curve network or mesh
value_mesh_points, value_mesh_edges, value_mesh_faces = func_visual.function_visualization.create_value_points_edges_mesh(5, vertice_grid)     
#value_curve_network = ps.register_curve_network("my_future_mesh", value_mesh_points, value_mesh_edges)  
value_mesh = ps.register_surface_mesh("my_value_mesh", value_mesh_points, value_mesh_faces)      

# coloring the mesh
value_mesh_colors = func_visual.function_visualization.create_mesh_colors(value_mesh_faces, value_mesh_points)
value_mesh.add_color_quantity("value_mesh_colors", value_mesh_colors, defined_on='faces', enabled=True)
    

   

        



ps.show()