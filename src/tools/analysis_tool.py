"""
用户意图识别和情感分析工具
"""

import json
from langchain.tools import tool
from typing import Optional, Dict
from coze_coding_utils.runtime_ctx.context import new_context


@tool
def analyze_user_intent(user_message: str) -> str:
    """
    分析用户的意图

    Args:
        user_message: 用户的输入消息

    Returns:
        意图分析结果，包括意图类型、关键词等
    """
    ctx = new_context(method="analyze_user_intent")

    # 定义常见意图类型
    intent_categories = {
        "product_inquiry": "产品咨询",
        "order_query": "订单查询",
        "after_sales": "售后问题",
        "price_inquiry": "价格咨询",
        "shipping_inquiry": "物流咨询",
        "complaint": "投诉",
        "praise": "表扬",
        "greeting": "问候",
        "farewell": "道别",
        "unknown": "未知意图"
    }

    # 简单的意图识别逻辑（可以升级为使用 LLM）
    message_lower = user_message.lower()

    intent = "unknown"
    confidence = 0.5
    keywords = []

    # 基于关键词的意图识别
    intent_rules = {
        "product_inquiry": ["产品", "介绍", "推荐", "哪个好", "怎么样", "有什么", "详情"],
        "order_query": ["订单", "查询", "发货", "配送", "状态", "什么时候到"],
        "after_sales": ["退货", "退款", "换货", "质量问题", "坏了", "不满意"],
        "price_inquiry": ["价格", "多少钱", "贵", "便宜", "优惠", "折扣"],
        "shipping_inquiry": ["物流", "快递", "运费", "发货", "配送"],
        "complaint": ["投诉", "不负责", "差评", "不好", "垃圾", "骗人"],
        "praise": ["好", "棒", "优秀", "满意", "喜欢", "感谢"],
        "greeting": ["你好", "您好", "哈喽", "早上好", "下午好"],
        "farewell": ["再见", "拜拜", "谢谢", "结束"]
    }

    for intent_type, keywords_list in intent_rules.items():
        matched_keywords = [kw for kw in keywords_list if kw in message_lower]
        if matched_keywords:
            intent = intent_type
            confidence = min(0.5 + len(matched_keywords) * 0.1, 1.0)
            keywords = matched_keywords
            break

    result = {
        "intent": intent,
        "intent_name": intent_categories.get(intent, "未知"),
        "confidence": confidence,
        "keywords": keywords,
        "user_message": user_message
    }

    return json.dumps(result, ensure_ascii=False, indent=2)


@tool
def analyze_sentiment(user_message: str) -> str:
    """
    分析用户的情感倾向

    Args:
        user_message: 用户的输入消息

    Returns:
        情感分析结果，包括情感类型（积极/中性/消极）和情感强度
    """
    ctx = new_context(method="analyze_sentiment")

    message_lower = user_message

    # 情感关键词库
    positive_words = ["好", "棒", "优秀", "满意", "喜欢", "感谢", "不错", "赞", "开心", "高兴", "爱", "美丽", "漂亮", "舒服", "愉快"]
    negative_words = ["不好", "差", "垃圾", "糟糕", "生气", "难过", "失望", "讨厌", "烦", "烂", "问题", "投诉", "退货"]

    positive_count = sum(1 for word in positive_words if word in message_lower)
    negative_count = sum(1 for word in negative_words if word in message_lower)

    # 计算情感
    if positive_count > negative_count:
        sentiment = "positive"
        sentiment_name = "积极"
        intensity = min(positive_count * 0.2, 1.0)
    elif negative_count > positive_count:
        sentiment = "negative"
        sentiment_name = "消极"
        intensity = min(negative_count * 0.2, 1.0)
    else:
        sentiment = "neutral"
        sentiment_name = "中性"
        intensity = 0.0

    result = {
        "sentiment": sentiment,
        "sentiment_name": sentiment_name,
        "intensity": intensity,
        "positive_count": positive_count,
        "negative_count": negative_count,
        "user_message": user_message
    }

    return json.dumps(result, ensure_ascii=False, indent=2)


@tool
def should_transfer_to_human(user_message: str, intent_analysis: Optional[str] = None) -> str:
    """
    判断是否需要转接到人工客服

    Args:
        user_message: 用户的输入消息
        intent_analysis: 可选的意图分析结果

    Returns:
        是否需要转接的建议
    """
    ctx = new_context(method="should_transfer_to_human")

    # 需要转接的关键词
    transfer_keywords = ["人工", "客服", "转人工", "找不到", "不会用", "听不懂", "复杂", "紧急", "投诉"]

    message_lower = user_message.lower()

    # 检查是否包含转接关键词
    has_transfer_keyword = any(kw in message_lower for kw in transfer_keywords)

    # 如果有意图分析，检查是否为投诉或未知意图
    need_transfer = has_transfer_keyword

    if intent_analysis:
        try:
            intent_data = json.loads(intent_analysis)
            if intent_data.get("intent") in ["complaint", "unknown"]:
                need_transfer = True
        except:
            pass

    result = {
        "need_transfer": need_transfer,
        "reason": "用户要求转人工" if has_transfer_keyword else "识别为投诉或复杂问题" if need_transfer else "无需转接",
        "suggestion": "建议转接到人工客服" if need_transfer else "可以继续由 AI 处理"
    }

    return json.dumps(result, ensure_ascii=False, indent=2)
