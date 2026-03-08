# 🚀 元小吉智能客服 - 公网部署指南

## 📋 部署方式选择

本指南提供 3 种部署方式：

### 方式1️⃣：云服务器部署（推荐 ⭐）
适合：需要完全控制、可扩展的场景
- 阿里云、腾讯云、AWS、华为云等

### 方式2️⃣：Docker 容器部署（最简单）
适合：快速部署、环境隔离的场景

### 方式3️⃣：Serverless 部署（最便宜）
适合：低流量、按需付费的场景
- Vercel、Netlify、腾讯云函数等

---

## 方式1️⃣：云服务器部署

### 第1步：购买云服务器

推荐配置：
- **CPU**: 2核及以上
- **内存**: 4GB及以上
- **系统**: Ubuntu 20.04 / 22.04 LTS
- **带宽**: 5Mbps及以上
- **硬盘**: 40GB及以上

**价格参考**：
- 阿里云：约 ¥50-100/月
- 腾讯云：约 ¥50-100/月
- AWS：约 ¥100-200/月

---

### 第2步：连接服务器

```bash
# 使用 SSH 连接
ssh root@your_server_ip

# 或使用密钥
ssh -i your_key.pem root@your_server_ip
```

---

### 第3步：安装必要软件

```bash
# 更新系统
apt update && apt upgrade -y

# 安装 Python 和 pip
apt install -y python3 python3-pip python3-venv

# 安装 Nginx
apt install -y nginx

# 安装 Git
apt install -y git

# 安装 Supervisor（进程管理）
apt install -y supervisor

# 安装防火墙工具
apt install -y ufw
```

---

### 第4步：上传项目文件

**方式A：使用 SCP 上传**
```bash
# 在本地终端执行
scp -r /workspace/projects root@your_server_ip:/root/
```

**方式B：使用 Git**
```bash
# 在服务器上执行
git clone your_repository_url
cd your_project_folder
```

---

### 第5步：配置 Python 环境

```bash
# 进入项目目录
cd /root/projects

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 安装额外依赖
pip install gunicorn
```

---

### 第6步：配置环境变量

```bash
# 创建环境变量文件
nano /root/projects/.env
```

添加以下内容：
```bash
# API 配置
COZE_WORKLOAD_IDENTITY_API_KEY=your_api_key
COZE_INTEGRATION_MODEL_BASE_URL=https://api.coze.cn

# 服务配置
HOST=0.0.0.0
PORT=8000

# 日志配置
LOG_LEVEL=INFO

# 安全配置
SECRET_KEY=your_secret_key_change_this
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

---

### 第7步：测试服务

```bash
# 激活虚拟环境
source /root/projects/venv/bin/activate

# 测试运行
python src/main.py
```

如果看到服务启动成功，按 Ctrl+C 停止。

---

### 第8步：使用 Gunicorn 启动服务

```bash
# 创建 Gunicorn 配置
nano /root/projects/gunicorn_config.py
```

添加以下内容：
```python
import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 120
keepalive = 5
```

启动服务：
```bash
gunicorn --config gunicorn_config.py src.main:app
```

---

### 第9步：配置 Supervisor（开机自启）

```bash
# 创建 Supervisor 配置
nano /etc/supervisor/conf.d/agent.conf
```

添加以下内容：
```ini
[program:agent]
command=/root/projects/venv/bin/gunicorn --config /root/projects/gunicorn_config.py src.main:app
directory=/root/projects
user=root
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/root/projects/logs/gunicorn.log
stdout_logfile_maxbytes=50MB
stdout_logfile_backups=10
environment=PATH="/root/projects/venv/bin"
```

启动服务：
```bash
# 重新加载配置
supervisorctl reread
supervisorctl update

# 启动服务
supervisorctl start agent

# 查看状态
supervisorctl status

# 查看日志
supervisorctl tail agent
```

---

### 第10步：配置 Nginx 反向代理

```bash
# 创建 Nginx 配置
nano /etc/nginx/sites-available/agent
```

添加以下内容：
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # 静态文件
    location /static {
        alias /root/projects/assets;
        expires 30d;
    }

    # API 代理
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 超时设置
        proxy_connect_timeout 600;
        proxy_send_timeout 600;
        proxy_read_timeout 600;
        send_timeout 600;
    }

    # WebSocket 支持（如果需要）
    location /ws {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

启用配置：
```bash
# 创建软链接
ln -s /etc/nginx/sites-available/agent /etc/nginx/sites-enabled/

# 测试配置
nginx -t

