import numpy as np

# some semi-implicit functions:
# still written explicitly, but so that the expected 
# return value for the function would need to be 0
# to match the implicit function


# result = 0 -> x, y is a point on the specified circle
# returns a function that is 0 at the
def circle_function(center_x: float, center_y: float, radius: float):
    circle = lambda x, y: (x - center_x)**2 + (y - center_y)**2 - radius**2
    return circle

def circle_SDF(center_x: float, center_y: float, radius: float):
    circle = lambda x, y: np.sqrt((x - center_x)**2 + (y - center_y)**2)-radius
    return circle

def rectangle_function(center_x: float, center_y: float, length: float, height: float):
    # mid should be -, but somehow + seems to produce the expected result
    #rectangle = lambda x,y: np.linalg.norm(np.maximum(np.abs(np.asarray([x,y]))-np.asarray([length, height]), np.asarray([0,0]))) - np.amin(np.max(np.abs(np.asarray([x,y])) - np.asarray([length, height])),0)
    #rectangle = lambda x,y: np.linalg.norm(np.maximum(np.abs(np.asarray([(x-center_x),(y-center_y)]))-np.asarray([length, height]), np.asarray([0,0]))) - np.amin(np.max(np.abs(np.asarray([(x-center_x),(y-center_y)])) - np.asarray([length, height])),0)

    #rectangle = lambda x,y: np.linalg.norm(np.maximum(np.abs(np.asarray([x,y]))-np.asarray([length, height]), np.asarray([0,0]))) + np.amin(np.max(np.abs(np.asarray([x,y])) - np.asarray([length, height])),0)

    rectangle = lambda x,y: np.linalg.norm(np.maximum(np.abs(np.asarray([(x-center_x),(y-center_y)]))-np.asarray([length, height]), np.asarray([0,0]))) + np.amin(np.max(np.abs(np.asarray([(x-center_x),(y-center_y)])) - np.asarray([length, height])),0)

    
    return rectangle




def batman(x: float, y: float): 
    factor1 = (x/7)**2 * np.sqrt((np.abs(np.abs(x)-3)) / (np.abs(x)-3)) + (y/3)**2 * np.sqrt(  (np.abs(y + 3*np.sqrt(33)/7)/ (y + 3* np.sqrt(33)/7)))-1
    factor2 = np.abs(x/2) - (3*np.sqrt(33) - 7)/122 * x**2 - 3 + np.sqrt((1- np.abs(np.abs(x)-2)-1)**2)-y
    # still missing terms
    return factor1*factor2



# Boolean operations

# min -> A union B (two functions)
def union(function_a, function_b):
    min = lambda x,y: np.amin([function_a(x,y), function_b(x,y)])
    return min

# max -> A intersection B (two functions)
def intersection(function_a, function_b):
    max = lambda x,y: np.amax([function_a(x,y), function_b(x,y)])
    return max


# flip -> A complement (one function)
def complement(function_a):
    flipped = lambda x, y: -function_a(x, y)
    return flipped

# max(A, flip(B)) -> A\B (subtract B from A)
def subtract(function_a, function_b):
    subtract = lambda x, y: np.amax([function_a(x,y), complement(function_b)(x, y)])
    return subtract


