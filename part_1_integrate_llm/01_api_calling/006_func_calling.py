import os
from dotenv import load_dotenv
from openai import OpenAI
import json

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

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定位置的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "要查询天气的位置，例如：北京、上海、深圳",
                    },
                },
                "required": ["location"],
            },
        },
    }
]

def test():
    # 加载环境变量
    load_dotenv(override=True)
    # 获取 API Key
    api_key = os.getenv("DEEPSEEK_API_KEY")

    # 使用 DeepSeek 的 base_url
    client = OpenAI(
        base_url="https://api.deepseek.com/v1",
        api_key=api_key,
    )
    messages = [
        {"role": "user", "content": "北京的天气"}
    ]
    # 调用模型
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    message = response.choices[0].message
    tool_calls = message.tool_calls
    # 打印模型返回的消息
    print("模型返回:", message.content)

    if tool_calls:
        print("调用函数:", tool_calls)
        tool_call = tool_calls[0]
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        if function_name == "get_weather":
            weather_info = get_weather(**arguments)
            print("函数返回:", weather_info)
            messages.append(message)
            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": weather_info})

        final_response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages
        )
        print("最终模型返回:", final_response.choices[0].message.content)
    else:
        print("未调用函数，直接返回模型回复")
        print("最终模型返回:", response.choices[0].message.content)
test()