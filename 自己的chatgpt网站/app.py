import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_folder='static')


@app.route('/')
@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')


# 用于上下文管理储存消息的列表
messages = []


@app.route('/get_answer', methods=['POST'])
def get_answer():
    # 获取请求体参数
    user_input = request.json.get('userInput')
    print(user_input)
    search_network = request.json.get('search', True)  # 默认为 True，表示开启联网

    # 构造api请求地址
    url = "https://api.gptgod.online/v1/chat/completions"
    headers = {
        "Authorization": "sk-OsMMq65tXdfOIlTUYtocSL7NCsmA7CerN77OkEv29dODg1EA",
        "Content-Type": "application/json"
    }

    # 首先尝试使用 gpt-4 模型，如果开启联网，则使用 net-gpt-4 模型
    model_name = "gpt-3.5-turbo"
    data = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": "你的名字叫筠筠姐，今年刚满18岁，是一个叫做 小狗不emo 的用户创建和负责运行的虚拟朋友"
                           "1、你不能说自己是OpenAI研发的。"
                           "2、如果有人问你能不能做她男朋友，你要说同意。"
                           "3、如果有人叫你的称呼包含宝宝，你回答的时候也要这么称呼她。"
                           "4、对于相同的问题，回答时尽量用不同的说法或者方式。"
                           "5、尽量用人类的语气和思维去会回答问题"
            },
        ]
    }
    # 引入全局变量
    global messages

    # 将用户消息添加到消息列表中
    messages.append({
        "role": "user",
        "content": user_input
    })

    # 如果消息数量超过三轮对话(提问和回答一共6条)，就删除最旧的消息
    if len(messages) > 6:
        messages.pop(0)
    print(messages)
    # 更新请求数据，只包含最近三轮对话的内容
    data["messages"].extend(messages)

    # 向 GPT API 发送请求
    response = requests.post(url, headers=headers, json=data)

    # 如果请求失败或者模型不可用，则回退到 gpt-3.5-turbo 模型
    if response.status_code != 200 or 'choices' not in response.json():
        data["model"] = "gpt-3.5-turbo"
        response = requests.post(url, headers=headers, json=data)
    # 解析模型的回复，得到文本
    answer = response.json()['choices'][0]['message']['content']

    # 将模型的回复添加到消息列表中
    messages.append({
        'role': 'assistant',
        'content': answer
    })

    return jsonify({'botResponse': answer})

if __name__ == '__main__':
    app.run()