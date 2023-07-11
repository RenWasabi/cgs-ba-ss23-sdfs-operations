import polyscope as ps
import numpy as np
import functions
import marching_squares as ms


class function_visualization: 
    # create a mesh based on the function values on the z-axis, with x,y position being the corresponding input
    # resolution step specifies how many vertices in the original evalution grid shall be grouped/approximated by a single mesh vertex
    # smaller steps -> more precision (less than 1 doesn't make sense, for that, the evaluation grid should be adjusted)
    #
    # in order for this to work, previously marching squares has to be run (full_run()) on the evaluation grid for it to be
    # filled with the correct function values to be used here
    @staticmethod
    def create_value_points_edges_mesh(resolution_step: int, evaluation_grid: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        mesh_grid_x = np.int64(np.ceil(evaluation_grid.shape[0]/resolution_step))
        mesh_grid_y = np.int64(np.ceil(evaluation_grid.shape[1]/resolution_step))

        number_x_edges = mesh_grid_x*(mesh_grid_y-1)
        number_y_edges = (mesh_grid_x-1)*mesh_grid_y
        number_diag_edges = (mesh_grid_x-1)*(mesh_grid_y-1)
        number_total_edges = number_x_edges + number_y_edges + number_diag_edges
        number_of_faces = (mesh_grid_x-1)*(mesh_grid_y-1)*2

        value_mesh_points = np.ndarray((mesh_grid_x*mesh_grid_y, 3)) # flat array of 3D mesh points
        value_mesh_edges = np.ndarray((number_total_edges, 2)) # flat array of edges (as length 2 array)
        value_mesh_faces = np.ndarray((number_of_faces, 3)) # flat array of triangle (3 edges) faces

        for i in range(mesh_grid_x): 
            for j in range(mesh_grid_y):
                # the points
                value_mesh_points[i*mesh_grid_y+j,:] = evaluation_grid[i*resolution_step, j*resolution_step, :]

                # the edges and faces
                # face calculation is based on edges, one faces consists of the two edges of the diagonal and one x edge
                # may God have mercy on me for this index calculation

                # x direction edges for curves 
                if (j < mesh_grid_y-1):
                    x_edge_index = i*(mesh_grid_y-1)+j
                    value_mesh_edges[x_edge_index, :] = np.asarray([i*mesh_grid_y+j, i*mesh_grid_y+j+1])
                    # the x point for mesh faces 
                    if (i < mesh_grid_x-1):
                        value_mesh_faces[i*(mesh_grid_y-1)+j, 2] = np.int64(value_mesh_edges[x_edge_index,1])
                        value_mesh_faces[i*(mesh_grid_y-1)+j+number_of_faces//2, 2] = np.int64(value_mesh_edges[x_edge_index,0]+mesh_grid_x)

                # the y direction edges
                if (i < mesh_grid_x and (j != 0 or i==0) and i*(mesh_grid_y-1)+j+number_x_edges != number_x_edges+number_y_edges):
                    y_edge_index = i*(mesh_grid_y-1)+j+number_x_edges
                    value_mesh_edges[y_edge_index, :] = np.asarray([i*(mesh_grid_y-1)+j, (i+1)*mesh_grid_y+j-i])

                # the diagonal edges
                if (i >= mesh_grid_x-1 or j >= mesh_grid_y-1):
                    continue
                else:
                    diag_edge_index = i*(mesh_grid_y-1)+j+number_x_edges+number_y_edges
                    value_mesh_edges[diag_edge_index,:] = np.asarray([i*mesh_grid_y+j, (i+1)*mesh_grid_y+j+1])

                    # diagonal points for mesh faces
                    # first half (left half of square)
                    value_mesh_faces[i*(mesh_grid_y-1)+j, 0] = np.int64(value_mesh_edges[diag_edge_index,0])
                    value_mesh_faces[i*(mesh_grid_y-1)+j, 1] = np.int64(value_mesh_edges[diag_edge_index,1])
                    # right half
                    value_mesh_faces[i*(mesh_grid_y-1)+j+number_of_faces//2, 0] = np.int64(value_mesh_edges[diag_edge_index,0])
                    value_mesh_faces[i*(mesh_grid_y-1)+j+number_of_faces//2, 1] = np.int64(value_mesh_edges[diag_edge_index,1])

        return value_mesh_points, value_mesh_edges, value_mesh_faces
    

    # value_mesh_faces are the faces to be coloured
    # value_mesh_points needs to be passed because it contains the function values 
    # necessary for determining whether the face has positive or negative value
    # returns an np.ndarray that assigns a color to each face, can be used with 
    # polyscope's mesh.add_color_quantity(...)
    @staticmethod
    def create_mesh_colors(value_mesh_faces: np.ndarray, value_mesh_points: np.ndarray, isovalue: float) -> np.ndarray:
        # coloring the mesh
        # majority of point values determines color
        # ideally with LERP
        number_of_faces = value_mesh_faces.shape[0]
        value_mesh_colors = np.ndarray((number_of_faces,3))
        blue = np.asarray([0,0,1])
        red = np.asarray([1,0,0])
        for face in range (number_of_faces):
            positive_vertices = 0
            for vertice in range(3):
                this_vertice = value_mesh_faces[face,vertice]
                this_value = value_mesh_points[np.int64(this_vertice),2]
                if this_value > isovalue:
                    positive_vertices += 1
            if positive_vertices >= 2:
                # color face red
                value_mesh_colors[face] = red
            else:
                # color face blue
                value_mesh_colors[face] = blue
        return value_mesh_colors
    

    @staticmethod
    def create_mesh_colors_gradient(value_mesh_faces: np.ndarray, value_mesh_points: np.ndarray, isovalue: float) -> np.ndarray:
        # coloring the mesh
        # majority of point values determines color
        # ideally with LERP
        number_of_faces = value_mesh_faces.shape[0]
        value_mesh_colors = np.ndarray((number_of_faces,3))
        blue = np.asarray([0,0,1])
        red = np.asarray([1,0,0])
        max_average = 0
        min_average = 0
        for face in range (number_of_faces):
            value_sum = 0
            for vertice in range(3):
                this_vertice = value_mesh_faces[face,vertice]
                this_value = value_mesh_points[np.int64(this_vertice),2]
                value_sum += this_value
            av_value = value_sum / 3
            value_mesh_colors[face] = np.asarray([av_value,0,0]) 
            if av_value > max_average:
                max_average = av_value
            if av_value < min_average:
                min_average = av_value
        # scale value between 0, 1 according to highest and lowest value
        # make sure middle is at value 0 -> split according to values above and below, then scale each linearly
        val_range_pos = np.amax([max_average, 0])
        val_range_neg = np.abs(min_average)
        # normalize, create correct color values
        for face in range(number_of_faces):
            value = value_mesh_colors[face,0]
            if value >= 0:
                if val_range_pos != 0:
                    # if value = max then 1, else between 0.5 and 1
                    value_mesh_colors[face,0] = np.amin([value_mesh_colors[face,0] /val_range_pos*2, 1])
                # else value must be 0 => no scaling needed
            else:
                if val_range_neg != 0:
                    value_mesh_colors[face,0] = np.max([0.5+value_mesh_colors[face,0] /val_range_neg*2, 0])

            value_mesh_colors[face,2] = 1-value_mesh_colors[face,0]
            # making it light in the middle looks better
            value_mesh_colors[face,1] = (1-np.amax([value_mesh_colors[face]]))/2
            
        return value_mesh_colors




"""
# visualizing functions values on z axis, as vectors
#value_vectors = np.ndarray((vertice_grid.shape[0]*vertice_grid.shape[1], 3))
value_vectors_points = []
value_vectors_edges = []
value_vectors_edge_colors = []
point_index_counter = 0
edge_index_counter = 0
for i in range(0,vertice_grid_shape[0],25):
    for j in range(0,vertice_grid_shape[1], 25):
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
"""