# %%
from bayes_opt import UtilityFunction
from objective_functions import objective_function_v3
from custom_bayesian_optimization import CustomBayesianOptimization


def run_simulation(hyperparameter: UtilityFunction, bounds: dict, epochs: int) -> CustomBayesianOptimization:
    random_truth_value = [220, 4, 40]
    optimizer = CustomBayesianOptimization(
        f=lambda x, y, z: objective_function_v3(
            x, y, z, random_truth_value, minimize=False
        ),
        parameter_step_sizes=[5, 1, 10],
        pbounds=bounds,
        verbose=2,  # verbose = 1 prints only when a maximum is observed, verbose = 0 is silent
    )
    for _ in range(epochs):
        next_point = optimizer.suggest(hyperparameter)
        print(next_point)
        rank = objective_function_v3(
            next_point['x'],
            next_point['y'],
            next_point['z'],
            random_truth_value,
            minimize=False
        )
        optimizer.register(params=next_point, target=rank)
    return optimizer


# %%
acquisition_functions = ['ucb', 'ei', 'poi']

pbounds = {'x': (180, 220), 'y': (2, 8), 'z': (30, 60)}

result = run_simulation(
    hyperparameter=UtilityFunction(
        kind="ucb", kappa=10, xi=1
    ),
    bounds=pbounds,
    epochs=12
)

print(result.max)
# %%
