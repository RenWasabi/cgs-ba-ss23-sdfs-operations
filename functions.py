import numpy as np

# result = 0 -> x, y is a point on the unit circle
def unit_circle(x: float, y: float):
    return x**2 + y**2 - 1

def batman(x: float, y: float): 
    factor1 = (x/7)**2 * np.sqrt((np.abs(np.abs(x)-3)) / (np.abs(x)-3)) + (y/3)**2 * np.sqrt(  (np.abs(y + 3*np.sqrt(33)/7)/ (y + 3* np.sqrt(33)/7)))-1
    factor2 = np.abs(x/2) - (3*np.sqrt(33) - 7)/122 * x**2 - 3 + np.sqrt((1- np.abs(np.abs(x)-2)-1)**2)-y
    return factor1*factor2