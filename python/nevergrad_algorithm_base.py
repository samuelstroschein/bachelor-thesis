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
        # print(x.args)
        loss = self.objective_function(*x.args)
        self.optimizer.tell(x, loss)
