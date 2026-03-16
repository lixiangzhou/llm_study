import time
import os
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, RateLimitError, APIError, APIConnectionError

# 加载环境变量
load_dotenv(override=True)
# 获取 API Key
class Client:
    def __init__(self, name: str):
        self.name = name
        if name == "openrouter":
            self.api_key = os.getenv("OPENROUTER_API_KEY")
            self.base_url = "https://openrouter.ai/api/v1"
        elif name == "deepseek":
            self.api_key = os.getenv("DEEPSEEK_API_KEY")
            self.base_url = "https://api.deepseek.com/v1"
        elif name == "dashscope":
            self.api_key = os.getenv("DASHSCOPE_API_KEY")
            self.base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        elif name == "moonshot":
            self.api_key = os.getenv("MOONSHOT_API_KEY")
            self.base_url = "https://api.moonshot.cn/v1"
        else:
            raise ValueError(f"不支持的模型名称: {name}")
        
    def get_client(self):
        return OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )
    
    def get_response(self, model: str, content: str, stream: bool = False):
        for _ in range(3):
            print(f"第{_+1}次重试")
            try:
                client = self.get_client()
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": content}],
                    stream=stream
                )
                return response
            except AuthenticationError as e:
                return f"认证错误: {e}"
            except RateLimitError as e:
                wait_time = 2 ** _  # 指数退避
                print(f"速率限制错误: {e}, 等待 {wait_time} 秒后重试")
                time.sleep(wait_time)
                continue
            except APIError as e:
                return f"API错误: {e}"
            except APIConnectionError as e:
                print(f"API连接错误: {e}")
                continue
            except Exception as e:
                return f"其他错误: {e}"
        return "重试次数3用完，仍未成功"
            
    def get_response_content(self, model: str, content: str):
        response = self.get_response(model, content)
        if isinstance(response, str):
            return response
        return response.choices[0].message.content
    
client = Client("deepseek")

# 非stream 模式
response_content = client.get_response_content(
    model="deepseek-chat",
    content="你好"
)
print("用 SDK 的结果：", response_content)

# stream 模式
# response = client.get_response(
#     model="deepseek-chat",
#     content="你好",
#     stream=True
# )

# for chunk in response:
#     delta_content = chunk.choices[0].delta.content
#     if delta_content:
#         print(delta_content, end="", flush=True)
#         time.sleep(0.1)
