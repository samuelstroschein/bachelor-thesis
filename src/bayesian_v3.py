"""
retraction_distance = range(2,10)
retraction_speed = range(30,60)
prime_speed = range(30,60)
"""

# %%
from bayes_opt.util import acq_max
import warnings
from typing import List
import numpy as np
from bayes_opt import BayesianOptimization
from objective_functions import objective_function_v3


class DiscreteBayesianOptimization(BayesianOptimization):
    def __init__(self,
                 f,
                 pbounds,
                 parameter_step_sizes: List[int],
                 random_state=None,
                 verbose=2,
                 bounds_transformer=None,
                 ):
        """
        Extends BayesianOptimization and overwrites the point to probe next
        to be discrete.
        """
        self.parameter_step_sizes: List[int] = parameter_step_sizes
        super().__init__(f, pbounds, random_state=random_state,
                         verbose=verbose, bounds_transformer=bounds_transformer)

    def round_to_step(x: float, step: int) -> int:
        """
        Rounds a continuous value to the discrete value closest to the defined step size.

        Static and public because used in simulation.
        """
        return step * round(x/step)

    # @override
    def suggest(self, utility_function):
        """Most promissing point to probe next"""
        if len(self._space) == 0:
            return self._space.array_to_params(self._space.random_sample())

        # Sklearn's GP throws a large number of warnings at times, but
        # we don't really need to see them here.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self._gp.fit(self._space.params, self._space.target)

        # Finding argmax of the acquisition function.
        continuous_suggestion = acq_max(
            ac=utility_function.utility,
            gp=self._gp,
            y_max=self._space.target.max(),
            bounds=self._space.bounds,
            random_state=self._random_state
        )

        # transform each value in suggestion into the
        # discrete value closed to the defined step size
        discrete_suggestion: np.ndarray = np.array([
            DiscreteBayesianOptimization.round_to_step(
                x, self.parameter_step_sizes[i]
            ) for i, x in enumerate(continuous_suggestion)
        ])

        return self._space.array_to_params(discrete_suggestion)


# # %% Automatic steps

# TRUTH_VALUE = np.array([
#     210,  # print temperature
#     4,    # retraction distance
#     40    # reatraction speed
# ])

# pbounds = {'x': (180, 220), 'y': (2, 8), 'z': (30, 60)}

# optimizer = DiscreteBayesianOptimization(
#     f=lambda x, y, z: objective_function_v3(
#         x, y, z, TRUTH_VALUE, minimize=False
#     ),
#     pbounds=pbounds,
#     parameter_step_sizes=[5, 1, 10],
#     verbose=2,  # verbose = 1 prints only when a maximum is observed, verbose = 0 is silent
#     random_state=1,
# )

# # set first initial point
# optimizer.probe(
#     params=[180, 2, 30],
#     lazy=True,
# )

# # set second initial point
# optimizer.probe(
#     params=[220, 8, 60],
#     lazy=True,
# )

# optimizer.maximize(
#     init_points=0,
#     n_iter=20,
#     acq="ei",
#     kappa=10
# )

# print(optimizer.max)
