
from flask import Flask, request, Response, render_template
import requests
import json
import logging

app = Flask(__name__, template_folder='./templates', static_folder='./static')
logging.basicConfig(level=logging.DEBUG)

# API Configurations
API_KEY_1 = 'sk-74b54d1248b9a34d12e95c5ea723bdf2'  # iFlow平台 API Key
API_KEY_2 = 'sk-74b54d1248b9a34d12e95c5ea723bdf2'  # 第二个API Key（可替换为其他Key）

# iFlow平台API端点
API_ENDPOINT = 'https://platform.iflow.cn/v1/chat/completions'

def create_headers(api_key):
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

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
            payload = {
                "model": "qwen3-coder-plus",
                "messages": [{"role": "user", "content": prompt}],
                "stream": True,
                "temperature": 0.7,
                "top_p": 0.95,
                "max_tokens": 1500,
                "stop": None,
                "repetition_penalty": 1.0
            }
            
            response = requests.post(
                API_ENDPOINT,
                headers=create_headers(API_KEY_1),
                json=payload,
                stream=True
            )
            
            if response.status_code != 200:
                error_msg = f"API error: {response.status_code} - {response.text}"
                app.logger.error(error_msg)
                yield error_msg
                return

            app.logger.debug("Stream created successfully for gen")
            
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith("data: "):
                        line = line[6:]
                    
                    if line.strip() == '[DONE]':
                        continue
                    
                    try:
                        json_data = json.loads(line)
                        if 'choices' in json_data and len(json_data['choices']) > 0:
                            content = json_data['choices'][0].get('delta', {}).get('content')
                            if content:
                                app.logger.debug(f"Yielding chunk: {content}")
                                yield content
                    except json.JSONDecodeError as e:
                        app.logger.error(f"JSON decode error: {e}")
                        continue
                    
        except Exception as e:
            error_msg = f"Error in generate_stream: {str(e)}"
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
            payload = {
                "model": "qwen3-coder-plus",
                "messages": [{"role": "user", "content": prompt}],
                "stream": True,
                "temperature": 0.8,
                "top_p": 0.95,
                "max_tokens": 1500,
                "stop": None,
                "repetition_penalty": 1.0
            }
            
            response = requests.post(
                API_ENDPOINT,
                headers=create_headers(API_KEY_2),
                json=payload,
                stream=True
            )
            
            if response.status_code != 200:
                error_msg = f"API error: {response.status_code} - {response.text}"
                app.logger.error(error_msg)
                yield error_msg
                return

            app.logger.debug("Stream created successfully for gen2")
            
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith("data: "):
                        line = line[6:]
                    
                    if line.strip() == '[DONE]':
                        continue
                    
                    try:
                        json_data = json.loads(line)
                        if 'choices' in json_data and len(json_data['choices']) > 0:
                            content = json_data['choices'][0].get('delta', {}).get('content')
                            if content:
                                app.logger.debug(f"Yielding chunk: {content}")
                                yield content
                    except json.JSONDecodeError as e:
                        app.logger.error(f"JSON decode error: {e}")
                        continue
                    
        except Exception as e:
            error_msg = f"Error in generate_stream: {str(e)}"
            app.logger.error(error_msg)
            yield error_msg
    
    return Response(generate_stream(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True, port=60000, host="0.0.0.0")
