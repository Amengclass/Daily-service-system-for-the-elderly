# -*- coding: utf-8 -*-
from flask import Flask, render_template, Response, jsonify, request, redirect, session, url_for, send_from_directory
import requests
import cv2
import mediapipe as mp
import time
import os

# 音乐文件目录
MUSIC_DIRECTORY = os.path.join(os.getcwd(), 'static', 'music')

# 假设的用户登录数据
users = {
    'xwy': {'password': 'xwy', 'name': '向维茵'},
    'zxb': {'password': 'zxb', 'name': '郑兴邦'},
    'ny': {'password': 'ny', 'name': '农苑'},
    'zyj': {'password': 'zyj', 'name': '张逸筠'},
    'xhf': {'password': 'xhf', 'name': '谢海峰'},
}

# 设置紧急联系人数据
emergency_contacts = {
    'xwy': [{'name': "谢海峰", "phone": "13877678416"}, {"name": "警察", "phone": "110"},
            {'name': "消防", "phone": "119"}, ],
    'zxb': [{'name': "谢海峰", "phone": "13877678416"}, {'name': "消防", "phone": "119"},
            {"name": "警察", "phone": "110"}],
    'ny': [{'name': "消防", "phone": "119"}, {"name": "警察", "phone": "110"}],
    'zyj': [{'name': "谢海峰", "phone": "13877678416"}, {"name": "警察", "phone": "110"}],
    'xhf': [{'name': "谢海峰", "phone": "13877678416"}, {"name": "中国移动", "phone": "10086"}],
    'user2': [{"name": "紧急联系人2", "phone": "987654321"}],
    # 添加更多紧急联系人...
}  # 列表里元素是字典，其中每个字典的值又是一个字典

# 设置您的 API 密钥
app_id = 'nqsilfmoroilwpoi'
app_secret = 'RFhwZFEzUWt5cUtBS01ZMDFhQkFwdz09'

"""
创建一个 Flask 应用程序实例，通常命名为 app。在这里，__name__ 是 Python 中的一个特殊变量，它表示当前模块的名称。
static_folder表示指定静态文件目录，这样才能引入css
"""
app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'
"""
    @app.route 是 Flask 框架中的一个装饰器，用于在 Python 中声明一个视图函数，
并将其与一个 URL 路由绑定起来。当用户访问这个 URL 时，Flask 会调用相应的视图函数来处理请求。
"""


@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


# -------------------------------------聊天机器人模块开始----------------------------------------------聊天机器人
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

#用户创建了新聊天，所以要请客历史维护记录
@app.route('/clear_messages', methods=['POST'])
def clear_messages():
    global messages
    messages = []  # 清空消息列表
    return jsonify({'message': 'Messages cleared successfully'})
# ------------------------------------------------聊天机器人模块结束----------------------------------------------

# -----------------------------------------------------音乐模块开始------------------------------------------
@app.route('/music')
def music():
    return render_template('music.html')


def get_song_list():
    songs = []
    for filename in os.listdir(MUSIC_DIRECTORY):
        if filename.endswith('.mp3'):
            songs.append(filename)
    return songs


# 获取音乐文件路径
def get_song_path(song_name):
    return os.path.join(MUSIC_DIRECTORY, song_name)


# 获取音乐文件
@app.route('/play_song')
def play_song():
    song_name = request.args.get('song')
    # song_path = get_song_path(song_name)
    return send_from_directory(MUSIC_DIRECTORY, song_name)


# 获取音乐列表
@app.route('/get_songs')
def get_songs():
    songs = get_song_list()
    return jsonify({'songs': songs})


# ----------------------------------------------------音乐模块结束--------------------------------------------


# ----------------------------------------------------视频模块开始--------------------------------------------
@app.route('/video1')
def video1():
    return render_template('video1.html')


# @app.route('/video2')
# def video1():
#     return render_template('video2.html')
# ----------------------------------------------------视频模块结束--------------------------------------------


# -------------------------------------------------张逸筠专属代码开始--------------------------------------------
@app.route('/zyj')  # 设置主页目录
@app.route('/welcome/zyj')  # 设置主页目录
def ztj():
    return render_template('zyj.html')


@app.route('/come')  # 张逸筠的引导页
@app.route('/come/<user_id>')
def come(user_id=None):
    return render_template('come.html', user_id=user_id)


# -------------------------------------------------张逸筠专属代码结束--------------------------------------------


@app.route('/sign_up', methods=['POST'])  # 注册处理
def sign_up():
    # 声明全局变量
    global emergency_contacts
    print("进来了sign_up")
    data = request.json
    print("前端发来的注册数据:", end=' ')
    print(data)
    # 从 JSON 数据中获取注册的用户名和密码
    user_id = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if user_id in users:  # 如果用户名已存在，则返回错误信息
        return jsonify({'user_id': user_id, 'status': "sign up failed"})
    else:
        # users是一个字典，添加新字典键值对直接添加即可
        users[user_id] = {'password': password, 'email': email}
        session[user_id] = True
        print(users)
        return jsonify({'user_id': user_id, 'status': "sign up success"})


