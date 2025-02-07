import dashscope
from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI
from dashscope import Application

app = Flask(__name__)


# 存储对话记录
chat_history =  [{"role": "system", "content": "你是一个聊天机器人。"}]

@app.route('/')
def home():     
    # 将对话记录传递给模板
    return render_template('chatindex.html', chat_history=chat_history)

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['user_message']
    chat_history.append({"role": "user", "content": user_message})
    # 这里可以替换为更复杂的逻辑来生成机器人的响应
    bot_response=None
    try:
        '''
        使用dev1        Open AI方式:  
        client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        '''
        response = Application.call(
    # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        app_id='b932bccd1fe8430babcb553a9b276604',
        
        messages=chat_history)
        
        response = dashscope.Generation.call(
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        model="qwen-turbo-ft-202501301520-8320", # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': user_message}
            ],
        result_format='message'
        )
        
        '''
        result = client.chat.completions.create(
            model='qwen-turbo-ft-202501291624-e649',
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': user_message}
            ],
            #result_format="message"
        )
        '''
        bot_response=response.output.text
    except Exception as e:
        print(f"错误信息：{e}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
    
    #bot_response = completion.choices[0].message.content
   
    # 将对话记录添加到历史中
    
    chat_history.append({"role": "assistant", "content": bot_response})
       
    # 返回机器人的响应
    return jsonify({'response': bot_response})


if __name__ == '__main__':
    app.run(debug=True)
