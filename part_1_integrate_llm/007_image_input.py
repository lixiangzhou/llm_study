import base64
import os
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image
import io

def image_url_test():
    load_dotenv(override=True)
    api_key = os.getenv("OPENROUTER_API_KEY")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )
    image_url = "https://n.sinaimg.cn/sinacn10109/600/w1920h1080/20200222/6437-ipvnsze6417759.jpg"
    response = client.chat.completions.create(
        model="qwen/qwen-vl-plus",
        messages=[
            {
                "role": "user", 
                "content": [
                    {"type": "text", "text": "描述这张图片"},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            },
        ],
        max_tokens=500
    )
    print(response.choices[0].message.content)

# image_url_test()

def compress_image(image_path, max_size=(800, 800)):
    """压缩图片到指定最大尺寸"""
    with Image.open(image_path) as image:
        # 缩放图片到最大尺寸
        image.thumbnail(max_size)
        #  转换为 JPEG 格式并压缩质量
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=85)
        # 编码为 base64 字符串
        return base64.b64encode(buffer.getvalue()).decode('utf-8')

def local_image_test():
    load_dotenv(override=True)
    api_key = os.getenv("OPENROUTER_API_KEY")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )
    # 压缩图片
    image_url = compress_image("part_1_integrate_llm/resources/image_1.jpg")

    response = client.chat.completions.create(
        model="qwen/qwen-vl-plus",
        messages=[
            {
                "role": "user", 
                "content": [
                    {"type": "text", "text": "描述这张图片"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_url}"}}
                ]
            },
        ],
        max_tokens=500
    )
    print(response.choices[0].message.content)

local_image_test()
