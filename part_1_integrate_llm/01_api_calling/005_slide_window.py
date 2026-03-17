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
    return slide_window(conversation_history)

# 滑动窗口机制，只保留最近的 max_turns 轮对话，超出部分会被截断。
def slide_window(conversation_history: list, max_turns: int = 3):
    system_message = [msg for msg in conversation_history if msg["role"] == "system"]
    dialog_messages = [msg for msg in conversation_history if msg["role"] != "system"]
    if len(dialog_messages) <= max_turns:
        return system_message + dialog_messages
    recent_dialog_messages = dialog_messages[-(max_turns * 2):]
    return system_message + recent_dialog_messages

loop_history = chat_loop()
for msg in loop_history:
    print(msg)