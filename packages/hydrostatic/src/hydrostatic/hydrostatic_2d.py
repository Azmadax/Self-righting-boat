# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import numpy as np
from scipy.optimize import bisect
import matplotlib.pyplot as plt


def close_curve(curve_points: list[list[float]]) -> list[list[float]]:
    """
    Ensure to close curve in order to get a polygon
    Args:
        curve_points (list[list[float]]): Curve which is already close or not

    Returns:
        list[list[float]]: The closed curve (polygon)
    """
    if curve_points:
        if curve_points[0] == curve_points[-1]:
            pass
        else:
            curve_points.append(curve_points[0])
    return curve_points


def computed_submerged_points(
    curve_points: list[list[float]],
) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute the submerged points below y=0 of a polygon chain (first point must be repeated in last position for polygon)

    Args:
        curve_points (list[list[float]]): list of points defining the curve.

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
) -> tuple[float, float, float]:
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
        if area == 0:
            # Take the lowest point for continuity with the solid ground case
            i_bottom = np.argmin(y)
            cx = x[i_bottom]
            cy = y[i_bottom]
        else:
            cx = (1 / (6 * area)) * np.sum(
                (x[:-1] + x[1:]) * (x[:-1] * y[1:] - x[1:] * y[:-1])
            )
            cy = (1 / (6 * area)) * np.sum(
                (y[:-1] + y[1:]) * (x[:-1] * y[1:] - x[1:] * y[:-1])
            )
    return abs(area), cx, cy


def compute_submerged_area_and_centroid(
    curve_points: list[list[float]],
) -> tuple[float, float, float]:
    """
    Compute the submerged area and centroid for a given curve below y=0.

    Args:
        curve_points (list[list[float]]): list of points defining the curve.

    Returns:
        Tuple[float, float, float]: Area, x-coordinate of centroid, and y-coordinate of centroid.
    """
    x, y = computed_submerged_points(curve_points)
    area, cx, cy = compute_area_and_centroid(x, y)
    return area, cx, cy


