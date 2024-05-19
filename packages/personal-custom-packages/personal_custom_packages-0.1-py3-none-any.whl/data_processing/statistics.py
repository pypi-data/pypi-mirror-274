import numpy as np


def correlation_coefficient(x,y):
    new_x = np.array(x)
    new_y = np.array(y)
    correlation_coefficient = np.corrcoef(new_x,new_y)
    return correlation_coefficient[0,1]




