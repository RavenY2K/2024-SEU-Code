import matplotlib.pyplot as plt
import time


# Define the robot positions and routes
robot_x = [0, 0, 0]
robot_y = [0, 0, 0]

robot_route = []
data = [
    [22.3116, 10.3, 2.56, 18.8561, 18.3448, 1.37619, -22.0837],
    [14.3531, 18.4, 18.4, 1.47728, -10.0642, -18.529, -14.1402],
    ['0', '10', '15', '5', '20', '20', '20'],
    [22.31, -14.38, -16.9854, -17.0225, -14.38],
    [17.07, 22.34, 22.3604, 12.5804, 6.62],
    ['0', '10', '1', '1', '1'],
    [14.2332, -15.685, -15.685, -6.22556, -18.3904, -21.9446, -18.361, -1.5],
    [-22.0538, -1.32853, -1.32853, -1.43066, 2.61558, -1.26094, 10.3555, 18.9],
    ['0', '15', '15', '5', '20', '20', '20', '20'],
    [16.95, 14.3369, 16.0361],
    [-22.0669, -6.33414, 1.48067],
    ['0', '10', '15'],
    [25.0, 2.56, -3.09063, -2.2251, -25.0, -25.0, -3.09063, -3.09063],
    [25.0, 3.1, 2.55748, -3.07714, 2.61558, 2.61558, 2.55748, 2.55748],
    ['0', '5', '1', '1', '1', '1', '5', '5'],
    [-25.0, -2.37188, 25.0, 25.0, 25.0, 2.56],
    [25.0, -25.0, -25.0, -2.32435, -2.32435, 3.1],
    ['0', '5', '1', '1', '1', '5']
]
for i in range(0, len(data), 3):
    row = []
    for j in range(len(data[i])):
        row = [(round(x, 1), round(y, 1), int(z)) for x, y, z in zip(
            data[i], data[i+1], data[i+2])]
    robot_route.append(row)

print(robot_route)

# Define the waypoint coordinates
waypoints = [(2, 2), (5, 5), (8, 8), (9, 9), (7, 7), (4, 4)]
waypointsText = ['1', '2', '3', '4',  '5',  '6',]

# Define the duration each robot should wait at each waypoint
wait_times = [[2, 3, 4], [1, 1, 1], [2, 2, 2]]

# Define the time for each frame i the animation
frame_time = 0.25

# Create the plot and set the axis limits
fig, ax = plt.subplots()
ax.set_xlim(-30, 30)
ax.set_ylim(-30, 30)

# Plot the waypoints as circles
for waypoint in waypoints:
    ax.add_patch(plt.Circle(waypoint, 0.5, color='gray'))

# Define the update function for the animation
def update(frame):
    # Check if each robot has arrived at its current waypoint
    for i in range(len(robot_x)):
        if len(robot_route[i]) == 0:
            plt.pause(50000)
        current_waypoint = robot_route[i][0]
        if (robot_x[i], robot_y[i]) == current_waypoint:
            # If the robot has arrived at the waypoint, wait for the specified time
            wait_time = wait_times[i][0]
            if frame < int(wait_time / frame_time):
                continue
            else:
                # If the wait time is over, remove the current waypoint from the robot's route
                robot_route[i] = robot_route[i][1:]
        else:
            # If the robot hasn't arrived at the waypoint, move it closer to the waypoint
            dx = current_waypoint[0] - robot_x[i]
            dy = current_waypoint[1] - robot_y[i]
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance > 1:
                robot_x[i] += dx * 1 / distance
                robot_y[i] += dy * 1 / distance
            else:
                robot_x[i] = current_waypoint[0]
                robot_y[i] = current_waypoint[1]

    # Plot the robots' positions
    ax.clear()
    ax.set_xlim(-30, 30)
    ax.set_ylim(-30, 30)
    for i,waypoint in enumerate(waypoints):
        ax.add_patch(plt.Circle(waypoint, 0.5, color='gray'))
        ax.text(waypoint[0], waypoint[1],
                waypointsText[i], ha='center', va='center')
    ax.plot(robot_x, robot_y, 'ro')
    ax.set_title('Time: {:.2f} s'.format(frame * frame_time))
    plt.pause(frame_time)


# Run the animation
for i in range(2000):
    update(i)
