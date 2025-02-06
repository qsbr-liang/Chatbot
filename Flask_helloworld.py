from datetime import datetime
from flask import Flask, jsonify, render_template, request, session

app=Flask(__name__)

@app.route('/')
def hello_world():
    items = [
        {'title': '项目1', 'description': '这是项目1的描述。'},
        {'title': '项目2', 'description': '这是项目2的描述。'},
        {'title': '项目3', 'description': '这是项目3的描述。'}
    ]
    return render_template('index.html', items=items)

@app.route('/info')
def info():
    user_agent = request.headers.get('User-Agent')
    return f'Your user agent is {user_agent}'+datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") 

@app.errorhandler(404)
def not_found(error):
    return 'Sorry,Page not found', 404

@app.before_request
def before_request():
    print ('Before request'+datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") )

@app.after_request
def after_request(response):
    print ('After request'+datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") )
    return response

@app.teardown_request
def teardown_request(exception):
    print ('Teardown request'+datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") )

@app.route('/render')
def home():
    return render_template('index.html', title='Welcome Page', name='John Doe')

if __name__ == '__main__':
    app.run(debug=True)