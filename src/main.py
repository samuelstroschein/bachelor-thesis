# %%
from bayes_opt import UtilityFunction
from custom_bayesian_optimization import CustomBayesianOptimization

bounds = {
    'x': (180, 220),
    'y': (2, 8),
    'z': (90, 110)
}

step_sizes = [5, 1, 2]

hyperparameter = UtilityFunction(
    kind='ei',
    kappa=1,
    xi=0.7,
),

optimizer = CustomBayesianOptimization(
    f=None,
    parameter_step_sizes=step_sizes,
    pbounds=bounds,
    verbose=2,
)
first_point = optimizer.parameters_to_array(
    optimizer.suggest(hyperparameter)
)
second_point = optimizer.parameters_to_array(
    optimizer.suggest(hyperparameter)
)
print(f'You have to print: {first_point}')
print(f"You have to print: {second_point}")

response = input(
    "Is the second print better than the first one? Answer with 0 or 1: ")

optimizer.tell_ranking(
    [first_point, second_point] if response == "1" else [second_point, first_point]
)

for _ in range(15):
    next_point = optimizer.parameters_to_array(
        optimizer.suggest(hyperparameter)
    ).tolist()
    print(f"Next test print: {next_point}")
    already_probed_points: list = optimizer._space._params.tolist()
    response = int(input(f"Which rank does the print have? "))  # type: ignore
    already_probed_points.insert(response, next_point)  # type:ignore
    optimizer.tell_ranking(already_probed_points)

# %%
