import os
import openai
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
# Set your OpenAI API key
import requests
import json

API_KEY = "1iTcOnGE0Q3bDtwofwxN5wPm"
SECRET_KEY = "D9ueDfoBw2Ql4mLyOTNCnUQDxc66FV5M"


def get_score(text):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-3.5-128k?access_token=" + get_access_token()

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": f"请给以下报告打分:\n\n{text}"
            }
        ],
        "system": "你是一位教授人工智能导论课程的大学教师，需要对学生提交的课程项目报告进行评估。"
                  "请评估以下<报告文本/总结报告文本>在描述<结构完整性>，<逻辑清晰度>， <语言连贯性>， <内容独特性和创新性>， <参考文献规范性>，<课程知识掌握度>方面的表现，"
                  "并根据各指标<占比比例>进行打分与点评，打分范围0-10分。并最终按照<打分模版>给出学生报告打分结果与评价”。打分模板如下：“最终打分：<> (范围0-10分)"
                  "1. 结构完整性得分：<>, 占比20%，原因如下：<>"
                  "2. 逻辑清晰度得分：<>, 占比20%，原因如下：<>"
                  "3. 语言连贯性得分：<>, 占比20%，原因如下：<>"
                  "4. 内容独特性和创新性得分：<>, 占比20%，原因如下：<>"
                  "5. 参考文献规范性得分：<>, 占比10%，原因如下：<>"
                  "6. 课程知识掌握度得分：<>, 占比10%，原因如下：<>”"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    result = 'None'
    if 'result' in json.loads(response.text).keys():
        result = json.loads(response.text)['result']
        print(result)
    return result


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


def process_reports(root_path):
    """Process all text reports and score them using GPT."""
    extract_report_dir = os.path.join(root_path, "extract_report")
    result_csv_path = os.path.join(root_path, "result_wenxin.csv")
    # original_scores_csv_path = os.path.join(root_path, "original_report", "original_report.csv")

    # Load original scores
    # original_scores_df = pd.read_csv(original_scores_csv_path,encoding='gbk')

    # Prepare a list to hold the results
    results = []

    # Process each .txt file in the extract_report directory
    for txt_file in os.listdir(extract_report_dir):
        if txt_file.endswith(".txt"):
            file_path = os.path.join(extract_report_dir, txt_file)
            with open(file_path, 'r', encoding='utf-8') as f:
                report_text = f.read()

            # Get the score from GPT
            gpt_score = get_score(report_text)

            if gpt_score is not None:
                # Process filename: split by underscore and take the third part
                processed_filename = txt_file.split('_')[2].split('.')[0]

                # Append the result to the list
                results.append({"filename": processed_filename, "return": gpt_score})

    # Create a DataFrame for the results and save to CSV
    results_df = pd.DataFrame(results)
    results_df.to_csv(result_csv_path, index=False)


# Example usage
if __name__ == '__main__':
    root_path = "C:\\Users\\Administrator\\Desktop\\22CS103报告文件"  # Replace with your actual root path
    # mae, mse = process_reports(root_path)
    process_reports(root_path)
