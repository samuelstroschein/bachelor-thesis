# %%
from mpl_toolkits.mplot3d.axes3d import get_test_data
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from typing import Callable, List, Tuple
import numpy as np
from bayes_opt import UtilityFunction
from custom_bayesian_optimization import CustomBayesianOptimization
import pandas as pd
import statistics
import random


def calculate_loss(parameters: np.ndarray, step_sizes: List[int], truth_value):
    """
    Calculates the deviation of each individual the TRUTH_VALUES
    while adjusting each values weight based on the range of the parameters.
    """
    result = []
    for i in range(len(parameters)):
        result.append(abs(truth_value[i] - parameters[i]) / step_sizes[i])
    return -1 * np.sum(result)


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
    step_sizes: List[int],
    bounds: dict,
    epochs: int,
    truth_value: list,
) -> Tuple[CustomBayesianOptimization, List]:
    optimizer = CustomBayesianOptimization(
        f=None,
        parameter_step_sizes=step_sizes,
        pbounds=bounds,
        verbose=2,  # verbose = 1 prints only when a maximum is observed, verbose = 0 is silent
    )
    first_point = optimizer.parameters_to_array(
        optimizer.suggest(hyperparameter)
    )
    second_point = optimizer.parameters_to_array(
        optimizer.suggest(hyperparameter)
    )
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
        optimizer.tell_ranking(
            simulated_ranking(
                already_probed_points + [next_point],
                step_sizes,
                truth_value,
                calculate_loss
            )
        )
    return optimizer, order_of_probed_points


