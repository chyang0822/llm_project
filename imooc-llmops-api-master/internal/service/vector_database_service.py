#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/6/30 16:34
@Author  : thezehui@gmail.com
@File    : vector_database_service.py
"""
import os
from pathlib import Path

from injector import inject
from langchain_core.vectorstores import VectorStoreRetriever

from internal.core.vector_store import MemoryVectorStore
from .embeddings_service import EmbeddingsService

# 向量数据库的集合名字
COLLECTION_NAME = "Dataset"


@inject
class VectorDatabaseService:
    """向量数据库服务 - 使用自定义内存向量数据库"""
    vector_store: MemoryVectorStore
    embeddings_service: EmbeddingsService

    def __init__(self, embeddings_services: EmbeddingsService):
        """构造函数，完成向量数据库服务的自定义向量数据库实例的创建"""
        # 1.赋值embeddings_service
        self.embeddings_service = embeddings_services

        # 2.创建自定义内存向量数据库
        # 尝试使用缓存embeddings，如果Redis不可用则使用普通embeddings
        try:
            embeddings = self.embeddings_service.cache_backed_embeddings
            print("使用带Redis缓存的embeddings")
        except Exception as e:
            print(f"Warning: Redis cache not available, using direct embeddings. Error: {e}")
            embeddings = self.embeddings_service.embeddings
        
        # 创建自定义内存向量数据库实例
        self.vector_store = MemoryVectorStore(embedding=embeddings)
        print(f"自定义内存向量数据库初始化完成")

    def get_retriever(self, **kwargs) -> VectorStoreRetriever:
        """获取检索器
        
        Args:
            **kwargs: 检索器参数，如search_kwargs={'k': 4}
            
        Returns:
            VectorStoreRetriever实例
        """
        return self.vector_store.as_retriever(**kwargs)

    def add_texts(self, texts: list[str], metadatas: list[dict] = None) -> list[str]:
        """添加文本到向量数据库
        
        Args:
            texts: 文本列表
            metadatas: 元数据列表
            
        Returns:
            添加的文档ID列表
        """
        return self.vector_store.add_texts(texts=texts, metadatas=metadatas)

    def delete_by_ids(self, ids: list[str]) -> bool:
        """根据ID删除文档
        
        Args:
            ids: 文档ID列表
            
        Returns:
            是否删除成功
        """
        return self.vector_store.delete(ids=ids)

    def similarity_search(self, query: str, k: int = 4):
        """相似度搜索
        
        Args:
            query: 查询文本
            k: 返回结果数量
            
        Returns:
            相似文档列表
        """
        return self.vector_store.similarity_search(query, k=k)

    def similarity_search_with_score(self, query: str, k: int = 4):
        """带分数的相似度搜索
        
        Args:
            query: 查询文本
            k: 返回结果数量
            
        Returns:
            (文档, 分数)元组列表
        """
        return self.vector_store.similarity_search_with_score(query, k=k)

    def clear(self):
        """清空所有数据"""
        self.vector_store.clear()

    def count(self) -> int:
        """返回存储的文档数量
        
        Returns:
            文档数量
        """
        return self.vector_store.count()

    def get_by_ids(self, ids: list[str]):
        """根据ID获取文档
        
        Args:
            ids: 文档ID列表
            
        Returns:
            文档列表
        """
        return self.vector_store.get_by_ids(ids)
