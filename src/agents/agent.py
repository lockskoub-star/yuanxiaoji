"""
Agent 主逻辑
智能客服系统 - 元小吉
"""

import os
import json
from typing import Annotated
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from coze_coding_utils.runtime_ctx.context import default_headers
from storage.memory.memory_saver import get_memory_saver

# 导入所有工具
from tools.stream_run_tool import stream_run, stream_run_with_params
from tools.knowledge_base_tool import (
    search_knowledge,
    add_knowledge,
    list_categories,
    get_faq_by_category
)
from tools.analysis_tool import (
    analyze_user_intent,
    analyze_sentiment,
    should_transfer_to_human
)
from tools.ticket_tool import (
    create_ticket,
    get_ticket,
    add_ticket_message,
    update_ticket_status,
    list_tickets,
    get_ticket_statistics
)

# LLM 配置文件路径
LLM_CONFIG = "config/agent_llm_config.json"

# 默认保留最近 20 轮对话 (40 条消息)
MAX_MESSAGES = 40


def _windowed_messages(old, new):
    """滑动窗口: 只保留最近 MAX_MESSAGES 条消息"""
    return add_messages(old, new)[-MAX_MESSAGES:]  # type: ignore


class AgentState(MessagesState):
    messages: Annotated[list[AnyMessage], _windowed_messages]


def build_agent(ctx=None):
    """
    构建智能客服 Agent - 元小吉

    Args:
        ctx: 可选的上下文对象

    Returns:
        构建好的 Agent 实例
    """
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    config_path = os.path.join(workspace_path, LLM_CONFIG)

    # 读取配置文件
    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    # 获取环境变量中的 API 配置
    api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
    base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")

    # 初始化 LLM
    llm = ChatOpenAI(
        model=cfg['config'].get("model"),
        api_key=api_key,
        base_url=base_url,
        temperature=cfg['config'].get('temperature', 0.7),
        streaming=True,
        timeout=cfg['config'].get('timeout', 600),
        extra_body={
            "thinking": {
                "type": cfg['config'].get('thinking', 'disabled')
            }
        },
        default_headers=default_headers(ctx) if ctx else {}
    )

    # 定义所有工具列表
    tools = [
        # 流式接口工具
        stream_run,
        stream_run_with_params,

        # 知识库工具
        search_knowledge,
        add_knowledge,
        list_categories,
        get_faq_by_category,

        # 意图识别和情感分析工具
        analyze_user_intent,
        analyze_sentiment,
        should_transfer_to_human,

        # 工单系统工具
        create_ticket,
        get_ticket,
        add_ticket_message,
        update_ticket_status,
        list_tickets,
        get_ticket_statistics
    ]

    # 构建并返回 Agent
    return create_agent(
        model=llm,
        system_prompt=cfg.get("sp"),
        tools=tools,
        checkpointer=get_memory_saver(),
        state_schema=AgentState,
    )
