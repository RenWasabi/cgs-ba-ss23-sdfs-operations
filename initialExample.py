import polyscope as ps
import numpy as np
import functions
import marching_squares as ms


# todo
# - implement linear interpolation for the marching squares cut
# - implement the marching squares situation in which there is two cuts in one square
#
# - implement smooth version of math functions for Boolean operations (+ research)
# - fully implement batman function
# - for parametric functions (e.g. shifted unit circle): somehow pass parameters in calling script

# some options
ps.set_program_name("initial polyscope test")
ps.set_verbosity(0)
ps.set_use_prefs_file(False)

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







# create the grid to discretely evaluate the function on

# specifies in which 2D domain input should be sampled
x_range = np.arange(-5,5, 0.01)
y_range = np.arange(-5,5, 0.01)

# grid: [x_position, y_position, function_value]
vertice_grid_shape = (x_range.size, y_range.size, 3)
vertice_grid = np.ndarray(vertice_grid_shape)
# set initial coordinates and values for the grid
for i in range(vertice_grid_shape[0]):
    for j in range(vertice_grid_shape[1]):
        vertice_grid[i,j,0] = x_range[i] # set x coordinate
        vertice_grid[i,j,1] = y_range[j] # set y coordinate
        vertice_grid[i,j,2] = 100 # set initial value


# use marching squares on a function
#test_square_grid = ms.MS_Grid(vertice_grid, 0, functions.unit_circle)

"""
# unit circle
squares_unit_circle = ms.MS_Grid(vertice_grid, 0, functions.unit_circle)
unit_circle_points, unit_circle_edges = squares_unit_circle.full_run()
ps.register_curve_network("unit_circle", unit_circle_points, unit_circle_edges)


# shifted unit circle
squares_shifted_circle = ms.MS_Grid(vertice_grid, 0, functions.shifted_unit_circle)
shifted_circle_points, shifted_circle_edges = squares_shifted_circle.full_run()
ps.register_curve_network("shifted_circle", shifted_circle_points, shifted_circle_edges)
"""

#squares_circles_union = ms.MS_Grid(vertice_grid, 0, functions.union(functions.unit_circle, functions.shifted_unit_circle))
#circles_union_points, circles_union_edges = squares_circles_union.full_run()
#ps.register_curve_network("circles_union", circles_union_points, circles_union_edges)

#squares_circles_intersection = ms.MS_Grid(vertice_grid, 0, functions.intersection(functions.unit_circle, functions.shifted_unit_circle))
#circles_intersection_points, circles_intersection_edges = squares_circles_intersection.full_run()
#ps.register_curve_network("circles_intersection", circles_intersection_points, circles_intersection_edges)

squares_circles_subtract = ms.MS_Grid(vertice_grid, 0, functions.subtract(functions.unit_circle, functions.shifted_unit_circle))
circles_subtract_points, circles_subtract_edges = squares_circles_subtract.full_run()
ps.register_curve_network("circles_subtract", circles_subtract_points, circles_subtract_edges)

ps.show()