"""
扣子知识库工具
支持从扣子知识库导入和搜索文档
"""

import json
from langchain.tools import tool
from typing import Optional, List
from coze_coding_utils.runtime_ctx.context import new_context, Context
from coze_coding_dev_sdk import KnowledgeClient, Config, KnowledgeDocument, DataSourceType, ChunkConfig


@tool
def add_document_to_knowledge(content: str, source_type: str = "text", url: Optional[str] = None) -> str:
    """
    添加文档到扣子知识库

    Args:
        content: 文档内容（文本内容）
        source_type: 来源类型 (text/url/uri)
        url: 如果是url类型，需要提供url

    Returns:
        添加结果
    """
    ctx = new_context(method="add_document_to_knowledge")

    try:
        config = Config()
        client = KnowledgeClient(config=config, ctx=ctx)

        # 确定数据源类型
        if source_type == "url":
            if not url:
                return "错误：URL类型必须提供url参数"
            doc = KnowledgeDocument(
                source=DataSourceType.URL,
                url=url
            )
        else:
            doc = KnowledgeDocument(
                source=DataSourceType.TEXT,
                raw_data=content
            )

        # 配置分块策略
        chunk_config = ChunkConfig(
            separator="\n",
            max_tokens=2000,
            remove_extra_spaces=True
        )

        # 添加文档
        response = client.add_documents(
            documents=[doc],
            table_name="coze_doc_knowledge",
            chunk_config=chunk_config
        )

        if response.code == 0:
            return f"成功添加文档到知识库！\n文档ID: {', '.join(response.doc_ids)}"
        else:
            return f"添加文档失败: {response.msg}"

    except Exception as e:
        return f"添加文档时发生错误: {str(e)}"


@tool
def search_coze_knowledge(query: str, top_k: int = 5, min_score: float = 0.0) -> str:
    """
    在扣子知识库中搜索相关信息

    Args:
        query: 搜索关键词或问题
        top_k: 返回结果数量（默认5）
        min_score: 最小相似度阈值（0.0-1.0）

    Returns:
        搜索结果
    """
    ctx = new_context(method="search_coze_knowledge")

    try:
        config = Config()
        client = KnowledgeClient(config=config, ctx=ctx)

        # 搜索知识库
        response = client.search(
            query=query,
            table_names=None,  # 搜索所有数据集
            top_k=top_k,
            min_score=min_score
        )

        if response.code == 0:
            if not response.chunks:
                return f"未找到与'{query}'相关的信息"

            results = []
            for i, chunk in enumerate(response.chunks):
                results.append({
                    "rank": i + 1,
                    "score": f"{chunk.score:.4f}",
                    "content": chunk.content[:500] + "..." if len(chunk.content) > 500 else chunk.content,
                    "doc_id": chunk.doc_id
                })

            return json.dumps(results, ensure_ascii=False, indent=2)
        else:
            return f"搜索失败: {response.msg}"

    except Exception as e:
        return f"搜索时发生错误: {str(e)}"


@tool
def import_url_to_knowledge(url: str) -> str:
    """
    导入网页内容到知识库

    Args:
        url: 网页URL

    Returns:
        导入结果
    """
    ctx = new_context(method="import_url_to_knowledge")

    try:
        config = Config()
        client = KnowledgeClient(config=config, ctx=ctx)

        doc = KnowledgeDocument(
            source=DataSourceType.URL,
            url=url
        )

        chunk_config = ChunkConfig(
            separator="\n",
            max_tokens=2000,
            remove_extra_spaces=True
        )

        response = client.add_documents(
            documents=[doc],
            table_name="coze_doc_knowledge",
            chunk_config=chunk_config
        )

        if response.code == 0:
            return f"成功导入网页到知识库！\n文档ID: {', '.join(response.doc_ids)}"
        else:
            return f"导入网页失败: {response.msg}"

    except Exception as e:
        return f"导入网页时发生错误: {str(e)}"


@tool
def import_text_to_knowledge(text: str, title: Optional[str] = None) -> str:
    """
    导入文本内容到知识库

    Args:
        text: 文本内容
        title: 文档标题（可选）

    Returns:
        导入结果
    """
    ctx = new_context(method="import_text_to_knowledge")

    try:
        config = Config()
        client = KnowledgeClient(config=config, ctx=ctx)

        # 如果有标题，添加到文本前面
        if title:
            full_text = f"# {title}\n\n{text}"
        else:
            full_text = text

        doc = KnowledgeDocument(
            source=DataSourceType.TEXT,
            raw_data=full_text
        )

        chunk_config = ChunkConfig(
            separator="\n\n",
            max_tokens=1500,
            remove_extra_spaces=True
        )

        response = client.add_documents(
            documents=[doc],
            table_name="coze_doc_knowledge",
            chunk_config=chunk_config
        )

        if response.code == 0:
            return f"成功导入文本到知识库！\n文档ID: {', '.join(response.doc_ids)}"
        else:
            return f"导入文本失败: {response.msg}"

    except Exception as e:
        return f"导入文本时发生错误: {str(e)}"