def area_difference(
    draft_offset: float, target_area: float, curve_points: list[list[float]]
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


def find_draft_offset_at_vertical_equilibrium(
    target_displacement_area, curve_points: list[list[float]]
) -> float:
    """
    Find the vertical offset to get the draft which enables to get the displacement of the ship

    Args:
        target_displacement_area (float): The target displacement (area in 2D)
        curve_points (List[List[float]]: The points describing the 2D ship

    Returns:
        float: The vertical offset (positive to move geometry down, and increase draft and displacement)
    """
    y_min = min([p[1] for p in curve_points])
    y_max = max([p[1] for p in curve_points])

    draft_offset_min, draft_offset_max = (
        y_min - 10,
        y_max + 10,
    )  # Adjust bounds as needed
    try:
        draft_offset_equilibrium: float = bisect(
            area_difference,
            draft_offset_min,
            draft_offset_max,
            args=(
                target_displacement_area,
                curve_points,
            ),
        )
    except ValueError as e:
        if str(e) == "f(a) and f(b) must have different signs":
            raise ValueError("Ship is sinking")
        else:
            # Reraise error otherwise
            raise ValueError(repr(e))

    return draft_offset_equilibrium


def compute_righting_arm(
    curve_points: list[list[float]],
    target_area: float,
    center_of_gravity: list[float],
    plot: bool = False,
) -> float:
    """
    Compute the righting arm GZ

    Args:
        curve_points (list[list[float]]): list of coordinates of points describing the 2D hull [m]
        target_area (float): target submerged area [m²]
        center_of_gravity (list[float]): coordinate of center of gravity[m]
        plot (bool): if at True, plot debug graph

    Returns:
        float: the righting arm GZ [m]
    """
    draft_offset_equilibrium = find_draft_offset_at_vertical_equilibrium(
        target_displacement_area=target_area, curve_points=curve_points
    )

    # Apply the found draft_offset to compute the submerged area and centroid
    shifted_points = [[p[0], p[1] - draft_offset_equilibrium] for p in curve_points]
    area, cx, cy = compute_submerged_area_and_centroid(shifted_points)
    x, y = computed_submerged_points(shifted_points)
    righting_arm = (
        center_of_gravity[0] - cx
    )  # Sign convention chosen to have positive slope when stable

    if plot:
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
        plt.xlabel("X [m]")
        plt.ylabel("Y [m]")
        plt.title(
            f"Vertical equilibrium.\nTarget area = {target_area}m², GZ = {righting_arm:.2f}m"
        )
        ax = plt.gca()
        ax.set_aspect("equal", "box")
        plt.show()

    return righting_arm


def rotate(points: list[list[float]], angle) -> list[list[float]]:
    """
    Rotate list of 2D points by angle (direct rotation)

    Args:
        points (list[list[float]]): list of coordinates of points describing the 2D hull [m]
        angle (float): angle of rotation [rad]

    Returns:
        (list[list[float]]): list of coordinates of points describing the 2D hull rotated around [0,0] [m]
    """
    complex_points = [p[0] + p[1] * 1j for p in points]
    complex_point_rotated = [c * np.exp(1j * angle) for c in complex_points]
    rotated_points = [(c.real, c.imag) for c in complex_point_rotated]
    return rotated_points


def compute_righting_arm_curve(
    curve_points,
    center_of_gravity,
    target_area: float,
    angles_deg: list[float],
    plot: bool = False,
):
    """

    Args:
        angles_deg:

    Returns:

    """
    righting_arms = []  # List of GZs
    for angle_deg in angles_deg:
        rotated_curve_points = rotate(points=curve_points, angle=np.deg2rad(angle_deg))
        rotated_center_of_gravity = rotate(
            points=[center_of_gravity], angle=np.deg2rad(angle_deg)
        )[0]

        # Step 2: find draft_offset using bisection to match the target_area

        righting_arm = compute_righting_arm(
            curve_points=rotated_curve_points,
            target_area=target_area,
            center_of_gravity=rotated_center_of_gravity,
            plot=False,
        )
        righting_arms.append(righting_arm)

    if plot:
        plt.title("GZ curve")
        plt.plot(angles_deg, righting_arms, label="GZ")
        plt.grid()
        plt.xlabel("Angle of rotation [deg]")
        plt.ylabel("Righting arm GZ [m]")
        plt.show()
    return righting_arms


def find_equilibrium_points(
    curve_points: list[list[float]],
    center_of_gravity: list[float],
    target_area: float,
    plot=False,
) -> float:
    """
    Find the different equilibrium points (both heel and vertical equilibrium)

    Args:
        curve_points(list[list[float]]: list of coordinates of 2D points
        center_of_gravity (list[float]): 2D coordinates of center of gravity
        target_area (float): target submerged area

    Returns:
        list[float]: angles of equilibrium points [deg]
    """
    angles_deg = range(-180, 182)  # enlarge a bit

    righting_arm_curves = compute_righting_arm_curve(
        curve_points=curve_points,
        center_of_gravity=center_of_gravity,
        target_area=target_area,
        angles_deg=angles_deg,
        plot=plot,
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
            curve_points=curve_points,
            angles_deg=[angle_deg],
            center_of_gravity=center_of_gravity,
            target_area=target_area,
            plot=False,
        )[0]
        return righting_arm

    # Based on https://stackoverflow.com/questions/72333164/find-all-roots-of-an-arbitrary-interpolated-function-in-a-given-interval

    # Evaluate the function at several points with the sufficient accuracy
    f_p = np.array(righting_arm_curves)
    # Find the discrete points where sign is changing
    (indices,) = np.nonzero(f_p[:-1] * f_p[1:] <= 0)

    equilibrium_angles_deg = []
    # Search for zero between these points
    for i in range(indices.shape[0]):
        guess_min = angles_deg[indices[i]]
        guess_max = angles_deg[indices[i] + 1]
        if guess_min > guess_max:
            guess_min, guess_max = guess_max, guess_min
        equilibrium_angle_deg = bisect(f, a=guess_min, b=guess_max)
        equilibrium_angles_deg.append(equilibrium_angle_deg)

    # Filter to avoid duplicate
    equilibrium_angles_deg = mod_minus_180_180(
        unique_angles_deg(equilibrium_angles_deg)
    )
    if plot:
        for equilibrium_angle_deg in equilibrium_angles_deg:
            compute_righting_arm(
                curve_points=rotate(curve_points, np.deg2rad(equilibrium_angle_deg)),
                target_area=target_area,
                center_of_gravity=rotate(
                    [center_of_gravity], np.deg2rad(equilibrium_angle_deg)
                )[0],
                plot=True,
            )
    return equilibrium_angles_deg


def unique_angles_deg(angles_deg: list[float], decimal: float = 1) -> list[float]:
    """
    Compute unique angle within a tolerance

    Args:
        angles_deg (list[float]): list of angles to be filtered to remove duplicates
        decimal (int): number of decimals of degree to round the result

    Returns:
        list[float]: the list of float with suppressed angles
    """
    unique_angles_deg_list = []
    tolerance = 10 ** (-decimal)

    for angle_deg in angles_deg:
        # Normalize the angle to the range [0, 360) for better comparison
        normalized_angle_deg = angle_deg % 360

        # Check if the angle is within tolerance of any already added angle
        is_unique = True
        for existing_angle in unique_angles_deg_list:
            # Check if the difference between angles is less than the tolerance
            if (
                abs(normalized_angle_deg - existing_angle) < tolerance
                or abs(360 - abs(normalized_angle_deg - existing_angle)) < tolerance
            ):
                is_unique = False
                break

        # If unique, add to the list
        if is_unique:
            unique_angles_deg_list.append(normalized_angle_deg)

    return np.round(unique_angles_deg_list, decimals=decimal)


def mod_minus_180_180(angle_deg: float):
    """
    Compute modulo of angles between ]-180;180]

    Args:
        angle_deg: angle [deg]

    Returns:
        float: angle between ]-180;180] [deg]
    """
    return -((-np.array(angle_deg) + 180) % 360 - 180)
