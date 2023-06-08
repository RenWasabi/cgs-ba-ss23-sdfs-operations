import polyscope as ps
import numpy as np
import functions
import marching_squares as ms
import evaluation_grid as ev_grid
import function_visualization as func_visual
import sys # for printing max

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


class FOB:
    # the ev_* terms describe the location and dimension of the discrete grid on which the function will be evaluated
    # the isovalue determines the isocurve
    # resolution does not affect the isocurve, but the resolution of the mesh (/curve network) visualizing the function values
    def __init__(self, function, isovalue: float, ev_center_x: float, ev_center_y: float, ev_sidelength: float, resolution_step: int):
        self.function = function
        self.isovalue = isovalue
        self.ev_center_x = ev_center_x
        self.ev_center_y = ev_center_y
        self.ev_sidelenth = ev_sidelength
        self.resolution_step = resolution_step

        # create the vertice grid to discretely evaluate the function on
        # format: [x_position, y_position, function_value]
        self.evaluation_grid = ev_grid.evaluation_grid().create_vertice_grid(0,0,4,0.01)

        # use Marching Squares on the function (marching squares object)
        MS_FOB = ms.MS_Grid(self.evaluation_grid, isovalue, function)
        self.isocurve_points, self.isocurve_edges = MS_FOB.full_run()

    # computes the edges (curve network) points, mesh faces and mesh colors representing the values of the function
    # with the specified resolution step
    def compute_value_visuals(self):
        # visualizing functions as curve network or mesh
        self.value_mesh_points, self.value_mesh_edges, self.value_mesh_faces = func_visual.function_visualization.create_value_points_edges_mesh(self.resolution_step, self.evaluation_grid)     
        self.value_mesh_colors = func_visual.function_visualization.create_mesh_colors(self.value_mesh_faces, self.value_mesh_points)

    