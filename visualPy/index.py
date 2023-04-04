import matplotlib.pyplot as plt
import time
from matplotlib.animation import FuncAnimation


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

# Define the robot positions and routes
robot_x = [0, 0, 0]
robot_y = [0, 0, 0]
result = []

for i in range(len(data)):
    row = []
    for j in range(len(data[i])):
        if len(result) <= j:
            result.append([])
        if len(result[j]) < i:
            result[j].append(None)
        result[j].append(data[i][j])
    row = [(x, y, z) for x, y, z in zip(
        result[j][0:i], result[j][i:i+3], result[j][i+3:])]
    result[j] = row

print(result)

robot_route = result
[2, 5, 8]
[1, 3, 8]
[2, 2, 1]
[3, 3]
[3, 8]
[7, 2]
[4, 7, 10]
[4, 7, 10]
[2, 7, 3]


# Define the pause time for each robot
pause_time = [2, 3, 4]

# Set up the plot
plt.figure()
plt.xlim(0, 12)
plt.ylim(0, 12)
plt.gca().set_aspect('equal', adjustable='box')
plt.xlabel('X')
plt.ylabel('Y')

# Plot the robot initial positions
robot_labels = []
for i in range(len(robot_x)):
    label = f'robot{i+1}'
    robot_labels.append(label)
    plt.plot(robot_x[i], robot_y[i], 'o', label=label)

# Plot the robot routes
for i in range(len(robot_route)):
    x = [p[0] for p in robot_route[i]]
    y = [p[1] for p in robot_route[i]]
    plt.plot(x, y)

# Initialize the robot trail
robot_trail = [[(x, y)] for x, y in zip(robot_x, robot_y)]

# Start the animation loop
for frame in range(len(robot_route[0])):
    plt.legend(robot_labels)
    for i in range(len(robot_x)):
        # Check if the robot has arrived at the current waypoint
        if (robot_x[i], robot_y[i]) == robot_route[i][frame][:2]:
            # Pause the robot for the specified time
            if robot_trail[i]:
                plt.plot(*zip(*robot_trail[i]), label=None,
                         linestyle='--', color='gray')
            time.sleep(pause_time[i])
        else:
            # Move the robot towards the current waypoint
            x_diff = robot_route[i][frame][0] - robot_x[i]
            y_diff = robot_route[i][frame][1] - robot_y[i]
            dist = ((x_diff ** 2) + (y_diff ** 2)) ** 0.5
            if dist > 0.1:
                robot_x[i] += 0.1 * x_diff / dist
                robot_y[i] += 0.1 * y_diff / dist
            else:
                robot_x[i], robot_y[i] = robot_route[i][frame][:2]

        # Add current position to the robot trail
        robot_trail[i].append((robot_x[i], robot_y[i]))

    # Update the plot
    plt.clf()
    plt.xlim(0, 12)
    plt.ylim(0, 12)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlabel('X')
    plt.ylabel('Y')
    for i in range(len(robot_x)):
        plt.plot(robot_x[i], robot_y[i], 'o', label=f'robot{i+1}')
        plt.plot(*zip(*robot_trail[i]), label=None,
                 linestyle='--', color='gray')
        if frame > 0:
            plt.plot(*zip(*robot_trail[i][:-1]), label=None,
                     linestyle='-', color='gray')


# Add the legend
plt.legend(robot_labels)

# Update the plot and pause briefly before moving to the next frame
plt.draw()
plt.pause(0.1)
plt.show()
