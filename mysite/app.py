from flask import Flask, render_template, Response, jsonify, request
import requests
import cv2
# import mediapipe as mp
import time

# 设置您的 API 密钥
app_id = 'nqsilfmoroilwpoi'
app_secret = 'RFhwZFEzUWt5cUtBS01ZMDFhQkFwdz09'

"""
创建一个 Flask 应用程序实例，通常命名为 app。在这里，__name__ 是 Python 中的一个特殊变量，它表示当前模块的名称。
static_folder表示指定静态文件目录，这样才能引入css
"""
app = Flask(__name__, static_folder='static')

"""
    @app.route 是 Flask 框架中的一个装饰器，用于在 Python 中声明一个视图函数，
并将其与一个 URL 路由绑定起来。当用户访问这个 URL 时，Flask 会调用相应的视图函数来处理请求。
"""


@app.route('/')  # 设置主页目录
def index():
    return render_template('index.html')


@app.route('/zyj')  # 设置主页目录
def ztj():
    return render_template('zyj.html')


@app.route('/help')  # 设置一键帮助
def help():
    return render_template('help.html')


@app.route('/404')  # 设置一键帮助
def fail():
    return render_template('404.html')


@app.route('/help/fall_detection')  # /一键帮助/摔倒检测
def fall_detection():
    return render_template('help/fall_detection.html')


@app.route('/help/fall_detection/recognition')  # 一键帮助/摔倒检测/识别
def recognition():
    return render_template('help/recognition.html')


# 一键帮助/摔倒检测/识别
@app.route('/help/emergency_contact')
def emergency():
    return render_template('help/emergency_contact.html')


# 姿势识别
# @app.route('/video_feed')
# def video_feed():
#     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# def gen_frames():
#     mpPose = mp.solutions.pose
#     pose = mpPose.Pose()
#     mpDraw = mp.solutions.drawing_utils
#
#     cap = cv2.VideoCapture(0)
#     pTime = 0
#
#     while True:
#         success, img = cap.read()
#         imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         results = pose.process(imgRGB)
#
#         if results.pose_landmarks:
#             mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
#
#             for id, lm in enumerate(results.pose_landmarks.landmark):
#                 h, w, c = img.shape
#                 cx, cy = int(lm.x * w), int(lm.y * h)
#                 cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
#
#         cTime = time.time()
#         fps = 1 / (cTime - pTime)
#         pTime = cTime
#         cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
#         ret, buffer = cv2.imencode('.jpg', img)
#         frame = buffer.tobytes()
#         yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#


# 设置位置服务界面
@app.route('/location')
def location():
    return render_template('location.html')


# ip位置信息查询
@app.route('/location/info', methods=['GET'])
def location_info():
    print("进来了")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    url = 'https://whois.pconline.com.cn/ipJson.jsp?json=true'
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
def get_weather():
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
        return jsonify({'temperature': weather_data['data']['temp'], 'weather': weather_data['data']['weather']}), 200
    else:
        return jsonify({'error': 'Failed to get weather data'}), 500


@app.route('/health')  # 设置健康检测界面
def health():
    return render_template('health.html')


@app.route('/tools')  # 设置智能工具界面
def tools():
    return render_template('tools.html')


@app.route('/tools/weather')  # 设置智能工具界面
def weather():
    return render_template('tools/weather.html')


@app.route('/tools/Memo')  # 设置智能工具界面
def Memo():
    return render_template('tools/Memorandum.html')


if __name__ == '__main__':
    app.run(debug=True)
