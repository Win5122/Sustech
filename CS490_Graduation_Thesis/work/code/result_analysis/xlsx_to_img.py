import matplotlib.pyplot as plt
import pandas as pd


def plot_bar(name, data, min, max):
    # 设置全局字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 数据准备
    df = pd.DataFrame(data)

    # 创建图表
    plt.figure(figsize=(16, 9))
    bars = plt.bar(df['模型'], df['最终打分'])

    # 添加数据标签（柱子上的数字）
    for bar in bars:
        height = bar.get_height()
        va = 'bottom' if height >= 0 else 'top'  # 正数在下，负数在上
        offset = 0.03 * (max - min)
        y_pos = height + offset if height >= 0 else height - offset
        plt.text(bar.get_x() + bar.get_width() / 2., y_pos,
                 f'{height:.2f}',
                 ha='center', va=va,
                 fontsize=24)  # 柱子数字大小

    # 设置坐标轴刻度标签大小
    plt.xticks(fontsize=26)  # X轴标签大小
    plt.yticks(fontsize=26)  # Y轴标签大小

    # 其他设置
    plt.ylim(min, max)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=50, ha='right')

    plt.tight_layout()
    plt.savefig(f'{name}_python.svg', dpi=300, bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    xlsx = [{
        'name': '无提示语时各模型打分均分',
        'data': {
            '模型': ['教师评分结果', '通义千问-Plus', '通义千问2.5-14B-1M',
                     '通义千问-Turbo', 'DeepSeek-V3', 'DeepSeek-R1'],
            '最终打分': [8.39, 9.13, 8.30, 8.30, 8.49, 8.09]
        },
        'min': 7,
        'max': 9.5,
    }, {
        'name': '无提示语时各模型打分平均绝对误差(MAE)',
        'data': {
            '模型': ['通义千问-Plus', '通义千问2.5-14B-1M',
                     '通义千问-Turbo', 'DeepSeek-V3', 'DeepSeek-R1'],
            '最终打分': [0.94, 0.93, 0.52, 0.64, 0.53]
        },
        'min': 0,
        'max': 1.2,
    }, {
        'name': '无提示语时各模型打分均方误差(MSE)',
        'data': {
            '模型': ['通义千问-Plus', '通义千问2.5-14B-1M',
                     '通义千问-Turbo', 'DeepSeek-V3', 'DeepSeek-R1'],
            '最终打分': [1.27, 1.76, 0.48, 1.09, 0.49]
        },
        'min': 0,
        'max': 2,
    }, {
        'name': '无提示语时各模型打分皮尔逊相关系数(PCC)',
        'data': {
            '模型': ['通义千问-Plus', '通义千问2.5-14B-1M',
                     '通义千问-Turbo', 'DeepSeek-V3', 'DeepSeek-R1'],
            '最终打分': [0.23, -0.14, 0.17, 0.12, 0.36]
        },
        'min': -0.4,
        'max': 0.6,
    }]
    for item in xlsx:
        name = item['name']
        data = item['data']
        min = item['min']
        max = item['max']
        plot_bar(name, data, min, max)
