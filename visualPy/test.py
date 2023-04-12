
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
for i in range(0,len(data),3):
    row = []
    for j in range(len(data[i])):
        row = [(x, y, int(z)) for x, y, z in zip(
            data[i], data[i+1], data[i+2])]
    robot_route.append(row)

print(robot_route)