import numpy as np
from scipy.optimize import bisect

from hydrostatic_2d import (
    computed_submerged_points,
    compute_submerged_area_and_centroid,
)


def test_no_points_below_zero():
    """Test when there are no points below y=0."""
    curve_points = [[-1, 1], [0, 2], [1, 3], [2, 4]]
    x, y = computed_submerged_points(curve_points)
    assert np.all(y <= 0)
    assert len(x) == 0
    assert len(y) == 0


def test_all_points_below_zero():
    """Test when all points are below y=0."""
    curve_points = [[-2, -1], [0, -2], [2, -3], [3, -1]]
    x, y = computed_submerged_points(curve_points)
    assert np.all(y <= 0)
    assert len(x) == len(curve_points)  # All points should be below y=0
    assert np.array_equal(y, np.array([-1, -2, -3, -1]))


def test_curve_crossing_zero_once():
    """Test when the curve crosses y=0 exactly once."""
    curve_points = [[-2, -1], [0, 0], [2, 1]]
    x, y = computed_submerged_points(curve_points)
    assert np.all(y <= 0)
    assert len(x) == 2  # There should be one point exactly on y=0
    assert np.array_equal(x, np.array([-2, 0]))  # x-coordinates of submerged points
    assert np.array_equal(y, np.array([-1, 0]))  # y-coordinates of submerged points


def test_curve_crossing_zero_multiple_times():
    """Test when the curve crosses y=0 multiple times."""
    curve_points = [[-2, -2], [0, 2], [2, -2], [3, -1], [5, 1]]
    x, y = computed_submerged_points(curve_points)
    assert np.all(y <= 0)
    assert len(x) == 6  # Points below y=0 should be found
    assert np.array_equal(
        x, np.array([-2, -1, 1, 2, 3, 4])
    )  # X-coordinates of submerged points
    assert np.array_equal(
        y, np.array([-2, 0, 0, -2, -1, 0])
    )  # Y-coordinates of submerged points


def test_curve_no_intersection_with_zero():
    """Test when the curve does not intersect with y=0."""
    curve_points = [[-2, 1], [0, 2], [2, 3], [3, 4]]
    x, y = computed_submerged_points(curve_points)
    assert np.all(y <= 0)
    assert len(x) == 0
    assert len(y) == 0


def test_empty_input():
    """Test when the input list is empty."""
    curve_points = []
    x, y = computed_submerged_points(curve_points)
    assert np.all(y <= 0)
    assert len(x) == 0
    assert len(y) == 0


def test_single_point_on_zero():
    """Test when there is exactly one point on y=0."""
    curve_points = [[0, 0]]
    x, y = computed_submerged_points(curve_points)
    assert np.all(y <= 0)
    assert len(x) == 1
    assert len(y) == 1


def test_points_on_y_zero_and_below():
    """Test when points are on y=0 and some below y=0."""
    curve_points = [[-1, 0], [0, -1], [1, 1], [2, -1]]
    x, y = computed_submerged_points(curve_points)
    assert np.all(y <= 0)
    assert len(x) == 5  # 0 is not considered submerged
    assert np.array_equal(
        x, np.array([-1, 0, 0.5, 1.5, 2])
    )  # Submerged points (includes points below)
    assert np.array_equal(y, np.array([0, -1, 0, 0, -1]))  # Correct y values below zero


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
    assert np.isnan(cx) and np.isnan(cy), (
        f"Expected centroid at (0, 0), but got ({cx}, {cy})"
    )


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
