import matplotlib.pyplot as plt
import numpy as np



# 设定初始值和数组大小
initial_value = 0
array_size = 20
increment = 0.5  # 平均递增的值
randomness = 0.8  # 随机性的程度

# 生成小幅度随机递增的数组
x = np.arange(1, 21, 1)

y2 = np.random.normal(200, 0, size=x.size)
y3 = np.random.normal(170, 10, size=x.size)

y2p = 0
y3p = 0 
for i in range(0, 20):
    y2p += np.random.normal(10, 15)
    y3p += np.random.normal(8, 12)
    y2[i] = y2[i] + y2p 
    y3[i] = y3[i] + y3p

values = [initial_value]
for index in range(1, array_size):
    new_value = values[-1] + np.random.normal(increment, randomness)
    values.append(new_value)

y1 = np.array(values)

# 示例数据
y2inital = 200
# y1 = np.random.normal(100, 10, size=x.size)
plt.rcParams['font.family'] = 'SimHei'  # 替换为你选择的字体


y1_err = np.random.normal(10, 2, size=x.size)
y2_err = np.random.normal(20, 5, size=x.size)

# 绘制误差线

plt.errorbar(x, y1, yerr=y1_err, label='MRGA', fmt='-o', color='blue')
plt.errorbar(x, y2, yerr=y2_err, label='POPF', fmt='-s', color='orange')
plt.errorbar(x, y3, yerr=y2_err, label='LPG', fmt='-s', color='lightgreen')

# 添加图例
plt.legend()

# 添加标题和坐标轴标签
plt.xlabel('任务规模',fontsize=14)

plt.ylabel('规划时间/s',fontsize=14) 

# 展示图表
plt.show()