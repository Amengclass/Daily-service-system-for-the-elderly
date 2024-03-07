from flask import Flask, request, render_template, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 假设的用户数据
users = {
    'user1': {'password': '123456', 'name': 'User One'},
    'user2': {'password': 'password2', 'name': 'User Two'}
}
# 登录页面
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['username']
        password = request.form['password']
        if user_id in users and users[user_id]['password'] == password:
            session[user_id] = True
            return redirect(url_for('protected',user_id = user_id))
        else:
            return '登录失败，请重试'
    return render_template('login.html')

# 受保护的页面
@app.route('/protected')
@app.route('/protected/<user_id>')
def protected(user_id=None):
    if user_id is None or user_id not in session:
        return redirect(url_for('login'))
    return f'欢迎 {users[user_id]["name"]} 访问受保护的页面'


# 退出登录
@app.route('/logout')
@app.route('/logout/<user_id>')
def logout(user_id=None):
    session.pop(user_id, None)  # 删除存储在会话中的用户ID
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
