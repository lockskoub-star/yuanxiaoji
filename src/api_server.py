"""
元小吉对话 API 服务
提供 HTTP 接口，可以直接调用元小吉进行对话
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.stream_run_tool import stream_run

# 创建 FastAPI 应用
app = FastAPI(
    title="元小吉对话 API",
    description="直接与元小吉进行对话的 Web 服务",
    version="1.0.0"
)

# 添加 CORS 中间件，允许跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源（生产环境应限制）
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)


# 定义请求和响应模型
class ChatRequest(BaseModel):
    """聊天请求模型"""
    message: str  # 用户的消息


class ChatResponse(BaseModel):
    """聊天响应模型"""
    success: bool  # 是否成功
    reply: str  # 元小吉的回复
    raw_data: str  # 原始返回数据（调试用）


@app.get("/")
async def root():
    """根路径，返回 API 信息"""
    return {
        "service": "元小吉对话 API",
        "version": "1.0.0",
        "endpoints": {
            "POST /chat": "发送消息给元小吉",
            "GET /health": "健康检查"
        },
        "usage": {
            "example": "POST /chat with JSON body: {\"message\": \"你好\"}"
        }
    }


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "service": "元小吉对话 API"
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    与元小吉对话

    Args:
        request: 包含用户消息的请求

    Returns:
        ChatResponse: 包含元小吉回复的响应

    Example:
        >>> POST /chat
        >>> {"message": "你好"}
        <<< {"success": true, "reply": "你好呀！...", "raw_data": "..."}
    """
    try:
        # 调用 stream_run 工具
        result = stream_run(message=request.message)

        # 解析结果，提取元小吉的回复
        import json
        import re

        # 从返回数据中提取机器人回复
        reply_text = ""

        # 尝试查找 "机器人回复：" 后面的内容
        match = re.search(r'机器人回复：(.*?)(?:\n\n|\n\*\*|$)', result, re.DOTALL)
        if match:
            reply_text = match.group(1).strip()
        else:
            # 如果找不到，返回原始结果
            reply_text = "解析失败，原始结果：\n" + result

        return ChatResponse(
            success=True,
            reply=reply_text,
            raw_data=result
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"处理请求时发生错误: {str(e)}"
        )


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    与元小吉对话（流式返回）

    这个接口会返回原始的流式数据，适合需要自己处理流式响应的场景

    Args:
        request: 包含用户消息的请求

    Returns:
        dict: 包含完整的流式响应数据
    """
    try:
        # 调用 stream_run 工具
        result = stream_run(message=request.message)

        return {
            "success": True,
            "message": request.message,
            "result": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"处理请求时发生错误: {str(e)}"
        )


def start_server(host: str = "0.0.0.0", port: int = 8001):
    """
    启动 API 服务器

    Args:
        host: 监听的主机地址
        port: 监听的端口号
    """
    print(f"""
    ╔════════════════════════════════════════╗
    ║   元小吉对话 API 服务已启动           ║
    ╠════════════════════════════════════════╣
    ║  本地访问: http://localhost:{port}       ║
    ║  API 文档: http://localhost:{port}/docs  ║
    ║  对话接口: POST http://localhost:{port}/chat ║
    ╚════════════════════════════════════════╝
    """)

    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )


if __name__ == "__main__":
    start_server()
