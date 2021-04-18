# %%
import nevergrad as ng
import numpy as np
from typing import Tuple


class NevergradAlgorithmBase:
    def __init__(self,
                 objective_function,
                 optimizer,
                 retraction_distance_range: Tuple[float, float] = (2, 10),
                 retraction_speed_range: Tuple[float, float] = (30, 60),
                 prime_speed_range: Tuple[float, float] = (30, 60),
                 ) -> None:
        self.objective_function = objective_function
        instrumentation = instrumentation = ng.p.Instrumentation(
            ng.p.Scalar(
                lower=retraction_distance_range[0],
                upper=retraction_distance_range[1]
            ),
            ng.p.Scalar(
                lower=retraction_speed_range[0],
                upper=retraction_speed_range[1]
            ),
            ng.p.Scalar(
                lower=prime_speed_range[0],
                upper=prime_speed_range[1]
            ),
        )
        self.optimizer = optimizer(
            parametrization=instrumentation,
            budget=5,
            num_workers=1
        )

    def step(self):
        x = self.optimizer.ask()
        print(x.args)
        loss = self.objective_function(*x.args)
        self.optimizer.tell(x, loss)


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
        abs((TRUTH_VALUE[0]*10 - x[0]*10)) ** 2,
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


algorithm = NevergradAlgorithmBase(
    objective_function_variables, ng.optimizers.NGOpt)


for _ in range(20):  # type: ignore
    algorithm.step()

recommendation = algorithm.optimizer.provide_recommendation()
print('\n')
print(f'recommendation: {recommendation.args}\ntruth value: {TRUTH_VALUE}')

# %%
