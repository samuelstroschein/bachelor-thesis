# %%
import nevergrad as ng
import numpy as np


RETRACTION_DISTANCE = range(2, 11)
RETRACTION_SPEED = range(30, 61)
PRIME_SPEED = range(30, 61)

TRUTH_VALUE = np.array([
    3,  # retraction_distance is 3 but * 10 to be equal to other parameters
    30,  # retraction_speed
    40   # prime_speed
])


def objective_function(x: np.ndarray) -> float:
    """
    Caluclates the absolute distance of x to the TRUTH_VALUE squared.
    """
    result = [
        abs((TRUTH_VALUE[0]*10 - x[0] * 10)) ** 2,
        abs(TRUTH_VALUE[1] - x[1]) ** 2,
        abs(TRUTH_VALUE[2] - x[2]) ** 2,
    ]
    return abs(np.sum(result))


def objective_function_variables(
    x: ng.p.Scalar,
    y: ng.p.Scalar,
    z: ng.p.Scalar
) -> float:
    return objective_function(np.array([x, y, z]))

# %%


instrumentation = ng.p.Instrumentation(
    ng.p.Scalar(
        lower=RETRACTION_DISTANCE[0],
        upper=RETRACTION_DISTANCE[-1]
    ),
    ng.p.Scalar(
        lower=RETRACTION_SPEED[0],
        upper=RETRACTION_SPEED[-1]
    ),
    ng.p.Scalar(
        lower=PRIME_SPEED[0],
        upper=PRIME_SPEED[-1]
    ),
)

optimizer = ng.optimizers.NGOpt(
    parametrization=instrumentation,
    budget=5,
    num_workers=1
)

# optimizer.suggest([5, 50, 50])

for _ in range(optimizer.budget):  # type: ignore
    x = optimizer.ask()
    print(x.args)
    loss = objective_function_variables(*x.args)
    optimizer.tell(x, loss)

recommendation = optimizer.provide_recommendation()
print(recommendation.args)

# %%
