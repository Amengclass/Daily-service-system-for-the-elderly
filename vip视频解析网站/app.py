# coding:utf-8
from flask import Flask, render_template
app = Flask(__name__)

#视频解析网站1
@app.route('/video1')
def video_analysis():
    return render_template('video_analysis1.html')

#视频解析网站2
# @app.route('/video2')
# def video_analysis():
#     return render_template('video_analysis1.html')

# @app.route('/video_analysis', methods=['POST'])
# def video_analysis():
#     titurl = request.form.get('titurl')
#     # 在这里进行视频解析或其他相关操作，然后返回结果给前端
#     # 例如，你可以调用某个解析视频的函数，然后将解析结果返回给前端
#     analysis_result = "B6 vip观影 - 地址解析成功！"
#     return analysis_result

@app.route('/music')
def music():
    return render_template('music.html')

if __name__ == '__main__':
    app.run(port=5001)
