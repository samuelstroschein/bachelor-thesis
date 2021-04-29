import nevergrad as ng
from nevergrad.optimization.base import Optimizer
from objective_functions import objective_function_v2_lego


class LegoBase:
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
        instrumentation = instrumentation = ng.p.Instrumentation(
            ng.p.TransitionChoice(temperature_range),
            ng.p.TransitionChoice(retraction_distance_range),
            ng.p.TransitionChoice(retraction_speed_range),
            # ng.p.TransitionChoice(prime_speed_range),
        )
        self.optimizer = optimizer(
            parametrization=instrumentation,
            budget=5,
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


algorithm = LegoBase(
    ng.families.ParametrizedBO(
        utility_kind="ei",
        utility_kappa=1,
        utility_xi=0
    )
)

# two initial steps to start ranking
steps = [algorithm.step(), algorithm.step()]
# initial ranking
ranking = [[*steps[0].args], [*steps[1].args]]  # type: ignore
# tell the initial ranking
algorithm.tell_loss(
    steps[0], objective_function_v2_lego(*steps[0].args, ranking))  # type: ignore
algorithm.tell_loss(
    steps[1], objective_function_v2_lego(*steps[1].args, ranking))  # type: ignore

print(f'First step {steps[0].args}')  # type:ignore
print(f'Second step {steps[1].args}')  # type:ignore

for i in range(10):
    steps.append(algorithm.step())
    print(f"Next step: {steps[-1].args}")  # type:ignore
    rank = int(input("Which rank does the new step has? "))
    ranking.insert(rank, [*steps[-1].args])  # type: ignore
    # reinitialize the algorithm (to apply new ranking)
    algorithm = LegoBase(
        ng.families.ParametrizedBO(
            utility_kind="ei",
            utility_kappa=1,
            utility_xi=0
        )
    )
    # tell new ranking
    for step in steps:
        algorithm.tell_loss(step, objective_function_v2_lego(  # type: ignore
            *step.args, ranking))  # type: ignore

print(algorithm.optimizer.provide_recommendation().args)  # type:ignore
