import random
import math
import pickle

class Robot:
    def __init__(self, x, y, abilities):
        self.x = x
        self.y = y
        self.abilities = abilities
        self.task_times = []

    def can_do(self, task):
        return task is not None and task.ability in self.abilities

    def do_task(self, task):
        distance = math.sqrt((self.x - task.x) ** 2 + (self.y - task.y) ** 2)
        # self.task_times.append(distance / task.ability) 为啥除以ability
        self.task_times.append(distance)

    def get_time(self):
        return sum(self.task_times)

class Task:
    def __init__(self, x, y, ability):
        self.x = x
        self.y = y
        self.ability = ability

class State:
    def __init__(self, robots, tasks):
        self.robots = robots
        self.tasks = tasks

    def get_actions(self):
        actions = []
        for i in range(len(self.robots)):
            for j in range(len(self.tasks)):
                if self.tasks[j] is not None and self.robots[i].can_do(self.tasks[j]):
                    actions.append((i, j))
        return actions

    def apply_action(self, action):
        robot_index, task_index = action
        robot = self.robots[robot_index]
        task = self.tasks[task_index]
        robot.do_task(task)
        self.tasks[task_index] = None

    def is_terminal(self):
        return all(task is None for task in self.tasks)

    def get_reward(self):
        return max(robot.get_time() for robot in self.robots)

    def __str__(self):
        return f"State(robots={self.robots}, tasks={self.tasks})"

class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
        self.reward = 0
        self.visits = 0
        self.children = []
        self.untried_actions = state.get_actions()

    def expand(self):
        action = self.untried_actions.pop()
        new_state = State(
            [robot for robot in self.state.robots],
            [task for task in self.state.tasks]
        )
        new_state.apply_action(action)
        new_node = Node(new_state, self, action)
        self.children.append(new_node)
        return new_node

    def is_fully_expanded(self):
        return not self.untried_actions

    def is_terminal(self):
        return self.state.is_terminal()

    def select_child(self, exploration_constant=1.4):
        max_score = -1
        selected_child = None
        for child in self.children:
            score = child.reward / child.visits + exploration_constant * math.sqrt(
                2 * math.log(self.visits) / child.visits
        )
        if score > max_score:
            max_score = score
            selected_child = child
        return selected_child

    def backpropagate(self, reward):
        self.visits += 1
        self.reward += reward
        if self.parent is not None:
            self.parent.backpropagate(reward)

class MCTS:
    def __init__(self, state):
        self.root = Node(state, None, None)

    def run(self, max_iterations):
        for _ in range(max_iterations):
            node = self.root
            while not node.is_terminal():
                if not node.is_fully_expanded():
                    child = node.expand()
                    return child.reward
                else:
                    node = node.select_child()
            reward = node.state.get_reward() 
            node.backpropagate(reward)

        best_child = self.root.children[0]
        for child in self.root.children:
            if child.visits > best_child.visits:
                best_child = child
        return best_child.action

# #生成随机任务和机器人
# tasks = []
# for i in range(10):
#     task = Task(round(random.uniform(0, 10), 2), round(random.uniform(0, 10), 2), random.randint(1, 3))
#     tasks.append(task)
 
# # 保存为txt文件
filenameA = './config/tasks.data'
# with open(filename, 'wb') as file:
#     pickle.dump(tasks, file)

# 从txt文件读取
with open(filenameA, 'rb') as file:
    tasks = pickle.load(file)

# 输出数组
for task in tasks:
    print(task.x, task.y, task.ability)


# robots = [
# Robot(random.randint(0, 10), random.randint(0, 10), [random.randint(1, 3)])
# for _ in range(3)
# ]
 
filenameB = './config/robots.data'
# with open(filenameB, 'wb') as file:
#     pickle.dump(robots, file)

# 从txt文件读取
with open(filenameB, 'rb') as file:
    robots = pickle.load(file)

# 输出数组
for robot in robots:
    print(robot.x, robot.y, robot.abilities)

#初始化状态
state = State(robots, tasks)

#运行 MCTS 算法
mcts = MCTS(state)
best_action = mcts.run(1000)
print("Best action:", best_action)

