# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pyrobotics.visualize import RobotModel, Trajectory2D

# 创建一个机器人模型
robot = RobotModel()

# 添加一个盒子作为机器人的机身
robot.add_link("Body", 1, [1, 1, 0.5], [0, 0, 0])

# 添加两个轮子作为机器人的运动部件
robot.add_wheel("LeftWheel", "Body", [-0.5, -0.5, 0], [0, 0, 1])
robot.add_wheel("RightWheel", "Body", [-0.5, 0.5, 0], [0, 0, 1])

# 创建一个2D轨迹绘制对象
traj = Trajectory2D()

# 设置机器人的初始位置和朝向
robot.set_pose([0, 0, 0], [1, 0, 0, 0])

# 定义一个控制程序，在每个时间步长里更新机器人的状态和轨迹
def control(i):
    t = float(i) / 10
    x = np.sin(t)
    y = np.cos(t)
    theta = t
    robot.set_pose([x, y, 0], [np.cos(theta/2), 0, 0, np.sin(theta/2)])
    traj.add_point([x, y])

# 创建一个动画对象
ani = animation.FuncAnimation(fig=plt.figure(), func=control, frames=100)

# 展示动画和轨迹
robot.show(ani, traj)
