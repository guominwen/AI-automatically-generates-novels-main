import requests
import time

# 等待Flask应用启动
time.sleep(2)

try:
    response = requests.get('http://127.0.0.1:60000', timeout=5)
    print(f"Status Code: {response.status_code}")
    print(f"Content Length: {len(response.text)}")
    print(f"First 100 chars: {response.text[:100]}")
    
    if response.status_code == 200:
        print("✅ 成功加载index.html页面！")
    else:
        print("❌ 请求失败")
        
except requests.exceptions.RequestException as e:
    print(f"❌ 请求异常: {e}")
    print("可能的原因：Flask应用未启动或端口被占用")