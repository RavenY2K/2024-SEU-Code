import matplotlib.pyplot as plt

# 示例数据
x = [0.0, 0.1, 0.2, 0.3, 0.4]

y1 = [100.9, 97.7, 99.2, 102.4, 104.2] # Dec-MCTS-SP的平均值
y2 = [141.2, 138.5, 135.2, 137.3, 144.2] # Dec-MCTS的平均值

errors1 = [9, 12, 13, 8, 11] # 误差值，假设为标准差
errors1 = [11, 13, 15, 11, 12] # 误差值，假设为标准差


plt.errorbar(x, y1, yerr=errors1, fmt='-o', label='4Robots-12Tasks',capsize=4,color='r')
plt.errorbar(x, y2, yerr=errors1, fmt='-s', label='4Robots-20Tasks',capsize=4,color='black')

plt.xlabel('k value')
plt.ylabel('Time(s)')
plt.legend()
plt.show()