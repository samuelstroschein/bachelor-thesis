import nevergrad as ng
from nevergrad.optimization.base import Optimizer
from objective_functions import objective_function_v2
from nevergrad_algorithm_base import NevergradAlgorithmBase


algorithm = NevergradAlgorithmBase(
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
    steps[0], objective_function_v2(*steps[0].args, ranking))  # type: ignore
algorithm.tell_loss(
    steps[1], objective_function_v2(*steps[1].args, ranking))  # type: ignore

print(f'First step {steps[0].args}')  # type:ignore
print(f'Second step {steps[1].args}')  # type:ignore

for i in range(10):
    steps.append(algorithm.step())
    print(f"Next step: {steps[-1].args}")  # type:ignore
    rank = int(input("Which rank does the new step has? "))
    ranking.insert(rank, [*steps[-1].args])  # type: ignore
    # reinitialize the algorithm (to apply new ranking)
    algorithm = NevergradAlgorithmBase(
        ng.families.ParametrizedBO(
            utility_kind="ei",
            utility_kappa=1,
            utility_xi=0
        )
    )
    # tell new ranking
    for step in steps:
        algorithm.tell_loss(step, objective_function_v2(  # type: ignore
            *step.args, ranking))  # type: ignore

print(algorithm.optimizer.provide_recommendation().args)  # type:ignore
