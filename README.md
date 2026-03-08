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
- 🌐 **公网访问**：支持多种部署方案（ngrok、Railway、云服务器）

---

## 🚀 快速开始

### 方式1：本地运行

```bash
# 启动服务
python src/main.py

# 访问 API 文档
open http://localhost:5000/docs
```

### 方式2：Railway 部署（推荐，免费且稳定）

**10分钟获得固定公网地址！**

查看快速部署教程：[Railway 快速部署](docs/RAILWAY_QUICK_START.md)

**完整文档：** [Railway 部署指南](docs/RAILWAY_DEPLOYMENT_GUIDE.md)

### 方式3：ngrok 部署（快速测试）

```bash
# 1. 注册并获取 authtoken
# https://ngrok.com/signup

# 2. 安装 ngrok
wget https://bin.equinox.io/c/bNyj1mQVY4c/v3/ngrok-linux-amd64.zip
unzip ngrok-linux-amd64.zip
chmod +x ngrok
./ngrok config add-authtoken YOUR_TOKEN

# 3. 启动
./ngrok http 5000
```

**更多部署方案：** [公网访问指南](docs/PUBLIC_ACCESS_GUIDE.md)

---

## 📱 部署方案对比

| 方案 | 时间 | 费用 | 稳定性 | 固定域名 | 推荐度 |
|------|------|------|--------|---------|--------|
| **Railway** | 10分钟 | 免费（$5/月额度） | ⭐⭐⭐⭐⭐ | ✅ 是 | ⭐⭐⭐⭐⭐ |
| ngrok | 5分钟 | 免费（有限制） | ⭐⭐⭐⭐ | ❌ 否 | ⭐⭐⭐⭐ |
| 云服务器 | 30分钟 | ¥150/月起 | ⭐⭐⭐⭐⭐ | ✅ 是 | ⭐⭐⭐ |

**强烈推荐使用 Railway！**

---

## 📁 项目结构

```
.
├── config/                       # 配置文件
│   └── agent_llm_config.json     # 模型配置
├── docs/                         # 文档
│   ├── RAILWAY_QUICK_START.md    # Railway 快速部署
│   ├── RAILWAY_DEPLOYMENT_GUIDE.md # Railway 详细指南
│   ├── PUBLIC_ACCESS_GUIDE.md    # 公网访问指南
│   └── QUICK_PUBLIC_DEPLOYMENT.md # 快速部署教程
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
│   ├── utils/                     # 工具函数
│   ├── api_server.py              # FastAPI 服务
│   └── main.py                    # 主入口
├── Dockerfile                    # Docker 镜像
├── docker-compose.yml            # Docker Compose 配置
├── Procfile                      # Railway 启动配置
├── railway.toml                  # Railway 项目配置
├── gunicorn_config.py            # Gunicorn 配置
└── requirements.txt              # Python 依赖
```

---

## 🛠️ 技术栈

- **Python**：3.11+
- **Web 框架**：FastAPI
- **Agent 框架**：LangChain + LangGraph
- **大模型**：豆包（doubao-seed-1-6-251015）
- **容器化**：Docker
- **部署平台**：Railway / ngrok / 云服务器

---

## 🧪 测试

### 本地测试

```bash
# 健康检查
curl http://localhost:5000/health

# 发送消息
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'

# 访问 API 文档
http://localhost:5000/docs
```

### Railway 测试

```bash
# 健康检查
curl https://yuanxiaoji-production.up.railway.app/health

# 发送消息
curl -X POST https://yuanxiaoji-production.up.railway.app/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'

# 访问 API 文档
https://yuanxiaoji-production.up.railway.app/docs
```

---

## ⚙️ 配置

### Railway 环境变量

在 Railway 项目设置中添加：

```env
COZE_WORKLOAD_IDENTITY_API_KEY=your_api_key
COZE_INTEGRATION_MODEL_BASE_URL=your_base_url
LOG_LEVEL=info
MAX_MESSAGE_HISTORY=20
```

详细配置：查看 [Railway 部署指南](docs/RAILWAY_DEPLOYMENT_GUIDE.md#配置环境变量)

---

## 📚 文档

### 部署相关

- **[Railway 快速部署](docs/RAILWAY_QUICK_START.md)** - 10分钟快速部署到 Railway
- **[Railway 部署指南](docs/RAILWAY_DEPLOYMENT_GUIDE.md)** - Railway 详细部署教程
- **[公网访问指南](docs/PUBLIC_ACCESS_GUIDE.md)** - 多种公网部署方案
- **[快速部署教程](docs/QUICK_PUBLIC_DEPLOYMENT.md)** - 5分钟快速部署

---

## 🌐 公网部署方案

### ⭐ Railway（强烈推荐）

**优点：**
- ✅ 完全免费（$5/月额度）
- ✅ 固定域名
- ✅ 自动 HTTPS
- ✅ 零运维
- ✅ 自动扩展

**快速开始：**
1. 访问 https://railway.app
2. 连接 GitHub 仓库
3. 配置环境变量
4. 部署完成

详细教程：[Railway 快速部署](docs/RAILWAY_QUICK_START.md)

---

### ngrok

**优点：**
- ✅ 快速启动（5分钟）
- ✅ 速度快
- ✅ 免费（有限制）

**缺点：**
- ❌ 地址不固定
- ❌ 免费版有限制

详细教程：[公网访问指南](docs/PUBLIC_ACCESS_GUIDE.md#方案1ngrok内网穿透-推荐)

---

### 云服务器

**优点：**
- ✅ 高性能
- ✅ 完全控制
- ✅ 适合大规模部署

**推荐：**
- 阿里云 ECS：2核4G ¥89/月
- 腾讯云 CVM：2核4G ¥70/月

详细教程：[公网访问指南](docs/PUBLIC_ACCESS_GUIDE.md#方案2云服务器部署)

---

## 🔍 常见问题

### Q1: 如何部署到 Railway？

查看：[Railway 快速部署](docs/RAILWAY_QUICK_START.md)

### Q2: Railway 免费额度够用吗？

对于小规模应用（<1000 次请求/天），免费额度完全够用！

### Q3: 本地如何访问服务？

```bash
# 启动服务
python src/main.py

# 访问
http://localhost:5000/docs
```

### Q4: 如何重启服务？

**本地：**
```bash
# 停止后重新启动
python src/main.py
```

**Railway：**
在控制台点击 "Redeploy"

---

## 📊 服务状态

### 本地服务

- **健康检查**：`http://localhost:5000/health`
- **API 文档**：`http://localhost:5000/docs`

### Railway 服务

- **健康检查**：`https://yuanxiaoji-production.up.railway.app/health`
- **API 文档**：`https://yuanxiaoji-production.up.railway.app/docs`

---

## 📞 支持

- **Railway 文档**：https://docs.railway.app
- **项目文档**：查看 `docs/` 目录

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
- ✅ 添加 Railway 部署支持
- ✅ 添加 ngrok 部署支持
- ✅ Docker 容器化部署

---

## 📄 许可证

MIT License

---

## 🙏 致谢

感谢 Coze 平台提供的强大支持！

---

## 🎉 开始使用

**立即部署到 Railway：**

[📖 查看快速部署教程](docs/RAILWAY_QUICK_START.md)

**10分钟获得稳定的公网地址！** 🚀
