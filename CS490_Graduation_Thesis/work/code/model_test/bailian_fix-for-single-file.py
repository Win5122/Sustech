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
    example_path_4 = r"D:\Sustech\course\CS490_Graduation_Thesis\work\data-preprocessed\2024本科论文\txt\12011916_黄德赐_毕设论文_中文_彩打.txt"
    with open(example_path_4, 'r', encoding='utf-8') as f:
        example_txt.append(f.read())
    example_path_5 = r"D:\Sustech\course\CS490_Graduation_Thesis\work\data-preprocessed\2024本科论文\txt\12012004_周兴雨_毕设论文_中文_彩打.txt"
    with open(example_path_5, 'r', encoding='utf-8') as f:
        example_txt.append(f.read())
    messages = [{
        'role': 'system',
        'content': system_prompt
    }]
    for i in range(count):
        messages.append({
            'role': 'user',
            'content': f'示例如下：\n'
                       f'以下报告:\n{example_txt[i]}'
                       f'打分结果：\n{example_result[i]}'
        })
    messages.append({
        'role': 'user',
        'content': f'请给以下报告打分:\n{text}'
    })
    return messages


def get_score(model_id, text, few_shot_count, system_prompt, example_result):
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
            messages=prepare_prompt(few_shot_count, text, system_prompt, example_result),
        )
        results = completion.choices[0].message.content
        # print(results)
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


def score_report(path, model_detail, few_shot_count, system_prompt, example_result):
    """
    给报告打分，遍历文件夹，读取报告内容，输给模型进行评分
    """
    responses = []
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

        # get the score from model
        scores = get_score(model_detail, text, few_shot_count, system_prompt, example_result)
        responses.append([path.split('.txt')[0].split('/')[-1], scores])
    # print("finished looping")
    return responses


def txt(model_info, path, few_shot_count, system_prompt, example_result):
    """
    将模型的评分结果进行格式重构，输出成txt文件
    """
    # print(f"start to get score of model {model_info[0]}")
    results = score_report(path, model_info[1], few_shot_count, system_prompt, example_result)
    for i in range(len(results)):
        file_content = results[i][1]


if __name__ == '__main__':
    system_original = ('你是一位大学教师教授，需要对学生提交的毕业设计论文进行评估。\n'
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
                       '修改意见：<>\n')
    system_Holistic = ('你是一位大学教师教授，需要对学生提交的毕业设计论文进行评估。\n'
                       '请评估以下<报告文本/总结报告文本>在描述<结构完整性>，<逻辑清晰度>， <语言连贯性>， <内容独特性和创新性>， <参考文献规范性>，<课程知识掌握度>方面的表现，'
                       '参考上述各个指标，综合六个维度给出最终分数。并最终按照<打分模版>给出学生报告打分结果与评价”。打分模板如下：\n'
                       '最终打分：<> (范围0-10分)\n'
                       '修改意见：<>\n'
                       '请严格按照以下格式返回结果，最终打分一行、修改意见一行，不要擅自添加换行：\n'
                       '最终打分：<> (范围0-10分)\n'
                       '修改意见：<>\n')
    system_withoutR = ('请评估以下<报告文本/总结报告文本>在描述<结构完整性>，<逻辑清晰度>， <语言连贯性>， <内容独特性和创新性>， <参考文献规范性>，<课程知识掌握度>方面的表现，'
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
                       '修改意见：<>\n')
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
    example_result_Holistic = [
        '最终打分：8.2 (范围0-10分)\n',
        '最终打分：8.3 (范围0-10分)\n',
        '最终打分：9 (范围0-10分)\n',
        '最终打分：8.4 (范围0-10分)\n',
        '最终打分：7.5 (范围0-10分)\n',
    ]
    models = [
        # 通义 - 文本生成
        # ["通义千问-Plus", "qwen-plus"],
        # ["通义千问2.5-14B-1M", "qwen2.5-14b-instruct-1m"],
        ["通义千问-Turbo", "qwen-turbo"],
        # DeepSeek - 文本生成
        # ["DeepSeek-V3", "deepseek-v3"],
        # DeepSeek - 推理模型
        # ["DeepSeek-R1", "deepseek-r1"],
    ]
    systems = [
        # ['system-original', system_original, example_result_original],
        # ['system-holistic', system_Holistic, example_result_Holistic],
        ['system-w-o-role', system_withoutR, example_result_original],
    ]
    file_name_list = [
        '11910233_陈晓珊_基于多任务的糖尿病视网膜病变识别算法',
        '11910311_周一凡_基于虹膜OCT图像全局与局部分割框架的研究',
        '11911108_魏一磊_毕设论文_中文',
        '11911425_李怀武_基于ChatGPT的语音聊天机器人',
        '11912732_马子晗_基于语义标签图的手术场景图像生成',
        '11912913_王一帆_毕设论文_中文',
        '12010112_潘和伟_毕设论文_中文_彩打',
        '12010513_刘向荣_毕设论文_中文_彩打',
        '12010923_徐剑_毕设论文_中_黑打',
        '12011407_李博翱_毕设论文_中文_彩打',
        '12011507_黄宇海_毕设论文_中文_彩打',
        '12011916_黄德赐_毕设论文_中文_彩打',
        '12012530_张力宇_毕设论文_英语_彩打',
        '12012921_夏祎杨_毕业论文_中文_彩打',
    ]
    few_shot_count = 3
    print(f"{few_shot_count}-shot")
    for model in models:
        print(f"model: {model[0]}")
        for system in systems:
            print(f"system: {system[0]}")
            for file_name in file_name_list:
                print(f"fix for report: {file_name}")
                input_path = rf"../../data-preprocessed/all/txt/{file_name}.txt"
                txt(model, input_path, few_shot_count, system[1], system[2])
                print(f"处理完成")
                time.sleep(50)
