# %%
from typing import Callable, List, Tuple
import numpy as np
from bayes_opt import UtilityFunction
from custom_bayesian_optimization import CustomBayesianOptimization
import pandas as pd
import statistics


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


def run_simulation(
    hyperparameter: UtilityFunction,
    bounds: dict,
    epochs: int,
    truth_value: list,
) -> Tuple[CustomBayesianOptimization, List]:
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
        truth_value,
        calculate_loss
    ))
    order_of_probed_points: List[List[int]] = [
        first_point.tolist(), second_point.tolist()
    ]
    for _ in range(epochs):
        next_point = optimizer.parameters_to_array(
            optimizer.suggest(hyperparameter)
        ).tolist()
        order_of_probed_points.append(next_point)
        already_probed_points = optimizer._space._params.tolist()
        print(next_point)
        optimizer.tell_ranking(
            simulated_ranking(
                already_probed_points + [next_point],
                step_sizes,
                truth_value,
                calculate_loss
            )
        )
    return optimizer, order_of_probed_points


def experiment(
    acquisition_function: str,
    bounds: dict,
    kappa: np.ndarray,
    xi: np.ndarray,
    trials=5
) -> List[dict]:
    result: List[dict] = []
    for k in kappa:
        for x in xi:
            epochs_until_solution = []  # type:ignore
            losses_of_solutions = []  # type:ignore
            for _ in range(trials):
                random_truth_value = [200, 4, 40]
                simulation, order_of_probed_points = run_simulation(
                    hyperparameter=UtilityFunction(
                        kind=acquisition_function,
                        kappa=k,
                        xi=x,
                    ),
                    truth_value=random_truth_value,
                    bounds=bounds,
                    epochs=10
                )
                best_point = simulation.parameters_to_array(
                    simulation.max['params']
                ).astype(int).tolist()
                losses_of_solutions.append(
                    calculate_loss(
                        parameters=best_point,
                        step_sizes=simulation.parameter_step_sizes,
                        truth_value=random_truth_value,
                    )
                )
                epochs_until_solution.append(
                    order_of_probed_points.index(best_point)
                )
            result.append({
                "acquisition_function": acquisition_function,
                "kappa": k,
                "xi": x,
                "median_best_solution": statistics.median(epochs_until_solution),
                "mean_loss": statistics.mean(losses_of_solutions)
            })
            print(result[-1])
    return result


# %%
acquisition_functions = ['ucb', 'ei', 'poi']

pbounds = {'x': (180, 220), 'y': (2, 8), 'z': (30, 60)}

results = pd.DataFrame(
    columns=[
        'acquisition_function',
        'kappa',
        'xi',
        'median_best_solution',
        'mean_loss'
    ]
)

results = []

results = results + experiment(
    acquisition_function='ei',
    bounds=pbounds,
    kappa=np.arange(0, 10, 4),
    xi=np.arange(0, 1, 0.4)
)

df = pd.DataFrame(results)

print(df)
# %%
