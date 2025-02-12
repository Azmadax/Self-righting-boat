# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from geomdl import NURBS

from hydrostatic.hydrostatic_2d import (
    close_curve,
    find_equilibrium_points,
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
center_of_gravity = input_curve_points.pop()
# Duplicated first point in last position to get a polygon
input_curve_points = close_curve(input_curve_points)

eq = find_equilibrium_points(
    curve_points=input_curve_points,
    center_of_gravity=center_of_gravity,
    target_area=target_area,
    plot=True,
)
