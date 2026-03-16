import os, time, asyncio
from openai import OpenAI, AsyncOpenAI
from dotenv import load_dotenv

load_dotenv(override=True)
sync_client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

async_client = AsyncOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

questions = [
    "什么是Python？",
    "什么是JavaScript？",
    "什么是Go语言？",
    "什么是Rust？",
    "什么是TypeScript？"
]

def sync_batch():
    print("*" * 60)
    print("同步批量调用")
    print("*" * 60)
    
    start_time = time.time()
    results = []

    for question in questions:
        response = sync_client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": question}],
            max_tokens=50
        )
        results.append(response.choices[0].message.content)
    
    elapsed_time = time.time() - start_time
    print(f"同步批量调用耗时: {elapsed_time:.2f} 秒")
    return results, elapsed_time

async def ask_question_async(question):
    response = await async_client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": question}],
        max_tokens=50
    )
    return response.choices[0].message.content

async def async_batch():
    print("*" * 60)
    print("异步批量调用")
    print("*" * 60)
    
    start_time = time.time()
    results = []

    tasks = [ask_question_async(question) for question in questions]
    results = await asyncio.gather(*tasks)
    
    elapsed_time = time.time() - start_time
    print(f"异步批量调用耗时: {elapsed_time:.2f} 秒")
    return results, elapsed_time

sync_results, sync_time = sync_batch()
async_results, async_time = asyncio.run(async_batch())
