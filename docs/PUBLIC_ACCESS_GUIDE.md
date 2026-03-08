# 🌐 元小吉智能客服 - 公网访问指南

> 让你的智能客服 Agent 可被全球访问！

---

## 📋 目录

- [快速方案](#快速方案)
- [稳定方案](#稳定方案)
- [免费方案](#免费方案)
- [配置指南](#配置指南)
- [测试验证](#测试验证)

---

## 🚀 快速方案（5分钟）

### 方案1：ngrok 内网穿透 ⭐ 推荐

**适用场景**：快速测试、开发环境演示

**优点**：
- ✅ 5分钟完成配置
- ✅ 无需购买服务器
- ✅ 自动 HTTPS
- ✅ 免费版可用

#### 步骤：

##### 1️⃣ 注册 ngrok 账号

访问：https://ngrok.com/signup

##### 2️⃣ 获取 Authtoken

登录后访问：https://dashboard.ngrok.com/get-started/your-authtoken

复制你的 authtoken，类似：
```
2xxx...xxx...xxx
```

##### 3️⃣ 安装 ngrok

**Linux/Mac:**
```bash
# 方法1：使用脚本安装
./scripts/quick_public.sh

# 方法2：手动安装
wget https://bin.equinox.io/c/bNyj1mQVY4c/v3/ngrok-linux-amd64.zip
unzip ngrok-linux-amd64.zip
chmod +x ngrok
./ngrok config add-authtoken YOUR_AUTH_TOKEN
```

**Windows:**
```bash
# 下载安装包
https://ngrok.com/download

# 或使用 Chocolatey
choco install ngrok
```

##### 4️⃣ 启动 ngrok

```bash
# 确保 API 服务已启动
docker-compose up -d

# 启动 ngrok
ngrok http 8000
```

##### 5️⃣ 获取公网地址

ngrok 启动后会显示：
```
Forwarding  https://xxxx-xx-xx-xx-xx.ngrok-free.app -> http://localhost:8000
```

复制这个 HTTPS 地址，这就是你的公网访问地址！

**示例**：
```
https://a1b2-c3d4.ngrok-free.app
```

##### 6️⃣ 访问你的服务

打开浏览器访问：
```
https://a1b2-c3d4.ngrok-free.app/docs
```

---

## 💎 稳定方案（生产环境）

### 方案2：云服务器部署

**适用场景**：生产环境、高可用、自有域名

**推荐配置**：
- CPU：2核
- 内存：4GB
- 带宽：5Mbps
- 系统：Ubuntu 22.04 LTS

#### 推荐云服务商：

| 服务商 | 入门配置 | 价格 | 链接 |
|--------|---------|------|------|
| 阿里云 | 2核4G | ¥89/月 | [ECS](https://www.aliyun.com/product/ecs) |
| 腾讯云 | 2核4G | ¥70/月 | [CVM](https://cloud.tencent.com/product/cvm) |
| 华为云 | 2核4G | ¥75/月 | [ECS](https://www.huaweicloud.com/product/ecs) |

#### 部署步骤：

##### 1️⃣ 购买云服务器

选择区域：推荐距离用户最近的区域（如华东、华南）

##### 2️⃣ 连接到服务器

```bash
# 使用 SSH 连接
ssh root@your_server_ip

# 或使用密钥
ssh -i your_key.pem root@your_server_ip
```

##### 3️⃣ 安装 Docker

```bash
# 安装 Docker
curl -fsSL https://get.docker.com | sh

# 安装 Docker Compose
apt install docker-compose -y

# 验证安装
docker --version
docker-compose --version
```

##### 4️⃣ 上传部署包

**在本地电脑：**
```bash
# 打包项目
tar -czf yuanxiaoji.tar.gz ./

# 上传到服务器
scp yuanxiaoji.tar.gz root@your_server_ip:/root/

# 或使用 rsync
rsync -avz --exclude='.git' ./ root@your_server_ip:/root/yuanxiaoji/
```

**在服务器上：**
```bash
# 解压
cd /root
tar -xzf yuanxiaoji.tar.gz
cd yuanxiaoji

# 检查配置
cat .env  # 确认环境变量
```

##### 5️⃣ 启动服务

```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 查看状态
docker-compose ps
```

##### 6️⃣ 配置防火墙

```bash
# 开放端口
ufw allow 80
ufw allow 443
ufw allow 8000
ufw reload
```

##### 7️⃣ （可选）配置域名

**A. 购买域名**
- 阿里云：https://wanwang.aliyun.com
- 腾讯云：https://dnspod.cloud.tencent.com

**B. 解析域名**
在你的域名管理中添加 A 记录：
```
类型: A
主机记录: @ 或 www
记录值: 你的服务器IP
```

**C. 修改 nginx 配置**

```nginx
# 修改 nginx.conf
server_name your_domain.com;
```

**D. 重启服务**
```bash
docker-compose restart nginx
```

##### 8️⃣ （可选）配置 HTTPS

**使用 Let's Encrypt 免费证书：**

```bash
# 安装 certbot
apt install certbot python3-certbot-nginx -y

# 获取证书
certbot --nginx -d your_domain.com -d www.your_domain.com

# 自动续期
certbot renew --dry-run
```

---

## 🆓 免费方案

### 方案3： Railway 云平台

**适用场景**：快速部署、无需运维

**优点**：
- ✅ 完全免费（$5/月额度）
- ✅ 一键部署
- ✅ 自动 HTTPS
- ✅ 自动扩展

#### 部署步骤：

##### 1️⃣ 注册账号

访问：https://railway.app

##### 2️⃣ 新建项目

点击 "New Project" → "Deploy from Dockerfile"

##### 3️⃣ 连接 GitHub

**A. Fork 项目到你的 GitHub**

**B. 在 Railway 中选择 GitHub 仓库**

##### 4️⃣ 配置环境变量

在 Railway 项目设置中添加环境变量：

```env
COZE_WORKLOAD_IDENTITY_API_KEY=your_api_key
COZE_INTEGRATION_MODEL_BASE_URL=your_base_url
```

##### 5️⃣ 部署

点击 "Deploy" 开始部署

等待 2-3 分钟，部署完成后获得公网 URL：
```
https://yuanxiaoji.up.railway.app
```

##### 6️⃣ 访问

打开浏览器：
```
https://yuanxiaoji.up.railway.app/docs
```

---

### 方案4： Render 平台

**适用场景**：与 Railway 类似

**部署步骤：**

1. 注册：https://render.com
2. 新建 Web Service
3. 选择 Python 或 Docker
4. 连接 GitHub 仓库
5. 配置环境变量
6. 部署完成

---

### 方案5：Fly.io

**适用场景**：全球边缘部署

**部署步骤：**

```bash
# 安装 flyctl
curl -L https://fly.io/install.sh | sh

# 登录
flyctl auth signup
flyctl auth login

# 初始化
flyctl init

# 部署
flyctl deploy
```

---

## 📝 配置指南

### 环境变量配置

创建 `.env` 文件：

```env
# API 配置
API_HOST=0.0.0.0
API_PORT=8000

# 豆包模型配置
COZE_WORKLOAD_IDENTITY_API_KEY=your_api_key_here
COZE_INTEGRATION_MODEL_BASE_URL=your_base_url_here

# 可选配置
LOG_LEVEL=INFO
MAX_MESSAGE_HISTORY=20
```

### Nginx 配置

`nginx.conf` 示例：

```nginx
events {
    worker_connections 1024;
}

http {
    upstream api {
        server api:8000;
    }

    server {
        listen 80;
        server_name your_domain.com;

        location / {
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /docs {
            proxy_pass http://api/docs;
        }
    }
}
```

---

## 🧪 测试验证

### 1. 健康检查

```bash
curl http://your_public_url/health
```

预期输出：
```json
{
  "status": "healthy",
  "service": "元小吉智能客服",
  "version": "1.0.0"
}
```

### 2. API 文档访问

浏览器访问：
```
http://your_public_url/docs
```

### 3. 对话测试

```bash
curl -X POST http://your_public_url/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'
```

### 4. 性能测试

```bash
# 使用 Apache Bench
ab -n 100 -c 10 http://your_public_url/health

# 使用 wrk
wrk -t4 -c100 -d30s http://your_public_url/health
```

---

## 🔒 安全建议

### 1. 限制访问

**Nginx IP 白名单：**

```nginx
allow 1.2.3.4;  # 允许的IP
deny all;
```

### 2. 使用 HTTPS

**Let's Encrypt：**
```bash
certbot --nginx -d your_domain.com
```

### 3. 添加 API 密钥认证

```python
# 在 FastAPI 中添加
@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    api_key = request.headers.get("X-API-Key")
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return await call_next(request)
```

### 4. 速率限制

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/chat")
@limiter.limit("10/minute")
async def chat(request: Request, message: str):
    ...
```

---

## 📊 监控和日志

### 1. 查看日志

```bash
# Docker 日志
docker-compose logs -f api

# Nginx 日志
docker-compose logs -f nginx
```

### 2. 性能监控

使用 Prometheus + Grafana 或云平台提供的监控工具。

### 3. 错误追踪

集成 Sentry：
```python
import sentry_sdk

sentry_sdk.init(
    dsn="your_sentry_dsn",
    traces_sample_rate=1.0,
)
```

---

## 🆘 故障排查

### 问题1：无法访问

**检查：**
1. 服务是否启动：`docker-compose ps`
2. 端口是否开放：`netstat -tuln`
3. 防火墙状态：`ufw status`

### 问题2：ngrok 连接失败

**解决：**
```bash
# 检查配置
ngrok config check

# 重新配置
ngrok config add-authtoken YOUR_TOKEN
```

### 问题3：Docker 容器崩溃

**检查日志：**
```bash
docker-compose logs api
```

---

## 📚 更多资源

- [FastAPI 官方文档](https://fastapi.tiangolo.com)
- [Docker 官方文档](https://docs.docker.com)
- [Nginx 官方文档](https://nginx.org/en/docs)
- [ngrok 文档](https://ngrok.com/docs)

---

## 🎉 快速开始

**立即体验（5分钟）：**

```bash
# 1. 启动服务
docker-compose up -d

# 2. 使用脚本快速部署
./scripts/quick_public.sh

# 3. 访问你的服务
# 复制 ngrok 显示的公网地址
# 在浏览器中打开：https://xxxx.ngrok-free.app/docs
```

---

**祝你部署顺利！🚀**
