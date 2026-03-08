from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv(override=True)

# 读取环境变量
api_key = os.getenv("OPENROUTER_API_KEY")

print(api_key)