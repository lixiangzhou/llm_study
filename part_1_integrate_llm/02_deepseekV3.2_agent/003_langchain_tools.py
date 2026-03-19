from langchain.tools import tool

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

print(get_weather.name)
print(get_weather.description)
print(get_weather.args)