import polyscope as ps
import numpy as np
import functions
import marching_squares as ms



class evaluation_grid:
        # create the grid to discretely evaluate a function on
        # creates a square grid with specified sidelength and center
        # the returned format of is a 3dimensional np.ndarray: [x_position, y_position, function_value]
        # x position and y position represent the actual spacial coordinates of the grid vertices
        # function_value can be filled with the value of a function at these points later and is initialized to 0
    @staticmethod
    def create_vertice_grid(center_x:float, center_y: float, sidelength: float, resolution: float) -> np.ndarray:
        

        # specifies in which 2D domain input should be sampled
        x_range = np.arange(center_x-sidelength/2,center_x+sidelength/2, resolution)
        y_range = np.arange(center_y-sidelength/2,center_y+sidelength/2, resolution)

        # grid: [x_position, y_position, function_value]
        vertice_grid_shape = (x_range.size, y_range.size, 3)
        vertice_grid = np.ndarray(vertice_grid_shape)
        # set initial coordinates and values for the grid
        for i in range(vertice_grid_shape[0]):
            for j in range(vertice_grid_shape[1]):
                vertice_grid[i,j,0] = x_range[i] # set x coordinate
                vertice_grid[i,j,1] = y_range[j] # set y coordinate
                vertice_grid[i,j,2] = 0 # set initial value
            
        return vertice_grid


