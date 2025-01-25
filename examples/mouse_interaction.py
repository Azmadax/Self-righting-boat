import matplotlib.pyplot as plt


def get_mouse_clicks(title):
    """
    Capture mouse click positions on a matplotlib figure, ending on a double-click.

    Returns:
        list of tuples: A list of (x, y) coordinates of clicked points.
    """
    clicked_points = []

    def onclick(event):
        # Capture the click event
        if event.dblclick:  # Double-click detected
            print("Double-click detected. Finishing point capture.")
            plt.close()  # Close the plot
        elif event.xdata is not None and event.ydata is not None:
            clicked_points.append((event.xdata, event.ydata))
            print(f"Point captured: ({event.xdata:.2f}, {event.ydata:.2f})")

    fig, ax = plt.subplots()
    ax.set_title("Click to capture points (double-click to finish)")
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    plt.plot([-0.5, 0.5, 0.5, -0.5, -0.5], [-0.5, -0.5, 0.5, 0.5, -0.5])
    plt.legend(["Minimal reference area=1m²"])

    # Connect the click event to the handler
    cid = fig.canvas.mpl_connect("button_press_event", onclick)
    plt.grid()
    plt.title(title)

    # Show the plot and wait for interaction
    plt.show()

    # Disconnect the event to avoid side effects
    fig.canvas.mpl_disconnect(cid)

    return clicked_points