@app.route('/sign_in', methods=['POST'])  # 登录处理
def sign_in():
    # 声明全局变量
    global emergency_contacts
    data = request.json
    user_id = data.get('username')
    password = data.get('password')
    user_type = data.get('type')  # 只有游客有,正常用户都是返回None

    # 判断账号密码是否正确
    if user_id in users and users[user_id]['password'] == password:
        session[user_id] = True
        return jsonify({'user_id': user_id, 'status': "sign in success"})
    else:
        # 如果是新游客，注册并记录会话
        if user_type == 'guest':
            users[user_id] = {'password': password}
            session[user_id] = True  # 标记用户登录信息
            emergency_contacts[user_id] = [{'name': "谢海峰", "phone": "13877678416"}]  # 给每个游客添加一个紧急联系人
            return jsonify({'user_id': user_id, 'status': "sign in success"})
        # 如果不是游客
        return jsonify({'user_id': user_id, 'status': "Wrong password"})


@app.route('/protected')  # 受保护的界面，验证登录状态
@app.route('/protected/<user_id>')
def protected(user_id=None):
    print("进来了protect")
    print("当前的user：", users)
    if user_id is None or user_id not in session:
        return redirect(url_for('login'))
    return render_template('index.html', user_id=user_id)


@app.route('/index')  # 设置主页目录
@app.route('/index/<user_id>')  # 设置主页目录
def index(user_id=None):
    return render_template('index.html', user_id=user_id)


@app.route('/help')  # 设置一键帮助
@app.route('/help/<user_id>')
def help(user_id=None):
    return render_template('help.html', user_id=user_id)
    # if user_id is None or user_id not in session:
    #     return redirect(url_for('login'))
    # return render_template('help.html')


@app.route('/404')  # 设置404
def fail():
    return render_template('404.html')


@app.route('/help/fall_detection')  # /一键帮助/摔倒检测
@app.route('/help/fall_detection/<user_id>')  # /一键帮助/摔倒检测
def fall_detection(user_id=None):
    return render_template('help/fall_detection.html')


@app.route('/help/fall_detection/recognition')  # 一键帮助/摔倒检测/识别
@app.route('/help/fall_detection/recognition/<user_id>')  # 一键帮助/摔倒检测/识别
def recognition(user_id=None):
    return render_template('help/recognition.html')


# 一键帮助/摔倒检测/识别
@app.route('/help/set_emergency')
@app.route('/help/set_emergency/<user_id>')
def set_emergency(user_id=None):
    print("进来了emergency")
    if user_id is not None and user_id in session:
        return render_template('help/set_emergency.html', user_id=user_id)
    else:
        return redirect(url_for('login'))


@app.route('/help/get_emergency', methods=['GET'])  # 摔倒识别
@app.route('/help/get_emergency/<user_id>', methods=['GET'])
def get_emergency(user_id):
    # 声明全局变量
    global emergency_contacts
    print("进来了get_emergency")
    if user_id in emergency_contacts:
        return jsonify(
            {'user_id': user_id, 'status': "success", "data": emergency_contacts[user_id]})  # 返回的contacts是一个紧急联系人列表
    else:
        return jsonify({'status': "未找到联系人列表", "data": []})


@app.route('/help/add_emergency/<user_id>', methods=['POST'])
def add_emergency(user_id=None):
    # 声明全局变量
    global emergency_contacts

    print("进来了save_emergency")
    print(emergency_contacts.get(user_id))

    # 检查用户是否已登录
    if user_id is not None and session.get(user_id):
        # 获取表单数据，提供默认值以避免 KeyError
        name = request.form.get('name', '')
        phone = request.form.get('phone', '')
        print(name, phone)

        # 检查已经紧急联系人的姓名
        names = [contact["name"] for contact in emergency_contacts.setdefault(user_id, [])]
        try:
            # 检查是否已经设置过该紧急联系人
            if name and phone:
                if name not in names:
                    # 如果姓名不存在，则将联系人添加到紧急联系人列表中
                    emergency_contacts[user_id].append({"name": name, "phone": phone})
                    print("紧急联系人已添加")
                    print(emergency_contacts[user_id])
                    return jsonify({'user_id': user_id, 'status': "添加成功", "data": emergency_contacts[user_id]})
                else:
                    return jsonify({'status': "联系人已存在"})
            else:
                return jsonify({'status': "姓名和电话不能为空"})
        except KeyError:
            return jsonify({'status': "KeyError: 用户ID不存在"})
    else:
        return jsonify({'status': "未登录"})


@app.route('/help/delete_emergency', methods=['POST'])  # 设置紧急联系人
@app.route('/help/delete_emergency/<user_id>', methods=['POST'])
def delete_emergency(user_id=None):
    # 声明全局变量
    global emergency_contacts
    print("后端:进来了delete_emergency")
    print(user_id)
    name = request.form.get('name')  # 获取要删除的联系人的姓名
    if user_id is not None and user_id in session:
        if name is not None:
            # 查找要删除的联系人在紧急联系人列表中的索引
            print("要删除的联系人：")
            if emergency_contacts[user_id] is not None:
                for index, contact in enumerate(emergency_contacts[user_id]):
                    if contact["name"] == name:
                        # 找到对应的联系人并删除
                        del emergency_contacts[user_id][index]
                        return jsonify(
                            {'name': name, 'status': "删除成功", 'emergency_contacts': emergency_contacts[user_id]})
        return jsonify({'status': "找不到联系人", 'name': name, 'emergency_contacts': emergency_contacts[user_id]})
    return jsonify({'status': "未登录"})


