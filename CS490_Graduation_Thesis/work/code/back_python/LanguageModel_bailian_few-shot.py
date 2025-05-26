# Form the API
import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel

# other pre-defined variables
contents = None


class Report(BaseModel):
    text: str


# build API
app = FastAPI()

# set CORS
origins = [
    "http://localhost:5173",  # your frontend address
    "http://127.0.0.1:3000",  # additional address
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # the list of origins that are allowed to make requests
    allow_credentials=True,
    allow_methods=["*"],  # the list of HTTP methods that are allowed
    allow_headers=["*"],  # the list of HTTP headers that are allowed
)


def prepare_prompt(count, text):
    example_txt = []
    example_path_1 = f"../../data-preprocessed/2024本科论文/txt/12011507_黄宇海_毕设论文_中文_彩打.txt"
    with open(example_path_1, 'r', encoding='utf-8') as f:
        example_txt.append(f.read())
    example_path_2 = f"../../data-preprocessed/2024本科论文/txt/12011311_徐思创_毕设论文_中文_彩打.txt"
    with open(example_path_2, 'r', encoding='utf-8') as f:
        example_txt.append(f.read())
    example_path_3 = f"../../data-preprocessed/2024本科论文/txt/12010112_潘和伟_毕设论文_中文_彩打.txt"
    with open(example_path_3, 'r', encoding='utf-8') as f:
        example_txt.append(f.read())
    example_path_4 = f"../../data-preprocessed/2024本科论文/txt/12011916_黄德赐_毕设论文_中文_彩打.txt"
    with open(example_path_4, 'r', encoding='utf-8') as f:
        example_txt.append(f.read())
    example_path_5 = f"../../data-preprocessed/2024本科论文/txt/12012004_周兴雨_毕设论文_中文_彩打.txt"
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
    print(messages)
    return messages


def get_score(model_id, text, max_few_shot):
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
            messages=prepare_prompt(max_few_shot, text),
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


@app.post("/Committing/")
async def score_report(report: Report):
    print("receive the request: Committing")
    texts = report.text
    if not texts and not contents:
        return {"error": "Please upload the report first"}
    print(texts)
    print(contents)
    # fake result
    gpt_score = ("最终打分：5.3 (范围0-10分)" + "\n" +
                 "1. 结构完整性得分：6, 占比20%，原因如下：报告虽然标题为“这是一篇报告”，但缺乏明确的引言、正文、结论等结构部分，导致整体结构不够完整。" + "\n" +
                 "2. 逻辑清晰度得分：4, 占比20%，原因如下：由于报告内容过于简略，缺乏详细的论述和逻辑连接词，使得整体逻辑不够清晰，难以把握作者的思路和观点。" + "\n" +
                 "3. 语言连贯性得分：5, 占比20%，原因如下：虽然报告语言简洁，但由于内容不足，导致句子之间缺乏必要的过渡和联系，使得整体语言连贯性受到影响。" + "\n" +
                 "4. 内容独特性和创新性得分：3, 占比20%，原因如下：报告内容过于泛泛，缺乏独特的见解和创新性的思考，未能体现出作者对人工智能导论课程相关内容的深入理解。" + "\n" +
                 "5. 参考文献规范性得分：0, 占比10%，原因如下：报告未提供任何参考文献，无法评估其引用的规范性和准确性。" + "\n" +
                 "6. 课程知识掌握度得分：5, 占比10%，原因如下：从报告内容来看，作者对人工智能导论课程的基础知识有一定的了解，但缺乏深入的分析和应用。" + "\n" +
                 "修改意见：建议作者增加报告的详细内容和结构，明确引言、正文、结论等部分，并在论述中注重逻辑连接和过渡。同时，应增加对人工智能导论课程相关内容的深入分析和应用，展现独特的见解和创新性的思考。")
    # real result
    if not texts:
        inputs = contents
    elif not contents:
        inputs = texts
    else:
        inputs = "还没想好，哭了"
    gpt_score = get_score("deepseek-r1", texts, 3)
    print("finish scoring")
    return {"return": gpt_score}


# Uploading Part
@app.post("/Uploading/")
async def update_report(file: UploadFile):
    global contents
    print("receive the request: Uploading")
    contents = await file.read()
    try:
        with open(f"uploaded_files/{file.filename}", "wb") as f:
            f.write(contents)
        print("finish Uploading successful")
        return {"return": "success"}
    except Exception as e:
        print("finish uploading failed")
        return {"error": str(e)}


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
