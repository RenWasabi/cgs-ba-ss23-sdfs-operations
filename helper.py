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

    def ps_register_and_list_whole_FOB(myFOB: fob.FOB, name: str, example_list: list):
        isocurve1 = ps.register_curve_network(name+"_isocurve", myFOB.isocurve_points, myFOB.isocurve_edges)
        example_list.append(isocurve1)
        myFOB.compute_value_visuals()
        value_mesh1 = ps.register_surface_mesh(name+"_value_mesh", myFOB.value_mesh_points, myFOB.value_mesh_faces)
        example_list.append(value_mesh1)
        value_mesh1.add_color_quantity(name+"_value_mesh_colors", myFOB.value_mesh_colors, defined_on='faces', enabled=True)
        value_plane1 = ps.register_surface_mesh(name+"_value_plane", myFOB.value_plane_points, myFOB.value_mesh_faces)
        example_list.append(value_plane1)
        value_plane1.add_color_quantity(name+"_value_plane_colors", myFOB.value_mesh_colors, defined_on='faces', enabled=True)


    @staticmethod
    def create_coordinate_axis():
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
                                   