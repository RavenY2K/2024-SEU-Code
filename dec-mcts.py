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


class State:
    def __init__(self, robot, tasks):
        self.robot = robot
        self.tasks = tasks
        self.actions_list = []
        self.able_task = []
        self.get_actions_list()

    def get_actions_list(self):
        for i in range(len(self.tasks)):
            if self.tasks[i] is not None:
                if self.robot.can_do(self.tasks[i]):
                    self.actions_list.append(self.tasks[i].index)
                    self.able_task.append(self.tasks[i].index)

    def apply_action(self, action):
        task_index = action
        robot = self.robot
        task = self.tasks[task_index]
        if task_index != -1:
            self.able_task.remove(task_index)
        robot.do_task(task)

    def is_terminal(self):
        return len(self.able_task) == 0

    def get_reward(self):
        return self.robot.get_time()

    def __str__(self):
        return f"State(robots={self.robots}, tasks={self.tasks})"

class Node:
    def __init__(self, state, parent, action, untried_actions = None):
        self.state = state
        self.parent = parent
        self.action = action
        self.reward = 0
        self.visits = 0
        self.children = []
        self.untried_actions = untried_actions
        if untried_actions == None:
            self.untried_actions = state.actions_list



    def simulate(self):
        current_state = copy.deepcopy(self.state)
        while not current_state.is_terminal():
            task = random.choice(current_state.actions_list)
            current_state.actions_list.remove(task)
            current_state.apply_action(task)
                
        return current_state.get_reward()
    
    
    def expand(self): 
        new_state = State(
            copy.deepcopy(self.state.robot),
            copy.deepcopy(self.state.tasks)
        )
        action = random.choice(self.state.actions_list)
        
        new_state.apply_action(action)
        new_state.actions_list.remove(action)
        new_node = Node(new_state, self, action)
        self.children.append(new_node)
        return new_node

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0
    
    def reward(self):
        return self.state.get_reward()
 
    def is_terminal(self):
        return self.state.is_terminal()

    def select_child(self, exploration_constant=100):
        max_score = -10000000
        
        # 此处自定义 self.exploration_constant 为 当前树的最优reward的 15%
        exploration_constant = self.reward * 0.15
        selected_child = None
        for child in self.children:
            score = (
                0 - child.reward
                + exploration_constant * math.sqrt(2 * math.log(self.visits) / child.visits)
            )
            # print ('===', child.reward, exploration_constant * math.sqrt(2 * math.log(self.visits) / child.visits), score)
            # print(0 - child.reward / child.visits)
            # print(1.41 * math.sqrt(2 * math.log(self.visits) / child.visits))
            if score > max_score:
                max_score = score
                selected_child = child
        return selected_child

    def backpropagate(self, reward):
        self.visits += 1
        if self.reward == 0:
            self.reward = reward
        else:
            self.reward = self.reward if self.reward < reward else reward

        if self.parent != None:
            try:
                self.parent.untried_actions.remove(self.action)
            except ValueError:
               pass
        if self.parent is not None:
            self.parent.backpropagate(reward)

class MCTS:
    def __init__(self, state):
        self.root = Node(state, None, None)

    def get_best_child(self,node):
        best_child = None
        min_reward = float("inf")
        for child in node.children:
            if child.visits > 0 and child.reward  < min_reward:
                best_child = child
                min_reward = child.reward 
        return best_child


    def run(self, max_iterations):
        start_time = time.time()
        for i in range(max_iterations):
            node = self.root
            if i%100 == 0:
                pass
                print (i,round(time.time()-start_time,1),self.root.reward )
                

            while not node.is_terminal():
                # 一定的循环次数之后, 假设100此迭代式第一个任务刚好做完, 之后的迭代从第一个任务已经完成的状态开始
                if i > 100 and node.parent == None:
                    node = self.get_best_child(node)

                else:
                    if not node.is_fully_expanded():
                        child = node.expand()
                        node = child
                        reward = node.simulate()
                        break
                    else:
                        node = node.select_child()
            
            # reward = node.state.get_reward() 
            
            node.backpropagate(reward)


        return self.root



RobotSpawnMap = {}
Map = {}
mapData = 'Ros\scripts\mrga_tp\mrga_waypoints.txt'
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
    # robots = pickle.load(file)


# filenameB = './config/robots.data' #二进制数据
# # 从txt文件读取
# with open(filenameB, 'rb') as file:
#     robots = pickle.load(file)

robots = []
robotData = 'Ros\scripts\mrga_tp\mrga_robots.txt'
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
taskssData = 'Ros\scripts\mrga_tp\mrga_goals.txt'
with open(taskssData, 'r') as file:
    index = 0
    for s in file:
        if s[0] == '#':
            continue
        name = s[s.index(' ') + 1:s.index(')')]
        ability = s[s.index(')') + 1:].rstrip('\n')
        tasks.append(Task(index, name,Map[name][0],Map[name][1],ability,tasks_do_time[ability]))
        index+=1
# # 输出数组
# for robot in robots:
#     if robot.x == 1:
#         robot.abilities.append(2)
#     print(robot.x, robot.y, robot.abilities)

# with open(filenameB, 'wb') as file:
#     pickle.dump(robots, file)

husky_robots = []
auv_robots = []

for robot in robots:
    if "husky" in robot.name:
        husky_robots.append(robot)
    else:
        auv_robots.append(robot)

husky_tasks = []
auv_tasks = []
for task in tasks:
    if "wpg" in task.point:
        husky_tasks.append(task)
    else:
        auv_tasks.append(task)
#初始化状态


#定义主程序
def run_mcts(robots,tasks,name):
    start_time = time.time()
    index = 0
    for task in tasks:
        task.index = index
        index += 1
    index = 0
    for robot in robots:
        robot.index = index
        index += 1
    for robot in robots:
        state = State(robot, tasks)
        mcts = MCTS(state)
        actions = mcts.run(201)
        result = actions.reward
        end_time = time.time()
        diff_time = end_time-start_time
        print(name+'time: ', round(diff_time, 2), round(result,2))
    return round(result,2)

#运行 MCTS 算法
start_time = time.time()
husky_result = run_mcts(husky_robots,husky_tasks,'husky')
end_time = time.time()
husky_time = end_time-start_time
# print(husky_time)

start_time = time.time()
auv_result = run_mcts(auv_robots,auv_tasks,'auv')
end_time = time.time()
auv_time = end_time-start_time



print("sum_time:", round(auv_time+husky_time,2), round(max(husky_result,auv_result),2))
