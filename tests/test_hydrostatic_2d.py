import numpy as np
from scipy.optimize import bisect
from hydrostatic_2d import (
    compute_submerged_area_and_centroid,
)


# Test for curve above y=0 (no submerged area)
def test_curve_above_y0():
    curve_points_above = [[0.0, 2.0], [2.0, 3.0], [4.0, 2.0], [3.0, 4.0]]
    area, cx, cy = compute_submerged_area_and_centroid(curve_points_above)
    assert area == 0, f"Expected area = 0, but got {area}"


# Test for curve below y=0 (entire curve submerged)
def test_curve_below_y0():
    curve_points_submerged = [
        [0.0, -2.0],
        [2.0, -3.0],
        [4.0, -2.0],
        [3.0, -4.0],
        [1.0, -4.0],
        [-1.0, -2.0],
        [0.0, -2.0],
    ]
    area, cx, cy = compute_submerged_area_and_centroid(curve_points_submerged)
    assert area > 0, f"Expected positive area, but got {area}"


# Test for curve with multiple intersections with y=0
def test_curve_intersects_y0():
    curve_points_intersect = [
        [0.0, 2.0],
        [1.0, 1.0],
        [2.0, 0.0],
        [3.0, -1.0],
        [4.0, -2.0],
        [5.0, -1.0],
        [6.0, 0.0],
    ]
    area, cx, cy = compute_submerged_area_and_centroid(curve_points_intersect)
    assert area > 0, f"Expected positive area, but got {area}"


# Test for bisection method
def test_bisection_method():
    target_area = 6.0
    curve_points = [
        [0.0, 2.0],
        [2.0, 3.0],
        [4.0, 2.0],
        [3.0, -2.0],
        [1.0, -2.0],
        [-1.0, 0.0],
        [0.0, 2.0],
    ]

    def area_diff(draft_offset: float):
        shifted_points = [[p[0], p[1] - draft_offset] for p in curve_points]
        area, _, _ = compute_submerged_area_and_centroid(shifted_points)
        return area - target_area

    draft_offset_min, draft_offset_max = -5.0, 5.0
    draft_offset_equilibrium = bisect(area_diff, draft_offset_min, draft_offset_max)
    assert draft_offset_equilibrium is not None, (
        "Bisection failed to find equilibrium offset"
    )

    shifted_points = [[p[0], p[1] - draft_offset_equilibrium] for p in curve_points]
    area, cx, cy = compute_submerged_area_and_centroid(shifted_points)
    assert np.isclose(area, target_area, atol=0.1), (
        f"Expected area ≈ {target_area}, but got {area}"
    )


# Test for edge case: Single point curve
def test_single_point_curve():
    curve_points_single = [[0.0, 0.0]]  # Single point
    area, cx, cy = compute_submerged_area_and_centroid(curve_points_single)
    assert area == 0, f"Expected area = 0, but got {area}"
    assert cx == 0 and cy == 0, f"Expected centroid at (0, 0), but got ({cx}, {cy})"


# Test for edge case: Empty curve
def test_empty_curve():
    curve_points_empty = []
    area, cx, cy = compute_submerged_area_and_centroid(curve_points_empty)
    assert area == 0, f"Expected area = 0, but got {area}"
    assert cx == 0 and cy == 0, f"Expected centroid at (0, 0), but got ({cx}, {cy})"


# Test for simple curve for which results where visually checked
def test_non_regression():
    curve_points_simple = [
        [0.0, 2.0],
        [2.0, 3.0],
        [4.0, 2.0],
        [3.0, -2.0],
        [1.0, -2.0],
        [-1.0, 0.0],
        [0.0, 2.0],
    ]
    area, cx, cy = compute_submerged_area_and_centroid(curve_points_simple)
    assert area > 0, f"Expected area > 0, but got {area}"
    assert np.isclose(cx, 1.576, atol=0.1), f"Expected centroid x ≈ 1.0, but got {cx}"
    assert np.isclose(cy, -0.871, atol=0.1), f"Expected centroid y ≈ -1.0, but got {cy}"
