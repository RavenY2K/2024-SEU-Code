import random
import math
import re
import time
import copy

def dec_mcts():
    
    class Robot:
        def __init__(self, index,  name, x, y, abilities):
            self.name = name
            self.index = index
            self.x = x
            self.y = y
            self.abilities = abilities
            self.task_times = []
            self.allocated_tasks=[]

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
                distance = round(math.sqrt((round(float(self.x),2) - round(float(task.x),2)) ** 2 + (round(float(self.y),2) - round(float(task.y),2)) ** 2),2)
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
            
            cur_task = None
            for task in self.tasks:
                if task.index == task_index:
                    cur_task = task
                    break
            
            if task_index != -1:
                self.able_task.remove(task_index)
            robot.do_task(cur_task)

        def is_terminal(self,cur_allocated_task=[]):
            filtered_array = [x for x in self.able_task if x not in cur_allocated_task]
            return len(filtered_array) == 0

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

        def select_child_by_index(self,index):
            for cur_node in self.children:
                if cur_node.action == index:
                    return cur_node


        def simulate(self,cur_allocated_task=[]):
            current_state = copy.deepcopy(self.state)
            while not current_state.is_terminal(cur_allocated_task):
                task = random.choice([x for x in current_state.actions_list if x not in cur_allocated_task])
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

        def change_node(self,state):
            pass
            
        
        def is_fully_expanded(self):
            return len(self.untried_actions) == 0
        
        def reward(self):
            return self.state.get_reward()

        def is_terminal(self,cur_allocated_task=[]):
            return self.state.is_terminal(cur_allocated_task)

        def select_child(self, cur_allocated_task = [],exploration_constant=100):
            max_score = -10000000
            
            # 此处自定义 self.exploration_constant 为 当前树的最优reward的 15%
            exploration_constant = self.reward * 0.15
            selected_child = None
            for child in self.children:
                score = (
                    0 - child.reward
                    + exploration_constant * math.sqrt(2 * math.log(self.visits) / child.visits)
                    -(10000000 if child.action in cur_allocated_task else 0)
                )
                # print ('===', child.reward, exploration_constant * math.sqrt(2 * math.log(self.visits) / child.visits), score)
                # print(0 - child.reward / child.visits)
                # print(1.41 * math.sqrt(2 * math.log(self.visits) / child.visits))
                if score > max_score:
                    max_score = score
                    selected_child = child
            return selected_child

        def backpropagate(self, reward):
            if reward == None:
                return 
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
                self.robot = state.robot

            def get_best_child(self,node):
                best_child = None
                min_reward = float("inf")
                for child in node.children:
                    if child.visits > 0 and child.reward  < min_reward:
                        best_child = child
                        min_reward = child.reward 
                return best_child


            def run(self, max_iterations):
                cur_root = self.root 
                # for index in self.robot.allocated_tasks:
                #     cur_root = cur_root.select_child_by_index(index)
                start_time = time.time()
                cur_allocated_task =  husky_allocated_tasks if 'husky' in self.robot.name else uav_allocated_tasks
                
                
                for i in range(max_iterations):
                    node = cur_root

                    if i%100 == 0:
                        pass
                        # print (i,round(time.time()-start_time,1),self.root.reward )
                        
                    reward = None
                    while not node.is_terminal(cur_allocated_task):
                        # 若已经安排了任务则必定选择


                        if not node.is_fully_expanded():
                            child = node.expand()
                            node = child
                            reward = node.simulate(cur_allocated_task)
                            break
                        else:
                            node = node.select_child(cur_allocated_task)
                
                    # reward = node.state.get_reward() 
                    
                    node.backpropagate(reward)

                return self.root


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
    # # 输出数组
    # for robot in robots:
    #     if robot.x == 1:
    #         robot.abilities.append(2)
    #     print(robot.x, robot.y, robot.abilities)

    # with open(filenameB, 'wb') as file:
    #     pickle.dump(robots, file)

    def set_index(arr):
        for list in arr:
            index = 0
            for item in list:
                item.index =index
                index+=1

    #初始化数据
    husky_robots = []
    uav_robots = []

    for robot in robots:
        if "husky" in robot.name:
            husky_robots.append(robot)
        else:
            uav_robots.append(robot)

    husky_tasks = []
    uav_tasks = []
    for task in tasks:
        if "wpg" in task.point:
            husky_tasks.append(task)
        else:
            uav_tasks.append(task)

    set_index([husky_robots,husky_tasks,uav_robots,uav_tasks])     
            
    # 最终工作顺序
    husky_allocated_tasks = []
    uav_allocated_tasks = []


    #定义主程序
    def init_mcts(robots,tasks,name,budge_time):
        start_time = time.time()
        all_mcts_tree = []
        
        cur_allocated_tasks = husky_allocated_tasks if 'husky' in name else uav_allocated_tasks
        for task in cur_allocated_tasks:
            tasks = [x for x in tasks if x.index not in cur_allocated_tasks]
            
        for robot in robots:
            state = State(robot, tasks)
            mcts = MCTS(state)
            all_mcts_tree.append(mcts)
            actions = mcts.run(budge_time)
            result = actions.reward
            end_time = time.time()
            diff_time = end_time-start_time
            # print(name+'time: ', round(diff_time, 3), round(result,2))
        return all_mcts_tree


    def run_mcts(all_mcts_tree,name):
        cur_allocated_tasks = husky_allocated_tasks if 'husky' in name else uav_allocated_tasks
        cur_robots = husky_robots if 'husky' in name else uav_robots
        for mcts in all_mcts_tree:
            cur_root = mcts.root
            for task_index in mcts.robot.allocated_tasks:
                cur_root = cur_root.select_child_by_index(task_index)
            new_state = State(mcts.robot, [x for x in cur_root.state.tasks if x.index not in cur_allocated_tasks])
            pass
        

    def allocateTask(result,name):
        cur_allocated_tasks = husky_allocated_tasks if 'husky' in name else uav_allocated_tasks
        cur_tasks =  husky_tasks if 'husky' in name else uav_tasks
        for element in result:
            robot = element.robot
            cur_root = element.root
            
            # for task in robot.allocated_tasks:
            #     cur_root=cur_root.select_child_by_index(task)

            sorted_children = sorted(cur_root.children, key=lambda x: x.reward)
            for item in sorted_children:
                if item.action not in cur_allocated_tasks:
                    robot.allocated_tasks.append(item.action)
                    
                    cur_task = None
                    for task in cur_tasks:
                        if task.index == item.action:
                            cur_task = task
                    robot.do_task(cur_task)
                        
                
                    cur_allocated_tasks.append(item.action)
                    break
    
    #运行 MCTS 算法
    start_time = time.time()
    husky_result = init_mcts(husky_robots,husky_tasks,'husky',101)
    allocateTask(husky_result,'husky')
    end_time = time.time()
    husky_time = end_time-start_time


    start_time = time.time()
    uav_result = init_mcts(uav_robots,uav_tasks,'uav',101)
    allocateTask(uav_result,'uav')
    end_time = time.time()
    uav_time = end_time-start_time

    # run_mcts(husky_result,'husky')
    while len(husky_allocated_tasks) < len(husky_tasks):
        # print('---------------------------------------------------------------')
        husky_result = init_mcts(husky_robots,husky_tasks,'husky',501)
        allocateTask(husky_result,'husky')



    # print('---------------------------------------------------------------')
    # print('---------------------------------------------------------------')
    # print('---------------------------------------------------------------')
        

    final_score = 0
    for robot in husky_robots:
        cur_score = robot.get_time()
        final_score = cur_score if cur_score > final_score else final_score
        # print(robot.name,cur_score)
    pass
    # print("sum_time:", round(uav_time+husky_time,2), round(max(husky_result,uav_result),2))
    return final_score

results = []  # 创建一个列表来存储每一遍的最终结果

for _ in range(3):  # 循环运行程序10次
    # 在这里运行你的程序，假设最终结果是 result
    result = dec_mcts()
    results.append(result)
    
for i, result in enumerate(results, start=1):
    print(f"第 {i} 遍的最终结果: {result}")
print(results)

    
