import os
import re

import openpyxl

"""
将结果转换成xlsx文件进行结果统计
"""


def get_texts(txt_path):
    """
    遍历文件夹，从文档中获取文本，获得结果
    """
    results = []
    for root, dirs, files in os.walk(txt_path):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_name = file.split('.')[0]
                    file_content = f.read()
                    while file_content.count('\n\n') > 0:
                        file_content = file_content.replace('\n\n', '\n')
                    # print(file_content)
                    results.append([file_name, file_content])
    return results


def pick_out_score(results):
    """
    从文本中提取评分和总分
    """
    for result in results:
        # print(result[0])
        content = result[1]
        # print(content)
        # 使用正则表达式匹配评分和总分
        score_patterns = [
            # 匹配 "得分：8", "得分为：8.5", "得分：**8" 等
            r"(?:得分|总分|评分|总评|打分) {0,1}\*{0,2} {0,1}为{0,1}(?:：|: |:|) {0,1}\*{0,2} {0,1}(\d+(?:\.\d+)?)",
        ]
        scores = []
        for pattern in score_patterns:
            matches = re.findall(pattern, content)
            scores.extend(matches) if matches else None
        # 将字符串分数转换为浮点数
        scores = [float(score) for score in scores] if scores else [-1]
        # 去重并按照分数从大到小排序
        scores = [score if score < 10 else -1 for score in scores]
        scores = sorted(set(scores), reverse=True)
        # print(scores)
        score = scores[0] if scores else -1
        # print(score)
        result.append(score)
    return results


def form_xlsx(input_path, folder_name, model_name):
    """
    摘取所需数据，生成xlsx文件
    """
    print(f"start to get score of model {model_name}")
    results = get_texts(rf"{input_path}\{model_name}\{folder_name}")
    results = pick_out_score(results)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"{model_name}"
    ws.append(
        ["题目", "打分", "原文"])
    for result in results:
        print(f"start to get score of {result[0]}")
        ws.append([result[0], result[2], result[1]])
    wb.save(rf"{path}\{model_name}\{folder_name}.xlsx")


if __name__ == '__main__':
    path = rf"../../../work/results/aliyunbailian"
    models = [
        # 通义 - 文本生成
        # "通义千问-Plus",
        # "通义千问2.5-14B-1M",
        # "通义千问-Turbo",
        # DeepSeek - 文本生成
        # "DeepSeek-V3",
        # DeepSeek - 推理模型
        # "DeepSeek-R1",
    ]
    print("save xlsx file")
    folder = "all_without_system"
    print(f"正在处理：{folder}")
    for model in models:
        print(f"正在处理：{model}")
        form_xlsx(path, folder, model)
