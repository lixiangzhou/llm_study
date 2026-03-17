import base64
import os
from dotenv import load_dotenv
from openai import OpenAI
import io

load_dotenv(override=True)
api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

response = client.chat.completions.create(
    model="google/gemini-3-pro-image-preview",
    messages=[{"role": "user", "content": "生成一张一家团圆的图片"}],
    extra_body={"modalities": ["image", "text"]}
)

response = response.choices[0].message
if response.images:
    for image in response.images:
        image_url = image["image_url"]["url"]
        print(image_url)


# 没有测试通过，模型不可用