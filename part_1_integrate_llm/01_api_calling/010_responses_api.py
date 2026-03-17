import os
from openai import OpenAI
from dotenv import load_dotenv
from openai import NotFoundError

load_dotenv(override=True)
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)
model = "openai/gpt-5-nano"
# 为了记住历史内容，需要在每次调用模型时，都需要将 conversation_history 作为参数传递，以保持上下文的连贯性。
# 或者对 conversation_history 进行处理，例如对 conversation_history 进行压缩，或者对 conversation_history 进行摘要压缩。
# response api 可以在Server 通过 previous_response_id 自动维护对话内容
messages = []
try:
    response = client.responses.create(
        model=model,
        input="你好，我叫小米，请记住我的名字",
        store=True
    )
    print(response)
    response = client.responses.create(
        model=model,
        input="你还及得我叫什么名字吗？",
        previous_response_id=response.id,
        store=True
    )
    print(response)
except NotFoundError:
    print("NotFoundError")
    messages = [{"role": "user", "content": "你好，我叫小米，请记住我的名字"}]
    r1 = client.chat.completions.create(
        model=model,
        messages=messages
    )
    print(r1)
    messages.append({"role": "assistant", "content": r1.choices[0].message.content})
    messages.append({"role": "user", "content": "你还及得我叫什么名字吗？"})
    r2 = client.chat.completions.create(
        model=model,
        messages=messages
    )
    print(r2)


# 没有运行成功，很多Lib 没有实现 responses api
