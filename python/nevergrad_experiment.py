# %%
from typing import Tuple, Union
import nevergrad as ng
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from nevergrad_algorithm_base import NevergradAlgorithmBase

TRUTH_VALUE = np.array([
    3,  # retraction_distance is 3 but * 10 to be equal to other parameters
    30,  # retraction_speed
    40   # prime_speed
])


def objective_function(x: Union[ng.p.Scalar, float],
                       y: Union[ng.p.Scalar, float],
                       z: Union[ng.p.Scalar, float],
                       ) -> float:
    """
    Caluclates the absolute distance of x to the TRUTH_VALUE squared.
    """
    result = [
        abs((TRUTH_VALUE[0]*10 - x*10)) ** 2,
        abs(TRUTH_VALUE[1] - y) ** 2,
        abs(TRUTH_VALUE[2] - z) ** 2,
    ]
    return abs(np.sum(result))


# %%

def run_experiment(algorithm, epochs: int) -> Tuple[list, list, float]:
    """
    Returns recommendation, all losses and loss of recommendation
    """
    losses = []
    for _ in range(epochs):  # type: ignore
        x = algorithm.step()
        loss = objective_function(*x.args)
        losses.append(loss)
        algorithm.tell_loss(x, loss)
    recommendation = algorithm.optimizer.provide_recommendation()
    return recommendation.args, losses, objective_function(*recommendation.args)


# %%

epochs = 12

figure = go.Figure()

# ng_opt = run_experiment(NevergradAlgorithmBase(
#     objective_function,
#     ng.optimizers.NGOpt
# ), epochs=epochs)

# figure.add_trace(go.Scatter(x=list(range(0,epochs)), y=ng_opt[1],
#                     mode='lines+markers',
#                     name='ng_opt'))

#* ------- no good performance  -------------
# two_points_opt = run_experiment(NevergradAlgorithmBase(
#     objective_function,
#     ng.optimizers.TwoPointsDE
# ), epochs=epochs)

# figure.add_trace(go.Scatter(x=list(range(0,epochs)), y=two_points_opt[1],
#                     mode='lines+markers',
#                     name='two_points_opt'))

# portfolio_discrete_one_plus_one = run_experiment(NevergradAlgorithmBase(
#     objective_function,
#     ng.optimizers.PortfolioDiscreteOnePlusOne
# ), epochs=epochs)

# figure.add_trace(go.Scatter(x=list(range(0,epochs)), y=portfolio_discrete_one_plus_one[1],
#                     mode='lines+markers',
#                     name='portfolio_discrete_one_plus_one'))
#* -------------------------------------

# one_plus_one = run_experiment(NevergradAlgorithmBase(
#     objective_function,
#     ng.optimizers.OnePlusOne
# ), epochs=epochs)

# figure.add_trace(go.Scatter(x=list(range(0,epochs)), y=one_plus_one[1],
#                     mode='lines+markers',
#                     name='one_plus_one'))

bayesian1 = run_experiment(NevergradAlgorithmBase(
    objective_function, 
    ng.families.ParametrizedBO(
        utility_kind="ucb",
        utility_kappa=2,
        utility_xi=1
    )
), epochs=epochs)

figure.add_trace(go.Scatter(x=list(range(0,epochs)), y=bayesian1[1],
                    mode='lines+markers',
                    name='bayesian1'))

bayesian2 = run_experiment(NevergradAlgorithmBase(
    objective_function, 
    ng.families.ParametrizedBO(
        utility_kind="ucb",
        utility_kappa=1.75,
        utility_xi=1
    )
), epochs=epochs)

figure.add_trace(go.Scatter(x=list(range(0,epochs)), y=bayesian2[1],
                    mode='lines+markers',
                    name='bayesian2'))

figure.show()

# %%
