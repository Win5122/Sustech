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
                    'role': 'user',
                    'content': (
                        f'请给以下报告打分:\n{text}'
                        '范围0-10分，给出具体得分，并在返回结果第一行单独一行表明总分\n'
                        '第一行总分格式具体格式如下：最终打分：<> (范围0-10分)\n'
                    )
                },
            ],
        )
        results = completion.choices[0].message.content
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
    output_path = rf"D:\Sustech\course\CS490_Graduation_Thesis\work\results\aliyunbailian"
    folder_list = [
        "all",
        # "2023本科论文",
        # "2023组内毕设",
        # "2024本科论文",
    ]
    models = [
        # 通义 - 文本生成
        # ["通义千问-Plus", "qwen-plus"],
        ["通义千问2.5-14B-1M", "qwen2.5-14b-instruct-1m"],
        ["通义千问-Turbo", "qwen-turbo"],
        ["通义千问-Turbo-Latest", "qwen-turbo-latest"],
        # DeepSeek - 文本生成
        # ["DeepSeek-V3", "deepseek-v3"],
        # DeepSeek - 推理模型
        # ["DeepSeek-R1", "deepseek-r1"],
    ]
    min_times = 0
    max_times = 5
    for folder in folder_list:
        print(f"正在处理：{folder}")
        fileCount = 100
        input_path = rf"D:\Sustech\course\CS490_Graduation_Thesis\work\data-preprocessed\{folder}\txt"
        for model in models:
            print(f"正在处理：{model[0]}")
            for times in range(min_times, max_times):
                if max_times > 1:
                    print(f"正在处理：{times + 1}")
                saving_path = rf"{output_path}/{model[0]}/{folder}_without-system"
                saving_path = saving_path + (f"_{times + 1}" if max_times > 1 else "")
                txt(model, input_path, fileCount, saving_path)
        print(f"处理完成：{folder}")
