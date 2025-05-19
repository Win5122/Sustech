import json
import os
import time

import openpyxl
import qianfan
import requests

"""
项目主体：获取access token，访问模型，得到模型输出的结果
"""


API_KEY = "UmZ7cAQkNenzYb8W4xfKWNYB"
SECRET_KEY = "wrBhOrXsCzwiMTzwG2Sb8wIXRqdaWVRv"


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    # print("getting access token")
    # Set up the request to get an access token
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    # print("getting access token success")
    return str(requests.post(url, params=params).json().get("access_token"))


def get_score_url(model_url, text):
    """
    通过接口URL访问模型，得到模型打分
    """
    # print("getting score")
    # Set up the API request
    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{model_url}?access_token=" + get_access_token()
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": f"请给以下报告打分:\n\n{text}"
            },
        ],
        "system": "你是一位大学教师教授，需要对学生提交的毕业设计论文进行评估。"
                  "请评估以下<报告文本/总结报告文本>在描述<结构完整性>，<逻辑清晰度>， <语言连贯性>， <内容独特性和创新性>， <参考文献规范性>，<课程知识掌握度>方面的表现，"
                  "并根据各指标<占比比例>进行打分与点评，打分范围0-10分。并最终按照<打分模版>给出学生报告打分结果与评价”。打分模板如下：“最终打分：<> (范围0-10分)"
                  "1. 结构完整性得分：<>, 占比20%，原因如下：<>"
                  "2. 逻辑清晰度得分：<>, 占比20%，原因如下：<>"
                  "3. 语言连贯性得分：<>, 占比20%，原因如下：<>"
                  "4. 内容独特性和创新性得分：<>, 占比20%，原因如下：<>"
                  "5. 参考文献规范性得分：<>, 占比10%，原因如下：<>"
                  "6. 课程知识掌握度得分：<>, 占比10%，原因如下：<>”"
                  "请严格按照以下格式返回结果，最终打分一行、6个维度各自一行、修改意见一行，不要擅自添加换行："
                  "最终打分：<> (范围0-10分)"
                  "1. 结构完整性得分：<>, 占比20%，原因如下：<>"
                  "2. 逻辑清晰度得分：<>, 占比20%，原因如下：<>"
                  "3. 语言连贯性得分：<>, 占比20%，原因如下：<>"
                  "4. 内容独特性和创新性得分：<>, 占比20%，原因如下：<>"
                  "5. 参考文献规范性得分：<>, 占比10%，原因如下：<>"
                  "6. 课程知识掌握度得分：<>, 占比10%，原因如下：<>"
                  "修改意见：<>"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.text)
    # Parse the response
    url_result = 'None'
    if 'error_code' in json.loads(response.text).keys():
        print(RuntimeError(json.loads(response.text)['error_msg']))
        url_result = (f"最终打分：{json.loads(response.text)['error_msg']}"
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
    # print(url_result)
    # print("getting score success")
    while url_result.count('\n') > 0:
        url_result = url_result.replace('\n', '')
    url_result = url_result.replace('1. 结构完整性得分', '\n1. 结构完整性得分')
    url_result = url_result.replace('2. 逻辑清晰度得分', '\n2. 逻辑清晰度得分')
    url_result = url_result.replace('3. 语言连贯性得分', '\n3. 语言连贯性得分')
    url_result = url_result.replace('4. 内容独特性和创', '\n4. 内容独特性和创')
    url_result = url_result.replace('5. 参考文献规范性', '\n5. 参考文献规范性')
    url_result = url_result.replace('6. 课程知识掌握度', '\n6. 课程知识掌握度')
    url_result = url_result.replace('修改意见：', '\n修改意见：')
    # print(url_result)
    return url_result


def get_score_sdk(model_id, text):
    """
    通过接口SDK访问模型，得到模型打分
    """
    chat_comp = qianfan.ChatCompletion()
    resp = chat_comp.do(model=model_id,
                        messages=[
                            {
                                "role": "user",
                                "content": f"请给以下报告打分:\n\n{text}"
                            },
                        ],
                        system="你是一大学教授，需要对学生提交的毕业设计论文进行评估。"
                               "请评估以下<报告文本/总结报告文本>在描述<结构完整性>，<逻辑清晰度>， <语言连贯性>， <内容独特性和创新性>， <参考文献规范性>，<课程知识掌握度>方面的表现，"
                               "并根据各指标<占比比例>进行打分与点评，打分范围0-10分。并最终按照<打分模版>给出学生报告打分结果与评价”。打分模板如下：“最终打分：<> (范围0-10分)"
                               "1. 结构完整性得分：<>, 占比20%，原因如下：<>"
                               "2. 逻辑清晰度得分：<>, 占比20%，原因如下：<>"
                               "3. 语言连贯性得分：<>, 占比20%，原因如下：<>"
                               "4. 内容独特性和创新性得分：<>, 占比20%，原因如下：<>"
                               "5. 参考文献规范性得分：<>, 占比10%，原因如下：<>"
                               "6. 课程知识掌握度得分：<>, 占比10%，原因如下：<>”"
                               "请严格按照以下格式返回结果，最终打分一行、6个维度各自一行、修改意见一行，不要擅自添加换行："
                               "最终打分：<> (范围0-10分)"
                               "1. 结构完整性得分：<>, 占比20%，原因如下：<>"
                               "2. 逻辑清晰度得分：<>, 占比20%，原因如下：<>"
                               "3. 语言连贯性得分：<>, 占比20%，原因如下：<>"
                               "4. 内容独特性和创新性得分：<>, 占比20%，原因如下：<>"
                               "5. 参考文献规范性得分：<>, 占比10%，原因如下：<>"
                               "6. 课程知识掌握度得分：<>, 占比10%，原因如下：<>"
                               "修改意见：<>"
                        )
    response = resp["body"]
    sdk_result = response["result"]
    return sdk_result


def score_report(path, model_detail, max_count):
    """
    给报告打分，遍历文件夹，读取报告内容，输给模型进行评分
    """
    count = 1
    responses = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    if count > max_count:
                        print("out of range, quit")
                        return responses
                    print(f"the time {count}")
                    scores = get_score_url(model_detail, f.read())
                    # scores = get_score_sdk(model_detail, f.read())
                    while scores.count('\n\n') != 0:
                        scores = scores.replace('\n\n', '\n')
                    responses.append([file.split('.')[0], scores])
                    count += 1
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


def xlsx(model_info, path, limitation, saving):
    """
    将模型的评分结果进行格式重构，输出成xlsx文件
    """
    print(f"start to get score of model {model_info[0]}")
    results = score_report(path, model_info[1], limitation)
    for i in range(len(results)):
        result = results[i][1]
        # print(f"result {i}\n: {result}")
        final = []
        result = result.split('\n')
        for j in range(len(result)):
            col = 0
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
                col = j
                final.append(result[j].split('修改意见：')[1])
            elif j > col:
                final[-1] += result[j]
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
        score = result[1][0]
        sub_score_1 = result[1][1][0]
        sub_reason_1 = result[1][1][1]
        sub_score_2 = result[1][2][0]
        sub_reason_2 = result[1][2][1]
        sub_score_3 = result[1][3][0]
        sub_reason_3 = result[1][3][1]
        sub_score_4 = result[1][4][0]
        sub_reason_4 = result[1][4][1]
        sub_score_5 = result[1][5][0]
        sub_reason_5 = result[1][5][1]
        sub_score_6 = result[1][6][0]
        sub_reason_6 = result[1][6][1]
        if len(result[1]) > 7:
            suggest = result[1][7]
        else:
            suggest = ""
        ws.append([title, score, sub_score_1, sub_reason_1, sub_score_2, sub_reason_2, sub_score_3, sub_reason_3,
                   sub_score_4, sub_reason_4, sub_score_5, sub_reason_5, sub_score_6, sub_reason_6, suggest])
    wb.save(saving)


if __name__ == '__main__':
    # all_folders = ["2023本科论文", "2023组内毕设", "2024本科论文"]
    folder_list = ["2023本科论文"]
    for folder in folder_list:
        print(f"正在处理：{folder}")
        fileCount = 1
        input_path = rf"D:\Sustech\course\CS490_Graduation_Thesis\work\data-preprocessed\{folder}\txt"
        output_path = rf"D:\Sustech\course\CS490_Graduation_Thesis\work\results\{folder}"
        models = [
            ["ERNIE-Speed-128K", "ernie-speed-128k"],
        ]
        print("save txt file")
        for model in models:
            txt(model, input_path, fileCount, rf"{output_path}/{model[0]}")
        # print("save xlsx file")
        # for model in models:
        #     xlsx(model, input_path, fileCount, f"./result/only-without-22AI/{model[0]}.xlsx")
        print(f"处理完成：{folder}")