@app.route('/help/call_for_help')
@app.route('/help/call_for_help/<user_id>')
def call(user_id=None):
    # 需要登录版本
    print("进来了call_for_help")
    # 如果用户未登录，则重定向到登录页面
    print(user_id)
    if user_id is None or user_id not in session:
        return redirect(url_for('login'))

    # 获取用户的紧急联系人列表，如果不存在则返回None
    user_contacts = emergency_contacts.get(user_id)

    # 如果用户存在紧急联系人列表
    if user_contacts:
        # 获取第一个紧急联系人的电话号码
        phone_number = user_contacts[0]["phone"]
        # 渲染呼叫帮助页面，并传递电话号码
        return render_template('help/call.html', phone_number=phone_number)
    else:
        # 如果用户没有设置紧急联系人，则跳转到设置紧急联系人页面
        return redirect(url_for('set_emergency', user_id=user_id))


@app.route('/help/sms_for_help')
@app.route('/help/sms_for_help/<user_id>')
def sms(user_id=None):
    print("进来了sms")  # 输出调试信息

    # 如果 user_id 为 None 或者不在 session 中，重定向到登录页面
    if user_id is None or user_id not in session:
        return redirect(url_for('login'))

    # 获取用户的紧急联系人列表
    user_emergency_contacts = emergency_contacts.get(user_id)  # 如果不存在这个键或者这个键没有值，则为None

    # 如果用户没有设置紧急联系人，重定向到设置紧急联系人页面
    if not user_emergency_contacts:
        return redirect(url_for('set_emergency', user_id=user_id))

    # 渲染模板并返回响应
    return render_template('help/sms.html', emergency_contacts=user_emergency_contacts)


# 姿势识别
@app.route('/video_feed')
@app.route('/video_feed/<user_id>')
def video_feed(user_id=None):
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def gen_frames():
    mpPose = mp.solutions.pose
    pose = mpPose.Pose()
    mpDraw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    pTime = 0

    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)

        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# 设置位置服务界面
@app.route('/location')
@app.route('/location/<user_id>')
def location(user_id=None):
    return render_template('location.html', user_id=user_id)


# ip位置信息查询
@app.route('/location/info', methods=['GET'])
@app.route('/location/info/<user_id>', methods=['GET'])
def location_info(user_id=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    ip = request.remote_addr
    url = f'https://whois.pconline.com.cn/ipJson.jsp?ip={ip}&json=true'
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        if data:
            return jsonify({'ip': data['ip'], 'city': data['city'], 'location': data['addr']})
    except Exception as e:
        print("Error:", e)
    return jsonify({'error': 'Failed to fetch location information.'})


# 天气查询
@app.route('/tools/weather/get_weather', methods=['POST'])
@app.route('/tools/weather/get_weather/<user_id>', methods=['POST'])
def get_weather(user_id=None):
    print("进来了")
    # 获取用户选择的省份和城市
    data = request.get_json()
    print(data)
    city = data['city']
    print(city)
    # 使用 requests 模块发送 API 请求
    response = requests.get(
        f'https://www.mxnzp.com/api/weather/current/{city}?app_id=nqsilfmoroilwpoi&app_secret=RFhwZFEzUWt5cUtBS01ZMDFhQkFwdz09')

    # 解析 JSON 响应
    if response.ok:
        weather_data = response.json()
        print(weather_data)
        return jsonify({'temperature': weather_data['data']['temp'], 'weather': weather_data['data']['weather'],
                        'city': city}), 200
    else:
        return jsonify({'error': 'Failed to get weather data'}), 500


@app.route('/health')  # 设置健康检测界面
@app.route('/health/<user_id>')  # 设置健康检测界面
def health(user_id=None):
    return render_template('health.html', user_id=user_id)


@app.route('/health/sleep')  # 设置健康检测界面
@app.route('/health/sleep/<user_id>')  # 设置健康检测界面
def sleep(user_id=None):
    return render_template('health/sleep.html')


@app.route('/tools')  # 设置智能工具界面
@app.route('/tools/<user_id>')  # 设置智能工具界面
def tools(user_id=None):
    return render_template('tools.html', user_id=user_id)


@app.route('/tools/weather')  # 设置智能工具界面
@app.route('/tools/weather/<user_id>')  # 设置智能工具界面
def weather(user_id=None):
    return render_template('tools/weather.html')


@app.route('/tools/Memo')  # 设置智能工具界面
@app.route('/tools/Memo/<user_id>')  # 设置智能工具界面
def Memo(user_id=None):
    return render_template('tools/Memorandum.html')


@app.route('/logout')  # 退出界面
@app.route('/logout/<user_id>')
def logout(user_id=None):
    session.pop(user_id, None)  # 删除存储在会话中的用户ID
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
