"""
retraction_distance = range(2,10)
retraction_speed = range(30,60)
prime_speed = range(30,60)
"""

# %%
from bayes_opt import UtilityFunction
from typing import Tuple, Callable
import nevergrad as ng
import numpy as np
from bayes_opt import BayesianOptimization
from objective_functions import objective_function_v3

TRUTH_VALUE = np.array([
    210,  # print temperature
    4,    # retraction distance
    40    # reatraction speed
])


def round_to_step(x: float, step: int) -> int:
    return step * round(x/step)


def discrete_step_wrapper(
    x: Tuple[float, range],
    y: Tuple[float, range],
    z: Tuple[float, range]
):
    """
    Wraps the continous probs from the bayesian optimizer into
    discrete values binned to the specified step size.
    """

    nx = round_to_step(x[0], x[1].step)
    ny = round_to_step(y[0], y[1].step)
    nz = round_to_step(z[0], z[1].step)

    return objective_function_v3(nx, ny, nz, TRUTH_VALUE, minimize=False)


def mutate_previous_probe_then_do(optimizer: BayesianOptimization, then_do: Callable):
    """
    The optimizers previously probed point is overwritten with the result
    of round_to_step. E.g. the optimizer probes 178.481284 which is
    casted to 175. The probe will be overwritten from 178.481284
    to 175.
    """
    if len(optimizer.res) > 0:
        optimizer.res[-1]['params']['x'] = round_to_step(
            optimizer.res[-1]['params']['x'], x_range.step)
        optimizer.res[-1]['params']['y'] = round_to_step(
            optimizer.res[-1]['params']['y'], y_range.step)
        optimizer.res[-1]['params']['z'] = round_to_step(
            optimizer.res[-1]['params']['z'], z_range.step)

    return then_do


x_range = range(180, 220, 5)
y_range = range(2, 8, 1)
z_range = range(30, 60, 10)

pbounds = {'x': (180, 220), 'y': (2, 8), 'z': (30, 60)}

# %% Automatic steps

optimizer = BayesianOptimization(
    f=lambda x, y, z:
        discrete_step_wrapper(
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
