import os
import time

from openai import OpenAI


def prepare_prompt(count, text, system_prompt, example_result):
    example_txt = []
    example_path_1 = r"D:\Sustech\course\CS490_Graduation_Thesis\work\data-preprocessed\2024本科论文\txt\12011507_黄宇海_毕设论文_中文_彩打.txt"
    with open(example_path_1, 'r', encoding='utf-8') as f:
        example_txt.append(f.read())
    example_path_2 = r"D:\Sustech\course\CS490_Graduation_Thesis\work\data-preprocessed\2024本科论文\txt\12011311_徐思创_毕设论文_中文_彩打.txt"
    with open(example_path_2, 'r', encoding='utf-8') as f:
        example_txt.append(f.read())
    example_path_3 = r"D:\Sustech\course\CS490_Graduation_Thesis\work\data-preprocessed\2024本科论文\txt\12010112_潘和伟_毕设论文_中文_彩打.txt"
    with open(example_path_3, 'r', encoding='utf-8') as f:
        example_txt.append(f.read())
    messages = [{
        'role': 'system',
        'content': system_prompt
    }]
    for i in range(count):
        messages.append({
            'role': 'user',
            'content': f'示例如下：\n'
                       f'以下报告：\n{example_txt[i]}'
                       f'打分结果：\n{example_result[i]}'
        })
    messages.append({
        'role': 'user',
        'content': f'请给以下论文打分：\n{text}'
    })
    # print(messages)
    return messages


def get_score(model_id, text, max_few_shot, system_prompt, example_result):
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
            messages=prepare_prompt(max_few_shot, text, system_prompt, example_result),
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


def score_report(path, model_detail, max_count, max_example, system_prompt, example_result):
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
                scores = get_score(model_detail, text, max_example, system_prompt, example_result)
                responses.append([file.split('_')[0], scores])
                time.sleep(30)
    print("finished looping")
    return responses


def txt(model_info, path, limitation, prompt_limit, saving, system_prompt, example_result):
    """
    将模型的评分结果进行格式重构，输出成txt文件
    """
    # print(f"start to get score of model {model_info[0]}")
    results = score_report(path, model_info[1], limitation, prompt_limit, system_prompt, example_result)
    for i in range(len(results)):
        file_name = results[i][0]
        file_content = results[i][1]
        if file_content is None:
            continue
        file_path = f'{saving}/{file_name}.txt'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(file_content)


