import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv(override=True)
# 获取 API Key
api_key = os.getenv("DEEPSEEK_API_KEY")

# 使用 DeepSeek 的 base_url
client = OpenAI(
    base_url="https://api.deepseek.com/v1",
    api_key=api_key,
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "你好"}]
)   
print("用 SDK 的结果：", response.choices[0].message.content)
