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