if __name__ == '__main__':
    # system without all - Holistic-SD Prompting - 无任何提示语设计，只是规范输出
    system_withoutA = ('评估以下<毕业设计论文>。\n'
                       '只给出最终打分，而不返回任何其他多余结果，打分范围均为0-10分。\n'
                       '按照<打分模版>给出打分结果与评价，打分模板如下：\n'
                       '最终打分：<> (范围0-10分)\n'
                       '请严格按照以下格式返回结果，仅用返回一行最终打分结果：\n'
                       '最终打分：<> (范围0-10分)\n')
    # system holistic - Holistic-SLOWPR Prompting - 无多维度提示词的结构化解释，不给出不同维度的小分，直接给出最终打分
    system_holistic = ('你是一位大学教师教授，需要对学生提交的毕业设计论文进行评估。\n'
                       '请参考<结构完整性>，<逻辑清晰度>，<语言连贯性>，<内容独特性和创新性>，<参考文献规范性>，<课程知识掌握度>六个维度，评估以下<毕业设计论文>。\n'
                       '根据各指标表现，综合得出最终打分，打分范围均为0-10分。\n'
                       '按照<打分模版>给出打分结果与评价，打分模板如下：\n'
                       '最终打分：<> (范围0-10分)\n'
                       '修改意见：<>\n'
                       '请严格按照以下格式返回结果，最终打分一行、修改意见一行，不要擅自添加换行：\n'
                       '最终打分：<> (范围0-10分)\n'
                       '修改意见：<>\n')
    # system original(final) - SLOWPR LLM - 提示语设计最完整版本，角色设计+多维度指标+格式规范
    system_original = ('你是一位大学教师教授，需要对学生提交的毕业设计论文进行评估。\n'
                       '请参考<结构完整性>，<逻辑清晰度>，<语言连贯性>，<内容独特性和创新性>，<参考文献规范性>，<课程知识掌握度>六个维度，评估以下<毕业设计论文>。\n'
                       '根据各指标<占比比例>进行打分与点评，并综合得出最终打分，打分范围均为0-10分。\n'
                       '按照<打分模版>给出打分结果与评价，打分模板如下：\n'
                       '最终打分：<> (范围0-10分)\n'
                       '1. 结构完整性得分：<>，占比20%，原因如下：<>\n'
                       '2. 逻辑清晰度得分：<>，占比20%，原因如下：<>\n'
                       '3. 语言连贯性得分：<>，占比20%，原因如下：<>\n'
                       '4. 内容独特性和创新性得分：<>，占比20%，原因如下：<>\n'
                       '5. 参考文献规范性得分：<>，占比10%，原因如下：<>\n'
                       '6. 课程知识掌握度得分：<>，占比10%，原因如下：<>\n'
                       '修改意见：<>\n'
                       '请严格按照以下格式返回结果，最终打分一行、六个维度各自一行、修改意见一行，不要擅自添加换行：\n'
                       '最终打分：<> (范围0-10分)\n'
                       '1. 结构完整性得分：<>，占比20%，原因如下：<>\n'
                       '2. 逻辑清晰度得分：<>，占比20%，原因如下：<>\n'
                       '3. 语言连贯性得分：<>，占比20%，原因如下：<>\n'
                       '4. 内容独特性和创新性得分：<>，占比20%，原因如下：<>\n'
                       '5. 参考文献规范性得分：<>，占比10%，原因如下：<>\n'
                       '6. 课程知识掌握度得分：<>，占比10%，原因如下：<>\n'
                       '修改意见：<>\n')
    # system without role-play - w/o Role-Play - 无角色设计，只提出需求
    system_withoutR = ('请参考<结构完整性>，<逻辑清晰度>，<语言连贯性>，<内容独特性和创新性>，<参考文献规范性>，<课程知识掌握度>六个维度，评估以下<毕业设计论文>。\n'
                       '根据各指标<占比比例>进行打分与点评，并综合得出最终打分，打分范围均为0-10分。\n'
                       '按照<打分模版>给出打分结果与评价，打分模板如下：\n'
                       '最终打分：<> (范围0-10分)\n'
                       '1. 结构完整性得分：<>，占比20%，原因如下：<>\n'
                       '2. 逻辑清晰度得分：<>，占比20%，原因如下：<>\n'
                       '3. 语言连贯性得分：<>，占比20%，原因如下：<>\n'
                       '4. 内容独特性和创新性得分：<>，占比20%，原因如下：<>\n'
                       '5. 参考文献规范性得分：<>，占比10%，原因如下：<>\n'
                       '6. 课程知识掌握度得分：<>，占比10%，原因如下：<>\n'
                       '修改意见：<>\n'
                       '请严格按照以下格式返回结果，最终打分一行、六个维度各自一行、修改意见一行，不要擅自添加换行：\n'
                       '最终打分：<> (范围0-10分)\n'
                       '1. 结构完整性得分：<>，占比20%，原因如下：<>\n'
                       '2. 逻辑清晰度得分：<>，占比20%，原因如下：<>\n'
                       '3. 语言连贯性得分：<>，占比20%，原因如下：<>\n'
                       '4. 内容独特性和创新性得分：<>，占比20%，原因如下：<>\n'
                       '5. 参考文献规范性得分：<>，占比10%，原因如下：<>\n'
                       '6. 课程知识掌握度得分：<>，占比10%，原因如下：<>\n'
                       '修改意见：<>\n')
    example_result_holistic = [
        '最终打分：8.2 (范围0-10分)\n',
        '最终打分：8.3 (范围0-10分)\n',
        '最终打分：9 (范围0-10分)\n',
        '最终打分：8.4 (范围0-10分)\n',
        '最终打分：7.5 (范围0-10分)\n',
    ]
    example_result_original = [
        (
            '最终打分：8.2 (范围0-10分)\n'
            '1. 结构完整性得分：8, 占比20%\n'
            '2. 逻辑清晰度得分：8, 占比20%\n'
            '3. 语言连贯性得分：8, 占比20%\n'
            '4. 内容独特性和创新性得分：7.5, 占比20%\n'
            '5. 参考文献规范性得分：10, 占比10%\n'
            '6. 课程知识掌握度得分：9, 占比10%\n'
        ),
        (
            '最终打分：8.3 (范围0-10分)\n'
            '1. 结构完整性得分：8, 占比20%\n'
            '2. 逻辑清晰度得分：8, 占比20%\n'
            '3. 语言连贯性得分：7.5, 占比20%\n'
            '4. 内容独特性和创新性得分：9, 占比20%\n'
            '5. 参考文献规范性得分：9, 占比10%\n'
            '6. 课程知识掌握度得分：9, 占比10%\n'
        ),
        (
            '最终打分：9 (范围0-10分)\n'
            '1. 结构完整性得分：8, 占比20%\n'
            '2. 逻辑清晰度得分：9, 占比20%\n'
            '3. 语言连贯性得分：9, 占比20%\n'
            '4. 内容独特性和创新性得分：9, 占比20%\n'
            '5. 参考文献规范性得分：10, 占比10%\n'
            '6. 课程知识掌握度得分：10, 占比10%\n'
        ),
        (
            '最终打分：8.4 (范围0-10分)\n'
            '1. 结构完整性得分：8, 占比20%\n'
            '2. 逻辑清晰度得分：8, 占比20%\n'
            '3. 语言连贯性得分：8, 占比20%\n'
            '4. 内容独特性和创新性得分：9, 占比20%\n'
            '5. 参考文献规范性得分：9, 占比10%\n'
            '6. 课程知识掌握度得分：9, 占比10%\n'
        ),
        (
            '最终打分：7.5 (范围0-10分)\n'
            '1. 结构完整性得分：7, 占比20%\n'
            '2. 逻辑清晰度得分：8, 占比20%\n'
            '3. 语言连贯性得分：8, 占比20%\n'
            '4. 内容独特性和创新性得分：7, 占比20%\n'
            '5. 参考文献规范性得分：7, 占比10%\n'
            '6. 课程知识掌握度得分：8, 占比10%\n'
        ),
    ]
    folder_list = [
        "all",
        # "2023本科论文",
        # "2023组内毕设",
        # "2024本科论文",
    ]
    models = [
        # 通义 - 文本生成
        ["通义千问-Plus", "qwen-plus"],
        ["通义千问2.5-14B-1M", "qwen2.5-14b-instruct-1m"],
        ["通义千问-Turbo", "qwen-turbo"],
        ["通义千问-Turbo-Latest", "qwen-turbo-latest"],
        # DeepSeek - 文本生成
        ["DeepSeek-V3", "deepseek-v3"],
        # DeepSeek - 推理模型
        ["DeepSeek-R1", "deepseek-r1"],
    ]
    systems = [
        # [system_type, system_content, few-shot_example_list, few-shot_times_list]
        # ['system-w-o-alls', system_withoutA, example_result_original, [0]],
        ['system-holistic', system_holistic, example_result_holistic, [
            # 0, 1, 2,
            3]],
        ['system-original', system_original, example_result_original, [0, 1, 2, 3]],
        ['system-w-o-role', system_withoutR, example_result_original, [2]],
    ]
    # the num of files would be scored
    fileCount = 100
    # repeat times
    min_times = 0
    max_times = 1
    for folder in folder_list:
        print(f"due withdue with folder：{folder}")
        input_path = rf"../../data-preprocessed/{folder}/txt"
        output_path = rf"../../results/aliyunbailian"
        for system in systems:
            print(f"due with system: {system[0]}")
            few_shot_times_list = system[3]
            for few_shot_times in few_shot_times_list:
                print(f"due with few-shot: {few_shot_times}")
                for times in range(min_times, max_times):
                    print(f"due with times: {times}")
                    for model in models:
                        print(f"due with model: {model[0]}")
                        saving_path = rf"{output_path}/{model[0]}/{folder}_{system[0]}_few-shot-{few_shot_times}"
                        saving_path = saving_path + (f"_{times}" if times > 0 else "")
                        txt(model, input_path, fileCount, few_shot_times, saving_path, system[1], system[2])
        print(f"处理完成：{folder}")
