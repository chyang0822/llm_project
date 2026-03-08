#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/6/30 8:12
@Author  : thezehui@gmail.com
@File    : test_custom_vector_store.py
自定义向量数据库测试示例
"""
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import dotenv
from langchain_openai import OpenAIEmbeddings

from internal.core.vector_store import MemoryVectorStore

# 加载环境变量
dotenv.load_dotenv()

# 1.准备测试数据
texts = [
    "笨笨是一只很喜欢睡觉的猫咪",
    "我喜欢在夜晚听音乐，这让我感到放松。",
    "猫咪在窗台上打盹，看起来非常可爱。",
    "学习新技能是每个人都应该追求的目标。",
    "我最喜欢的食物是意大利面，尤其是番茄酱的那种。",
    "昨晚我做了一个奇怪的梦，梦见自己在太空飞行。",
    "我的手机突然关机了，让我有些焦虑。",
    "阅读是我每天都会做的事情，我觉得很充实。",
    "他们一起计划了一次周末的野餐，希望天气能好。",
    "我的狗喜欢追逐球，看起来非常开心。",
]

metadatas = [
    {"page": 1, "category": "pet"},
    {"page": 2, "category": "hobby"},
    {"page": 3, "category": "pet"},
    {"page": 4, "category": "learning"},
    {"page": 5, "category": "food"},
    {"page": 6, "category": "dream"},
    {"page": 7, "category": "tech"},
    {"page": 8, "category": "hobby"},
    {"page": 9, "category": "activity"},
    {"page": 10, "category": "pet"},
]

# 2.创建嵌入模型
embedding = OpenAIEmbeddings(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="text-embedding-v4",
    api_key="sk-3927d686315447078d6d8ef4e7ac5b9d",
    check_embedding_ctx_length=False
)

# 3.构建自定义向量数据库
print("=" * 50)
print("初始化自定义内存向量数据库...")
db = MemoryVectorStore(embedding=embedding)

# 4.添加文本
print("=" * 50)
print("添加文本到向量数据库...")
ids = db.add_texts(texts, metadatas)
print(f"成功添加 {len(ids)} 条文档")
print(f"文档ID: {ids[:3]}...")  # 只显示前3个ID

# 5.查询文档数量
print("=" * 50)
print(f"当前数据库中的文档数量: {db.count()}")

# 6.执行相似度搜索
print("=" * 50)
print("执行相似度搜索: '笨笨是谁？'")
results = db.similarity_search("笨笨是谁？", k=3)
for i, doc in enumerate(results, 1):
    print(f"\n结果 {i}:")
    print(f"  内容: {doc.page_content}")
    print(f"  元数据: {doc.metadata}")

# 7.执行带分数的相似度搜索
print("=" * 50)
print("执行带分数的相似度搜索: '宠物相关的内容'")
results_with_score = db.similarity_search_with_score("宠物相关的内容", k=3)
for i, (doc, score) in enumerate(results_with_score, 1):
    print(f"\n结果 {i}:")
    print(f"  内容: {doc.page_content}")
    print(f"  元数据: {doc.metadata}")
    print(f"  相似度分数: {score:.4f}")

# 8.根据ID获取文档
print("=" * 50)
print("根据ID获取文档...")
first_id = ids[0]
docs = db.get_by_ids([first_id])
if docs:
    print(f"获取到的文档: {docs[0].page_content}")

# 9.删除文档
print("=" * 50)
print(f"删除文档 ID: {first_id}")
db.delete([first_id])
print(f"删除后的文档数量: {db.count()}")

# 10.清空数据库
print("=" * 50)
print("清空数据库...")
db.clear()
print(f"清空后的文档数量: {db.count()}")

print("=" * 50)
print("测试完成！")
