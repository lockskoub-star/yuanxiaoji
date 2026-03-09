# 💻 本地运行指南

> 在本地运行元小吉智能客服 Agent

---

## 📋 目录

1. [环境准备](#环境准备)
2. [安装依赖](#安装依赖)
3. [运行方式](#运行方式)
4. [测试服务](#测试服务)
5. [常见问题](#常见问题)

---

## 🔧 环境准备

### 系统要求

- Python 3.11+
- pip
- 8GB+ 内存（推荐）

### 检查 Python 版本

```bash
python --version
# 应该显示：Python 3.11.x 或更高
```

---

## 📦 安装依赖

### 方法 1：使用 pip（推荐）

```bash
cd /workspace/projects

# 安装所有依赖
pip install -r requirements.txt
```

### 方法 2：使用虚拟环境（推荐）

```bash
cd /workspace/projects

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/Mac:
source venv/bin/activate

# Windows:
# venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 方法 3：使用 conda

```bash
cd /workspace/projects

# 创建环境
conda create -n yuanxiaoji python=3.11

# 激活环境
conda activate yuanxiaoji

# 安装依赖
pip install -r requirements.txt
```

---

## 🚀 运行方式

### 方式 1：启动 HTTP 服务 ⭐ 推荐

**适用场景：** 通过 API 调用、Web 界面访问

#### 方法 1.1：使用脚本启动

```bash
cd /workspace/projects

# 默认端口 5000
bash scripts/http_run.sh

# 指定端口 8000
bash scripts/http_run.sh -p 8000
```

#### 方法 1.2：直接用 Python 启动

```bash
cd /workspace/projects

# 默认端口 5000
python src/main.py -m http

# 指定端口
python src/main.py -m http -p 8000
```

#### 方法 1.3：使用 uvicorn 直接启动（如果有 api_server.py）

```bash
cd /workspace/projects

# 启动 API 服务
uvicorn src.api_server:app --host 0.0.0.0 --port 5000 --reload
```

**启动成功后，会看到：**
```
INFO:     Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using StatReload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

### 方式 2：Flow 模式运行

**适用场景：** 直接运行工作流

```bash
cd /workspace/projects

# 运行默认输入
bash scripts/local_run.sh -m flow

# 指定输入（JSON 格式）
bash scripts/local_run.sh -m flow -i '{"text": "你好"}'

# 指定输入（纯文本）
bash scripts/local_run.sh -m flow -i '你好'
```

**或者直接用 Python：**

```bash
python src/main.py -m flow

# 带输入
python src/main.py -m flow -i '{"text": "你好"}'
```

---

### 方式 3：Node 模式运行

**适用场景：** 运行单个节点

```bash
cd /workspace/projects

# 运行指定节点
bash scripts/local_run.sh -m node -n node_id -i '{"text": "测试"}'

# 或者用 Python
python src/main.py -m node -n node_id -i '{"text": "测试"}'
```

---

### 方式 4：Agent 模式运行

**适用场景：** 流式运行 Agent

```bash
cd /workspace/projects

# 运行 Agent（默认输入）
python src/main.py -m agent
```

---

## 🧪 测试服务

### 如果启动了 HTTP 服务

#### 1. 健康检查

**使用浏览器：**
```
http://localhost:5000/health
```

**使用 curl：**
```bash
curl http://localhost:5000/health
```

**预期返回：**
```json
{
  "status": "ok",
  "message": "Service is running"
}
```

#### 2. 访问 API 文档

**在浏览器中打开：**
```
http://localhost:5000/docs
```

你会看到 Swagger UI 页面，可以在线测试 API。

#### 3. 发送测试消息

**使用 curl：**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'
```

**在 API 文档中测试：**
1. 访问 `http://localhost:5000/docs`
2. 展开 `/chat` 接口
3. 点击 "Try it out"
4. 输入：`{"message": "你好"}`
5. 点击 "Execute"
6. 查看响应

---

## 🔍 运行模式说明

### HTTP 模式（-m http）

**用途：** 启动 Web API 服务器

**特点：**
- ✅ 通过 HTTP 访问
- ✅ 支持多客户端
- ✅ 提供 API 文档
- ✅ 推荐用于生产环境

**命令：**
```bash
python src/main.py -m http -p 5000
```

---

### Flow 模式（-m flow）

**用途：** 运行完整工作流

**特点：**
- ✅ 一次性执行
- ✅ 适合测试和调试
- ✅ 可指定输入

**命令：**
```bash
python src/main.py -m flow -i '{"text": "你好"}'
```

---

### Node 模式（-m node）

**用途：** 运行单个节点

**特点：**
- ✅ 独立运行节点
- ✅ 适合调试单个组件
- ✅ 需要指定节点 ID

**命令：**
```bash
python src/main.py -m node -n node_id -i '{"text": "测试"}'
```

---

### Agent 模式（-m agent）

**用途：** 流式运行 Agent

**特点：**
- ✅ 实时流式输出
- ✅ 适合交互式场景
- ✅ 默认输入

**命令：**
```bash
python src/main.py -m agent
```

---

## 📝 环境变量配置

### 可选配置

创建 `.env` 文件：

```env
# 日志级别
LOG_LEVEL=INFO

# 消息历史记录数
MAX_MESSAGE_HISTORY=20

# API 密钥（如果需要）
COZE_WORKLOAD_IDENTITY_API_KEY=your_api_key
COZE_INTEGRATION_MODEL_BASE_URL=your_base_url
```

### 加载环境变量

```bash
# 使用脚本加载
source scripts/load_env.sh

# 然后启动服务
python src/main.py -m http
```

---

## 🔧 常见问题

### Q1: 提示 "ModuleNotFoundError"

**解决：**
```bash
# 确保安装了依赖
pip install -r requirements.txt

# 如果使用虚拟环境，确保已激活
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

---

### Q2: 端口已被占用

**解决：**

**方法 1：使用其他端口**
```bash
python src/main.py -m http -p 8000
```

**方法 2：停止占用端口的进程**
```bash
# 查找占用端口的进程
lsof -i :5000  # Linux/Mac
netstat -ano | findstr :5000  # Windows

# 停止进程
kill <PID>  # Linux/Mac
taskkill /PID <PID> /F  # Windows
```

---

### Q3: 如何停止服务？

**在运行的终端按：**
```
Ctrl + C
```

---

### Q4: 服务启动失败

**检查步骤：**

1. 检查 Python 版本
```bash
python --version  # 需要 3.11+
```

2. 检查依赖是否安装
```bash
pip list | grep -E "fastapi|langchain"
```

3. 查看错误日志
```bash
# 日志会显示在终端
```

---

### Q5: 如何查看详细日志？

**设置日志级别：**

```bash
# 临时设置
LOG_LEVEL=DEBUG python src/main.py -m http

# 或在 .env 文件中设置
echo "LOG_LEVEL=DEBUG" >> .env
```

---

## 📊 运行模式对比

| 模式 | 命令 | 用途 | 推荐度 |
|------|------|------|--------|
| **HTTP** | `python src/main.py -m http` | Web API 服务 | ⭐⭐⭐⭐⭐ |
| **Flow** | `python src/main.py -m flow` | 运行工作流 | ⭐⭐⭐ |
| **Node** | `python src/main.py -m node` | 运行单个节点 | ⭐⭐ |
| **Agent** | `python src/main.py -m agent` | 流式运行 | ⭐⭐⭐ |

---

## 🎯 快速开始

### 最简单的方式（推荐）

```bash
# 1. 进入项目目录
cd /workspace/projects

# 2. 启动服务
bash scripts/http_run.sh

# 或
python src/main.py -m http

# 3. 访问 API 文档
# 打开浏览器访问：http://localhost:5000/docs
```

### 只需要 3 步：

1. **启动服务**
   ```bash
   python src/main.py -m http
   ```

2. **访问文档**
   ```
   http://localhost:5000/docs
   ```

3. **测试对话**
   在 API 文档中发送测试消息

---

## 📚 相关文档

- [API 文档](http://localhost:5000/docs) - Swagger UI
- [README.md](README.md) - 项目说明
- [部署指南](docs/) - 各种部署方案

---

## 💡 提示

- **开发时使用 `--reload`**：代码修改后自动重启
- **使用虚拟环境**：隔离依赖，避免冲突
- **查看日志**：了解服务运行状态
- **使用 API 文档**：快速测试接口

---

## 🎉 开始使用

**立即启动服务：**

```bash
cd /workspace/projects
python src/main.py -m http
```

**访问 API 文档：**
```
http://localhost:5000/docs
```

**祝你使用愉快！** 🚀
