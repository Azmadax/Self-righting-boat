# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from geomdl import NURBS
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import bisect
from typing import List, Tuple

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


def computed_submerged_points(
    curve_points: List[List[float]],
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute the submerged points below y=0 of a closed NURBS curve.

    Args:
        curve_points (List[List[float]]): List of points defining the curve.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Arrays of x and y coordinates of submerged points below y=0.
    """
    below_points = []

    for i in range(len(curve_points) - 1):
        p1, p2 = curve_points[i], curve_points[i + 1]

        if p1[1] < 0 and p2[1] < 0:
            below_points.append(p1)
        elif p1[1] < 0 <= p2[1] or p2[1] < 0 <= p1[1]:
            # Linear interpolation to find intersection with y=0
            t = -p1[1] / (p2[1] - p1[1])
            intersect = [p1[0] + t * (p2[0] - p1[0]), 0.0]

            if p1[1] < 0:
                below_points.append(p1)
            below_points.append(intersect)

            if p2[1] < 0:
                below_points.append(p2)

    if len(below_points) == 0:
        return np.array([]), np.array([])
    else:
        below_points = np.array(below_points)
        x, y = below_points[:, 0], below_points[:, 1]
        return x, y


def compute_area_and_centroid(
    x: np.ndarray, y: np.ndarray
) -> Tuple[float, float, float]:
    """
    Compute the submerged area and centroid using the shoelace formula.

    Args:
        x (np.ndarray): x-coordinates of the submerged curve.
        y (np.ndarray): y-coordinates of the submerged curve.

    Returns:
        Tuple[float, float, float]: Area, x-coordinate of centroid, and y-coordinate of centroid.
    """
    if len(x) == 0:
        return 0, 0, 0
    else:
        area = 0.5 * np.sum(x[:-1] * y[1:] - x[1:] * y[:-1])
        cx = (1 / (6 * area)) * np.sum(
            (x[:-1] + x[1:]) * (x[:-1] * y[1:] - x[1:] * y[:-1])
        )
        cy = (1 / (6 * area)) * np.sum(
            (y[:-1] + y[1:]) * (x[:-1] * y[1:] - x[1:] * y[:-1])
        )
        return abs(area), cx, cy


def compute_submerged_area_and_centroid(
    curve_points: List[List[float]],
) -> Tuple[float, float, float]:
    """
    Compute the submerged area and centroid for a given curve below y=0.

    Args:
        curve_points (List[List[float]]): List of points defining the curve.

    Returns:
        Tuple[float, float, float]: Area, x-coordinate of centroid, and y-coordinate of centroid.
    """
    x, y = computed_submerged_points(curve_points)
    area, cx, cy = compute_area_and_centroid(x, y)
    return area, cx, cy


def area_difference(draft_offset: float, curve_points: List[List[float]]) -> float:
    """
    Function for calculating the difference between the desired submerged area and the area for a given draft offset.

    Args:
        draft_offset (float): The draft offset for shifting the curve.
        curve_points (List[List[float]]): List of points defining the curve.

    Returns:
        float: Difference between computed area and target area.
    """
    # Shift curve points by draft_offset
    shifted_points = [[p[0], p[1] - draft_offset] for p in curve_points]
    # Compute the area below y=0 for the shifted curve
    area, _, _ = compute_submerged_area_and_centroid(shifted_points)
    return area - target_area


# Step 2: Set the target area and find draft_offset using bisection
target_area = 6.0  # Set the desired submerged area
draft_offset_min, draft_offset_max = -5.0, 5.0  # Adjust bounds as needed
draft_offset_equilibrium = bisect(
    area_difference, draft_offset_min, draft_offset_max, args=(curve_points,)
)

# Apply the found draft_offset to compute the submerged area and centroid
shifted_points = [[p[0], p[1] - draft_offset_equilibrium] for p in curve_points]
area, cx, cy = compute_submerged_area_and_centroid(shifted_points)
x, y = computed_submerged_points(shifted_points)

# Output results
print(f"Submerged Area (Volume): {area}")
print(f"Centroid: ({cx}, {cy})")

# (Optional) Plot the curve and submerged region
curve_x, curve_y = zip(*shifted_points)
plt.plot(curve_x, curve_y, label="Closed NURBS Curve")

plt.plot(cx, cy, marker="o", label="Centroid")
plt.fill(x, y, color="blue", alpha=0.3, label="Submerged Region")
plt.axhline(0, color="red", linestyle="--", label="y=0 Line")
plt.legend()
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Submerged Region Below y=0")
plt.show()
