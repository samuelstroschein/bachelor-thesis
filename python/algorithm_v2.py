"""
retraction_distance = range(2,10)
retraction_speed = range(30,60)
prime_speed = range(30,60)
"""

# %%
import nevergrad as ng
import numpy as np
from bayes_opt import BayesianOptimization


RETRACTION_DISTANCE = range(2, 11)
RETRACTION_SPEED = range(30, 61)
PRIME_SPEED = range(30, 61)

TRUTH_VALUE = np.array([
    30,  # retraction_distance is 3 but * 10 to be equal to other parameters
    30,  # retraction_speed
    40   # prime_speed
])


def objective_function_vector(x: np.ndarray) -> float:
    """
    Caluclates the absolute distance of x to the TRUTH_VALUE.
    """
    return -1 * abs(np.sum(np.subtract(TRUTH_VALUE, x)))


def objective_function_variables(x: float, y: float, z: float) -> float:
    """
    Caluclates the absolute distance of x to the TRUTH_VALUE.
    """
    return -1 * abs(np.sum(np.subtract(TRUTH_VALUE, np.array([x * 10, y, z])))) 

# %%

pbounds = {'x': (2, 10), 'y': (30, 60), 'z': (30, 60)}

optimizer = BayesianOptimization(
    f=objective_function_variables,
    pbounds=pbounds,
    verbose=2,  # verbose = 1 prints only when a maximum is observed, verbose = 0 is silent
    random_state=1,
)

# set first initial point
optimizer.probe(
    params=[2, 30,30],
    lazy=True,
)

# set second initial point
optimizer.probe(
    params=[10, 60, 60],
    lazy=True,
)

optimizer.maximize(
    init_points=0,
    n_iter=8,
    kappa=1.75
)

print(optimizer.max)

# %%