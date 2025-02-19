# Set your OpenAI API key
import json
import requests
# Form the API
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# keys for access token
# model-1
# API_KEY = "1iTcOnGE0Q3bDtwofwxN5wPm"
# SECRET_KEY = "D9ueDfoBw2Ql4mLyOTNCnUQDxc66FV5M"
# model-2 (Yi-34B)
API_KEY = "l7vdl0rbH5w1WpyHF8Grw3gH"
SECRET_KEY = "hAS97OJVwEzOID8yIr2anBcvdeRC0zzA"

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


# Scoring Part
def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    print("getting access token")
    # Set up the request to get an access token
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    print("getting access token success")
    return str(requests.post(url, params=params).json().get("access_token"))


def get_score(text):
    print("getting score")
    # Set up the API request
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-3.5-128k?access_token=" + get_access_token()
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": f"请给以下报告打分:\n\n{text}"
            },
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
    print(response.text)
    # Parse the response
    result = 'None'
    if 'result' in json.loads(response.text).keys():
        result = json.loads(response.text)['result']
        print(result)
    print("getting score success")
    return result


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
    gpt_score = get_score(inputs)
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
