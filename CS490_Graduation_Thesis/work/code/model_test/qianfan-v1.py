import json
import os
import time

import requests

# 毕设
API_Key = "UmZ7cAQkNenzYb8W4xfKWNYB"
Secret_Key = "wrBhOrXsCzwiMTzwG2Sb8wIXRqdaWVRv"


def get_access_token():
    """
    使用应用API Key，应用Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """

    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_Key}&client_secret={Secret_Key}"

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


def get_score(model_id, text):
    """
    向模型发送请求，获取结果，规范格式
    """
    # get the score from model
    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{model_id}?access_token=" + get_access_token()
    payload = json.dumps({
        "messages": {
            "role": "user",
            "content": f"请给以下报告打分:\n{text}"
        },
        "system": "你是一位大学教师教授，需要对学生提交的毕业设计论文进行评估。\n"
                  "请评估以下<报告文本/总结报告文本>在描述<结构完整性>，<逻辑清晰度>， <语言连贯性>， <内容独特性和创新性>， <参考文献规范性>，<课程知识掌握度>方面的表现，"
                  "并根据各指标<占比比例>进行打分与点评，打分范围0-10分。并最终按照<打分模版>给出学生报告打分结果与评价”。打分模板如下：\n"
                  "最终打分：<> (范围0-10分)\n"
                  "1. 结构完整性得分：<>, 占比20%，原因如下：<>\n"
                  "2. 逻辑清晰度得分：<>, 占比20%，原因如下：<>\n"
                  "3. 语言连贯性得分：<>, 占比20%，原因如下：<>\n"
                  "4. 内容独特性和创新性得分：<>, 占比20%，原因如下：<>\n"
                  "5. 参考文献规范性得分：<>, 占比10%，原因如下：<>\n"
                  "6. 课程知识掌握度得分：<>, 占比10%，原因如下：<>\n"
                  "修改意见：<>\n"
                  "请严格按照以下格式返回结果，最终打分一行、6个维度各自一行、修改意见一行，不要擅自添加换行：\n"
                  "最终打分：<> (范围0-10分)\n"
                  "1. 结构完整性得分：<>, 占比20%，原因如下：<>\n"
                  "2. 逻辑清晰度得分：<>, 占比20%，原因如下：<>\n"
                  "3. 语言连贯性得分：<>, 占比20%，原因如下：<>\n"
                  "4. 内容独特性和创新性得分：<>, 占比20%，原因如下：<>\n"
                  "5. 参考文献规范性得分：<>, 占比10%，原因如下：<>\n"
                  "6. 课程知识掌握度得分：<>, 占比10%，原因如下：<>\n"
                  "修改意见：<>\n"
    })
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    # Parse the response
    url_result = 'None'
    if 'error_code' in json.loads(response.text).keys():
        error_message = json.loads(response.text)['error_msg']
        print(RuntimeError(error_message))
        url_result = (f"最终打分：{error_message}"
                      f"1. 结构完整性得分：, 占比20%，原因如下：<>"
                      f"2. 逻辑清晰度得分：, 占比20%，原因如下：<>"
                      f"3. 语言连贯性得分：, 占比20%，原因如下：<>"
                      f"4. 内容独特性和创新性得分：, 占比20%，原因如下："
                      f"5. 参考文献规范性得分：, 占比10%，原因如下："
                      f"6. 课程知识掌握度得分：, 占比10%，原因如下："
                      f"修改意见：<>"
                      )
    if 'result' in json.loads(response.text).keys():
        url_result = json.loads(response.text)['result']

    while url_result.count('\n') > 0:
        url_result = url_result.replace('\n', '')
    url_result = url_result.replace('1. 结构完整性得分', '\n1. 结构完整性得分')
    url_result = url_result.replace('2. 逻辑清晰度得分', '\n2. 逻辑清晰度得分')
    url_result = url_result.replace('3. 语言连贯性得分', '\n3. 语言连贯性得分')
    url_result = url_result.replace('4. 内容独特性和创', '\n4. 内容独特性和创')
    url_result = url_result.replace('5. 参考文献规范性', '\n5. 参考文献规范性')
    url_result = url_result.replace('6. 课程知识掌握度', '\n6. 课程知识掌握度')
    url_result = url_result.replace('修改意见：', '\n修改意见：')
    print(url_result)
    return url_result


def score_report(path, model_detail, max_count):
    """
    给报告打分，遍历文件夹，读取报告内容，输给模型进行评分
    """
    count = 1
    responses = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".txt"):
                # count the number of reports
                if count > max_count:
                    print("out of range, quit")
                    return responses
                print(f"the time {count}")
                count += 1

                # get all the text
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()

                # get the score from model
                scores = (
                    f"最终打分："
                    f"1. 结构完整性得分：, 占比20%，原因如下：<>"
                    f"2. 逻辑清晰度得分：, 占比20%，原因如下：<>"
                    f"3. 语言连贯性得分：, 占比20%，原因如下：<>"
                    f"4. 内容独特性和创新性得分：, 占比20%，原因如下："
                    f"5. 参考文献规范性得分：, 占比10%，原因如下："
                    f"6. 课程知识掌握度得分：, 占比10%，原因如下："
                    f"修改意见：<>"
                )
                scores = get_score(model_detail, text)
                responses.append([file.split('_')[0], scores])
                time.sleep(10)
    print("finished looping")
    return responses


def txt(model_info, path, limitation, saving):
    """
    将模型的评分结果进行格式重构，输出成txt文件
    """
    print(f"start to get score of model {model_info[0]}")
    results = score_report(path, model_info[1], limitation)
    for i in range(len(results)):
        file_name = results[i][0]
        file_content = results[i][1]
        file_path = f'{saving}/{file_name}.txt'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(file_content)


if __name__ == '__main__':
    # all_folders = ["2023本科论文", "2023组内毕设", "2024本科论文"]
    folder_list = ["2023本科论文"]
    for folder in folder_list:
        print(f"正在处理：{folder}")
        fileCount = 500
        input_path = rf"D:\Sustech\course\CS490_Graduation_Thesis\work\data-preprocessed\{folder}\txt"
        output_path = rf"D:\Sustech\course\CS490_Graduation_Thesis\work\results\baiduqianfan\v1"
        models = [
            ["ERNIE-Speed-128K", "ernie-speed-128k"],
            ["ERNIE-Speed-8K", "ernie_speed"],
            ["ERNIE-Lite-8K", "ernie-lite-8k"],
            ["ERNIE-Tiny-8K", "ernie-tiny-8k"],
            ["QwQ-32B", "completions"],
        ]
        print("save txt file")
        for model in models:
            txt(model, input_path, fileCount, rf"{output_path}/{model[0]}")
        print(f"处理完成：{folder}")
