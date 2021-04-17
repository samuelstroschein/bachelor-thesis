"""
retraction_distance = range(2,10)
retraction_speed = range(30,60)
prime_speed = range(30,60)
"""

#%%
import nevergrad as ng


def square(x, y=12):
    return sum((x - 0.5) ** 2) + abs(y)


#%%
# optimization on x as an array of shape (2,)
optimizer = ng.optimizers.NGOpt(parametrization=2, budget=100)
recommendation = optimizer.minimize(square)  # best value
print(recommendation.value)
