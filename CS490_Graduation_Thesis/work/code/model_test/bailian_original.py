import os
import time

from openai import OpenAI


def get_score(model_id, text):
    try:
        # get the score from model
        client = OpenAI(
            # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
            api_key="sk-5a5fa75d2a74454284667c9aea226258",
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

        completion = client.chat.completions.create(
            # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            model=model_id,
            messages=[
                {
                    'role': 'system',
                    'content': '你是一位大学教师教授，需要对学生提交的毕业设计论文进行评估。\n'
                               '请评估以下<报告文本/总结报告文本>在描述<结构完整性>，<逻辑清晰度>， <语言连贯性>， <内容独特性和创新性>， <参考文献规范性>，<课程知识掌握度>方面的表现，'
                               '并根据各指标<占比比例>进行打分与点评，打分范围0-10分。并最终按照<打分模版>给出学生报告打分结果与评价”。打分模板如下：\n'
                               '最终打分：<> (范围0-10分)\n'
                               '1. 结构完整性得分：<>, 占比20%，原因如下：<>\n'
                               '2. 逻辑清晰度得分：<>, 占比20%，原因如下：<>\n'
                               '3. 语言连贯性得分：<>, 占比20%，原因如下：<>\n'
                               '4. 内容独特性和创新性得分：<>, 占比20%，原因如下：<>\n'
                               '5. 参考文献规范性得分：<>, 占比10%，原因如下：<>\n'
                               '6. 课程知识掌握度得分：<>, 占比10%，原因如下：<>\n'
                               '修改意见：<>\n'
                               '请严格按照以下格式返回结果，最终打分一行、6个维度各自一行、修改意见一行，不要擅自添加换行：\n'
                               '最终打分：<> (范围0-10分)\n'
                               '1. 结构完整性得分：<>, 占比20%，原因如下：<>\n'
                               '2. 逻辑清晰度得分：<>, 占比20%，原因如下：<>\n'
                               '3. 语言连贯性得分：<>, 占比20%，原因如下：<>\n'
                               '4. 内容独特性和创新性得分：<>, 占比20%，原因如下：<>\n'
                               '5. 参考文献规范性得分：<>, 占比10%，原因如下：<>\n'
                               '6. 课程知识掌握度得分：<>, 占比10%，原因如下：<>\n'
                               '修改意见：<>\n'
                },
                {
                    'role': 'user',
                    'content': f'请给以下报告打分:\n{text}'
                }
            ],
        )
        results = completion.choices[0].message.content
        while results.count('\n') > 0:
            results = results.replace('\n', '')
        results = results.replace('1. 结构完整性得分', '\n1. 结构完整性得分')
        results = results.replace('2. 逻辑清晰度得分', '\n2. 逻辑清晰度得分')
        results = results.replace('3. 语言连贯性得分', '\n3. 语言连贯性得分')
        results = results.replace('4. 内容独特性和创', '\n4. 内容独特性和创')
        results = results.replace('5. 参考文献规范性', '\n5. 参考文献规范性')
        results = results.replace('6. 课程知识掌握度', '\n6. 课程知识掌握度')
        results = results.replace('修改意见：', '\n修改意见：')
        print(results)
        return results
    except Exception as e:
        print(f"错误信息：{e}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")


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
                print(f"the report {count}")
                count += 1
                # if count != 55:
                #     print("skip")
                #     continue

                # get all the text
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()

                # get the score from model
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
    folder_list = [
        "all",
        # "2023本科论文",
        # "2023组内毕设",
        # "2024本科论文",
    ]
    for folder in folder_list:
        print(f"正在处理：{folder}")
        fileCount = 500
        input_path = rf"D:\Sustech\course\CS490_Graduation_Thesis\work\data-preprocessed\{folder}\txt"
        output_path = rf"D:\Sustech\course\CS490_Graduation_Thesis\work\results\aliyunbailian"
        models = [
            # 通义 - 文本生成
            ["通义千问-Plus", "qwen-plus"],
            ["通义千问2.5-14B-1M", "qwen2.5-14b-instruct-1m"],
            ["通义千问-Turbo", "qwen-turbo"],
            # DeepSeek - 文本生成
            ["DeepSeek-V3", "deepseek-v3"],
            # DeepSeek - 推理模型
            ["DeepSeek-R1", "deepseek-r1"],
        ]
        print("save txt file")
        for model in models:
            txt(model, input_path, fileCount, rf"{output_path}/{model[0]}/{folder}")
        print(f"处理完成：{folder}")
