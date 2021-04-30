# %%
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
    Returns the recommendation, all losses and loss of recommendation
    """
    steps = []
    losses = []
    for _ in range(epochs):  # type: ignore
        x = algorithm.step()
        steps.append(x)
        loss = objective_function_v2(*x.args)
        losses.append(loss)
        algorithm.tell_loss(x, loss)
    recommendation = algorithm.optimizer.provide_recommendation()
    return Experiment(recommendation.args, objective_function_v2(*recommendation.args), losses, steps)


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
