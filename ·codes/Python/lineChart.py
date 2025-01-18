from array import array

import matplotlib.pyplot as plt

# 示例数据
x = [1, 2, 4, 8, 16, 32]
y1 = [0.305130, 0.448451, 0.483239, 1.087587, 1.974306, 6.538984]
y2 = [0.312590, 0.338332, 0.479638, 0.937762, 1.958424, 4.431457]
y3 = [0.300974, 0.345285, 0.457441, 0.936405, 1.954648, 4.726106]
# y是平均值
y = [(y1[i] + y2[i] + y3[i]) / 3 for i in range(len(y1))]

# 创建折线图
plt.plot(x, y1, marker='o', linestyle='-', color='r', label='test1')
plt.plot(x, y2, marker='o', linestyle='-', color='g', label='test2')
plt.plot(x, y3, marker='o', linestyle='-', color='b', label='test3')
plt.plot(x, y, marker='o', linestyle='-', color='y', label='average')

# 添加标题和标签
plt.title('relationship between number of processes and computation latency')
plt.xlabel('the number of mpiSize')
plt.ylabel('the time used to finish (s)')
plt.legend()

# 保存图表
plt.savefig('line_chart.png')

# 显示图表
plt.show()
