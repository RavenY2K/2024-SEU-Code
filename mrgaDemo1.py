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
    def __init__(self, robots, tasks):
        self.robots = robots
        self.tasks = tasks

    def get_actions(self,robots,tasks,actions_list,actions = []):
        i=0
        for j in range(len(tasks)):
            if tasks[j] is not None:
                if robots[i].can_do(tasks[j]):
                    actions.append((robots[i].index, tasks[j].index))
                    new_robots = robots.copy()
                    new_robots.remove(robots[i])
                    new_tasks = tasks.copy()
                    if tasks[j].index != -1:
                        new_tasks.remove(tasks[j])
                    if len(new_robots) != 0:
                        self.get_actions(new_robots,new_tasks,actions_list,actions)
                        actions.pop()
                    else:
                        # 一轮机器人任务分配完成
                        tasks_not_allocate = 0
                        flag = False
                        for x in range(len(actions)):
                            if actions[x][1] != -1: 
                                flag = True
                        # flag 为true表示机器人没有全部wait
                        if flag:
                            actions_list.append(actions.copy())
                        actions.pop()
                        pass

    def get_actions_list(self):
        actions_list = []
        self.get_actions(self.robots, self.tasks, actions_list)
        return actions_list

    def apply_action(self, action):
        robot_index, task_index = action
        robot = self.robots[robot_index]
        task = self.tasks[task_index]
        if task_index != -1:
            self.tasks[task_index] = None
        robot.do_task(task)

    def is_terminal(self):
        return all(self.tasks[i] is None for i in range(len(self.tasks) -1))

    def get_reward(self):
        return max(robot.get_time() for robot in self.robots)

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
        if untried_actions == None:
            self.untried_actions = state.get_actions_list()
            pass
        else:
            self.untried_actions = untried_actions


    def simulate(self):
        current_state = copy.deepcopy(self.state)
        while not current_state.is_terminal():
            task = random.choice(current_state.tasks)
            if task == None :
                continue
            if task.index == -1:
                continue
            while 1:
                robot = random.choice(current_state.robots)
                if robot.can_do(task):
                    current_state.apply_action((robot.index,task.index))
                    break
                
        return current_state.get_reward()
    
    def expand(self): 
        new_state = State(
            copy.deepcopy(self.state.robots),
            copy.deepcopy(self.state.tasks)
        )     
            
        actions = random.choice(self.untried_actions)
        if self.parent == None:
            has_no_1 = True
            for element in actions:
                if element[1] == -1:
                    has_no_1 = False
            while(not has_no_1):
                pass
                actions = random.choice(self.untried_actions)
                has_no_1 = True
                for element in actions:
                    if element[1] == -1:
                        has_no_1 = False
            
        for action in actions:   
            new_state.apply_action(action)
        new_node = Node(new_state, self, actions)
        self.children.append(new_node)
        return new_node

    def is_fully_expanded(self):
        for i in range(len(self.untried_actions)):
            if len(self.untried_actions[i]) != 0:
                return False
        return True
    
    def reward(self):
        return self.state.get_reward()

    def is_terminal(self):
        return self.state.is_terminal()

    def select_child(self, exploration_constant=2):
        max_score = -10000000
        selected_child = None
        for child in self.children:
            score = (
                0 - child.reward
                + exploration_constant * math.sqrt(2 * math.log(self.visits) / child.visits)
            )

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
            if (i%100 == 0 and i<2000):
                print (i,round(time.time()-start_time,1),self.root.reward )
            else :
                if (i%1000 == 0 ):
                    print (i,round(time.time()-start_time,1),self.root.reward )
 
            while not node.is_terminal():
                # 一定的循环次数之后, 假设100此迭代式第一个任务刚好做完, 之后的迭代从第一个任务已经完成的状态开始
                if i > 1500 and node.parent == None:
                    node = self.get_best_child(node)

                else:
                    if not node.is_fully_expanded():
                        child = node.expand()
                        node = child
                        reward = node.simulate()
                        break
                    else:
                        # print ('fully expanded' )
                        node = node.select_child()
            
            # reward = node.state.get_reward() 
            
            node.backpropagate(reward)


        return self.root

# #生成随机任务和机器人
# tasks = []
# for i in range(10):
#     task = Task(round(random.uniform(0, 10), 2), round(random.uniform(0, 10), 2), random.randint(1, 3))
#     tasks.append(task)
 
# # # 保存为txt文件
# filenameA = './config/tasks.data'
# # with open(filename, 'wb') as file:
# #     pickle.dump(tasks, file)

# # 从txt文件读取
# with open(filenameA, 'rb') as file:
#     tasks = pickle.load(file)

# # 输出数组
# for task in tasks:
#     print(task.x, task.y, task.ability)

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
    # robots = pickle.load(file)


# filenameB = './config/robots.data' #二进制数据
# # 从txt文件读取
# with open(filenameB, 'rb') as file:
#     robots = pickle.load(file)

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
taskssData = 'Ros/scripts/mrga_tp/mrga_goals.txt'
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


#运行 MCTS 算法
start_time = time.time()

robots = husky_robots
tasks = husky_tasks
index = 0
for task in tasks:
    task.index = index
    index += 1
tasks.append(Task(-1, 'wait',0,0,'cap',0))
index = 0
for robot in robots:
    robot.index = index
    index += 1
husky_state = State(husky_robots, husky_tasks)
husky_mcts = MCTS(husky_state)
husky_actions = husky_mcts.run(20000)
husky_result = husky_actions.reward
end_time = time.time()

husky_time = end_time-start_time
print('husky_time: ', round(husky_time, 2), round(husky_result,2))

# start_time = time.time()

# robots = auv_robots
# tasks = auv_tasks
# index = 0
# for task in tasks:
#     task.index = index
#     index += 1
# tasks.append(Task(-1, 'wait',0,0,'cap',0))
# index = 0
# for robot in robots:
#     robot.index = index
#     index += 1
# auv_state = State(auv_robots, auv_tasks)
# auv_mcts = MCTS(auv_state)
# auv_result = auv_mcts.run(200).reward
# end_time = time.time()
# auv_time = end_time-start_time
# print('auv_time: ', round(auv_time,2), round(auv_result,2))

# print("sum_time:", round(auv_time+husky_time,2), round(max(husky_result,auv_result),2))
