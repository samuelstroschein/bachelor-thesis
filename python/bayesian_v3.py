"""
retraction_distance = range(2,10)
retraction_speed = range(30,60)
prime_speed = range(30,60)
"""

# %%
from bayes_opt import UtilityFunction
from typing import Tuple
import nevergrad as ng
import numpy as np
from bayes_opt import BayesianOptimization
from objective_functions import objective_function_v3

TRUTH_VALUE = np.array([
    210,  # print temperature
    4,    # retraction distance
    40    # reatraction speed
])


def discrete_step_wrapper(
    x: Tuple[float, range],
    y: Tuple[float, range],
    z: Tuple[float, range]
):
    """
    Wraps the continous probs from the bayesian optimizer into 
    discrete values binned to the specified step size.
    """
    return objective_function_v3(x[0], y[0], z[0], TRUTH_VALUE, minimize=False)


x_range = range(180, 220, 5)
y_range = range(2, 8, 1)
z_range = range(30, 60, 10)

pbounds = {'x': (180, 220), 'y': (2, 8), 'z': (30, 60)}

# %% Automatic steps

optimizer = BayesianOptimization(
    f=lambda x, y, z: discrete_step_wrapper(
        (x, x_range), (y, y_range), (z, z_range),
    ),
    pbounds=pbounds,
    verbose=2,  # verbose = 1 prints only when a maximum is observed, verbose = 0 is silent
    random_state=1,
)

# set first initial point
optimizer.probe(
    params=[180, 2, 30],
    lazy=True,
)

# set second initial point
optimizer.probe(
    params=[220, 8, 60],
    lazy=True,
)

optimizer.maximize(
    init_points=0,
    n_iter=100,
    kappa=1.75
)

print(optimizer.max)

# %% Manual ask/tell steps

optimizer = BayesianOptimization(
    f=None,
    pbounds=pbounds,
    verbose=2,  # verbose = 1 prints only when a maximum is observed, verbose = 0 is silent
    random_state=10,
)

utility = UtilityFunction(kind="ucb", kappa=2, xi=0.0)

for i in range(4):
    next_point = optimizer.suggest(utility)
    print(next_point)
    rank = objective_function_v3(
        next_point['x'],
        next_point['y'],
        next_point['z'],
        TRUTH_VALUE,
        minimize=False
    )
    optimizer.register(params=next_point, target=rank)
