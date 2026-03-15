from flask import Flask, render_template

# 创建一个简单的测试应用
app = Flask(__name__, template_folder='templates')

@app.route('/')
def test_index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=60001, host="0.0.0.0", use_reloader=False)