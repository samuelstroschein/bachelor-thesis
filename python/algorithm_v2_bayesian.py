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


RETRACTION_DISTANCE = range(2, 11)
RETRACTION_SPEED = range(30, 61)
PRIME_SPEED = range(30, 61)

TRUTH_VALUE = np.array([
    30,  # retraction_distance is 3 but * 10 to be equal to other parameters
    30,  # retraction_speed
    40   # prime_speed
])


def objective_function(x: Union[ng.p.Scalar, float],
                       y: Union[ng.p.Scalar, float],
                       z: Union[ng.p.Scalar, float],
                       ) -> float:
    """
    Caluclates the absolute distance of x to the TRUTH_VALUE squared.
    """
    result = [
        abs((TRUTH_VALUE[0]*10 - x*10)) ** 2,
        abs(TRUTH_VALUE[1] - y) ** 2,
        abs(TRUTH_VALUE[2] - z) ** 2,
    ]
    return -1 * abs(np.sum(result))

# %%


pbounds = {'x': (2, 10), 'y': (30, 60), 'z': (30, 60)}

# %% Automatic steps

optimizer = BayesianOptimization(
    f=objective_function,
    pbounds=pbounds,
    verbose=2,  # verbose = 1 prints only when a maximum is observed, verbose = 0 is silent
    random_state=1,
)

# set first initial point
optimizer.probe(
    params=[2, 30, 30],
    lazy=True,
)

# set second initial point
optimizer.probe(
    params=[10, 60, 60],
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
    rank = objective_function(
        next_point['x'], next_point['y'], next_point['z'])
    optimizer.register(params=next_point, target=rank)

# %%


def black_box_function(x, y):
    return -x ** 2 - (y - 1) ** 2 + 1


optimizer = BayesianOptimization(
    f=None,
    pbounds={'x': (-2, 2), 'y': (-3, 3)},
    verbose=2,
    random_state=1,
)


for _ in range(5):
    next_point = optimizer.suggest(utility)
    target = black_box_function(**next_point)
    optimizer.register(params=next_point, target=target)

    print(target, next_point)
print(optimizer.max)
# %%
