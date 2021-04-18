from typing import Union
import nevergrad as ng
import numpy as np

TRUTH_VALUE = np.array([
    3,  # retraction_distance is 3 but * 10 to be equal to other parameters
    30,  # retraction_speed
    40   # prime_speed
])


def objective_function_v1(x: Union[ng.p.Scalar, float],
                          y: Union[ng.p.Scalar, float],
                          z: Union[ng.p.Scalar, float],
                          ) -> float:
    """
    Caluclates the absolute distance of all values to the TRUTH_VALUEs squared.
    Furthermore, multiplies x by 10 to get it to the same levels of y and z
    """
    result = [
        abs((TRUTH_VALUE[0]*10 - x*10)) ** 2,
        abs(TRUTH_VALUE[1] - y) ** 2,
        abs(TRUTH_VALUE[2] - z) ** 2,
    ]
    return abs(np.sum(result))
