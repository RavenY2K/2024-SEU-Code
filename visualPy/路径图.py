import matplotlib.pyplot as plt

# 假设的数据
x = [0,13, 18, 20, 17.6, 28,30]
y = [60,10, 10, 5,2.7 , 7.3, 5.5]
groups = ['','A', 'A', 'B', 'A ', 'C','C']

x1 = [0, 38, 42, 40, 39.3, 35,37]
y1 = [60,48, 45, 47, 44.8 , 42, 24.6]
groups1 = ['','A', 'B', 'B', 'A ', 'B','B']

x2 = [0,6, 16, 14, 14.7, 20.2,]
y2 = [60,52, 45, 42, 33 , 32, ]
groups2 = ['','C', 'C', 'C', 'A ', 'C']



# 创建图表和轴对象
fig, ax = plt.subplots()

# 散点图，不同组使用不同颜色和标记
scatter = ax.scatter(x, y, alpha=0.6)
scatter1 = ax.scatter(x1, y1, alpha=0.6)
scatter2 = ax.scatter(x2, y2, alpha=0.6)

# 为每个点添加文本标签
for i, txt in enumerate(groups):
    ax.annotate(txt, (x[i], y[i]))
for i, txt in enumerate(groups1):
    ax.annotate(txt, (x1[i], y1[i]))
for i, txt in enumerate(groups2):
    ax.annotate(txt, (x2[i], y2[i]))

# 连接点
for i in range(len(x)-1):
    ax.plot(x[i:i+2], y[i:i+2], 'r--x')
for i in range(len(x1)-1):
    ax.plot(x1[i:i+2], y1[i:i+2], 'b--o')
for i in range(len(x2)-1):
    ax.plot(x2[i:i+2], y2[i:i+2], 'g--+',label='capA,capB,capC')
ax.plot( 'r--x',label='capA,capB,capC')
ax.plot( 'r--x',label='capA,capB')
ax.plot( 'r--x',label='capA,capC')

# 设置标题和轴标签
ax.set_xlabel('X coordinates (m)')
ax.set_ylabel('Y coordinates (m)')

# 显示图例
ax.legend(handles=scatter.legend_elements()[0], labels=groups)
ax.legend(handles=scatter1.legend_elements()[0], labels=groups1)
ax.legend(handles=scatter2.legend_elements()[0], labels=groups2)

# 显示图表
plt.show()