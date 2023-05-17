import polyscope as ps
import numpy as np
import polyscope as ps

class MS_Grid:
    # x squares, y squares, 3 (position x y , value)
    def __init__(self, vertice_grid: np.ndarray, isovalue: float, function):
        self.vertices = vertice_grid
        self.shape = (vertice_grid.shape[0]-1, vertice_grid.shape[1]-1)
        # square_info stores information about the intersections through squares
        # made by marching squares
        self.square_infos = [[None for i in range(self.shape[0])] for j in range(self.shape[1])]
        self.isovalue = isovalue
        self.function = function
        # flattened infos
        self.cut_vertice_list = np.zeros(1)
        self.cut_edge_list = np.zeros(1)


    def get_square_infos(self):
        print(self.square_infos)


    """
    one square should store:
     -  all necessary intersection points on its edges (determined LERP)
     - pair/pairs of indices for which of these points are connected by an outline
    """

    def evaluate_function(self):
        for i in range(self.vertices.shape[0]):
            for j in range(self.vertices.shape[1]):
                # value at i, j      = function evaluated at x, y coordinates belonging to i,j
                self.vertices[i,j,2] = self.function(self.vertices[i,j,0], self.vertices[i,j,1])

    # functions for retrieving the four vertices of a specified square
    def get_vertice_upper_left(self, square_index_x: int, square_index_y: int):
        return self.vertices[square_index_x, square_index_y]
    
    def get_vertice_upper_right(self, square_index_x: int, square_index_y: int):
        return self.vertices[square_index_x+1, square_index_y]
    
    def get_vertice_lower_left(self, square_index_x: int, square_index_y: int):
        return self.vertices[square_index_x, square_index_y+1]
    
    def get_vertice_lower_right(self, square_index_x: int, square_index_y: int):
        return self.vertices[square_index_x+1, square_index_y+1]
    
    
    # return the square type (int 0-15) of the specified square
    # LSB: left upper, going clockwise to MSB: left lower, 0 -> point inside or on isocurve, 1 -> outside
    def square_type(self, square_index_x: int, square_index_y: int):

        # upper left
        value_upper_left = self.get_vertice_upper_left(square_index_x, square_index_y)[2]
        #print("the function value is" , value_upper_left)
        if (value_upper_left <= self.isovalue):
            a = "0"
        else:
            a = "1"

        # upper right
        value_upper_right = self.get_vertice_upper_right(square_index_x, square_index_y)[2]
        if (value_upper_right <= self.isovalue):
            b = "0"
        else:
            b = "1"

        # lower right
        value_lower_right = self.get_vertice_lower_right(square_index_x, square_index_y)[2]
        if (value_lower_right <= self.isovalue):
            c = "0"
        else:
            c = "1"

        # lower right
        value_lower_left = self.get_vertice_lower_left(square_index_x, square_index_y)[2]
        if (value_lower_left <= self.isovalue):
            d = "0"
        else:
            d = "1"

        square_type = int(d+c+b+a,2)

        return square_type

        #print("square[" , square_index_x, "][", square_index_y, "] has type:" , square_type)

    
    # 
    def cut_square(self, square_index_x: int, square_index_y: int):
        square_type = self.square_type(square_index_x, square_index_y)  
        square_info = Square_Info()


        # all 0 or all 1 -> not cut
        if (square_type == 0 or square_type == 15):
            square_info.intersection_points = None
            square_info.intersection = None

        # get all four vertices in the beginning for better readibility
        a = self.get_vertice_upper_left(square_index_x, square_index_y)
        b = self.get_vertice_upper_right(square_index_x, square_index_y)
        c = self.get_vertice_lower_right(square_index_x, square_index_y)
        d = self.get_vertice_lower_left(square_index_x, square_index_y)
        
        # one 0 three 1 or one 1 and three 0 -> one diagonal cut
        # sum of corresponding pairs here is always 15
        # left upper diagonal
        if (square_type == 1 or square_type == 14):
            square_info.intersection_points = np.zeros((2,3)) # 2 points in 3D
            square_info.intersection_points[0] = self.cut_edge(a,b)
            square_info.intersection_points[1] = self.cut_edge(a,d)
            square_info.intersection = np.asarray([0,1])
        if (square_type == 2 or square_type == 13):
            square_info.intersection_points = np.zeros((2,3)) # 2 points in 3D
            square_info.intersection_points[0] = self.cut_edge(a,b)
            square_info.intersection_points[1] = self.cut_edge(b,c)
            square_info.intersection = np.asarray([0,1])
        if (square_type == 4 or square_type == 11):
            square_info.intersection_points = np.zeros((2,3)) # 2 points in 3D
            square_info.intersection_points[0] = self.cut_edge(b,c)
            square_info.intersection_points[1] = self.cut_edge(c,d)
            square_info.intersection = np.asarray([0,1])
        if (square_type == 8 or square_type == 7):
            square_info.intersection_points = np.zeros((2,3)) # 2 points in 3D
            square_info.intersection_points[0] = self.cut_edge(a,d)
            square_info.intersection_points[1] = self.cut_edge(c,d)
            square_info.intersection = np.asarray([0,1])


        # two 1 two 0
        # one vertical line
        if (square_type == 9 or square_type == 6):
            square_info.intersection_points = np.zeros((2,3)) # 2 points in 3D
            square_info.intersection_points[0] = self.cut_edge(a,b)
            square_info.intersection_points[1] = self.cut_edge(d, c)
            square_info.intersection = np.asarray([0,1])
        # one horizontal line
        if (square_type == 3 or square_type == 12):
            square_info.intersection_points = np.zeros((2,3)) # 2 points in 3D
            square_info.intersection_points[0] = self.cut_edge(a,d)
            square_info.intersection_points[1] = self.cut_edge(b,c)
            square_info.intersection = np.asarray([0,1])
        # two diagonal cuts
        # unclear situation, needs extra handling


        self.square_infos[square_index_x][square_index_y] = square_info


    # param: vertices of the edge to be cut
    # returns: the point of intersection as 2d np.array
    def cut_edge(self, vertice_a : np.array, vertice_b: np.array):
        intersection = vertice_b + (vertice_a-vertice_b)/2 # the middle between a and b
        return intersection
    
    
    # fill self.square_infos with one Square_info object per square
    # containing information about where this square needs to be cut
    def march(self):
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.cut_square(i,j)
        

    # turn the 2D info stored in squares_infos as Square_Info objects into
    # two flat lists:
    # cut_vertice_list contains all the vertices belonging to the final cut (including a lot of doubled points)
    # cut_edge_list contains indices (pairs of 2) referencing cut_edge_list, indicating which vertices are connected by a cut
    def flatten_infos(self):
        cut_vertice_list = []
        cut_edge_list = []

        vertice_index = -1 # necessary so that adding the first vertice at index 0 will result in 0
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                if (self.square_infos[i][j].intersection_points is not None):
                    # this one is important because sometimes there is one cut, sometimes two cuts
                    number_of_vertices = self.square_infos[i][j].intersection_points.shape[0]
                    for vertice in range(number_of_vertices):
                        isoline_vertice = self.square_infos[i][j].intersection_points[vertice]
                        # set the z coordinate (currently storing value) to isoline value (usually zero)
                        isoline_vertice = np.asarray([isoline_vertice[0], isoline_vertice[1], self.isovalue])
                        cut_vertice_list.append(isoline_vertice)
                        vertice_index += 1

                        # uneven index -> 2 new vertices -> 1 new edge (add edge between last two vertices)
                        if (vertice_index % 2 == 1):
                            cut_edge_list.append(np.asarray([vertice_index-1, vertice_index]))
                    
        
                    
                      
        self.cut_vertice_list = np.asarray(cut_vertice_list)

        self.cut_edge_list = np.asarray(cut_edge_list)


        

        #print(cut_edge_list)
    
        
        
class Square_Info:
    #def __init__(self):
        # the points on the edges of the square that are intersected by the isocurve
    intersection_points = None # numpy array of [[x_0, y_0] ...]
    intersection = np.zeros(1)   # numpy array, indices of the intersection vertices to be connected by an edge
    

    

    





# def outsourced_function(x: int, y:int, method_to_run):
#     return method_to_run(x,y)


# def marching_squares(vertice_grid: np.ndarray, isovalue: float, function):


#     square_grid_shape = (vertice_grid.shape[0]-1, vertice_grid.shape[1]-1)
#     square_grid = np.ndarray(square_grid_shape)

#     for i in range(square_grid_shape[0]):
#         for j in range(square_grid_shape[1]):

    