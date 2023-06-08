import polyscope as ps
import numpy as np
import functions
import marching_squares as ms
import evaluation_grid as ev_grid
import function_visualization as func_visual
import sys # for printing max
import function_object as fob

class hlp:

    @staticmethod
    def ps_register_whole_FOB(myFOB: fob.FOB, name: str):
        isocurve1 = ps.register_curve_network(name+"_isocurve", myFOB.isocurve_points, myFOB.isocurve_edges)
        myFOB.compute_value_visuals()
        value_mesh1 = ps.register_surface_mesh(name+"_value_mesh", myFOB.value_mesh_points, myFOB.value_mesh_faces)
        value_mesh1.add_color_quantity(name+"_value_mesh_colors", myFOB.value_mesh_colors, defined_on='faces', enabled=True)

        value_plane1 = ps.register_surface_mesh(name+"_value_plane", myFOB.value_plane_points, myFOB.value_mesh_faces)
        value_plane1.add_color_quantity(name+"_value_plane_colors", myFOB.value_mesh_colors, defined_on='faces', enabled=True)
                                   