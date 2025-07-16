import os
import re

import openpyxl

"""
将结果转换成xlsx文件进行结果统计
"""


def clean_string(s):
    """移除Excel非法字符（保留常见可打印字符）"""
    if isinstance(s, str):
        # 替换非法字符为空格，保留字母、数字、常见符号和空格
        return re.sub(r'[^\x20-\x7E\u00A0-\uFFFF]', ' ', s)
    return s


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
                    while file_content.count('\n') > 0:
                        file_content = file_content.replace('\n', '')
                    # print(file_content)
                    file_content = file_content.replace('1. 结构完整性得分', '\n1. 结构完整性得分')
                    file_content = file_content.replace('2. 逻辑清晰度得分', '\n2. 逻辑清晰度得分')
                    file_content = file_content.replace('3. 语言连贯性得分', '\n3. 语言连贯性得分')
                    file_content = file_content.replace('4. 内容独特性和创', '\n4. 内容独特性和创')
                    file_content = file_content.replace('5. 参考文献规范性', '\n5. 参考文献规范性')
                    file_content = file_content.replace('6. 课程知识掌握度', '\n6. 课程知识掌握度')
                    file_content = file_content.replace('修改意见：', '\n修改意见：')
                    while file_content.count('<>') > 0:
                        file_content = file_content.replace('<>', '')
                    # print(file_content)
                    results.append([file_name, file_content])
    return results


def form_xlsx(input_path, folder_name, model_name):
    """
    摘取所需数据，生成xlsx文件
    """
    print(f"start to get score of model {model_name}")
    results = get_texts(rf"{input_path}/{model_name}/{folder_name}")
    for i in range(len(results)):
        print(f"start to get score of {results[i][0]}")
        # if results[i][0] != '12011507':
        #     continue
        result = results[i][1]
        # print(f"result {i}\n: {result}")
        final = []
        result = result.split('\n')
        for j in range(len(result)):
            if (result[j].startswith('最终打分')
                    or result[j].startswith('最终评分')
                    or result[j].startswith('最终得分')
                    or result[j].startswith('打分结果：最终打分')
            ):
                final.append(
                    result[j]
                    .split('打分结果：')[-1]
                    .split('：')[1]
                    .split('(')[0]
                    .split('（')[0]
                    .split('/')[0]
                    .strip()
                    .replace('<', '')
                    .replace('>', '')
                    .replace('**', '')
                )
            elif result[j].startswith('1. 结构完整性得分') \
                    or result[j].startswith('2. 逻辑清晰度得分') \
                    or result[j].startswith('3. 语言连贯性得分') \
                    or result[j].startswith('4. 内容独特性和创新性得分') \
                    or result[j].startswith('5. 参考文献规范性得分') \
                    or result[j].startswith('6. 课程知识掌握度得分'):
                score = (
                    result[j]
                    .split('分：')[1]
                    .split(',')[0]
                    .split('，')[0]
                    .split('占比')[0]
                    .split('原因如下')[0]
                    .split('-')[0]
                    .strip()
                    .replace('<', '')
                    .replace('>', '')
                    .replace('**', '')
                )
                reason = ""
                if result[j].count('原因如下：') > 0:
                    reason = result[j].split('原因如下：')[1]
                final.append([score, reason])
            elif result[j].startswith('修改意见'):
                final.append(result[j].split('修改意见：')[1])
            else:
                final = result[j]
        # print(final)
        results[i][1] = final
        # print(results[i])
    print(f"start to write score of model {model_name}")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"{model_name}"
    ws.append(
        ["题目", "最终打分", "结构完整性得分", "1原因", "逻辑清晰度得分", "2原因", "语言连贯性得分", "3原因",
         "内容独特性和创新性得分", "4原因", "参考文献规范性得分", "5原因", "课程知识掌握度得分", "6原因", "修改意见"])
    for result in results:
        print(f"start to write score of {result[0]}")
        title = result[0]
        # print(f"title: {title}")
        content = result[1]
        if isinstance(content, list) and len(content) > 6:
            score = float(content[0])
            sub_score_1 = float(content[1][0])
            sub_reason_1 = content[1][1]
            sub_score_2 = float(content[2][0])
            sub_reason_2 = content[2][1]
            sub_score_3 = float(content[3][0])
            sub_reason_3 = content[3][1]
            sub_score_4 = float(content[4][0])
            sub_reason_4 = content[4][1]
            sub_score_5 = float(content[5][0]) if content[5][0] != 'N/A' else 0
            sub_reason_5 = content[5][1]
            sub_score_6 = float(content[6][0])
            sub_reason_6 = content[6][1]
            if len(content) > 7:
                suggest = content[7]
            else:
                suggest = ""
        else:
            score = content
            sub_score_1 = ""
            sub_reason_1 = ""
            sub_score_2 = ""
            sub_reason_2 = ""
            sub_score_3 = ""
            sub_reason_3 = ""
            sub_score_4 = ""
            sub_reason_4 = ""
            sub_score_5 = ""
            sub_reason_5 = ""
            sub_score_6 = ""
            sub_reason_6 = ""
            suggest = ""
        ws.append([
            title, score,
            sub_score_1, clean_string(sub_reason_1),
            sub_score_2, clean_string(sub_reason_2),
            sub_score_3, clean_string(sub_reason_3),
            sub_score_4, clean_string(sub_reason_4),
            sub_score_5, clean_string(sub_reason_5),
            sub_score_6, clean_string(sub_reason_6),
            clean_string(suggest)])
    wb.save(rf"{path}/{model_name}/{folder_name}.xlsx")


if __name__ == '__main__':
    # 阿里云百炼 aliyunbailian
    aliyunbailian_path = rf"../../results/aliyunbailian"
    aliyunbailian_models = [
        # 通义 - 文本生成
        "通义千问-Plus",
        "通义千问2.5-14B-1M",
        "通义千问-Turbo",
        # DeepSeek - 文本生成
        "DeepSeek-V3",
        # DeepSeek - 推理模型
        "DeepSeek-R1",
        "通义千问-Turbo-Latest",
    ]
    # 网页端大语言模型 llmwebui
    llmwebui_path = rf"/results/LLM_web-ui"
    llmwebui_models = [
        "chatGPT",
        "deepseek",
        "tongyiqianwen",
        "wenxinyiyan",
    ]
    print("save xlsx file")
    folder_list = [
        'all_system-original_few-shot-0',
        'all_system-original_few-shot-1',
        'all_system-original_few-shot-2',
        'all_system-original_few-shot-3',
        'all_system-w-o-role_few-shot-2',
    ]
    path = aliyunbailian_path
    models = aliyunbailian_models
    for folder in folder_list:
        for model in models:
            print(f"正在处理：{folder}")
            print(f"正在处理：{model}")
            form_xlsx(path, folder, model)
