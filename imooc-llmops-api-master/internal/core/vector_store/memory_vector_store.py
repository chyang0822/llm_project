#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/6/30 8:12
@Author  : thezehui@gmail.com
@File    : memory_vector_store.py
自定义内存向量数据库实现
"""
import uuid
from typing import List, Optional, Any, Iterable, Type

import numpy as np
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore


class MemoryVectorStore(VectorStore):
    """基于内存+欧几里得距离的自定义向量数据库"""
    
    def __init__(self, embedding: Embeddings):
        """初始化向量数据库
        
        Args:
            embedding: 文本嵌入模型
        """
        self._embedding = embedding
        self.store: dict = {}  # 存储向量的字典

    def add_texts(
        self, 
        texts: Iterable[str], 
        metadatas: Optional[List[dict]] = None, 
        **kwargs: Any
    ) -> List[str]:
        """将文本添加到向量数据库中
        
        Args:
            texts: 要添加的文本列表
            metadatas: 对应的元数据列表
            **kwargs: 其他参数
            
        Returns:
            添加的文档ID列表
        """
        # 1.检测metadata的数据格式
        texts_list = list(texts)
        if metadatas is not None and len(metadatas) != len(texts_list):
            raise ValueError("metadatas长度必须与texts长度相同")

        # 2.将文本转换成向量嵌入
        embeddings = self._embedding.embed_documents(texts_list)
        ids = [str(uuid.uuid4()) for _ in texts_list]

        # 3.组装数据记录并存储
        for idx, text in enumerate(texts_list):
            self.store[ids[idx]] = {
                "id": ids[idx],
                "text": text,
                "vector": embeddings[idx],
                "metadata": metadatas[idx] if metadatas is not None else {},
            }

        return ids

    def similarity_search(
        self, 
        query: str, 
        k: int = 4, 
        **kwargs: Any
    ) -> List[Document]:
        """执行相似性搜索
        
        Args:
            query: 查询文本
            k: 返回的结果数量
            **kwargs: 其他参数
            
        Returns:
            相似文档列表
        """
        # 1.将query转换成向量
        embedding = self._embedding.embed_query(query)

        # 2.计算与所有存储向量的欧几里得距离
        result = []
        for key, record in self.store.items():
            distance = self._euclidean_distance(embedding, record["vector"])
            result.append({"distance": distance, **record})

        # 3.按距离排序（距离越小越相似）
        sorted_result = sorted(result, key=lambda x: x["distance"])

        # 4.取前k条结果
        result_k = sorted_result[:k]

        return [
            Document(
                page_content=item["text"], 
                metadata={**item["metadata"], "score": item["distance"]}
            )
            for item in result_k
        ]

    def similarity_search_with_score(
        self, 
        query: str, 
        k: int = 4, 
        **kwargs: Any
    ) -> List[tuple[Document, float]]:
        """执行相似性搜索并返回分数
        
        Args:
            query: 查询文本
            k: 返回的结果数量
            **kwargs: 其他参数
            
        Returns:
            (文档, 分数)元组列表
        """
        # 1.将query转换成向量
        embedding = self._embedding.embed_query(query)

        # 2.计算与所有存储向量的欧几里得距离
        result = []
        for key, record in self.store.items():
            distance = self._euclidean_distance(embedding, record["vector"])
            result.append({"distance": distance, **record})

        # 3.按距离排序
        sorted_result = sorted(result, key=lambda x: x["distance"])

        # 4.取前k条结果
        result_k = sorted_result[:k]

        return [
            (
                Document(page_content=item["text"], metadata=item["metadata"]),
                item["distance"]
            )
            for item in result_k
        ]

    @classmethod
    def from_texts(
        cls: Type["MemoryVectorStore"], 
        texts: List[str], 
        embedding: Embeddings,
        metadatas: Optional[List[dict]] = None,
        **kwargs: Any
    ) -> "MemoryVectorStore":
        """从文本列表构建向量数据库
        
        Args:
            texts: 文本列表
            embedding: 嵌入模型
            metadatas: 元数据列表
            **kwargs: 其他参数
            
        Returns:
            MemoryVectorStore实例
        """
        memory_vector_store = cls(embedding=embedding)
        memory_vector_store.add_texts(texts, metadatas, **kwargs)
        return memory_vector_store

    def delete(self, ids: Optional[List[str]] = None, **kwargs: Any) -> Optional[bool]:
        """删除指定ID的文档
        
        Args:
            ids: 要删除的文档ID列表
            **kwargs: 其他参数
            
        Returns:
            是否删除成功
        """
        if ids is None:
            return False
        
        for doc_id in ids:
            if doc_id in self.store:
                del self.store[doc_id]
        
        return True

    def get_by_ids(self, ids: List[str]) -> List[Document]:
        """根据ID获取文档
        
        Args:
            ids: 文档ID列表
            
        Returns:
            文档列表
        """
        documents = []
        for doc_id in ids:
            if doc_id in self.store:
                record = self.store[doc_id]
                documents.append(
                    Document(
                        page_content=record["text"],
                        metadata=record["metadata"]
                    )
                )
        return documents

    def clear(self):
        """清空所有数据"""
        self.store.clear()

    def count(self) -> int:
        """返回存储的文档数量"""
        return len(self.store)

    @staticmethod
    def _euclidean_distance(vec1: list, vec2: list) -> float:
        """计算两个向量的欧几里得距离
        
        Args:
            vec1: 向量1
            vec2: 向量2
            
        Returns:
            欧几里得距离
        """
        return float(np.linalg.norm(np.array(vec1) - np.array(vec2)))
