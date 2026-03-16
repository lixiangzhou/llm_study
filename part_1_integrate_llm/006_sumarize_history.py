from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv(override=True)
api_key = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(
    base_url="https://api.deepseek.com/v1",
    api_key=api_key,
)

def chat_loop(max_turns: int = 5):
    # 注意：每次调用模型时，都需要将 conversation_history 作为参数传递，以保持上下文的连贯性。
    conversation_history = [{"role": "system", "content": "你是一位友好的 AI 助手"}]
    for turn in range(1, 1 + max_turns):
        print("=" * 20)
        print(f"第{turn}轮对话")
        print("=" * 20)
        user_input = input("用户: ").strip()
        if not user_input:
            print("用户输入不能为空，请重新输入")
            continue
        if user_input.lower() in ["exit", "quit"]:
            print("用户退出对话")
            break
        conversation_history.append({"role": "user", "content": user_input})
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages= conversation_history
            )
            deepseek_response = response.choices[0].message.content
        except Exception as e:
            print(f"DeepSeek模型调用失败: {e}")
            conversation_history.pop()
            continue
        conversation_history.append({"role": "assistant", "content": deepseek_response})
        print(f"DeepSeek: {deepseek_response}")
    return sumarize_history(conversation_history)

# 摘要压缩
def sumarize_history(conversation_history: list):
    conversion_txt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个专业的摘要压缩模型"},
            {"role": "user", "content": f"请压缩以下对话记录，保留核心信息：\n{conversion_txt}"}
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content
chat_loop()