# -*- coding: utf-8 -*-
from flask import Flask, render_template, Response, jsonify, request, redirect, session, url_for
import requests
import cv2
import mediapipe as mp
import time

# 假设的用户登录数据
users = {
    'user1': {'password': '123456', 'name': '谢海峰'},
    'user2': {'password': 'password2', 'name': 'User Two'}
}

# 设置紧急联系人数据
emergency_contacts = {
    'user1': [{'name': "谢海峰", "phone": "13877678416"}, {"name": "中国移动", "phone": "10086"}],
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


@app.route('/sign_up', methods=['POST'])  # 注册处理
def sign_up():
    print("进来了sign_up")
    data = request.json
    print("前端发来的注册数据:", end=' ')
    print(data)
    # 从 JSON 数据中获取用户名和密码
    user_id = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if user_id in users:
        return jsonify({'user_id': user_id, 'status': "sign up success"})
    else:
        users[user_id] = {'password': password, 'email': email}
        session[user_id] = True
        print(users)
        return jsonify({'user_id': user_id, 'status': "sign up success"})


@app.route('/sign_in', methods=['POST'])  # 登录处理
def sign_in():
    data = request.json
    user_id = data.get('username')
    password = data.get('password')
    user_type = data.get('type')

    # 判断账号密码是否正确
    if user_id in users and users[user_id]['password'] == password:
        session[user_id] = True
        return jsonify({'user_id': user_id, 'status': "sign in success"})
    else:
        # 如果是新游客，注册并记录会话，然后登录
        if user_type == 'guest':
            users[user_id] = {'password': password}
            session[user_id] = True
            return jsonify({'user_id': user_id, 'status': "sign in success"})
        # 如果不是游客，直接登录
        return jsonify({'user_id': user_id, 'status': "sign in failed"})


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


@app.route('/zyj')  # 设置主页目录
def ztj():
    return render_template('zyj.html')


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
    print("进来了get_emergency")
    if user_id in emergency_contacts:
        contacts = emergency_contacts[user_id]
        print(contacts)
        return contacts
    else:
        return "未找到紧急联系人列表"


@app.route('/help/save_emergency', methods=['POST'])  # 设置紧急联系人
@app.route('/help/save_emergency/<user_id>', methods=['POST'])
def add_emergency(user_id=None):
    print("进来了save_emergency")
    print(user_id)
    if user_id is not None and user_id in session:
        name = request.form['name']
        phone = request.form['phone']
        # 检查联系人是否已存在
        contacts = emergency_contacts.setdefault(user_id, [])
        names = [contact["name"] for contact in contacts]
        if name not in names:
            # 如果姓名不存在，则将联系人添加到紧急联系人列表中
            contacts.append({"name": name, "phone": phone})
            print("紧急联系人已添加")
            print(emergency_contacts)
            return "添加成功"
        return "相同姓名的联系人已存在"
    return "未登录"


@app.route('/help/delete_emergency', methods=['POST'])  # 设置紧急联系人
@app.route('/help/delete_emergency/<user_id>', methods=['POST'])
def delete_emergency(user_id=None):
    print("进来了delete_emergency")
    print(user_id)
    if user_id is not None and user_id in session:
        name = request.form.get('name')  # 获取要删除的联系人的姓名
        print(name)
        if name is not None:
            # 查找要删除的联系人在紧急联系人列表中的索引
            print(name)
            contacts = emergency_contacts.get(user_id, [])
            for index, contact in enumerate(contacts):
                if contact["name"] == name:
                    # 找到对应的联系人并删除
                    del contacts[index]
                    print("紧急联系人已删除")
                    print(emergency_contacts)
                    return "删除成功"
            return "未找到要删除的联系人"
        return "未登录"


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
    if user_id is None or user_id not in session:
        return redirect(url_for('login'))
    if user_id in emergency_contacts:
        print(emergency_contacts[user_id])
        return render_template('help/sms.html', emergency_contacts=emergency_contacts[user_id])
    else:
        return redirect(url_for('set_emergency', user_id=user_id))


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
    return render_template('location.html')


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
    return render_template('health.html')


@app.route('/health/sleep')  # 设置健康检测界面
@app.route('/health/sleep/<user_id>')  # 设置健康检测界面
def sleep(user_id=None):
    return render_template('health/sleep.html')


@app.route('/tools')  # 设置智能工具界面
@app.route('/tools/<user_id>')  # 设置智能工具界面
def tools(user_id=None):
    return render_template('tools.html')


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
