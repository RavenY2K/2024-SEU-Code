import random
import math
import re
import time
import copy

class Robot:
    def __init__(self, index,  name, x, y, abilities):
        self.name = name
        self.index = index
        self.x = x
        self.y = y
        self.abilities = abilities
        self.task_times = []

    def can_do(self, task):
        if task.index == -1:
            return True
        if 'husky' in self.name:
            if 'a' in task.point:
                return False
        else: 
            if 'g' in task.point:
                return False
        return task is not None and task.ability in self.abilities

    def do_task(self, task):
        if task.index != -1:
            distance = math.sqrt((float(self.x) - float(task.x)) ** 2 + (float(self.y) - float(task.y)) ** 2)
            self.x = task.x
            self.y = task.y
            self.task_times.append(distance+task.do_time)
        else:
            pass

    def get_time(self):
        return sum(self.task_times)

class Task:
    def __init__(self,index, point,  x, y, ability, do_time):
        self.index = index
        self.point = point
        self.x = x
        self.y = y
        self.ability = ability
        self.do_time = do_time


RobotSpawnMap = {}
Map = {}
mapData = 'Ros/scripts/mrga_tp/mrga_waypoints.txt'
with open(mapData, 'r') as file:
    for line in file:
        name = line[:line.index('[')]
        Robotname = ''
        RobotSpawnRegex = r"\{(.*?)\}"
        RobotSpawnmatches = re.search(RobotSpawnRegex, line)
        if RobotSpawnmatches:
            Robotname = RobotSpawnmatches.group(1)

        regex = r"\[(.*?)\]"
        matches = re.search(regex, line)
        if matches:
            XYindex = matches.group(1).split(', ')

        if Robotname:
            RobotSpawnMap[Robotname] = XYindex
        else:
            Map[name]= XYindex

robots = []
robotData = 'Ros/scripts/mrga_tp/mrga_robots.txt'
with open(robotData, 'r') as file:
    index = 0
    for line in file:
        if line[0] == '#':
            continue
        name = line[:line.index('[')]
        regex = r"\[(.*?)\]"
        matches = re.search(regex, line)
        if matches:
            # 将匹配的子串拆分为数组
            ablities = matches.group(1).split(', ')
        robots.append(Robot(index, name, RobotSpawnMap[name][0],RobotSpawnMap[name][1], ablities))
        index+=1

tasks = []
tasks_do_time = {
    'cap4': 15,
    'cap5': 5,
    'cap6': 20,
    'cap7': 10,
    'cap8': 10
}
tasksData = 'Ros/scripts/mrga_tp/mrga_goals.txt'
with open(tasksData, 'r') as file:
    index = 0
    for s in file:
        if s[0] == '#':
            continue
        name = s[s.index(' ') + 1:s.index(')')]
        ability = s[s.index(')') + 1:].rstrip('\n')
        tasks.append(Task(index, name,Map[name][0],Map[name][1],ability,tasks_do_time[ability]))
        index+=1
    tasks.append(Task(-1, 'wait',0,0,'cap',0))

MrgaAllocationData = 'Ros/config/allocation_solution.txt'
with open(MrgaAllocationData, 'r') as file:
    index = 0
    for s in file:
        if s[0] == '#':
            continue
        words = s.split()
        curRobot = None
        curTask = None
        robotName = words[1]
        taskName = words[2].rstrip(')')
        for robot in robots:
            if robot.name == robotName:
                curRobot = robot
        name = s[s.index(' ') + 1:s.index(')')]
        for task in tasks:
            if task.point == taskName:
                curTask = task
        curRobot.do_task(curTask)
    maxTime = 0
    for robot in robots:
        time =  sum(robot.task_times)
        maxTime = max(maxTime, time)
    print(maxTime)

      


