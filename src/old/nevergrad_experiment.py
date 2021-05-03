# %%
from typing import Any, List, Tuple
import nevergrad as ng
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from nevergrad_algorithm_base import NevergradAlgorithmBase
from objective_functions import objective_function_v1, rank_function_v1, objective_function_v3


def plot_optimization(bo):
    x = np.linspace(-2, 10, 10000)
    mean, sigma = bo._gp.predict(x.reshape(-1, 1), return_std=True)

    plt.figure(figsize=(16, 9))
    plt.plot(x, mean)
    plt.fill_between(x, mean + sigma, mean - sigma, alpha=0.1)
    plt.scatter(bo.space.params.flatten(),
                bo.space.target, c="red", s=50, zorder=10)
    plt.show()


class Experiment:
    def __init__(self,
                 recommendation: list,
                 loss_of_recommendation: float,
                 losses: list,
                 steps: list,
                 optimizer=None,
                 ) -> None:
        self.recommendation = recommendation
        self.loss_of_recommendation = loss_of_recommendation
        self.losses = losses
        self.steps = steps
        self.optimizer = optimizer


def run_experiment_v1(algorithm, epochs: int) -> Experiment:
    """
    Returns the recommendation, all losses and loss of recommendation
    """
    steps = []
    losses = []
    for _ in range(epochs):  # type: ignore
        x = algorithm.step()
        steps.append(x)
        loss = objective_function_v1(*x.args)
        losses.append(loss)
        algorithm.tell_loss(x, loss)
    recommendation = algorithm.optimizer.provide_recommendation()
    return Experiment(recommendation.args, objective_function_v1(*recommendation.args), losses, steps, algorithm.optimizer)


def run_experiment_v2(algorithm_init, epochs: int) -> Experiment:
    """
    Returns the recommendation, all losses and loss of recommendation.

    Utilizes ranking based objective_function_v3. The ranking position
    is determined by the objective_v1 loss.
    """
    # two initial steps to start ranking
    algorithm = algorithm_init()
    first_step = algorithm.optimizer.parametrization.spawn_child(
        new_value=((215, 7, 50), algorithm.instrumentation.kwargs)
    )
    second_step = algorithm.optimizer.parametrization.spawn_child(
        new_value=((185, 3, 30), algorithm.instrumentation.kwargs)
    )
    # steps = tuple (step, loss from objective_function_v1)
    steps: List[Tuple] = [
        (first_step, objective_function_v3(*first_step.args)),
        (second_step, objective_function_v3(*second_step.args)),
    ]
    # tell the initial ranking
    # initial ranking
    intial_ranking: Any = [list(steps[0][0].args), list(steps[1][0].args)]

    algorithm.tell_loss(first_step, rank_function_v1(  # type: ignore
        *steps[0][0].args, intial_ranking
    ))  # type: ignore
    algorithm.tell_loss(second_step, rank_function_v1(  # type: ignore
        *steps[1][0].args, intial_ranking
    ))  # type: ignore
    for _ in range(epochs):  # type: ignore
        step = algorithm.step()
        loss = objective_function_v3(*step.args)
        steps.append((step, loss))
        ranking: Any = steps.copy()
        # sort by loss
        ranking.sort(key=lambda x: x[1])
        # remove loss value
        ranking = list(map(lambda x: list(x[0].args), ranking))
        # recreate the algorithm in order to take new ranking into account
        algorithm = algorithm_init()
        # algorithm.tell_loss(step, objective_function_v3(  # type: ignore
        #     *step.args)
        # )
        # # tell new ranking
        for step in steps:
            algorithm.tell_loss(step[0], rank_function_v1(  # type: ignore
                *step[0].args, ranking
            )
            )

    recommendation = algorithm.optimizer.provide_recommendation()

    return Experiment(
        recommendation.args,
        0,  # loss is the 0 element in ranking so 0
        list(map(lambda x: x[1], steps)),
        list(map(lambda x: x[0], steps)),
        algorithm.optimizer
    )


# %%
# epochs = 12

# figure = go.Figure()

# bayesian1 = run_experiment_v1(NevergradAlgorithmBase(
#     ng.families.ParametrizedBO(
#         utility_kind="ei",
#         utility_kappa=1,
#         utility_xi=0
#     )
# ), epochs=epochs)

# figure.add_trace(go.Scatter(x=list(range(0, epochs)), y=bayesian1.losses,
#                             mode='lines+markers',
#                             name='bayesian1'))

# bayesian2 = run_experiment_v1(NevergradAlgorithmBase(
#     ng.families.ParametrizedBO(
#         utility_kind="ei",
#         utility_kappa=1,
#         utility_xi=0.5
#     )
# ), epochs=epochs)

# figure.add_trace(go.Scatter(x=list(range(0, epochs)), y=bayesian2.losses,
#                             mode='lines+markers',
#                             name='bayesian2'))

# figure.show()

# %%
epochs = 50

figure = go.Figure()

experiment1 = run_experiment_v2(lambda: NevergradAlgorithmBase(
    ng.families.ParametrizedBO(
        utility_kind='ei',
        utility_kappa=5,
        utility_xi=10,
        gp_parameters={'alpha': 1}
    )
), epochs=epochs)

figure.add_trace(
    go.Scatter(
        x=list(range(0, epochs)),
        y=experiment1.losses,
        mode='lines+markers',
        name='experiment1',
    )
)

experiment2 = run_experiment_v2(lambda: NevergradAlgorithmBase(
    ng.optimizers.cGA
), epochs=epochs)

figure.add_trace(
    go.Scatter(
        x=list(range(0, epochs)),
        y=experiment2.losses,
        mode='lines+markers',
        name='experiment2'
    )
)

# experiment3 = run_experiment_v2(lambda: NevergradAlgorithmBase(
#     ng.families.ParametrizedBO(
#         utility_kind='ei',
#         utility_kappa=3,
#         utility_xi=1,
#         gp_parameters={'alpha': 1}
#     )
# ), epochs=epochs)

# figure.add_trace(
#     go.Scatter(
#         x=list(range(0, epochs)),
#         y=experiment3.losses,
#         mode='lines+markers',
#         name='experiment3'
#     )
# )

# experiment4 = run_experiment_v2(lambda: NevergradAlgorithmBase(
#     ng.optimizers.RandomSearch
# ), epochs=epochs)

# figure.add_trace(
#     go.Scatter(
#         x=list(range(0, epochs)),
#         y=experiment4.losses,
#         mode='lines+markers',
#         name='experiment4'
#     )
# )

figure.show()

# %%
plot_optimization(experiment1.optimizer.bo)