# 🤖 元小吉智能客服

> 基于 Coze 平台的智能客服系统，支持多渠道接入、知识库管理和工单系统

---

## ✨ 特性

- 🤖 **多模型支持**：集成豆包大模型，支持智能对话
- 🔍 **知识库集成**：扣子知识库 + 本地向量库，双重知识增强
- 💬 **多渠道接入**：支持豆包、微信、网站、API 等多种渠道
- 🎭 **意图识别**：自动识别用户意图，精准回复
- 😊 **情感分析**：分析用户情绪，智能调整回复策略
- 📝 **工单系统**：自动创建和跟踪工单
- 🚀 **流式响应**：支持实时流式对话
- 🌐 **公网访问**：支持多种部署方案

---

## 🚀 快速开始

### 方式1：本地运行（推荐）

```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 访问 API 文档
open http://localhost:8000/docs
```

### 方式2：公网访问（5分钟）

```bash
# 1. 启动服务
docker-compose up -d

# 2. 使用内网穿透
npx localtunnel --port 8000 --subdomain yuanxiaoji

# 3. 访问公网地址
# 会显示：your url is: https://yuanxiaoji.loca.lt
```

**详细教程：** 查看 [公网访问指南](docs/PUBLIC_ACCESS_GUIDE.md)

---

## 📱 公网访问

### 当前公网地址

```
https://yuanxiaoji.loca.lt
```

### 访问方式

#### API 文档
```
https://yuanxiaoji.loca.lt/docs
```

#### 健康检查
```
GET https://yuanxiaoji.loca.lt/health
```

#### 对话接口
```
POST https://yuanxiaoji.loca.lt/chat
Content-Type: application/json

{
  "message": "你好"
}
```

**更多方案：** 查看 [公网访问成功指南](docs/PUBLIC_ACCESS_SUCCESS.md)

---

## 🛠️ 技术栈

- **Python**：3.11+
- **Web 框架**：FastAPI
- **Agent 框架**：LangChain + LangGraph
- **大模型**：豆包（doubao-seed-1-6-251015）
- **容器化**：Docker + Docker Compose
- **反向代理**：Nginx
- **WSGI 服务器**：Gunicorn

---

## 📁 项目结构

```
.
├── config/                       # 配置文件
│   └── agent_llm_config.json     # 模型配置
├── docs/                         # 文档
│   ├── PUBLIC_ACCESS_GUIDE.md    # 公网访问指南
│   ├── QUICK_PUBLIC_DEPLOYMENT.md # 快速部署教程
│   └── PUBLIC_ACCESS_SUCCESS.md  # 公网访问成功指南
├── scripts/                      # 脚本
│   ├── public_access.sh          # 公网访问部署脚本
│   └── quick_public.sh           # 快速启动脚本
├── src/                          # 源代码
│   ├── agents/                   # Agent 代码
│   │   └── agent.py              # 主 Agent 逻辑
│   ├── tools/                    # 工具定义
│   │   ├── coze_knowledge_tool.py     # 扣子知识库
│   │   ├── multi_channel_tool.py      # 多渠道管理
│   │   ├── knowledge_base_tool.py     # 本地知识库
│   │   ├── analysis_tool.py           # 意图识别和情感分析
│   │   └── ticket_tool.py             # 工单系统
│   ├── storage/                   # 存储
│   │   └── memory/                # 记忆存储
│   ├── utils/                     # 工具函数
│   └── api_server.py              # FastAPI 服务
├── assets/                       # 资源文件
├── tests/                        # 测试文件
├── Dockerfile                    # Docker 镜像
├── docker-compose.yml            # Docker Compose 配置
├── nginx.conf                    # Nginx 配置
├── gunicorn_config.py            # Gunicorn 配置
└── requirements.txt              # Python 依赖
```

---

## 🧪 测试

### 本地测试

```bash
# 测试健康检查
curl http://localhost:8000/health

# 测试对话
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'
```

### 公网测试

