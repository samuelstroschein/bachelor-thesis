# %%
import nevergrad as ng
import numpy as np
from python.nevergrad_algorithm_base import NevergradAlgorithmBase

TRUTH_VALUE = np.array([
    3,  # retraction_distance is 3 but * 10 to be equal to other parameters
    30,  # retraction_speed
    40   # prime_speed
])


def objective_function(x: np.ndarray) -> float:
    """
    Caluclates the absolute distance of x to the TRUTH_VALUE squared.
    """
    result = [
        abs((TRUTH_VALUE[0]*10 - x[0]*10)) ** 2,
        abs(TRUTH_VALUE[1] - x[1]) ** 2,
        abs(TRUTH_VALUE[2] - x[2]) ** 2,
    ]
    return abs(np.sum(result))


def objective_function_variables(
    x: ng.p.Scalar,
    y: ng.p.Scalar,
    z: ng.p.Scalar
) -> float:
    return objective_function(np.array([x, y, z]))

# %%

algorithm = NevergradAlgorithmBase(
    objective_function_variables, ng.optimizers.NGOpt)


for _ in range(20):  # type: ignore
    algorithm.step()

recommendation = algorithm.optimizer.provide_recommendation()
print('\n')
print(f'recommendation: {recommendation.args}\ntruth value: {TRUTH_VALUE}')

# %%
