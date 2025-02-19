import json
import os

import pandas as pd


def get_system():
    return ("你是一位教授人工智能导论课程的大学教师，需要对学生提交的课程项目报告进行评估。" + "\n" +
            "请评估以下<报告文本/总结报告文本>在描述<结构完整性>，<逻辑清晰度>， <语言连贯性>， <内容独特性和创新性>， <参考文献规范性>，<课程知识掌握度>方面的表现，" + "\n" +
            "并根据各指标<占比比例>进行打分与点评，打分范围0-10分。并最终按照<打分模版>给出学生报告打分结果与评价”。打分模板如下：“最终打分：<> (范围0-10分)" + "\n" +
            "1. 结构完整性得分：<>, 占比20%，原因如下：<>" + "\n" +
            "2. 逻辑清晰度得分：<>, 占比20%，原因如下：<>" + "\n" +
            "3. 语言连贯性得分：<>, 占比20%，原因如下：<>" + "\n" +
            "4. 内容独特性和创新性得分：<>, 占比20%，原因如下：<>" + "\n" +
            "5. 参考文献规范性得分：<>, 占比10%，原因如下：<>" + "\n" +
            "6. 课程知识掌握度得分：<>, 占比10%，原因如下：<>”" + "\n" +
            "请严格按照以下格式返回结果，最终打分一行、6个维度各自一行、修改意见一行，不要擅自添加换行：" + "\n" +
            "最终打分：<> (范围0-10分)" + "\n" +
            "1. 结构完整性得分：<>, 占比20%，原因如下：<>" + "\n" +
            "2. 逻辑清晰度得分：<>, 占比20%，原因如下：<>" + "\n" +
            "3. 语言连贯性得分：<>, 占比20%，原因如下：<>" + "\n" +
            "4. 内容独特性和创新性得分：<>, 占比20%，原因如下：<>" + "\n" +
            "5. 参考文献规范性得分：<>, 占比10%，原因如下：<>" + "\n" +
            "6. 课程知识掌握度得分：<>, 占比10%，原因如下：<>" + "\n" +
            "修改意见：<>"
            )


def get_texts(path):
    results = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    if file.endswith('_summary.txt'):
                        file_name = file.split('.')[0].split('_')[-2]
                    else:
                        file_name = file.split('.')[0].split('_')[-1]
                    results.append([file_name, f.read()])
    return results


def get_results(path, text_files, package):
    results = []
    data = pd.read_excel(path, sheet_name='result')
    ai_intro_row = data[data.iloc[:, 0].str.contains(package, na=False)].index[0]
    data_need = data.iloc[ai_intro_row + 1:]
    for file_info in text_files:
        file_name = file_info[0]
        user_content = file_info[1]
        row = data_need[data_need.iloc[:, 0].str.contains(file_name, na=False)]
        if row.empty:
            print(f"{file_name} not found")
            continue
        values = row.values[0]
        total_score = values[25]
        sub_score_1 = values[19]
        sub_score_2 = values[20]
        sub_score_3 = values[21]
        sub_score_4 = values[22]
        sub_score_5 = values[23]
        sub_score_6 = values[24]
        assistant_content = (f"最终打分：{total_score} (范围0-10分)\n" +
                             f"1. 结构完整性得分：{sub_score_1}, 占比20%\n" +
                             f"2. 逻辑清晰度得分：{sub_score_2}, 占比20%\n" +
                             f"3. 语言连贯性得分：{sub_score_3}, 占比20%\n" +
                             f"4. 内容独特性和创新性得分：{sub_score_4}, 占比20%\n" +
                             f"5. 参考文献规范性得分：{sub_score_5}, 占比10%\n" +
                             f"6. 课程知识掌握度得分：{sub_score_6}, 占比10%\n"
                             )
        results.append([user_content, assistant_content])
    return results


def form_json(path, system_content, contents):
    data = []
    for user_content, assistant_content in contents:
        message_json = {
            "messages": [
                {
                    "role": "system",
                    "content": system_content
                },
                {
                    "role": "user",
                    "content": user_content
                },
                {
                    "role": "assistant",
                    "content": assistant_content
                }
            ]
        }
        data.append(json.dumps(message_json, ensure_ascii=False))
    with open(path, 'w', encoding='utf-8') as f:
        for json_str in data:
            f.write(json_str + "\n")


def run(file, result, package, saving):
    system = get_system()
    texts = get_texts(file)
    responses = get_results(result, texts, package)
    form_json(saving, system, responses)


def run_summary(file, result, package, saving):
    system = get_system()
    texts = get_texts(file)
    responses = get_results(result, texts, package)
    form_json(saving, system, responses)


if __name__ == '__main__':
    section_name = "题目"
    result_path = "./data/result_strip.xlsx"
    input_path = "./data/创新实践/2022年春季学期创新实践/extract_report"
    saving_path = "./data/22_group.jsonl"
    # input_path_summary = "./data/课程报告/22人工智能导论/extract_report_summary"
    # saving_path_summary = "./data/课程报告/22人工智能导论/extract_report_summary.jsonl"
    run(input_path, result_path, section_name, saving_path)
    # run_summary(input_path_summary, result_path, package_name, saving_path_summary)
