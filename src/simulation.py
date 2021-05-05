# %%
from typing import Callable, List, Tuple
import numpy as np
from bayes_opt import UtilityFunction
from custom_bayesian_optimization import CustomBayesianOptimization


def calculate_loss(parameters: np.ndarray, step_sizes: List[int], truth_value) -> float:
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


def simulated_ranking(
    probed_points: List[np.ndarray],
    step_sizes: List[int],
    truth_value: List[int],
    calculate_loss: Callable
) -> List[List[int]]:
    """
    Calculates the loss for each probed point and returns the probed points as a sorted list.
    The index position of a point corresponds to the rank. The higher, the better. 
    Example:
        ranking[0] -> rank 0
        ranking[1] -> rank 1
        ...
    """
    losses: List[Tuple[np.ndarray, float]] = [
        (point, calculate_loss(point, step_sizes, truth_value)) for point in probed_points
    ]
    # sort by loss
    losses.sort(key=lambda x: x[1])
    # remove loss value
    ranking = list(map(lambda x: list(x[0]), losses))
    return ranking


def run_simulation(hyperparameter: UtilityFunction, bounds: dict, epochs: int) -> CustomBayesianOptimization:
    random_truth_value = [200, 4, 40]
    step_sizes = [5, 1, 10]
    optimizer = CustomBayesianOptimization(
        f=None,
        parameter_step_sizes=step_sizes,
        pbounds=bounds,
        verbose=2,  # verbose = 1 prints only when a maximum is observed, verbose = 0 is silent
    )
    first_point = np.array([180, 2, 30])
    second_point = np.array([220, 8, 60])
    optimizer.tell_ranking(simulated_ranking(
        [first_point, second_point],
        step_sizes,
        random_truth_value,
        calculate_loss
    ))
    for _ in range(epochs):
        next_point = optimizer.parameters_to_array(
            optimizer.suggest(hyperparameter)
        ).tolist()
        already_probed_points = optimizer._space._params.tolist()
        print(next_point)
        optimizer.tell_ranking(
            simulated_ranking(
                already_probed_points + [next_point],
                step_sizes,
                random_truth_value,
                calculate_loss
            )
        )
    return optimizer


# %%
acquisition_functions = ['ucb', 'ei', 'poi']

pbounds = {'x': (180, 220), 'y': (2, 8), 'z': (30, 60)}

result = run_simulation(
    hyperparameter=UtilityFunction(
        kind="ei",
        kappa=10,
        xi=0.1
    ),
    bounds=pbounds,
    epochs=10
)

print(result.max)
# %%
