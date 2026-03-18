import os
from dotenv import load_dotenv
from openai import OpenAI
import json

def get_weather(location: str) -> str:
    """获取指定位置的天气信息"""
    name_map = {
        "北京": "北京",
        "上海": "上海",
        "深圳": "深圳",
    }
    location = name_map.get(location, location)
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

def testChatModel():
    # 加载环境变量
    load_dotenv(override=True)
    # 获取 API Key
    api_key = os.getenv("DEEPSEEK_API_KEY")

    # 使用 DeepSeek 的 base_url
    client = OpenAI(
        base_url="https://api.deepseek.com/v1",
        api_key=api_key,
    )
    model = "deepseek-chat"
    messages = [{"role": "user", "content": "北京和上海的天气"}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    message = response.choices[0].message
    tool_calls = message.tool_calls
    print("模型返回:", message.content)
    if tool_calls:
        assistant_msg = {
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in tool_calls
            ]
        }
        messages.append(assistant_msg)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            if function_name == "get_weather":
                weather_info = get_weather(**arguments)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": weather_info
                })
                print("函数返回:", weather_info)
            else:
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": f"未实现的工具: {function_name}"
                })
                print("函数返回:", f"未实现的工具: {function_name}")
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        print("最终模型返回:", response.choices[0].message.content)

def testReasonerModel():
    # 加载环境变量
    load_dotenv(override=True)
    # 获取 API Key
    api_key = os.getenv("DEEPSEEK_API_KEY")

    # 使用 DeepSeek 的 base_url
    client = OpenAI(
        base_url="https://api.deepseek.com/v1",
        api_key=api_key,
    )
    model = "deepseek-reasoner"
    messages = [{"role": "user", "content": "北京和上海的天气"}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    message = response.choices[0].message
    tool_calls = message.tool_calls
    print("模型返回:", response.model_dump())
    if tool_calls:
        rc = message.model_dump().get("reasoning_content")
        assistant_msg = {
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in tool_calls
            ],
            "reasoning_content": rc,
        }
        messages.append(assistant_msg)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            if function_name == "get_weather":
                weather_info = get_weather(**arguments)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": weather_info
                })
                print("函数返回:", weather_info)
            else:
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": f"未实现的工具: {function_name}"
                })
                print("函数返回:", f"未实现的工具: {function_name}")
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        print("最终模型返回:", response)

testReasonerModel()
# testChatModel()
