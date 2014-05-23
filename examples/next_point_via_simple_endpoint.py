"""An example for accessing the gp_next_points_* endpoints.

:func:`moe.easy_interface.simple_endpoint.gp_next_points`

The function requires some historical information to inform the Gaussian Process

The result is the next best set of point(s) to sample
"""
import math
import random

from moe.easy_interface.experiment import Experiment
from moe.easy_interface.simple_endpoint import gp_next_points


def function_to_minimize(x):
    """Calculate an aribitrary 2-d function with some noise.

    This function has a minimum near [1, 2.6].
    """
    return math.sin(x[0]) * math.cos(x[1]) + math.cos(x[0] + x[1]) + random.uniform(-0.02, 0.02)

if __name__ == '__main__':
    exp = Experiment([[0, 2], [0, 4]])
    # Bootstrap with some known or already sampled point(s)
    exp.historical_data.append_sample_points([
        [[0, 0], 1.0, 0.01],  # sampled points have the form [point_as_a_list, objective_function_value, value_variance]
        ])

    # Sample 20 points
    for i in range(20):
        # Use MOE to determine what is the point with highest Expected Improvement to use next
        next_point_to_sample = gp_next_points(exp)[0]  # By default we only ask for one point
        # Sample the point from our objective function, we can replace this with any function
        value_of_next_point = function_to_minimize(next_point_to_sample)

        print "Sampled f(%s) = %f" % (str(next_point_to_sample), value_of_next_point)

        # Add the information about the point to the experiment historical data to inform the GP
        exp.historical_data.append_sample_points([[next_point_to_sample, value_of_next_point, 0.01]])  # We can add some noise