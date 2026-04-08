from langchain.tools import tool
from langchain_deepseek import ChatDeepSeek
#from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_agent
import os
from dotenv import load_dotenv
from datetime import datetime

@tool
def get_weather(location: str) -> str:
    """获取指定位置的天气信息"""
    weather_data = {
        "北京": {"temperature": 15, "condition": "晴天", "humidity": 45},
        "上海": {"temperature": 20, "condition": "多云", "humidity": 60},
        "深圳": {"temperature": 28, "condition": "小雨", "humidity": 75},
    }
    cities = weather_data.keys()
    if location not in cities:
        return f"未找到{location}的天气信息"
    data = weather_data[location]
    return f"天气信息：{location}的天气是{data['condition']}，温度{data['temperature']}度，湿度{data['humidity']}%"

def write_file(content: str) -> str:
    """将内容写入文件"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"output_{timestamp}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        abs_path = os.path.abspath(filename)
        return f"文件已写入{abs_path}"
    except Exception as e:
        return f"写入文件时出错：{str(e)}"

load_dotenv(override=True)
model = ChatDeepSeek(model="deepseek-chat", api_key=os.getenv("DEEPSEEK_API_KEY"))
agent = create_agent(model, tools=[get_weather, write_file], system_prompt="你是一名多才多艺的智能助手，可以调用工具帮助用户解决问题。")

result = agent.invoke({"messages": [{"role": "user", "content": "北京的天气如何，写入到文件中"}]})
print(result["messages"][-1].content)
for record in result["messages"]:
    print(record)
