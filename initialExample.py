import polyscope as ps
import numpy as np
import polyscope as ps

import marching_squares as ms

# some options
ps.set_program_name("initial polyscope test")
ps.set_verbosity(0)
ps.set_use_prefs_file(False)




# Initialize polyscope, creating graphics contexts and constructing a window.
# Should be called exactly once.
ps.init()

# Build visualizations, here or in distant code
# ...
# ...
# ...

""""
# build mesh
vertices = np.random.rand(100, 3) # (V,3) vertex position array
faces = np.random.randint(0, 100, size=(250,3)) # (F,3) array of indices 
                                                # for triangular faces

# visualize!
ps_mesh = ps.register_surface_mesh("my mesh", vertices, faces)


# Pass control flow to polyscope, displaying the interactive window.
# Function will return when user closes the window.
ps.show()
"""



# More of your code
# ...
# this creates a triangle
#vertices2 = np.array([[0,0,0],[1,0,0],[0,1,0]])
#faces2 = np.array([[0,1,2]])


#ps_mesh2 = ps.register_surface_mesh("my triangle", vertices2, faces2)

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






# within this range an input (x,y) is considered to be fulfilling the implicit equation
approximation_threshold = 0.2

# specifies in which 2D domain input should be sampled
x_range = np.arange(-10,10, 0.1)
y_range = np.arange(-10,10, 0.1)

# result = 0 -> x, y is a point on the unit circle
def unit_circle_equation(x: float, y: float):
    return x**2 + y**2 - 1

def batman_equation(x: float, y: float): 
    factor1 = (x/7)**2 * np.sqrt((np.abs(np.abs(x)-3)) / (np.abs(x)-3)) + (y/3)**2 * np.sqrt(  (np.abs(y + 3*np.sqrt(33)/7)/ (y + 3* np.sqrt(33)/7)))-1
    factor2 = np.abs(x/2) - (3*np.sqrt(33) - 7)/122 * x**2 - 3 + np.sqrt((1- np.abs(np.abs(x)-2)-1)**2)-y
    print(factor1*factor2)
    return factor1*factor2


# grid: [x_position, y_position, function_value]
vertice_grid_shape = (x_range.size, y_range.size, 3)
vertice_grid = np.ndarray(vertice_grid_shape)

for i in range(vertice_grid_shape[0]):
    for j in range(vertice_grid_shape[1]):
        vertice_grid[i,j,0] = x_range[i] # set x coordinate
        vertice_grid[i,j,1] = y_range[j] # set y coordinate
        vertice_grid[i,j,2] = 100 # set initial value



test_square_grid = ms.MS_Grid(vertice_grid, 0, batman_equation)
print("isovalue: " , test_square_grid.isovalue)
print(test_square_grid.get_vertice_upper_left(0,0))
# stores the positions considered to be on the zero isocontour
isocontour_positions = []



for i in range(x_range.size-1):
    for j in range(y_range.size-1):


        # evaluate circle function
        #value = x_range[i]**2 + y_range[j]**2 - 1
        value = unit_circle_equation(x_range[i], y_range[j])
        #values[i,j,0] = value
        test_square_grid.square_type(i,j)

        if np.isclose(value, 0, atol = approximation_threshold):
            position = np.array([x_range[i],0, y_range[j]])

            isocontour_positions.append(position)




test_square_grid.square_type(0,0)
circle_edges = np.array([[0,1], [1,2]])
test_square_grid.evaluate_function()
test_square_grid.get_square_infos()
test_square_grid.march()
test_square_grid.get_square_infos()
test_square_grid.flatten_infos()
test_points = test_square_grid.cut_vertice_list
#test_points = test_square_grid.isoline_info()


ps.register_curve_network("test", test_points, np.asarray([[0,0]]))
# vertices are the points considered to be on the zero isocontour
#ps.register_curve_network("my_circle", np.asarray(isocontour_positions), circle_edges)
#print(grid)


#def outsourced_function(x: int, y:int, method_to_run):
#    return method_to_run(x,y)

#print(ms.outsourced_function(1, 2, lambda x, y: x + y ))






# Show again. Data is preserved between calls to show()
# unless explicitly removed.
ps.show()