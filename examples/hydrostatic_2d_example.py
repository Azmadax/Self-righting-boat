# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from geomdl import NURBS
import matplotlib.pyplot as plt
from scipy.optimize import bisect

from hydrostatic.hydrostatic_2d import (
    area_difference,
    compute_submerged_area_and_centroid,
    computed_submerged_points,
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
curve_points = get_mouse_clicks(
    "Draw polygon by clicking on vertices and \n double click at center of gravity to finish."
)

# Last point is center of gravity
center_of_gravity = curve_points.pop()

# Duplicated first point in last position to get a polygon
curve_points.append(curve_points[0])


# Step 2: Set the target area and find draft_offset using bisection
target_area = 1.0  # Set the desired submerged area
draft_offset_min, draft_offset_max = -2.0, 2.0  # Adjust bounds as needed
draft_offset_equilibrium = bisect(
    area_difference,
    draft_offset_min,
    draft_offset_max,
    args=(
        target_area,
        curve_points,
    ),
)

# Apply the found draft_offset to compute the submerged area and centroid
shifted_points = [[p[0], p[1] - draft_offset_equilibrium] for p in curve_points]
area, cx, cy = compute_submerged_area_and_centroid(shifted_points)
x, y = computed_submerged_points(shifted_points)

# Output results
print(f"Submerged Area (Volume): {area}")
print(f"Center of buoyancy: ({cx}, {cy})")

# (Optional) Plot the curve and submerged region
curve_x, curve_y = zip(*shifted_points)
plt.fill(curve_x, curve_y, color="red", alpha=0.1, edgecolor="black")
plt.plot(curve_x, curve_y, color="black", label="Closed curve")

plt.plot(cx, cy, marker="o", label="Center of buoyancy")
plt.plot(
    center_of_gravity[0],
    center_of_gravity[1] - draft_offset_equilibrium,
    marker="o",
    markerfacecolor="red",
    label="Center of gravity",
)
left, right = plt.gca().get_xlim()
bottom, top = plt.gca().get_xlim()
plt.fill(
    [2 * left, 2 * left, 2 * right, 2 * right],
    [0, 2 * bottom, 2 * bottom, 0],
    color="blue",
    alpha=0.1,
    label="Dense fluid",
)
# plt.gca().set_xlim(left, right)
# plt.gca().set_ylim(bottom, top)
# plt.fill(x, y, color="blue", alpha=0.1, label="Submerged region")
plt.axhline(0, color="blue", linestyle="--", label="y=0 Line")
plt.legend()
plt.xlabel("X")
plt.ylabel("Y")
plt.title(
    f"Vertical equilibrium.\nTarget area = {target_area}, GZ = {cx - center_of_gravity[0]:.2f}"
)
plt.show()
