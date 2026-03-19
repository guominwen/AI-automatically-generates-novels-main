from flask import Flask, request, Response, render_template
import openai
import json
import logging
from http import HTTPStatus

app = Flask(__name__, template_folder='templates', static_folder='static')
logging.basicConfig(level=logging.DEBUG)

# API Configurations
API_KEY_1 = 'sk-1afc3abd99897ba33a97731b86cd00dd'  # 心流 API Key (请替换为您的实际密钥)
API_KEY_2 = 'sk-1afc3abd99897ba33a97731b86cd00dd'  # 第二个API Key（可替换为其他Key）

# 创建 OpenAI 客户端 - 心流 API 兼容
client_1 = openai.OpenAI(
    base_url="https://apis.iflow.cn/v1",
    api_key=API_KEY_1,
)

client_2 = openai.OpenAI(
    base_url="https://apis.iflow.cn/v1",
    api_key=API_KEY_2,
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gen', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', '')
    app.logger.debug(f"Received prompt for gen: {prompt}")
    
    def generate_stream():
        try:
            # 使用 client_1 调用心流 API
            response = client_1.chat.completions.create(
                model="qwen3-coder-plus",  # 用户指定的模型
                messages=[{"role": "user", "content": prompt}],
                stream=True,
                temperature=0.7,
                top_p=0.95,
                max_tokens=1500,
                stop=None,
                presence_penalty=0.0,
                frequency_penalty=0.0,
            )
            
            app.logger.debug("Stream created successfully for gen")
            
            for chunk in response:
                if chunk.choices and len(chunk.choices) > 0:
                    content = chunk.choices[0].delta.content
                    if content:
                        app.logger.debug(f"Yielding chunk: {content}")
                        yield content
                        
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            app.logger.error(error_msg)
            yield error_msg
    
    return Response(generate_stream(), mimetype='text/plain')

@app.route('/gen2', methods=['POST'])
def generate2():
    data = request.json
    prompt = data.get('prompt', '')
    app.logger.debug(f"Received prompt for gen2: {prompt}")
    
    def generate_stream():
        try:
            # 使用 client_2 调用心流 API
            response = client_2.chat.completions.create(
                model="qwen3-coder-plus",  # 用户指定的模型
                messages=[{"role": "user", "content": prompt}],
                stream=True,
                temperature=0.8,
                top_p=0.95,
                max_tokens=1500,
                stop=None,
                presence_penalty=0.0,
                frequency_penalty=0.0,
            )
            
            app.logger.debug("Stream created successfully for gen2")
            
            for chunk in response:
                if chunk.choices and len(chunk.choices) > 0:
                    content = chunk.choices[0].delta.content
                    if content:
                        app.logger.debug(f"Yielding chunk: {content}")
                        yield content
                        
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            app.logger.error(error_msg)
            yield error_msg
    
    return Response(generate_stream(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True, port=60000, host="0.0.0.0")