# %%
from typing import Any, List, Tuple
import nevergrad as ng
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from nevergrad_algorithm_base import NevergradAlgorithmBase
from objective_functions import objective_function_v1, objective_function_v2


class Experiment:
    def __init__(self,
                 recommendation: list,
                 loss_of_recommendation: float,
                 losses: list,
                 steps: list) -> None:
        self.recommendation = recommendation
        self.loss_of_recommendation = loss_of_recommendation
        self.losses = losses
        self.steps = steps


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
    return Experiment(recommendation.args, objective_function_v1(*recommendation.args), losses, steps)


def run_experiment_v2(algorithm, epochs: int) -> Experiment:
    """
    Returns the recommendation, all losses and loss of recommendation.

    Utilizes ranking based objective function v2. The ranking position
    is determined by the objective_v1 loss.
    """
    # two initial steps to start ranking
    first_step = algorithm.optimizer.parametrization.spawn_child(
        new_value=((215, 7, 50), {})
    )
    second_step = algorithm.optimizer.parametrization.spawn_child(
        new_value=((185, 3, 30), {})
    )
    # steps = tuple (step, loss from objective_function_v1)
    steps: List[Tuple] = [
        (list(first_step.args), objective_function_v1(*first_step.args)),
        (list(second_step.args), objective_function_v1(*second_step.args)),
    ]
    # tell the initial ranking
    # initial ranking
    intial_ranking: Any = [steps[0][0], steps[1][0]]

    algorithm.tell_loss(first_step, objective_function_v2(  # type: ignore
        *steps[0][0], intial_ranking
    ))  # type: ignore
    algorithm.tell_loss(second_step, objective_function_v2(  # type: ignore
        *steps[1][0], intial_ranking
    ))  # type: ignore
    for _ in range(epochs):  # type: ignore
        step = algorithm.step()
        loss = objective_function_v1(*step.args)
        steps.append((list(step.args), loss))
        ranking: Any = steps
        # sort by loss
        ranking.sort(key=lambda x: x[1])
        # remove loss value
        ranking = list(map(lambda x: list(x[0]), ranking))
        algorithm.tell_loss(
            step, objective_function_v2(*step.args, ranking)  # type: ignore
        )
    recommendation = algorithm.optimizer.provide_recommendation()
    final_ranking: Any = steps
    # sort by loss
    final_ranking.sort(key=lambda x: x[1])
    # remove loss value
    final_ranking = list(map(lambda x: list(x[0]), final_ranking))

    return Experiment(
        recommendation.args, objective_function_v2(  # type: ignore
            *recommendation.args, final_ranking
        ),
        list(map(lambda x: x[1], steps)),
        list(map(lambda x: x[0], steps))
    )


# %%
epochs = 12

figure = go.Figure()

bayesian1 = run_experiment_v1(NevergradAlgorithmBase(
    ng.families.ParametrizedBO(
        utility_kind="ei",
        utility_kappa=1,
        utility_xi=0
    )
), epochs=epochs)

figure.add_trace(go.Scatter(x=list(range(0, epochs)), y=bayesian1.losses,
                            mode='lines+markers',
                            name='bayesian1'))

bayesian2 = run_experiment_v1(NevergradAlgorithmBase(
    ng.families.ParametrizedBO(
        utility_kind="ei",
        utility_kappa=1,
        utility_xi=0.5
    )
), epochs=epochs)

figure.add_trace(go.Scatter(x=list(range(0, epochs)), y=bayesian2.losses,
                            mode='lines+markers',
                            name='bayesian2'))

figure.show()

# %%
epochs = 20

figure = go.Figure()

experiment1 = run_experiment_v2(NevergradAlgorithmBase(
    ng.families.ParametrizedBO(
        utility_kind='ei',
        utility_kappa=1,
        utility_xi=0,
        gp_parameters={'alpha': 1}
    )
), epochs=epochs)

figure.add_trace(
    go.Scatter(
        x=list(range(0, epochs)),
        y=experiment1.losses,
        mode='lines+markers',
        name='experiment1'
    )
)

experiment2 = run_experiment_v2(NevergradAlgorithmBase(
    ng.families.ParametrizedBO(
        utility_kind='ei',
        utility_kappa=1,
        utility_xi=0,
        gp_parameters={'alpha': 1}
    )
), epochs=epochs)

figure.add_trace(
    go.Scatter(
        x=list(range(0, epochs)),
        y=experiment2.losses,
        mode='lines+markers',
        name='experiment2'
    )
)

figure.show()

# %%
