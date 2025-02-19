import os

import openpyxl


def get_texts(path):
    results = []
    for root, dirs, files in os.walk(path):
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


def form_xlsx(model_info, path):
    print(f"start to get score of model {model_info}")
    results = get_texts(path + "files/" + model_info)
    for i in range(len(results)):
        result = results[i][1]
        # print(f"result {i}\n: {result}")
        final = []
        result = result.split('\n')
        for j in range(len(result)):
            if result[j].startswith('最终打分'):
                final.append(result[j].split('：')[1].split('(')[0])
            elif result[j].startswith('1. 结构完整性得分') \
                    or result[j].startswith('2. 逻辑清晰度得分') \
                    or result[j].startswith('3. 语言连贯性得分') \
                    or result[j].startswith('4. 内容独特性和创新性得分') \
                    or result[j].startswith('5. 参考文献规范性得分') \
                    or result[j].startswith('6. 课程知识掌握度得分'):
                score = result[j].split('分：')[1].split(',')[0]
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
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "22人工智能-3.5-25x4-1轮"
    ws.append(
        ["题目", "最终打分", "结构完整性得分", "1原因", "逻辑清晰度得分", "2原因", "语言连贯性得分", "3原因",
         "内容独特性和创新性得分", "4原因", "参考文献规范性得分", "5原因", "课程知识掌握度得分", "6原因", "修改意见"])
    for result in results:
        title = result[0]
        content = result[1]
        if isinstance(content, list) and len(content) > 6:
            score = content[0]
            sub_score_1 = content[1][0]
            sub_reason_1 = content[1][1]
            sub_score_2 = content[2][0]
            sub_reason_2 = content[2][1]
            sub_score_3 = content[3][0]
            sub_reason_3 = content[3][1]
            sub_score_4 = content[4][0]
            sub_reason_4 = content[4][1]
            sub_score_5 = content[5][0]
            sub_reason_5 = content[5][1]
            sub_score_6 = content[6][0]
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
        ws.append([title, score, sub_score_1, sub_reason_1, sub_score_2, sub_reason_2, sub_score_3, sub_reason_3,
                   sub_score_4, sub_reason_4, sub_score_5, sub_reason_5, sub_score_6, sub_reason_6, suggest])
    wb.save(path + model_info + ".xlsx")


if __name__ == '__main__':
    fileCount = 25
    input_path = "./data/课程报告/22人工智能导论/extract_report"
    models = [
        "original",
        "without-22AI-long-1轮",
        "without-22AI-long-3轮",
        "without-22AI-long-5轮",
    ]
    print("save xlsx file")
    for model in models:
        form_xlsx(model, f"./result/only-without-22AI/")
