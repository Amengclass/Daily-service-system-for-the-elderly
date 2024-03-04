from flask import Flask, request, render_template
from ipapi import location

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
        ip_address = request.form['ip_address']
        location_info = location(ip_address)
        return render_template('result.html', location_info=location_info)

if __name__ == '__main__':
    app.run(debug=True)
