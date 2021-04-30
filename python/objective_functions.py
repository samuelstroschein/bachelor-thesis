from typing import List, Union
import nevergrad as ng
import numpy as np

TRUTH_VALUE = np.array([
    210,  # print temperature
    4,  # retraction distance
    40   # reatraction speed
])


def objective_function_v1(x: Union[ng.p.Scalar, float],
                          y: Union[ng.p.Scalar, float],
                          z: Union[ng.p.Scalar, float],
                          ) -> float:
    """
    Calculates the absolute distance of all values to the TRUTH_VALUES.
    """
    result = [
        abs(TRUTH_VALUE[0] - x),
        abs(TRUTH_VALUE[1] - y),
        abs(TRUTH_VALUE[2] - z),
    ]
    return abs(np.sum(result))


# TODO
# take "very good point" and "very bad point" into consideration.
# after each print ask the user to rank and rate the print. For example:
# rank: 1, rating: 2 -> 0 = bad, 1 = neutral, 2 = good
def rank_function_v1(x: Union[ng.p.Scalar, float],
                          y: Union[ng.p.Scalar, float],
                          z: Union[ng.p.Scalar, float],
                          ranking: List[List],
                          ) -> float:
    """
    X,y,z are transformed into a list and then searched for in the
    ranking list. The index position of the search is the returned value. 

    E.g. [x,y,z], ranking = [[30,45,2], [x,y,z]] -> returns 1 
    """
    return ranking.index([x, y, z])
    # return ranking.index([x, y])

def rank_function_v2(x: Union[ng.p.Scalar, float],
                          y: Union[ng.p.Scalar, float],
                          z: Union[ng.p.Scalar, float],
                          ranking: List[List],
                          ) -> float:
    """
    X,y,z are transformed into a list and then searched for in the
    ranking list. The index position of the search is the returned value. 

    E.g. [x,y,z], ranking = [[30,45,2], [x,y,z]] -> returns 1 
    """
    return ranking.index([x, y, z])

def objective_function_v3(x: Union[ng.p.Scalar, float],
                          y: Union[ng.p.Scalar, float],
                          z: Union[ng.p.Scalar, float],
                          ) -> float:
    """
    Calculates the deviation of each individual the TRUTH_VALUES 
    while adjusting each values weight based on the ranged of the parameters.

    """
    result = [
        abs(TRUTH_VALUE[0] - x) * 2,
        abs(TRUTH_VALUE[1] - y) * 10,
        abs(TRUTH_VALUE[2] - z) * 1,
    ]
    return abs(np.sum(result))
