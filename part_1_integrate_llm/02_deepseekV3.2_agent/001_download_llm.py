from transformers import AutoModel, AutoTokenizer

# 第一次运行时会自动下载，后续会使用缓存
model = AutoModel.from_pretrained("bert-base-chinese")
tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")
print(model)
print(tokenizer)