```bash
# 测试健康检查
curl https://yuanxiaoji.loca.lt/health

# 测试对话
curl -X POST https://yuanxiaoji.loca.lt/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'
```

---

## 🔧 配置

### 环境变量

创建 `.env` 文件：

```env
# API 配置
API_HOST=0.0.0.0
API_PORT=8000

# 豆包模型配置
COZE_WORKLOAD_IDENTITY_API_KEY=your_api_key
COZE_INTEGRATION_MODEL_BASE_URL=your_base_url

# 可选配置
LOG_LEVEL=INFO
MAX_MESSAGE_HISTORY=20
```

### 模型配置

编辑 `config/agent_llm_config.json`：

```json
{
    "config": {
        "model": "doubao-seed-1-6-251015",
        "temperature": 0.7,
        "top_p": 0.9,
        "max_completion_tokens": 10000,
        "timeout": 600,
        "thinking": "disabled"
    },
    "sp": "你是元小吉，一个智能客服助手...",
    "tools": []
}
```

---

## 📚 文档

- [公网访问指南](docs/PUBLIC_ACCESS_GUIDE.md) - 详细的公网部署方案
- [快速部署教程](docs/QUICK_PUBLIC_DEPLOYMENT.md) - 5分钟快速部署
- [公网访问成功指南](docs/PUBLIC_ACCESS_SUCCESS.md) - 当前公网地址和使用方法

---

## 🌐 公网部署方案

### 方案1：ngrok（快速测试）

```bash
# 1. 注册并获取 authtoken
# https://ngrok.com/signup

# 2. 安装 ngrok
wget https://bin.equinox.io/c/bNyj1mQVY4c/v3/ngrok-linux-amd64.zip
unzip ngrok-linux-amd64.zip
chmod +x ngrok
./ngrok config add-authtoken YOUR_TOKEN

# 3. 启动
./ngrok http 8000
```

### 方案2：Railway（免费生产环境）

1. 访问 https://railway.app
2. 新建项目，连接 GitHub
3. 配置环境变量
4. 部署完成

### 方案3：云服务器（稳定生产环境）

- 阿里云 ECS：https://www.aliyun.com/product/ecs
- 腾讯云 CVM：https://cloud.tencent.com/product/cvm

详细步骤：查看 [公网访问指南](docs/PUBLIC_ACCESS_GUIDE.md)

---

## 🔍 常见问题

### Q1: 如何重启服务？

```bash
# 重启所有服务
docker-compose restart

# 重启 API 服务
docker-compose restart api

# 查看日志
docker-compose logs -f api
```

### Q2: 如何查看服务状态？

```bash
# 查看容器状态
docker-compose ps

# 查看健康状态
curl http://localhost:8000/health
```

### Q3: 公网地址不固定怎么办？

**解决方案：**
1. 使用 Railway（固定域名）
2. 购买域名并配置 DNS
3. 使用 ngrok 付费版（固定域名）

### Q4: 如何添加新的工具？

1. 在 `src/tools/` 中创建新的工具文件
2. 使用 `@tool` 装饰器定义工具函数
3. 在 `src/agents/agent.py` 中注册工具
4. 重启服务

---

## 📞 支持

如有问题，请查看：
- [项目文档](docs/)
- [公网访问指南](docs/PUBLIC_ACCESS_GUIDE.md)
- [快速部署教程](docs/QUICK_PUBLIC_DEPLOYMENT.md)

---

## 📝 更新日志

### v1.0.0 (2025-03-08)

- ✅ 初始版本发布
- ✅ 集成豆包大模型
- ✅ 支持多渠道接入
- ✅ 实现知识库管理
- ✅ 支持工单系统
- ✅ 实现意图识别和情感分析
- ✅ 支持流式对话
- ✅ 提供公网访问
- ✅ Docker 容器化部署

---

## 📄 许可证

MIT License

---

## 🙏 致谢

感谢 Coze 平台提供的强大支持！

---

**🎉 立即体验：[https://yuanxiaoji.loca.lt/docs](https://yuanxiaoji.loca.lt/docs)**
