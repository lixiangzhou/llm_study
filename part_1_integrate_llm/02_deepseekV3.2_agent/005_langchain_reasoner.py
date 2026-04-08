from typing import List, Optional, Dict, Any
from langchain.agents import create_agent
from langchain_core.language_models.models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.tools import BaseTool

class DeepSeekReasonerChatModel(BaseChatModel):
    """
    自定义 DeepSeek Reasoner 模型

    关键特性：
    1. 保留 reasoning_content 在 additional_kwargs 中
    2. 消息转换时恢复 reasoning_content
    3. 完整支持工具绑定和调用
    """
    def __init__(self, api_key: str):
        self.model = "deepseek-reasoner"
        self.base_url = "https://api.deepseek.cn"
        self.api_key = api_key
        self.temperature = 0.7
        self.bind_tools = None
       
    def _convert_messages_to_openai_format(self, messages):
        """
        将 langchain 格式的消息转换为 OpenAI 格式
        """
        openai_messages = []
        for msg in messages:
            if isinstance(msg, AIMessage):
                msg_dict = {"role": "assistant", "content": msg.content or ""}
                if msg.tool_calls:
                    msg_dict["tool_calls"] = msg.tool_calls
                if 'reasoning_content' in msg.additional_kwargs:
                    msg_dict["reasoning_content"] = msg.additional_kwargs['reasoning_content']
                
                print("msg_dict:", msg_dict)
                openai_messages.append(msg_dict)
        return openai_messages
    
    def _create_ai_message_from_response(self, response):
        """
        从 OpenAI 模型响应创建创建 langchain 消息
        """
        message = response.choices[0].message
        tool_calls = message.tool_calls or []
        additional_kwargs = {}
        if hasattr(message, "reasoning_content"):
            additional_kwargs['reasoning_content'] = message.reasoning_content
        
        return AIMessage(
            content=message.content or "",
            additional_kwargs=additional_kwargs,
            tool_calls=tool_calls
        )

    def bind_tools(self, tools: List[BaseTool], **kwargs):
        """绑定 LangChain 工具"""
        # 转换为 OpenAI 格式
        openai_tools = []
        for tool in tools:
            openai_tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.args_schema.model_json_schema()
                }
            })
        return self.__class__(
            api_key=self.api_key,
            base_url=self.base_url,
            model_name=self.model,
            temperature=self.temperature,
            bound_tools=openai_tools,  # 保存绑定的工具
            **kwargs
        )

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        """核心生成方法"""
        # 转换消息
        openai_messages = self._convert_messages_to_openai_format(messages)
        # 准备请求
        request_params = {
            "model": self.model,
            "messages": openai_messages,
            "temperature": self.temperature,
        }
        # 添加工具
        if self.bound_tools:
            request_params["tools"] = self.bound_tools
        
        response = self._client.chat.completions.create(**request_params)
        # 创建响应
        ai_message = self._create_ai_message_from_response(response)
        return ChatResult(generations=[ChatGeneration(message=ai_message)])
