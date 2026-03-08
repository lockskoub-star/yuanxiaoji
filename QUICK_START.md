# 🚀 快速部署到公网

## 最快方式（5分钟部署）

### 前提条件
- 已购买云服务器（阿里云/腾讯云/AWS等）
- 服务器已安装 Docker 和 Docker Compose

### 步骤

#### 1️⃣ 连接服务器
```bash
ssh root@your_server_ip
```

#### 2️⃣ 上传项目文件
```bash
# 在本地执行
scp -r /workspace/projects root@your_server_ip:/root/
```

#### 3️⃣ 配置环境变量
```bash
# 在服务器上执行
cd /root/projects
cp .env.example .env
nano .env
```

修改以下内容：
- `COZE_WORKLOAD_IDENTITY_API_KEY`: 你的 API Key
- `SECRET_KEY`: 随机字符串
- `ALLOWED_ORIGINS`: 你的域名

#### 4️⃣ 一键部署
```bash
cd /root/projects
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

#### 5️⃣ 配置域名（可选）
如果需要域名访问，使用 Nginx 配置域名和 HTTPS。

---

## 📋 部署检查清单

部署后，执行以下检查：

```bash
# 1. 检查服务状态
docker-compose ps

# 2. 检查健康
curl http://localhost:8000/health

# 3. 测试 API
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'

# 4. 查看日志
docker-compose logs -f
```

---

## 🔍 常见问题

### 问题1：端口被占用
```bash
# 检查端口
netstat -tlnp | grep 8000

# 修改端口
# 编辑 .env 文件，修改 PORT=8001
```

### 问题2：服务无法启动
```bash
# 查看详细日志
docker-compose logs agent

# 重新构建
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### 问题3：API 调用失败
```bash
# 检查环境变量
docker-compose exec agent env | grep API

# 测试网络连接
docker-compose exec agent curl -I https://api.coze.cn
```

---

## 📞 需要帮助？

查看详细部署指南：`DEPLOYMENT_GUIDE.md`

或检查：
- 服务日志：`docker-compose logs -f`
- Nginx 日志：`docker-compose logs nginx`
- 监控脚本：`./scripts/monitor.sh`
