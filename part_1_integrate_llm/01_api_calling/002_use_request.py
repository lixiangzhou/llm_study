import requests
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(override=True)
# 获取 API Key
api_key = os.getenv("DEEPSEEK_API_KEY")

# 使用 DeepSeek 的 base_url
response = requests.post(
    "https://api.deepseek.com/v1/chat/completions",  # DeepSeek 正确的 API 端点
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    json={"model": "deepseek-chat", "messages": [{"role": "user", "content": "你好"}]}
)

result = response.json()
print("不用 SDK 的结果：", result['choices'][0]['message']['content'])