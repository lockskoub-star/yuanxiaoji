"""
多渠道消息管理工具
支持豆包、微信等多渠道接入
"""

import json
from langchain.tools import tool
from typing import Optional, Dict
from coze_coding_utils.runtime_ctx.context import new_context
from coze_coding_dev_sdk import LLMClient
from langchain_core.messages import HumanMessage


@tool
def chat_with_doubao(message: str, history: Optional[str] = None) -> str:
    """
    使用豆包大模型进行对话

    Args:
        message: 用户消息
        history: 可选的对话历史（JSON字符串）

    Returns:
        豆包的回复
    """
    ctx = new_context(method="chat_with_doubao")

    try:
        client = LLMClient(ctx=ctx)

        # 构建消息列表
        messages = [HumanMessage(content=message)]

        # 如果有历史记录，添加到消息中
        if history:
            try:
                history_data = json.loads(history)
                for item in history_data:
                    if item.get("role") == "user":
                        messages.append(HumanMessage(content=item.get("content")))
            except:
                pass

        # 调用豆包
        response = client.invoke(
            messages=messages,
            model="doubao-seed-1-6-251015",
            temperature=0.7
        )

        # 处理响应内容
        if isinstance(response.content, str):
            return response.content
        elif isinstance(response.content, list):
            if response.content and isinstance(response.content[0], str):
                return " ".join(response.content)
            else:
                text_parts = [item.get("text", "") for item in response.content if isinstance(item, dict)]
                return " ".join(text_parts)
        else:
            return str(response.content)

    except Exception as e:
        return f"豆包对话出错: {str(e)}"


@tool
def get_channel_config(channel: str) -> str:
    """
    获取渠道配置信息

    Args:
        channel: 渠道名称 (doubao/wechat/website)

    Returns:
        渠道配置信息
    """
    ctx = new_context(method="get_channel_config")

    channel_configs = {
        "doubao": {
            "name": "豆包大模型",
            "status": "已启用",
            "model": "doubao-seed-1-6-251015",
            "features": ["文本对话", "多轮对话", "流式输出", "知识库增强"]
        },
        "wechat": {
            "name": "微信机器人",
            "status": "需要配置",
            "features": ["文本消息", "图片消息", "文件发送", "@通知"]
        },
        "website": {
            "name": "网站聊天",
            "status": "已启用",
            "features": ["实时聊天", "知识库查询", "工单创建", "多轮对话"]
        }
    }

    config = channel_configs.get(channel.lower())

    if not config:
        return f"未找到渠道 '{channel}' 的配置信息"

    return json.dumps(config, ensure_ascii=False, indent=2)


@tool
def list_available_channels() -> str:
    """
    列出所有可用渠道

    Returns:
        渠道列表
    """
    ctx = new_context(method="list_available_channels")

    channels = [
        {
            "id": "doubao",
            "name": "豆包大模型",
            "status": "active",
            "description": "使用豆包AI进行智能对话"
        },
        {
            "id": "wechat",
            "name": "微信机器人",
            "status": "pending_config",
            "description": "企业微信机器人，支持多种消息类型"
        },
        {
            "id": "website",
            "name": "网站聊天",
            "status": "active",
            "description": "Web端实时聊天接口"
        },
        {
            "id": "api",
            "name": "API接口",
            "status": "active",
            "description": "RESTful API，支持第三方集成"
        }
    ]

    return json.dumps(channels, ensure_ascii=False, indent=2)


@tool
def send_to_channel(channel: str, message: str, user_id: Optional[str] = None) -> str:
    """
    发送消息到指定渠道

    Args:
        channel: 渠道名称
        message: 消息内容
        user_id: 用户ID（可选）

    Returns:
        发送结果
    """
    ctx = new_context(method="send_to_channel")

    if channel == "doubao":
        # 使用豆包处理
        result = chat_with_doubao(message=message)
        return f"【豆包回复】\n{result}"
    elif channel == "wechat":
        # 微信需要额外配置
        return f"微信渠道需要先配置webhook。请使用企业微信后台获取webhook地址。"
    elif channel == "website":
        # 网站渠道，返回消息内容
        return f"【网站消息】\n用户 {user_id or '匿名'} 的消息: {message}\n\n待处理..."
    else:
        return f"不支持的渠道: {channel}"


@tool
def get_integration_guide(integration_type: str) -> str:
    """
    获取集成指南

    Args:
        integration_type: 集成类型 (doubao/wechat)

    Returns:
        集成指南
    """
    ctx = new_context(method="get_integration_guide")

    guides = {
        "doubao": """
# 豆包集成指南

## 使用方式
豆包已经内置在系统中，无需额外配置。

## 可用功能
1. 智能对话
2. 知识库增强
3. 多轮对话
4. 流式输出

## API调用
直接使用 `chat_with_doubao` 工具即可。
        """,
        "wechat": """
# 微信机器人集成指南

## 步骤1：配置企业微信机器人
1. 登录企业微信后台
2. 进入"群机器人"管理
3. 添加机器人，获取webhook地址
4. 配置webhook地址到环境变量

## 步骤2：配置环境变量
在扣子后台配置以下环境变量：
- WECHAT_ROBOT_WEBHOOK_KEY: webhook密钥

## 步骤3：测试
使用微信发送消息到机器人群，查看是否收到回复。

## 可用功能
1. 文本消息
2. 图片消息
3. 文件发送
4. @通知

## 注意事项
- webhook地址不要泄露
- 消息发送频率有限制
- 支持Markdown格式
        """,
        "coze_knowledge": """
# 扣子知识库集成指南

## 使用方式
扣子知识库已自动集成到系统中。

## 可用功能
1. 文档导入
2. 网页抓取
3. 语义搜索
4. 向量检索

## API调用
- `add_document_to_knowledge`: 添加文档
- `search_coze_knowledge`: 搜索知识库
- `import_url_to_knowledge`: 导入网页
- `import_text_to_knowledge`: 导入文本

## 在扣子后台添加资料库
1. 登录扣子后台
2. 进入"知识库"管理
3. 创建新的知识库
4. 上传文档或添加URL
5. 系统会自动向量化和索引

## 注意事项
- 文档会被自动分块
- 支持PDF、Word、网页等多种格式
- 搜索时会返回相关度和内容
        """
    }

    guide = guides.get(integration_type.lower())

    if not guide:
        return f"未找到 '{integration_type}' 的集成指南"

    return guide