# 重启 Nginx
systemctl restart nginx

# 设置开机自启
systemctl enable nginx
```

---

### 第11步：配置 HTTPS（SSL 证书）

**使用 Let's Encrypt（免费）**：
```bash
# 安装 Certbot
apt install -y certbot python3-certbot-nginx

# 获取证书（自动配置 Nginx）
certbot --nginx -d yourdomain.com -d www.yourdomain.com

# 测试自动续期
certbot renew --dry-run
```

Certbot 会自动更新 Nginx 配置，添加 SSL 支持。

---

### 第12步：配置防火墙

```bash
# 允许 SSH
ufw allow 22/tcp

# 允许 HTTP
ufw allow 80/tcp

# 允许 HTTPS
ufw allow 443/tcp

# 启用防火墙
ufw enable

# 查看状态
ufw status
```

---

### 第13步：测试部署

```bash
# 测试 HTTP
curl http://yourdomain.com/health

# 测试 HTTPS
curl https://yourdomain.com/health

# 测试 API
curl -X POST https://yourdomain.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'
```

---

## 方式2️⃣：Docker 容器部署

### 第1步：安装 Docker

```bash
# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 安装 Docker Compose
apt install -y docker-compose

# 启动 Docker
systemctl start docker
systemctl enable docker
```

---

### 第2步：创建 Dockerfile

```dockerfile
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 创建日志目录
RUN mkdir -p /app/logs

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "src.main:app"]
```

---

### 第3步：创建 docker-compose.yml

```yaml
version: '3.8'

services:
  agent:
    build: .
    ports:
      - "8000:8000"
    environment:
      - COZE_WORKLOAD_IDENTITY_API_KEY=${API_KEY}
      - COZE_INTEGRATION_MODEL_BASE_URL=https://api.coze.cn
      - HOST=0.0.0.0
      - PORT=8000
    volumes:
      - ./logs:/app/logs
      - ./assets:/app/assets
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./assets:/usr/share/nginx/html:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - agent
    restart: unless-stopped
```

---

### 第4步：启动服务

```bash
# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 查看状态
docker-compose ps
```

---

## 方式3️⃣：Serverless 部署

### 使用 Vercel

1. **安装 Vercel CLI**
```bash
npm install -g vercel
```

2. **创建 vercel.json**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "src/api_server.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "src/api_server.py"
    }
  ]
}
```

3. **部署**
```bash
vercel
```

---

## 🔒 安全配置

### 1. 配置 API 限流

```python
# 在 api_server.py 中添加
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/chat")
@limiter.limit("10/minute")  # 每分钟10次
async def chat(request: Request, request_data: ChatRequest):
    ...
```

### 2. 配置 CORS

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. 配置环境变量

确保敏感信息不要硬编码，使用环境变量：
```python
import os

API_KEY = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
```

---

## 📊 监控和日志

### 1. 日志管理

```bash
# 查看实时日志
tail -f /root/projects/logs/app.log

# 查看错误日志
tail -f /root/projects/logs/error.log
```

### 2. 性能监控

使用 Prometheus + Grafana 监控服务状态。

### 3. 告警配置

配置邮件或钉钉告警，服务异常时及时通知。

---

## 🔄 更新部署

```bash
# 更新代码
cd /root/projects
git pull

# 更新依赖
source venv/bin/activate
pip install -r requirements.txt

# 重启服务
supervisorctl restart agent
```

---

## 📝 部署检查清单

部署完成后，检查以下项目：

- [ ] 服务正常运行
- [ ] HTTP 可以访问
- [ ] HTTPS 可以访问
- [ ] API 接口正常
- [ ] 静态文件加载正常
- [ ] 日志记录正常
- [ ] 防火墙配置正确
- [ ] SSL 证书有效
- [ ] 自动重启配置
- [ ] 数据备份配置
- [ ] 监控告警配置

---

## 🆘 常见问题

### Q: 服务无法启动
A: 检查端口占用、依赖安装、环境变量配置

### Q: 502 错误
A: 检查 Gunicorn 是否正常运行

### Q: SSL 证书获取失败
A: 检查域名 DNS 配置、防火墙端口

### Q: 性能太慢
A: 增加 worker 数量、使用 CDN、优化数据库

---

## 📞 技术支持

如遇问题，查看：
1. 服务日志：`/root/projects/logs/`
2. Nginx 日志：`/var/log/nginx/`
3. Supervisor 日志：`/var/log/supervisor/`

---

**祝您部署顺利！** 🚀
