"""
知识库工具
支持查询产品信息、FAQ等知识库内容
"""

import json
import os
from langchain.tools import tool
from typing import Optional, List
from coze_coding_utils.runtime_ctx.context import new_context

# 知识库文件路径
KNOWLEDGE_BASE_FILE = "/workspace/projects/assets/knowledge_base.json"


def _load_knowledge_base() -> dict:
    """加载知识库"""
    if not os.path.exists(KNOWLEDGE_BASE_FILE):
        return {"products": [], "faqs": []}

    with open(KNOWLEDGE_BASE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def _save_knowledge_base(data: dict):
    """保存知识库"""
    os.makedirs(os.path.dirname(KNOWLEDGE_BASE_FILE), exist_ok=True)
    with open(KNOWLEDGE_BASE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@tool
def search_knowledge(query: str) -> str:
    """
    在知识库中搜索相关信息

    Args:
        query: 搜索关键词或问题

    Returns:
        匹配的知识库内容
    """
    ctx = new_context(method="search_knowledge")

    kb = _load_knowledge_base()

    results = []

    # 搜索产品信息
    for product in kb.get("products", []):
        product_text = f"{product.get('name', '')} {product.get('description', '')} {product.get('category', '')}"
        if query.lower() in product_text.lower():
            results.append({
                "type": "product",
                "name": product.get("name"),
                "description": product.get("description"),
                "price": product.get("price"),
                "category": product.get("category")
            })

    # 搜索 FAQ
    for faq in kb.get("faqs", []):
        faq_text = f"{faq.get('question', '')} {faq.get('answer', '')}"
        if query.lower() in faq_text.lower():
            results.append({
                "type": "faq",
                "question": faq.get("question"),
                "answer": faq.get("answer"),
                "category": faq.get("category")
            })

    if not results:
        return f"未找到与'{query}'相关的信息。建议：\n1. 尝试使用其他关键词\n2. 联系人工客服\n3. 记录为待解决问题"

    return json.dumps(results, ensure_ascii=False, indent=2)


@tool
def add_knowledge(
    knowledge_type: str,
    content: str,
    category: Optional[str] = None
) -> str:
    """
    向知识库添加新知识

    Args:
        knowledge_type: 知识类型 (product 或 faq)
        content: 知识内容（JSON格式字符串）
        category: 分类标签

    Returns:
        添加结果
    """
    ctx = new_context(method="add_knowledge")

    try:
        kb = _load_knowledge_base()

        if knowledge_type == "product":
            product_data = json.loads(content)
            product_data["category"] = category or "未分类"
            kb.setdefault("products", []).append(product_data)
        elif knowledge_type == "faq":
            faq_data = json.loads(content)
            faq_data["category"] = category or "未分类"
            kb.setdefault("faqs", []).append(faq_data)
        else:
            return f"错误：不支持的知识类型 '{knowledge_type}'，请使用 'product' 或 'faq'"

        _save_knowledge_base(kb)
        return f"成功添加{knowledge_type}到知识库"

    except json.JSONDecodeError:
        return "错误：content 参数必须是有效的 JSON 格式"
    except Exception as e:
        return f"添加知识时发生错误: {str(e)}"


@tool
def list_categories() -> str:
    """
    列出知识库中的所有分类

    Returns:
        分类列表
    """
    ctx = new_context(method="list_categories")

    kb = _load_knowledge_base()

    categories = set()

    # 收集产品分类
    for product in kb.get("products", []):
        if product.get("category"):
            categories.add(product["category"])

    # 收集 FAQ 分类
    for faq in kb.get("faqs", []):
        if faq.get("category"):
            categories.add(faq["category"])

    if not categories:
        return "知识库暂无分类"

    return json.dumps(list(categories), ensure_ascii=False, indent=2)


@tool
def get_faq_by_category(category: str) -> str:
    """
    获取指定分类下的所有 FAQ

    Args:
        category: 分类名称

    Returns:
        该分类下的 FAQ 列表
    """
    ctx = new_context(method="get_faq_by_category")

    kb = _load_knowledge_base()

    faqs = [faq for faq in kb.get("faqs", []) if faq.get("category") == category]

    if not faqs:
        return f"分类 '{category}' 下没有 FAQ"

    return json.dumps(faqs, ensure_ascii=False, indent=2)


# 初始化一些示例数据
def _init_sample_data():
    """初始化示例数据"""
    if not os.path.exists(KNOWLEDGE_BASE_FILE):
        sample_data = {
            "products": [
                {
                    "name": "沉香线香",
                    "description": "天然沉香制作，香气醇厚持久",
                    "price": "¥299",
                    "category": "香品"
                },
                {
                    "name": "檀香线香",
                    "description": "精选檀香木，清香怡人",
                    "price": "¥199",
                    "category": "香品"
                },
                {
                    "name": "香插",
                    "description": "手工制作陶瓷香插",
                    "price": "¥59",
                    "category": "配件"
                }
            ],
            "faqs": [
                {
                    "question": "如何使用沉香线香？",
                    "answer": "点燃线香一端，将燃烧端插入香插中，静置即可。注意远离易燃物品。",
                    "category": "使用方法"
                },
                {
                    "question": "沉香线香能燃烧多久？",
                    "answer": "通常一根沉香线香可以燃烧30-45分钟。",
                    "category": "产品信息"
                },
                {
                    "question": "如何储存香品？",
                    "answer": "请存放在阴凉干燥处，避免阳光直射和潮湿环境。建议密封保存。",
                    "category": "储存方法"
                },
                {
                    "question": "支持哪些支付方式？",
                    "answer": "支持微信支付、支付宝、银行卡支付。",
                    "category": "订单支付"
                },
                {
                    "question": "如何申请退款？",
                    "answer": "收到商品后7天内，如有质量问题可申请退款。请联系客服并提供订单号和问题照片。",
                    "category": "售后问题"
                }
            ]
        }
        _save_knowledge_base(sample_data)


# 初始化示例数据
_init_sample_data()
