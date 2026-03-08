"""
工单系统工具
用于创建、查询和管理客服工单
"""

import json
import os
from datetime import datetime
from langchain.tools import tool
from typing import Optional
from coze_coding_utils.runtime_ctx.context import new_context
import uuid

# 工单文件路径
TICKETS_FILE = "/workspace/projects/assets/tickets.json"


def _load_tickets() -> list:
    """加载工单数据"""
    if not os.path.exists(TICKETS_FILE):
        return []

    with open(TICKETS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def _save_tickets(tickets: list):
    """保存工单数据"""
    os.makedirs(os.path.dirname(TICKETS_FILE), exist_ok=True)
    with open(TICKETS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tickets, f, ensure_ascii=False, indent=2)


@tool
def create_ticket(
    user_name: str,
    contact: str,
    issue_type: str,
    description: str,
    priority: str = "medium"
) -> str:
    """
    创建新的客服工单

    Args:
        user_name: 用户姓名
        contact: 联系方式（电话或邮箱）
        issue_type: 问题类型（产品咨询/订单问题/售后/投诉/其他）
        description: 问题描述
        priority: 优先级（low/medium/high/urgent）

    Returns:
        创建结果，包含工单号
    """
    ctx = new_context(method="create_ticket")

    try:
        tickets = _load_tickets()

        # 验证优先级
        valid_priorities = ["low", "medium", "high", "urgent"]
        if priority not in valid_priorities:
            priority = "medium"

        # 创建工单
        ticket = {
            "ticket_id": str(uuid.uuid4())[:8].upper(),
            "user_name": user_name,
            "contact": contact,
            "issue_type": issue_type,
            "description": description,
            "priority": priority,
            "status": "open",  # open, in_progress, resolved, closed
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "messages": [
                {
                    "role": "user",
                    "content": description,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            ],
            "assignee": None,
            "resolution": None
        }

        tickets.append(ticket)
        _save_tickets(tickets)

        return f"工单创建成功！\n工单号：{ticket['ticket_id']}\n状态：待处理\n我们会尽快处理您的问题。"

    except Exception as e:
        return f"创建工单失败：{str(e)}"


@tool
def get_ticket(ticket_id: str) -> str:
    """
    查询工单详情

    Args:
        ticket_id: 工单号

    Returns:
        工单详情
    """
    ctx = new_context(method="get_ticket")

    tickets = _load_tickets()

    for ticket in tickets:
        if ticket["ticket_id"] == ticket_id:
            return json.dumps(ticket, ensure_ascii=False, indent=2)

    return f"未找到工单号为 '{ticket_id}' 的工单"


@tool
def add_ticket_message(ticket_id: str, message: str, role: str = "user") -> str:
    """
    向工单添加消息

    Args:
        ticket_id: 工单号
        message: 消息内容
        role: 角色（user/agent）

    Returns:
        添加结果
    """
    ctx = new_context(method="add_ticket_message")

    tickets = _load_tickets()

    for ticket in tickets:
        if ticket["ticket_id"] == ticket_id:
            ticket["messages"].append({
                "role": role,
                "content": message,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            ticket["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            _save_tickets(tickets)
            return f"消息已添加到工单 {ticket_id}"

    return f"未找到工单号为 '{ticket_id}' 的工单"


@tool
def update_ticket_status(ticket_id: str, status: str, assignee: Optional[str] = None) -> str:
    """
    更新工单状态

    Args:
        ticket_id: 工单号
        status: 新状态（open/in_progress/resolved/closed）
        assignee: 处理人（可选）

    Returns:
        更新结果
    """
    ctx = new_context(method="update_ticket_status")

    tickets = _load_tickets()

    valid_statuses = ["open", "in_progress", "resolved", "closed"]

    for ticket in tickets:
        if ticket["ticket_id"] == ticket_id:
            if status not in valid_statuses:
                return f"无效的状态值，请使用: {', '.join(valid_statuses)}"

            ticket["status"] = status
            ticket["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if assignee:
                ticket["assignee"] = assignee

            _save_tickets(tickets)

            status_names = {
                "open": "待处理",
                "in_progress": "处理中",
                "resolved": "已解决",
                "closed": "已关闭"
            }

            return f"工单 {ticket_id} 状态已更新为：{status_names.get(status, status)}"

    return f"未找到工单号为 '{ticket_id}' 的工单"


@tool
def list_tickets(status_filter: Optional[str] = None) -> str:
    """
    列出工单列表

    Args:
        status_filter: 状态过滤器（可选）

    Returns:
        工单列表
    """
    ctx = new_context(method="list_tickets")

    tickets = _load_tickets()

    if status_filter:
        tickets = [t for t in tickets if t["status"] == status_filter]

    if not tickets:
        return "没有找到工单"

    # 简化输出
    simplified = [
        {
            "ticket_id": t["ticket_id"],
            "user_name": t["user_name"],
            "issue_type": t["issue_type"],
            "status": t["status"],
            "priority": t["priority"],
            "created_at": t["created_at"]
        }
        for t in tickets
    ]

    return json.dumps(simplified, ensure_ascii=False, indent=2)


@tool
def get_ticket_statistics() -> str:
    """
    获取工单统计信息

    Returns:
        统计数据
    """
    ctx = new_context(method="get_ticket_statistics")

    tickets = _load_tickets()

    total = len(tickets)

    status_count = {}
    for ticket in tickets:
        status = ticket["status"]
        status_count[status] = status_count.get(status, 0) + 1

    priority_count = {}
    for ticket in tickets:
        priority = ticket["priority"]
        priority_count[priority] = priority_count.get(priority, 0) + 1

    issue_type_count = {}
    for ticket in tickets:
        issue_type = ticket["issue_type"]
        issue_type_count[issue_type] = issue_type_count.get(issue_type, 0) + 1

    statistics = {
        "total_tickets": total,
        "status_distribution": status_count,
        "priority_distribution": priority_count,
        "issue_type_distribution": issue_type_count
    }

    return json.dumps(statistics, ensure_ascii=False, indent=2)
