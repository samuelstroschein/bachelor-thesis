"""
retraction_distance = range(2,10)
retraction_speed = range(30,60)
prime_speed = range(30,60)
"""

# %%
import nevergrad as ng
import numpy as np

RETRACTION_DISTANCE = range(2, 11)
RETRACTION_SPEED = range(30, 61)
PRIME_SPEED = range(30, 61)

TRUTH_VALUE = np.array([
    3,   # retraction_distance
    30,  # retraction_speed
    40   # prime_speed
])


def objective_function(x: np.ndarray) -> float:
    """
    Caluclates the absolute distance of x to the TRUTH_VALUE.
    """
    return abs(np.sum(np.subtract(TRUTH_VALUE, x)))


# %%
# optimizer = ng.optimizers.NGOpt(parametrization=3, budget=100)
optimizer = ng.optimizers.RandomSearch(parametrization=3, budget=1000)

# retraction_distance constraint
optimizer.parametrization.register_cheap_constraint(
    lambda x: RETRACTION_DISTANCE[0] <= x[0])
# optimizer.parametrization.register_cheap_constraint(
#     lambda x: RETRACTION_DISTANCE[0] <= x[0] <= RETRACTION_DISTANCE[-1])
# # retraction_speed constraint
# optimizer.parametrization.register_cheap_constraint(
#     lambda x: RETRACTION_DISTANCE[0] <= x[1] <= RETRACTION_DISTANCE[-1])
# # prime_speed constraint
# optimizer.parametrization.register_cheap_constraint(
#     lambda x: RETRACTION_DISTANCE[0] <= x[2] <= RETRACTION_DISTANCE[-1])

recommendation = optimizer.minimize(
    objective_function=objective_function)  # best value
print(recommendation.value)

# %%
