# 🤖 元小吉智能客服 - 访问链接

## 📱 访问方式

### 方式1：本地访问（推荐）

如果您在本地运行，可以访问：

```
http://localhost:8000
```

然后在浏览器中打开聊天界面文件：
```
file:///workspace/projects/assets/chat.html
```

或者直接双击打开：`/workspace/projects/assets/chat.html`

---

### 方式2：API 文档访问

访问 API 文档页面：

```
http://localhost:8000/docs
```

这个页面提供了所有 API 接口的详细文档和在线测试功能。

---

### 方式3：使用 Python 测试

创建测试脚本：

```python
import requests

# 发送消息给元小吉
response = requests.post(
    "http://localhost:8000/chat",
    json={"message": "你好"}
)

print(response.json())
```

---

## 🚀 如何部署到公网

如果您想在公网上访问，可以：

### 选项1：使用 ngrok（临时测试）

```bash
# 安装 ngrok
# 从 https://ngrok.com/ 下载并安装

# 启动 ngrok
ngrok http 8000

# 会得到一个公网地址，例如：
# https://abc123.ngrok.io
```

然后修改 `chat.html` 中的 API_URL：

```javascript
const API_URL = 'https://abc123.ngrok.io';
```

### 选项2：使用云服务器

1. 将项目部署到云服务器（阿里云、腾讯云、AWS等）
2. 配置域名和 SSL 证书
3. 使用 Nginx 反向代理

### 选项3：使用 Vercel/Netlify（静态部署）

将 `chat.html` 部署到 Vercel 或 Netlify，然后配置 API 地址。

---

## 📊 当前服务状态

✅ **API 服务状态**：运行中  
✅ **监听端口**：8000  
✅ **监听地址**：0.0.0.0（所有网络接口）  
✅ **进程 ID**：202

---

## 🎯 快速开始

### 第1步：打开聊天界面

```bash
# 方式1：直接打开文件
open /workspace/projects/assets/chat.html

# 方式2：使用浏览器访问
# 复制文件路径到浏览器地址栏
```

### 第2步：开始对话

输入消息并点击发送，例如：
- "你好"
- "你们有什么产品？"
- "用豆包介绍一下沉香"
- "我要投诉"

### 第3步：体验功能

- 💬 多轮对话
- 🤖 豆包AI
- 📚 知识库查询
- 🎫 工单创建
- 😊 情感识别

---

## 🛠️ 服务管理

### 启动服务

```bash
cd /workspace/projects
python src/api_server.py
```

### 停止服务

```bash
# 查找进程
ps aux | grep api_server.py

# 停止进程
kill <PID>

# 或者使用启动脚本
pkill -f api_server.py
```

### 查看日志

```bash
tail -f /workspace/projects/logs/api_server.log
```

### 重启服务

```bash
cd /workspace/projects
pkill -f api_server.py
nohup python src/api_server.py > logs/api_server.log 2>&1 &
```

---

## 🌐 外部访问配置

如果您需要外部访问，请：

1. **检查防火墙**：确保8000端口已开放
   ```bash
   sudo ufw allow 8000
   ```

2. **获取服务器IP**：
   ```bash
   curl ifconfig.me
   ```

3. **访问地址**：`http://<服务器IP>:8000`

4. **配置域名**（可选）：
   - 在 DNS 提供商处添加 A 记录
   - 配置 Nginx 反向代理

---

## 📝 API 端点

| 端点 | 方法 | 描述 |
|------|------|------|
| `/` | GET | 服务信息 |
| `/health` | GET | 健康检查 |
| `/chat` | POST | 发送消息 |
| `/chat/stream` | POST | 流式对话 |
| `/docs` | GET | API 文档 |

---

## 🎨 自定义

### 修改机器人名称

编辑 `chat.html`：
```html
<h1>🤖 元小吉智能客服</h1>
```

### 修改颜色主题

编辑 `chat.html` 中的 CSS：
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### 添加快捷操作

编辑 `chat.html` 中的快捷按钮：
```html
<button class="quick-action-btn" onclick="quickSend('你的问题')">自定义问题</button>
```

---

## 🔒 安全建议

1. **使用 HTTPS**：生产环境必须配置 SSL 证书
2. **添加认证**：实现 API Key 或 JWT 认证
3. **限流**：防止恶意请求
4. **日志记录**：记录所有请求和响应
5. **数据加密**：敏感数据加密存储

---

## 📞 技术支持

如遇问题，请检查：

1. ✅ 服务是否运行：`ps aux | grep api_server.py`
2. ✅ 端口是否监听：`netstat -tlnp | grep 8000`
3. ✅ 防火墙是否开放：`sudo ufw status`
4. ✅ 日志是否有错误：`tail -f logs/api_server.log`

---

## 🎉 开始使用

**现在就开始与元小吉对话吧！**

打开 `chat.html` 文件，输入您的第一个消息！

祝您使用愉快！~ 😊✨
