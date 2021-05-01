"""
retraction_distance = range(2,10)
retraction_speed = range(30,60)
prime_speed = range(30,60)
"""

# %%
from bayes_opt import UtilityFunction
from typing import Union
import nevergrad as ng
import numpy as np
from bayes_opt import BayesianOptimization
from objective_functions import objective_function_v3

TRUTH_VALUE = np.array([
    210,  # print temperature
    4,  # retraction distance
    40   # reatraction speed
])


pbounds = {'x': (180, 220), 'y': (2, 8), 'z': (30, 60)}

# %% Automatic steps

optimizer = BayesianOptimization(
    f=lambda x, y, z: objective_function_v3(
        x, y, z, TRUTH_VALUE, minimize=False
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
    n_iter=20,
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
