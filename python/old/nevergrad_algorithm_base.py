import nevergrad as ng
from nevergrad.optimization.base import Optimizer
from typing import Tuple


class NevergradAlgorithmBase:
    def __init__(self,
                 optimizer,
                 temperature_range: range = range(180, 221, 5),
                 retraction_distance_range: range = range(2, 11, 1),
                 retraction_speed_range: range = range(30, 61, 10),
                 #  prime_speed_range: range = range(30, 60, 10),
                 ) -> None:
        """
        The ranges define the discret values for each parameter.

        E.g. the temperature range may lay between 180,221,10 which means
        each suggested temperature is either 180,190,200,210,220.
        """
        self.instrumentation = ng.p.Instrumentation(
            ng.p.TransitionChoice(temperature_range),
            ng.p.TransitionChoice(retraction_distance_range),
            ng.p.TransitionChoice(retraction_speed_range),
            # ng.p.TransitionChoice(prime_speed_range),
        )
        self.optimizer = optimizer(
            parametrization=self.instrumentation,
            budget=50,
            num_workers=1
        )

    def step(self) -> Optimizer:
        x = self.optimizer.ask()
        return x
        # # print(x.args)
        # loss = self.objective_function(*x.args)
        # self.optimizer.tell(x, loss)

    def tell_loss(self, x: Optimizer, loss: float) -> None:
        self.optimizer.tell(x, loss)
