from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek
# from langchain_community.tools.tavily_search import TavilySearchResults
import os
from dotenv import load_dotenv
from langchain_tavily import TavilySearch

load_dotenv(override=True)

web_search_tool = TavilySearch(
    tavily_api_key=os.getenv("TAVILY_API_KEY"),
    max_results=3
)
model = ChatDeepSeek(model="deepseek-chat", api_key=os.getenv("DEEPSEEK_API_KEY"))

agent = create_agent(
    model=model,
    tools=[web_search_tool],
    system_prompt="你是一名多才多艺的智能助手，可以调用工具帮助用户解决问题。"
)

result = agent.invoke({"messages": [{"role": "user", "content": "北京和上海的天气"}]})
print(result)