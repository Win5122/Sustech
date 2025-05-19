from openai import OpenAI


def prepare_prompt(count, text):
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
    example_result = [
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
    messages = [{
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
    print(len(str(messages)))
    return messages


def get_score(model_id, text, few_shot_count):
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
            messages=prepare_prompt(few_shot_count, text),
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


def score_report(path, model_detail, few_shot_count):
    """
    给报告打分，遍历文件夹，读取报告内容，输给模型进行评分
    """
    responses = []
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

        # get the score from model
        scores = get_score(model_detail, text, few_shot_count)
        responses.append([path.split('.')[0].split('\\')[1], scores])
    print("finished looping")
    return responses


def txt(model_info, path, few_shot_count):
    """
    将模型的评分结果进行格式重构，输出成txt文件
    """
    print(f"start to get score of model {model_info[0]}")
    results = score_report(path, model_info[1], few_shot_count)
    for i in range(len(results)):
        file_content = results[i][1]


if __name__ == '__main__':
    few_shot_count = 4
    input_path = rf"D:\Sustech\course\CS490_Graduation_Thesis\work\data-preprocessed\all\txt\11911839_聂雨荷_毕设论文_中文.txt"
    models = [
        # 通义 - 文本生成
        # ["通义千问-Plus", "qwen-plus"],
        # ["通义千问2.5-14B-1M", "qwen2.5-14b-instruct-1m"],
        # ["通义千问-Turbo", "qwen-turbo"],
        # DeepSeek - 文本生成
        ["DeepSeek-V3", "deepseek-v3"],
        # DeepSeek - 推理模型
        # ["DeepSeek-R1", "deepseek-r1"],
    ]
    print(f"fix for report: {input_path}")
    for model in models:
        txt(model, input_path, few_shot_count)
    print(f"处理完成")
