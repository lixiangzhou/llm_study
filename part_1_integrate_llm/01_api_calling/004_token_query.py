from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-v3")
text = "你好,世界!Hello World!"
tokens = tokenizer.encode(text)
print(f"Token 数量: {len(tokens)}")
# 中文约 1 字 ≈ 0.6 token

# Qwen (通义千问): 使用 Qwen tokenizer
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-7B")
tokens = tokenizer.encode(text)
print(f"Token 数量: {len(tokens)}")