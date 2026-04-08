from langchain_deepseek import ChatDeepSeek
import os
from dotenv import load_dotenv

load_dotenv(override=True)

model = ChatDeepSeek(model="deepseek-reasoner", api_key=os.getenv("DEEPSEEK_API_KEY"))
response = model.invoke("你好，请你介绍一下你自己。")
print(response.content)
print(response.model_dump())