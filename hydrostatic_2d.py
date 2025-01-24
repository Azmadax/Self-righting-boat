# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import numpy as np
from typing import List, Tuple


def computed_submerged_points(
    curve_points: List[List[float]],
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute the submerged points below y=0 of a polygon chain (first point must be repeated in last position for polygon)

    Args:
        curve_points (List[List[float]]): List of points defining the curve.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Arrays of x (horizontal) and y (vertical up) coordinates of submerged points below y=0.
    """
    below_points = []

    for i in range(len(curve_points) - 1):
        p1, p2 = curve_points[i], curve_points[i + 1]

        if p1[1] <= 0:
            below_points.append(p1)
        if p1[1] < 0 < p2[1] or p2[1] < 0 < p1[1]:
            # Linear interpolation to find intersection with y=0
            t = -p1[1] / (p2[1] - p1[1])
            intersect = [p1[0] + t * (p2[0] - p1[0]), 0.0]
            below_points.append(intersect)

    if curve_points:
        if curve_points[-1][1] <= 0:
            below_points.append(curve_points[-1])

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
    https://en.wikipedia.org/wiki/Shoelace_formula


    Args:
        x (np.ndarray): x-coordinates (horizontal) of the submerged curve.
        y (np.ndarray): y-coordinates (vertical up) of the submerged curve.

    Returns:
        Tuple[float, float, float]: Area, x-coordinate of centroid, and y-coordinate of centroid.
    """
    if len(x) == 0:
        area = 0
        cx = np.nan
        cy = np.nan
    elif len(x) == 1:
        area = 0
        cx = x[0]
        cy = y[0]
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


def area_difference(
    draft_offset: float, target_area: float, curve_points: List[List[float]]
) -> float:
    """
    Function for calculating the difference between the desired submerged area and the area for a given draft offset.

    Args:
        draft_offset (float): The draft offset for shifting the curve.
        target_area (float): The submerged area we aim (related to mass and density)
        curve_points (List[List[float]]): List of points defining the curve.

    Returns:
        float: Difference between computed area and target area.
    """
    # Shift curve points by draft_offset
    shifted_points = [[p[0], p[1] - draft_offset] for p in curve_points]
    # Compute the area below y=0 for the shifted curve
    area, _, _ = compute_submerged_area_and_centroid(shifted_points)
    return area - target_area
