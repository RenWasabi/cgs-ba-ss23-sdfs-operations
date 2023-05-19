import polyscope as ps
import numpy as np
import functions
import marching_squares as ms


# todo
# - implement linear interpolation for the marching squares cut
# - implement the marching squares situation in which there is two cuts in one square
# - improve marching squares performance
#
# - implement smooth version of math functions for Boolean operations (+ research)
# - fully implement batman function
# - for parametric functions (e.g. shifted unit circle): somehow pass parameters in calling script
# - currently I'm just using any implicit functions -> use signed distance functions
#
# - visualize SDF (function/distance) values
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







# create the grid to discretely evaluate the function on

# specifies in which 2D domain input should be sampled
x_range = np.arange(-2,2, 0.01)
y_range = np.arange(-2,2, 0.01)

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



unit_circle = functions.circle_function(0,0,1)
shifted_unit_circle = functions.circle_function(0, 0.7, 1.25)
squares_circles_subtract = ms.MS_Grid(vertice_grid, 0, functions.subtract(unit_circle, shifted_unit_circle))

circles_subtract_points, circles_subtract_edges = squares_circles_subtract.full_run()
shape_substract = ps.register_curve_network("circles_subtract", circles_subtract_points, circles_subtract_edges)


# visualizing functions values on z axis
#value_vectors = np.ndarray((vertice_grid.shape[0]*vertice_grid.shape[1], 3))
value_vectors_points = []
value_vectors_edges = []
value_vectors_edge_colors = []
point_index_counter = 0
edge_index_counter = 0
for i in range(0,vertice_grid_shape[0],10):
    for j in range(0,vertice_grid_shape[1], 10):
        # vertice_grid[i,j,2] = 100 should have the correct value still from ms squares
        base = np.asarray([vertice_grid[i,j,0], vertice_grid[i,j,1], 0]) # the coordinate
        top = np.asarray([vertice_grid[i,j,0], vertice_grid[i,j,1], vertice_grid[i,j,2]])
        value_vectors_points.append(base)
        value_vectors_points.append(top)
        value_vectors_edges.append(np.asarray([point_index_counter, point_index_counter+1]))

        # value <= 0 blue, else red
        if (vertice_grid[i,j,2] <= 0): 
            value_vectors_edge_colors.append(np.asarray([0,0,1]))
        else:
            value_vectors_edge_colors.append(np.asarray([1,0,0]))
        point_index_counter += 2
value_vectors_points = np.asarray(value_vectors_points)
value_vectors_edges = np.asarray(value_vectors_edges)
value_vectors_edge_colors = np.asarray(value_vectors_edge_colors)
value_net = ps.register_curve_network("my_value_vectors", value_vectors_points, value_vectors_edges, transparency=0.3)
value_net.add_color_quantity("my_value_colors", value_vectors_edge_colors, defined_on="edges", enabled=True)
        
        

ps.show()