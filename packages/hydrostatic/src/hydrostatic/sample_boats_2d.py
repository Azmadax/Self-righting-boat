import numpy as np
import matplotlib.pyplot as plt


def generate_culbuto_boat() -> tuple[list[tuple[float, float]], tuple[float, float]]:
    """Generates the points of a boat with a rectangle and a semi-circle centered at the top.

    Returns:
        list[tuple[float, float]:]: Coordinates of the points defining the boat's hull.
        tuple[float, float]: Center of gravity of the boat (0,0).
    """
    width = 4  # Width of the rectangle
    height = 2  # Height of the rectangle
    radius = width / 2  # Radius of the semi-circle
    draft_offset = 1  # Lowers all Y coordinates by 1 meter

    # Rectangle: base of the boat
    rect_x = np.linspace(-width / 2, width / 2, 10)  # 10 points along the bottom
    rect_bottom = [(x, -height / 2 - draft_offset) for x in rect_x]  # Y offset
    rect_right = [
        (width / 2, y - draft_offset) for y in np.linspace(-height / 2, height / 2, 5)
    ]
    rect_left = [
        (-width / 2, y - draft_offset) for y in np.linspace(height / 2, -height / 2, 5)
    ]

    # Semi-circle: centered at the top of the rectangle
    theta = np.linspace(0, np.pi, 10)  # 10 points for a smooth curve
    semi_circle = [
        (radius * np.cos(t), height / 2 + radius * np.sin(t) - draft_offset)
        for t in theta
    ]

    # Merge all points
    boat_shape = rect_bottom + rect_right + semi_circle + rect_left

    # Center of gravity at the middle of the rectangle
    center_of_gravity = (0, -draft_offset)

    return boat_shape, center_of_gravity


def generate_circular_boat() -> tuple[list[tuple[float, float]], tuple[float, float]]:
    """
    Generates the points of a boat in the shape of a circle.

    Returns:
        list[tuple[float, float]:]: Coordinates of the points defining the boat's hull.
        tuple[float, float]: Center of gravity of the boat.
    """
    radius = 2  # Radius of the circle
    num_points = 50  # Number of points to smooth the circle
    draft_offset = 1  # Lowers all Y coordinates by 1 meter

    # Generate circle points
    theta = np.linspace(0, 2 * np.pi, num_points)
    circle_points = [
        (radius * np.cos(t), radius * np.sin(t) - draft_offset) for t in theta
    ]

    # Center of gravity at the center of the circle
    center_of_gravity = (0, -draft_offset)

    return circle_points, center_of_gravity


def generate_square_boat() -> tuple[list[tuple[float, float]], tuple[float, float]]:
    """
    Generates the points of a boat in the shape of a square.

    Returns:
        list[tuple[float, float]:]: Coordinates of the points defining the boat's hull.
        tuple[float, float]: Center of gravity of the boat.
    """
    width = 4  # Width of the square
    height = 2  # Height of the square
    draft_offset = -1  # Lowers all Y coordinates by 1 meter

    # Generate square points
    x_min = -width / 2
    x_max = +width / 2
    y_min = -height / 2 - draft_offset
    y_max = +height / 2 - draft_offset

    # Center of gravity at the center of the square
    center_of_gravity = (0, -draft_offset)
    boat_shape_square = [(x_min, y_min), (x_min, y_max), (x_max, y_max), (x_max, y_min)]

    return boat_shape_square, center_of_gravity


if __name__ == "__main__":
    for method in [generate_culbuto_boat, generate_circular_boat, generate_square_boat]:
        # Generate boat shape and CG
        boat_points, center_of_gravity = method()

        # Visualize boat shape
        boat_x, boat_y = zip(*boat_points)
        plt.plot(boat_x, boat_y, marker="o", linestyle="-", label="Boat Shape")
        plt.fill(boat_x, boat_y, color="gray", alpha=0.5)

        # Display center of gravity
        plt.plot(
            center_of_gravity[0],
            center_of_gravity[1],
            "ro",
            markersize=8,
            label="Center of Gravity",
        )

        plt.axhline(0, color="blue", linestyle="--", label="Waterline")
        plt.legend()
        plt.xlabel("X [m]")
        plt.ylabel("Y [m]")
        plt.title(
            "Boat Shape: Rectangle + Semi-circle (CG at Rectangle Center, Lowered by 1m)"
        )
        plt.grid()
        plt.show()
