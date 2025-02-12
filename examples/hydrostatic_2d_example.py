# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from scipy.optimize import bisect

import numpy as np
from geomdl import NURBS

from hydrostatic.hydrostatic_2d import (
    close_curve,
    compute_righting_arm,
    rotate,
    compute_righting_arm_curve,
)
from mouse_interaction import get_mouse_clicks

# Step 1: Define a Closed NURBS Curve
curve = NURBS.Curve()
curve.degree = 3
curve.ctrlpts = [
    [0.0, 2.0],  # Control points
    [2.0, 3.0],
    [4.0, 2.0],
    [3.0, -2.0],
    [1.0, -2.0],
    [-1.0, 0.0],  # Close the curve by duplicating the starting control point
    [0.0, 2.0],
]
curve.knotvector = [0, 0, 0, 0, 1, 2, 3, 4, 4, 4, 4]  # Closed curve knot vector
curve.delta = 0.01  # Set resolution for sampling

# Evaluate points on the curve
curve_points = curve.evalpts
target_area = 1.0  # Set the desired submerged area
input_curve_points = get_mouse_clicks(
    "Draw polygon by clicking on vertices and \n double click at center of gravity to finish."
)
angles_deg = range(-180, 181)
center_of_gravity = input_curve_points.pop()
# Duplicated first point in last position to get a polygon
input_curve_points = close_curve(input_curve_points)
righting_arm_curves = compute_righting_arm_curve(
    curve_points=input_curve_points,
    center_of_gravity=center_of_gravity,
    target_area=target_area,
    angles_deg=angles_deg,
    plot=True,
)


# Define a function wrapper to be able to find root
def f(angle_deg: float) -> float:
    """
    Wrap the function computing righting arm to get a function of angle of rotation only

    Args:
        angle_deg (float): angle of rotation [deg]

    Returns:
        float: GZ [m]
    """
    righting_arm = compute_righting_arm_curve(
        curve_points=input_curve_points,
        angles_deg=[angle_deg],
        center_of_gravity=center_of_gravity,
        target_area=target_area,
        plot=False,
    )[0]
    return righting_arm


# Based on https://stackoverflow.com/questions/72333164/find-all-roots-of-an-arbitrary-interpolated-function-in-a-given-interval
# Evaluate function with suffcie
f_p = np.array(righting_arm_curves)
# Find the discrete points where sign is changing
(indices,) = np.nonzero(f_p[:-1] * f_p[1:] <= 0)

# Search for zero between these points
for i in range(indices.shape[0]):
    guess_min = angles_deg[indices[i]]
    guess_max = angles_deg[indices[i] + 1]
    if guess_min > guess_max:
        guess_min, guess_max = guess_max, guess_min

    print(f(guess_min), f(guess_max))

    equilibrium_angle_deg = bisect(f, a=guess_min, b=guess_max)
    GZ = compute_righting_arm(
        curve_points=rotate(input_curve_points, np.deg2rad(equilibrium_angle_deg)),
        target_area=target_area,
        center_of_gravity=rotate(
            [center_of_gravity], np.deg2rad(equilibrium_angle_deg)
        )[0],
        plot=True,
    )
    print("root", i + 1, "equilibrium_angle_deg=", equilibrium_angle_deg, "GZ=", GZ)
