import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_bar(name, data, y_name, y_min, y_max):
    # 设置全局字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 数据准备
    df = pd.DataFrame(data)

    # 提取类别和模型名称
    categories = df.columns[1:]
    models = df['模型'].values

    # 创建图表
    fig, ax = plt.subplots(figsize=(25, 16))

    # 设置每个类别的柱子宽度和间距
    bar_width = 0.18  # 适度增加柱宽
    index = np.arange(len(categories))

    # 绘制每个模型的柱状图
    for i, model in enumerate(models):
        values = df.iloc[i, 1:].values
        ax.bar(index + i * bar_width, values, bar_width, label=model)

    # 添加数据标签（柱子上的数字）
    for i, model in enumerate(models):
        values = df.iloc[i, 1:].values
        for j, value in enumerate(values):
            height = value
            va = 'bottom' if value >= 0 else 'top'
            offset = 0.03 * (y_max - y_min)
            y_pos = height + offset if height >= 0 else height - offset
            ax.text(index[j] + i * bar_width, y_pos, f'{value:.2f}', ha='center', va=va, fontsize=18)

    # 设置X轴刻度标签
    ax.set_xticks(index + bar_width * 2)
    ax.set_xticklabels(categories, fontsize=26, rotation=50, ha='right')

    # 设置坐标轴刻度标签大小
    plt.xticks(fontsize=28)  # X轴标签大小
    plt.yticks(fontsize=28)  # Y轴标签大小

    # 设置Y轴范围
    ax.set_ylim(y_min, y_max)

    # 添加图例
    ax.legend(fontsize=30)

    # 添加网格线
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # 调整布局
    plt.tight_layout()

    # 保存和显示图表
    plt.savefig(f'{name}_python.svg', dpi=300, bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    xlsx = [{
        'name': '提示语调控下各模型打分平均绝对误差(MAE)',
        'data': {
            '模型': ['通义千问-Plus', '通义千问2.5-14B-1M', '通义千问-Turbo', 'DeepSeek-V3', 'DeepSeek-R1'],
            '最终打分': [0.52, 0.61, 0.78, 0.39, 0.70],
            '结构完整性得分': [0.44, 0.59, 0.48, 0.98, 0.46],
            '逻辑清晰度得分': [0.54, 0.74, 0.93, 0.81, 0.56],
            '语言连贯性得分': [0.68, 0.67, 0.62, 0.50, 1.01],
            '内容独特性和创新性得分': [0.58, 0.74, 1.00, 0.51, 0.87],
            '参考文献规范性得分': [1.76, 1.08, 1.71, 1.48, 2.11],
            '课程知识掌握度得分': [0.51, 0.87, 1.35, 0.35, 0.87]
        },
        'y_name': '平均绝对误差(MAE)',
        'min': 0,
        'max': 3.5,
    }, {
        'name': '提示语调控下各模型打分均方误差(MSE)',
        'data': {
            '模型': ['通义千问-Plus', '通义千问2.5-14B-1M', '通义千问-Turbo', 'DeepSeek-V3', 'DeepSeek-R1'],
            '最终打分': [0.39, 0.58, 0.85, 0.36, 0.71],
            '结构完整性得分': [0.48, 0.65, 0.65, 1.11, 0.48],
            '逻辑清晰度得分': [0.55, 0.95, 1.24, 1.02, 0.64],
            '语言连贯性得分': [0.69, 0.77, 0.65, 0.52, 1.43],
            '内容独特性和创新性得分': [0.53, 0.81, 1.42, 0.47, 1.24],
            '参考文献规范性得分': [4.20, 2.36, 4.15, 3.22, 5.84],
            '课程知识掌握度得分': [0.57, 1.09, 2.29, 0.68, 1.30]
        },
        'y_name': '均方误差(MSE)',
        'min': 0,
        'max': 6.5,
    }, {
        'name': '提示语调控下各模型打分皮尔逊相关系数(PCC)',
        'data': {
            '模型': ['通义千问-Plus', '通义千问2.5-14B-1M', '通义千问-Turbo', 'DeepSeek-V3', 'DeepSeek-R1'],
            '最终打分': [0.41, 0.25, 0.11, 0.04, 0.33],
            '结构完整性得分': [0.34, 0.17, 0.11, 0.06, 0.37],
            '逻辑清晰度得分': [0.31, 0.27, 0.06, -0.21, 0.19],
            '语言连贯性得分': [0.30, 0.04, 0.10, 0.11, 0.31],
            '内容独特性和创新性得分': [0.47, 0.36, 0.44, 0.56, 0.30],
            '参考文献规范性得分': [0.00, 0.08, -0.01, -0.09, 0.11],
            '课程知识掌握度得分': [0.15, 0.02, 0.09, -0.23, 0.12]
        },
        'y_name': '皮尔逊相关系数(PCC)',
        'min': -0.3,
        'max': 0.7,
    }, {
        'name': '模型微调后各模型打分平均绝对误差(MAE)',
        'data': {
            '模型': ['通义千问-Plus', '通义千问2.5-14B-1M', '通义千问-Turbo', 'DeepSeek-V3', 'DeepSeek-R1'],
            '最终打分': [0.41, 0.42, 0.37, 0.34, 0.30],
            '结构完整性得分': [0.44, 0.73, 0.50, 0.78, 0.42],
            '逻辑清晰度得分': [0.60, 0.65, 0.47, 0.41, 0.44],
            '语言连贯性得分': [0.63, 0.49, 0.56, 0.43, 0.53],
            '内容独特性和创新性得分': [0.47, 0.45, 0.79, 0.54, 0.49],
            '参考文献规范性得分': [1.13, 1.07, 1.02, 0.93, 1.12],
            '课程知识掌握度得分': [0.53, 0.33, 0.38, 0.27, 0.36]
        },
        'y_name': '平均绝对误差(MAE)',
        'min': 0,
        'max': 1.7,
    }, {
        'name': '模型微调后各模型打分均方误差(MSE)',
        'data': {
            '模型': ['通义千问-Plus', '通义千问2.5-14B-1M', '通义千问-Turbo', 'DeepSeek-V3', 'DeepSeek-R1'],
            '最终打分': [0.25, 0.27, 0.21, 0.19, 0.15],
            '结构完整性得分': [0.50, 0.79, 0.70, 0.88, 0.59],
            '逻辑清晰度得分': [0.58, 0.61, 0.41, 0.38, 0.41],
            '语言连贯性得分': [0.69, 0.50, 0.48, 0.34, 0.48],
            '内容独特性和创新性得分': [0.43, 0.42, 0.85, 0.54, 0.47],
            '参考文献规范性得分': [3.53, 3.23, 2.68, 2.23, 2.75],
            '课程知识掌握度得分': [0.60, 0.33, 0.38, 0.29, 0.35]
        },
        'y_name': '均方误差(MSE)',
        'min': 0,
        'max': 4.2,
    }, {
        'name': '模型微调后各模型打分皮尔逊相关系数(PCC)',
        'data': {
            '模型': ['通义千问-Plus', '通义千问2.5-14B-1M', '通义千问-Turbo', 'DeepSeek-V3', 'DeepSeek-R1'],
            '最终打分': [0.21, 0.41, 0.40, 0.29, 0.56],
            '结构完整性得分': [0.29, 0.05, 0.23, 0.16, -0.06],
            '逻辑清晰度得分': [0.07, 0.07, 0.24, 0.10, 0.01],
            '语言连贯性得分': [-0.04, 0.24, 0.21, 0.24, 0.45],
            '内容独特性和创新性得分': [0.49, 0.70, 0.35, 0.54, 0.53],
            '参考文献规范性得分': [0.04, 0.02, 0.08, 0.35, 0.07],
            '课程知识掌握度得分': [-0.00, 0.07, 0.36, 0.06, 0.31]
        },
        'y_name': '皮尔逊相关系数(PCC)',
        'min': -0.2,
        'max': 0.9,
    }]
    for item in xlsx:
        name = item['name']
        data = item['data']
        y_name = item['y_name']
        y_min = item['min']
        y_max = item['max']
        plot_bar(name, data, y_name, y_min, y_max)