def random_baseline_simulation(
    hyperparameter: UtilityFunction,
    step_sizes: List[int],
    bounds: dict,
    epochs: int,
    truth_value: list,
) -> Tuple[CustomBayesianOptimization, List]:
    optimizer = CustomBayesianOptimization(
        f=None,
        parameter_step_sizes=step_sizes,
        pbounds=bounds,
        verbose=2,  # verbose = 1 prints only when a maximum is observed, verbose = 0 is silent
    )
    first_point = optimizer.parameters_to_array(
        optimizer.suggest(hyperparameter)
    )
    second_point = optimizer.parameters_to_array(
        optimizer.suggest(hyperparameter)
    )
    order_of_probed_points: List[List[int]] = [
        first_point.tolist(), second_point.tolist()
    ]
    for _ in range(epochs):
        next_point = optimizer.parameters_to_array(
            optimizer.suggest(hyperparameter)
        ).tolist()
        while next_point in order_of_probed_points:
            next_point = optimizer.parameters_to_array(
                optimizer.suggest(hyperparameter)
            ).tolist()
        order_of_probed_points.append(next_point)

    optimizer.tell_ranking(
        simulated_ranking(
            order_of_probed_points,  # type: ignore
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
    step_sizes: List[int],
    xi: np.ndarray,
    num_runs=10
) -> List[dict]:
    result: List[dict] = []
    for k in kappa:
        for x in xi:
            epochs_until_solution = []  # type:ignore
            losses_of_solutions = []  # type:ignore
            has_error = False
            for i in range(num_runs):
                print(f"starting run {i}")
                try:
                    bounds_as_list = list(bounds.values())
                    random_truth_value: List[int] = []
                    for lower, upper in bounds_as_list:
                        random_truth_value.append(
                            random.randint(lower, upper)
                        )
                    #! change simulation here to random or not
                    simulation, order_of_probed_points = run_simulation(
                        step_sizes=step_sizes,
                        hyperparameter=UtilityFunction(
                            kind=acquisition_function,
                            kappa=k,
                            xi=x,
                        ),
                        truth_value=random_truth_value,
                        bounds=bounds,
                        epochs=18
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
                except KeyError:
                    # a sampled point is not unique
                    print(
                        "Warning: a sampled point not not unique; trial terminated."
                    )
                    has_error = True
                    break
            if not has_error:
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

pbounds = {
    'x': (180, 220),
    'y': (2, 8),
    'z': (90, 110)
}

step_sizes = [5, 1, 2]

# %%
"""
First Simulation:

Determining if randomizing the initial samples improves convergence. 
"""
acquisition_functions = ['ucb', 'ei', 'poi']
results: List[dict] = []

for acquisition_function in acquisition_functions:
    results = results + experiment(
        step_sizes=step_sizes,
        acquisition_function=acquisition_function,
        bounds=pbounds,
        num_runs=10,
        kappa=np.arange(0, 10, 4),
        xi=np.arange(0, 1, 0.4)
    )

df = pd.DataFrame(results)
df.to_csv('hyperparameter_tuning_first_simulation.csv')


df.groupby("random_initial_points").mean()
"""
Result:
Randomized is better.
"""
# %%
"""
Second Simulation:

Determining which acquisition function and range of kappa,xi should further be investigated. 
"""
acquisition_functions = ['ucb', 'ei', 'poi']
results = []

for acquisition_function in acquisition_functions:
    results = results + experiment(
        step_sizes=step_sizes,
        acquisition_function=acquisition_function,
        bounds=pbounds,
        num_runs=10,
        kappa=np.arange(0, 10, 1),
        xi=np.arange(0, 1, 0.1)
    )

df2 = pd.DataFrame(results)

df2.to_csv('hyperparameter_tuning_second_simulation.csv')

acq = df2.groupby("acquisition_function")[["mean_loss"]].mean().round(2)
df_ei = df2.loc[df2['acquisition_function'] == "ei"]
kappa = df_ei.groupby("kappa")[["mean_loss"]].mean().round(2)
xi = df_ei.groupby("xi")[["mean_loss"]].mean().round(2)

"""
Result:
Expected Improvement acq function is best
Bounds of kappa and xi have been adjusted. See next simulation.
"""
# %%
"""
Third Simulation:

Determining optimal kappa and xi parameters for ei acquisition function.
"""
acquisition_functions = ['ei']
results = []

for acquisition_function in acquisition_functions:
    results = results + experiment(
        step_sizes=step_sizes,
        acquisition_function=acquisition_function,
        bounds=pbounds,
        num_runs=100,
        kappa=np.arange(1, 6, 1),
        xi=np.arange(0.5, 1.5, 0.1)
    )

df3 = pd.DataFrame(results)

df3.to_csv('hyperparameter_tuning_third_simulation.csv')

"""
Result:
kappa = 1, xi = 0.7 is optimzal (and ei acq function)
"""

# %%
"""
Fourth Simulation:

Random selection of next probes in order to create a baseline model
"""
acquisition_functions = ['ei']
results = []

for acquisition_function in acquisition_functions:
    results = results + experiment(
        step_sizes=step_sizes,
        acquisition_function=acquisition_function,
        bounds=pbounds,
        num_runs=100,
        kappa=np.arange(1, 2, 1),
        xi=np.arange(0.7, 0.75, 0.1)
    )

df4 = pd.DataFrame(results)

df4.to_csv('hyperparameter_tuning_random_baseline.csv')

"""
Result:
Better than random
"""

# %%
"""
Fifth Simulation:

Random and none random selection with 5 variables
"""

pbounds = {
    'a': (180, 220),
    'b': (2, 8),
    'c': (90, 110),
    'd': (30, 60),
    'd': (40, 50),
}

step_sizes = [5, 1, 2, 5, 1]

acquisition_functions = ['ei']
results = []

for acquisition_function in acquisition_functions:
    results = results + experiment(
        step_sizes=step_sizes,
        acquisition_function=acquisition_function,
        bounds=pbounds,
        num_runs=100,
        kappa=np.arange(1, 2, 1),
        xi=np.arange(0.7, 0.75, 0.1)
    )

df5 = pd.DataFrame(results)

# df5.to_csv('hyperparameter_tuning_random_baseline_5_parameter.csv')

df5.to_csv('hyperparameter_tuning_random_optimal_5_parameter.csv')

"""
Result:

"""

# %%
"""
Plotting convergence process
"""
pbounds = {
    'x': (180, 220),
    'y': (2, 8),
    'z': (90, 110),
}

step_sizes = [5, 1, 2]

truth_value = [215, 4, 98]

simulation, order_of_probed_points = run_simulation(
    step_sizes=step_sizes,
    hyperparameter=UtilityFunction(
        kind='ei',
        kappa=1,
        xi=0.7,
    ),
    truth_value=truth_value,
    bounds=pbounds,
    epochs=18
)

# %%


def plot_convergence(
    order_of_probed_points: List[List[int]],
    loss_function: Callable,
    truth_value: List[int],
    step_sizes: List[int],
) -> None:
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    # probed points
    x = np.array([point[0]
                 for point in order_of_probed_points] + [truth_value[0]])
    y = np.array([point[1]
                 for point in order_of_probed_points] + [truth_value[1]])
    z = np.array([point[2]
                 for point in order_of_probed_points] + [truth_value[2]])
    c = np.array([loss_function(point, step_sizes, truth_value)
                 for point in order_of_probed_points] + [0])
    # ax.plot3D(x, y, z, 'grey')
    image = ax.scatter3D(x, y, z, c=c, cmap=plt.cool())
    ax.set_xlabel('print temperature')
    ax.set_ylabel('retraction distance')
    ax.set_zlabel('flow rate')
    fig.colorbar(image, pad=0.05, label="loss", location='left')
    plt.show()


def plot_loss(
    order_of_probed_points: List[List[int]],
    loss_function: Callable,
    truth_value: List[int],
    step_sizes: List[int],
) -> None:
    x = np.arange(len(order_of_probed_points))
    loss = np.array([loss_function(point, step_sizes, truth_value)
                     for point in order_of_probed_points])
    best_point = [loss[0]]
    for l in loss[1:]:
        if l > best_point[-1]:
            best_point.append(l)
        else:
            best_point.append(best_point[-1])
    plt.step(x, loss, label='loss of probed point')
    plt.step(x, best_point, label='loss of best point', linestyle='dashed')
    plt.legend(loc='lower right', borderaxespad=0.)
    plt.xlabel("epochs")
    plt.ylabel("loss")


plot_convergence(
    order_of_probed_points,
    calculate_loss,
    truth_value,
    step_sizes
)

# %%
plot_loss(
    order_of_probed_points,
    calculate_loss,
    truth_value,
    step_sizes
)

# %%
