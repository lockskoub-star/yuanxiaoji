"""
流式调用 Coze 接口的工具
支持向 Coze 流式执行接口发送请求并实时获取结果
"""

import requests
import json
from langchain.tools import tool
from typing import Optional
from coze_coding_utils.runtime_ctx.context import new_context

# Coze 流式接口配置
STREAM_RUN_URL = "https://89z3fffv3y.coze.site/stream_run"
ACCESS_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjhiYzM2M2UzLTE3N2YtNDc4OC05NDBiLTIzOWRjY2ZjNmE2ZCJ9.eyJpc3MiOiJodHRwczovL2FwaS5jb3plLmNuIiwiYXVkIjpbIndOVDJNRld2OHpBTFZ5VVNxTU9wQ003RDV6elZnNDFqIl0sImV4cCI6ODIxMDI2Njg3Njc5OSwiaWF0IjoxNzcyNzkwMjkzLCJzdWIiOiJzcGlmZmU6Ly9hcGkuY296ZS5jbi93b3JrbG9hZF9pZGVudGl0eS9pZDo3NjEyNTcwMTc3MTA3OTE4ODQ4Iiwic3JjIjoiaW5ib3VuZF9hdXRoX2FjY2Vzc190b2tlbl9pZDo3NjE0MDc2MzM0NDA2MzY5MzE2In0.N5FdfGAZ6O4-I8qEzRvqEZOOrshXEJWDGYqFuZhheBJTBOkveVaXH6q9r1riqvv56P8a3B0a_m9Z9zZt4Y4X6m85YL61k4L4SY-l_HuppK3m-XUjh-YPc00_us6da26GhFMG6UDdhphj5fHCUbx0Xmyp6uaZVUxew4F2zLOOeUCw_F1egauvCUrbrA-_G2rR7oWbMpaUMKVoeZkccxxtI9yDrtYX4XZnc-Xp3KDTyAX4T2ls-HtjXfZCbpERoQDZPMSX-BIW-PwfCdJS_DdgTu5gzOqM6aiXSbORFHZW0TNh0PeZW4uYoTqQFNHZhqbJrzkF4yTIHvREVJxbF1kMnA"


@tool
def stream_run(message: str) -> str:
    """
    调用 Coze 流式执行接口，发送消息并获取处理结果

    Args:
        message: 要发送给 Coze 接口的消息内容

    Returns:
        接口返回的完整响应内容（流式输出的汇总）
    """
    ctx = new_context(method="stream_run")

    try:
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }

        # 构建请求参数
        payload = {
            "message": message,
            "stream": True,
        }

        response = requests.post(
            STREAM_RUN_URL,
            headers=headers,
            json=payload,
            timeout=60,
            stream=True,
        )

        if response.status_code != 200:
            return f"接口调用失败: HTTP {response.status_code} - {response.text}"

        # 收集流式输出
        full_content = []
        for line in response.iter_lines(decode_unicode=True):
            if line and line.startswith("data:"):
                try:
                    data_str = line[5:].strip()  # 移除 "data:" 前缀
                    if data_str == "[DONE]":
                        break
                    data = json.loads(data_str)
                    full_content.append(json.dumps(data, ensure_ascii=False))
                except json.JSONDecodeError:
                    continue

        if not full_content:
            return "接口调用成功，但没有返回数据"

        return f"流式执行成功！\n\n返回数据：\n{json.dumps(full_content, ensure_ascii=False, indent=2)}"

    except requests.exceptions.Timeout:
        return "接口调用超时，请稍后重试"
    except requests.exceptions.RequestException as e:
        return f"接口调用异常: {str(e)}"
    except Exception as e:
        return f"处理结果时发生错误: {str(e)}"


@tool
def stream_run_with_params(
    message: str,
    bot_id: Optional[str] = None,
    conversation_id: Optional[str] = None
) -> str:
    """
    调用 Coze 流式执行接口，支持自定义参数

    Args:
        message: 要发送的消息内容
        bot_id: 可选的机器人ID
        conversation_id: 可选的对话ID（用于保持会话上下文）

    Returns:
        接口返回的完整响应内容
    """
    ctx = new_context(method="stream_run_with_params")

    try:
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }

        # 构建请求参数
        payload = {
            "message": message,
            "stream": True,
        }

        # 添加可选参数
        if bot_id:
            payload["bot_id"] = bot_id
        if conversation_id:
            payload["conversation_id"] = conversation_id

        response = requests.post(
            STREAM_RUN_URL,
            headers=headers,
            json=payload,
            timeout=60,
            stream=True,
        )

        if response.status_code != 200:
            return f"接口调用失败: HTTP {response.status_code} - {response.text}"

        # 收集流式输出
        full_content = []
        event_data = {"message": message, "response_chunks": []}

        for line in response.iter_lines(decode_unicode=True):
            if line and line.startswith("data:"):
                try:
                    data_str = line[5:].strip()
                    if data_str == "[DONE]":
                        break
                    data = json.loads(data_str)
                    event_data["response_chunks"].append(data)
                except json.JSONDecodeError:
                    continue

        if not event_data["response_chunks"]:
            return "接口调用成功，但没有返回数据"

        return f"流式执行成功！\n\n完整响应：\n{json.dumps(event_data, ensure_ascii=False, indent=2)}"

    except requests.exceptions.Timeout:
        return "接口调用超时，请稍后重试"
    except requests.exceptions.RequestException as e:
        return f"接口调用异常: {str(e)}"
    except Exception as e:
        return f"处理结果时发生错误: {str(e)}"
