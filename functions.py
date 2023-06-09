import numpy as np
import math

# some semi-implicit functions:
# still written explicitly, but so that the expected 
# return value for the function would need to be 0
# to match the implicit function


### SDF
def circle_SDF(center_x: float, center_y: float, radius: float):
    circle = lambda x, y: np.sqrt((x - center_x)**2 + (y - center_y)**2)-radius
    return circle

# I think this is SDF (is similar to the one in Quilez 2D SDF article)
def rectangle_function(center_x: float, center_y: float, length: float, height: float):
    # mid should be -, but somehow + seems to produce the expected result
    #rectangle = lambda x,y: np.linalg.norm(np.maximum(np.abs(np.asarray([x,y]))-np.asarray([length, height]), np.asarray([0,0]))) - np.amin(np.max(np.abs(np.asarray([x,y])) - np.asarray([length, height])),0)
    #rectangle = lambda x,y: np.linalg.norm(np.maximum(np.abs(np.asarray([(x-center_x),(y-center_y)]))-np.asarray([length, height]), np.asarray([0,0]))) - np.amin(np.max(np.abs(np.asarray([(x-center_x),(y-center_y)])) - np.asarray([length, height])),0)
    #rectangle = lambda x,y: np.linalg.norm(np.maximum(np.abs(np.asarray([x,y]))-np.asarray([length, height]), np.asarray([0,0]))) + np.amin(np.max(np.abs(np.asarray([x,y])) - np.asarray([length, height])),0)
    rectangle = lambda x,y: np.linalg.norm(np.maximum(np.abs(np.asarray([(x-center_x),(y-center_y)]))-np.asarray([length, height]), np.asarray([0,0]))) + np.amin(np.max(np.abs(np.asarray([(x-center_x),(y-center_y)])) - np.asarray([length, height])),0)
    return rectangle

# m in [2,n]
def nstar_SDF(center_x: float, center_y: float, radius: float, n: float, m: float):
    # fixed (independent from x,y)
    an = np.pi/np.float64(n)
    en = np.pi/m # -> the external angle
    acs = np.asarray([np.cos(an), np.sin(an)])
    ecs = np.asarray([np.cos(en), np.sin(en)])
    # reduce to first sector (what is happening here?)
    bn = lambda x, y: (math.atan2(x,y)%2*an) - an
    p_1 = lambda x,y: np.linalg.norm(np.asarray([x,y])) * np.asarray( [np.cos(bn(x,y)), np.abs(np.sin(bn(x,y)))])
    p_2 = lambda x,y: p_1(x,y) - radius * acs
    p_3 = lambda x,y: p_2(x,y) + ecs * np.clip(-np.dot(p_2(x,y),ecs), 0.0, radius*acs[1]/ecs[1])
    function = lambda x,y: np.linalg.norm(p_3(x,y))*np.sign(p_3(x,y)[0])
    return function

### general implicit or unclear whether SDF

# result = 0 -> x, y is a point on the specified circle
# returns a function that is 0 at the
def circle_function(center_x: float, center_y: float, radius: float):
    circle = lambda x, y: (x - center_x)**2 + (y - center_y)**2 - radius**2
    return circle

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

# Smooth Boolean operations
# ts: transition size
def smooth_union(function_a, function_b, ts):
    # clip == clamp
    h = lambda x,y: np.clip(0.5+0.5*(function_b(x,y)-function_a(x,y))/ts , 0.0, 1.0)
    smooth_min = lambda x,y: function_b(x,y)*(1-h(x,y))+function_a(x,y)*h(x,y) + ts*h(x,y)*(1-h(x,y))
    return smooth_min

def smooth_intersection(function_a, function_b, ts):
    h = lambda x,y: np.clip(0.5-0.5*(function_b(x,y)-function_a(x,y))/ts , 0.0, 1.0)
    smooth_max = lambda x,y: function_b(x,y)*(1-h(x,y))+function_a(x,y)*h(x,y) + ts*h(x,y)*(1-h(x,y))
    return smooth_max

# note the order: a will be subtracted from b -> result b\a
def smooth_subtract(function_a, function_b, ts):
    h = lambda x,y: np.clip(0.5-0.5*(function_b(x,y)+function_a(x,y))/ts , 0.0, 1.0)
    smooth_subtract = lambda x,y: function_b(x,y)*(1-h(x,y))-function_a(x,y)*h(x,y) + ts*h(x,y)*(1-h(x,y))
    return smooth_subtract


