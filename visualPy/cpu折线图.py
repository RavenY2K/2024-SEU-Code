import matplotlib.pyplot as plt
import numpy as np


initial_value = 1.35
array_size = 7
increment = 0.3  # 平均递增的值
randomness = 0.04 # 随机性的程度


# 生成小幅度随机递增的数组
values = [initial_value]

for _ in range(1, array_size):
    new_value = values[-1] + np.random.normal(increment, randomness)
    increment-=0.05
    values.append(new_value)

y1 = np.array(values)

# 假设的数据
x = np.arange(2, 9)
y = np.random.randint(1000, 30000, size=len(x))  # 随机生成一些整数数据
plt.rcParams['font.family'] = 'SimHei'  # 替换为你选择的字体

plt.figure(figsize=(10, 6))  # 设置画布的大小
plt.plot(x, y1, color='lightblue', linewidth=3)  # 折线为浅蓝色，线宽为3

# 设置x和y轴的标签
plt.xlabel('CPU核心数量', fontsize=14)
plt.ylabel('单核时间/多核时间', fontsize=14)

plt.xticks(np.arange(min(x), max(x)+1, 1.0))
plt.ylim    (0, max(y1)+0.5)
# 开启网格线
plt.grid(True)

# 显示图表
plt.show()