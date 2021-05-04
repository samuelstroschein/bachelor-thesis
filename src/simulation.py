# %%
from typing import List
import numpy as np
from bayes_opt import UtilityFunction
from custom_bayesian_optimization import CustomBayesianOptimization


def simulate_objective_function(parameters: List[int], step_sizes: List[int], truth_value) -> float:
    """
    Calculates the deviation of each individual the TRUTH_VALUES 
    while adjusting each values weight based on the range of the parameters.
    """
    result = [
        abs(truth_value[0] - parameters[0]) * step_sizes[0],
        abs(truth_value[1] - parameters[1]) * step_sizes[1],
        abs(truth_value[2] - parameters[2]) * step_sizes[2],
    ]
    return -1 * abs(np.sum(result))


def simulate_ranking(probed_points: List[dict]) -> int:
    return 1


def run_simulation(hyperparameter: UtilityFunction, bounds: dict, epochs: int) -> CustomBayesianOptimization:
    random_truth_value = [220, 4, 40]
    step_sizes = [5, 1, 10]
    optimizer = CustomBayesianOptimization(
        f=None,
        parameter_step_sizes=step_sizes,
        pbounds=bounds,
        verbose=2,  # verbose = 1 prints only when a maximum is observed, verbose = 0 is silent
    )
    first_point = optimizer.suggest(hyperparameter)
    second_point = optimizer.suggest(hyperparameter)
    for _ in range(epochs):
        next_point = optimizer.suggest(hyperparameter)
        print(next_point)
        rank = simulate_objective_function(
            parameters=[
                next_point['x'],
                next_point['y'],
                next_point['z'],
            ],
            truth_value=random_truth_value,
            step_sizes=step_sizes,
        )
        optimizer.register(params=next_point, target=rank)
    return optimizer


# %%
acquisition_functions = ['ucb', 'ei', 'poi']

pbounds = {'x': (180, 220), 'y': (2, 8), 'z': (30, 60)}

result = run_simulation(
    hyperparameter=UtilityFunction(
        kind="ucb", kappa=20, xi=1
    ),
    bounds=pbounds,
    epochs=12
)

print(result.max)
# %%
