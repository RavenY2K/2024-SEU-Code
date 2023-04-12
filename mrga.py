import numpy as np
import copy

# Define the Robot class
class Robot:
    def __init__(self, id, skills):
        self.id = id
        self.skills = skills
        self.current_task = None
        self.time_to_complete_task = 0

# Define the Task class
class Task:
    def __init__(self, id, location, required_skills, time_to_complete):
        self.id = id
        self.location = location
        self.required_skills = required_skills
        self.time_to_complete = time_to_complete
        self.robot_assigned = None

# Define the State class
class State:
    def __init__(self, robots, tasks, time):
        self.robots = robots
        self.tasks = tasks
        self.time = time

# Define the Action class 
class Action:
    def __init__(self, robot_id, task_id):
        self.robot_id = robot_id
        self.task_id = task_id

# Define the Node class
class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
        self.children = []
        self.visits = 0
        self.reward = 0

    def is_fully_expanded(self):
        return len(self.children) == len(self.get_legal_actions())

    def get_legal_actions(self):
        legal_actions = []
        for robot in self.state.robots:
            if robot.current_task is None:
                for task in self.state.tasks:
                    if task.robot_assigned is None and set(task.required_skills).issubset(set(robot.skills)):
                        legal_actions.append(Action(robot.id, task.id))
        return legal_actions

    def select_child(self):
        for child in self.children:
            if child.visits == 0:
                print(111,child)
                return child
        max_ucb = float("-inf")
        selected_child = None 
        for child in self.children:
            ucb = child.reward / child.visits + np.sqrt(2 * np.log(self.visits) / child.visits)
            if ucb > max_ucb:
                max_ucb = ucb
                selected_child = child
        print(222,selected_child)
        return selected_child

    def expand(self):
        legal_actions = self.get_legal_actions()
        action = np.random.choice(legal_actions)
        robot = self.state.robots[action.robot_id]
        task = self.state.tasks[action.task_id]
        new_robots = copy.deepcopy(self.state.robots)
        new_tasks = copy.deepcopy(self.state.tasks)
        new_robot = Robot(robot.id, robot.skills)
        new_robot.current_task = task
        new_robot.time_to_complete_task = task.time_to_complete
        new_robots[robot.id] = new_robot
        new_task = Task(task.id, task.location, task.required_skills, task.time_to_complete)
        new_task.robot_assigned = robot.id
        new_tasks[task.id] = new_task
        new_state = State(new_robots, new_tasks, self.state.time)
        child_node = Node(new_state, self, action)
        self.children.append(child_node)
        return child_node

    def update(self, reward):
        self.visits += 1
        self.reward += reward

# Define the MCTS class
class MCTS:
    def __init__(self, root_state, budget):
        self.root = Node(root_state, None, None)
        self.budget = budget

    def search(self):
        for i in range(self.budget):
            node = self.root
            # Selection
            while not node.is_fully_expanded() and len(node.get_legal_actions()) > 0:
                node = node.select_child()
            # Expansion
            if len(node.get_legal_actions()) > 0:
                child_node = node.expand()
                # Simulation
                reward = self.simulate(child_node)
                # Backpropagation
                while child_node is not None:
                    child_node.update(reward)
                    child_node = child_node.parent
            else:
                # Simulation
                reward = self.simulate(node)
                # Backpropagation
                while node is not None:
                    node.update(reward)
                    node = node.parent

        best_child = self.get_best_child(self.root)
        return best_child.action

    def simulate(self, node):
        state = node.state
        time = state.time
        robots = state.robots
        tasks = state.tasks
        while not self.is_terminal(state):
            # Choose a random robot that has a task assigned
            assigned_robots = [robot for robot in robots if robot.current_task is not None]
            robot = np.random.choice(assigned_robots)
            task = robot.current_task
            # Move the robot towards the task location
            distance = np.linalg.norm(robot.current_task.location - robot.location)
            time += distance
            robot.location = robot.current_task.location
            # Decrease the remaining time to complete the task
            robot.time_to_complete_task -= distance
            if robot.time_to_complete_task <= 0:
                # Complete the task
                task.robot_assigned = None
                robot.current_task = None
            else:
                # Move the robot back to its original location
                distance = np.linalg.norm(task.location - robot.location)
                time += distance
                robot.location = task.location
        return -time

    def get_best_child(self, node):
        best_child = None
        max_reward = float("-inf")
        for child in node.children:
            if child.visits > 0 and child.reward / child.visits > max_reward:
                best_child = child
                max_reward = child.reward / child.visits
        return best_child

    def is_terminal(self, state):
        for task in state.tasks:
            if task.robot_assigned is None:
                return False
        return True

# Create 10 robots with different skills
robots = []
for i in range(10):
    skills = np.random.choice(['A', 'B', 'C', 'D'], size=3, replace=False)
    robot = Robot(i, skills)
    robots.append(robot)

# Create 20 tasks with different locations, required skills, and time to complete
tasks = []
for i in range(20):
    location = np.random.uniform(-10, 10, size=2)
    required_skills = np.random.choice(['A', 'B', 'C', 'D'], size=2, replace=False)
    time_to_complete = np.random.uniform(1, 5)
    task = Task(i, location, required_skills, time_to_complete)
    tasks.append(task)

# Create the root state
root_state = State(robots, tasks, 0)

# Create the MCTS object and run the search algorithm
mcts = MCTS(root_state, budget=10000)
best_action = mcts.search()

# Print the best action and the total time to complete all tasks
print("Best action:", best_action)
print("Total time:", -mcts.get_best_child(mcts.root).reward)

   
