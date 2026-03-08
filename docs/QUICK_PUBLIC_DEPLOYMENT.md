# 🌐 快速部署到公网（5分钟内完成）

## 方案选择

根据你的需求选择合适的方案：

| 方案 | 时间 | 费用 | 稳定性 | 推荐度 |
|------|------|------|--------|--------|
| ngrok | 5分钟 | 免费 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Railway | 10分钟 | 免费 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 云服务器 | 30分钟 | ¥150/月 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 🚀 方案1：ngrok（最简单，推荐）

### 步骤 1：注册账号

1. 访问 https://ngrok.com/signup
2. 使用邮箱注册（免费）
3. 验证邮箱

### 步骤 2：获取 Authtoken

1. 登录 ngrok
2. 访问：https://dashboard.ngrok.com/get-started/your-authtoken
3. 复制你的 authtoken（类似：`2xxx...xxx...xxx`）

### 步骤 3：安装并配置 ngrok

**如果你有 sudo 权限：**

```bash
# 方法1：使用官方脚本
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update
sudo apt install ngrok

# 配置 authtoken
ngrok config add-authtoken YOUR_AUTH_TOKEN_HERE
```

**如果没有 sudo 权限（当前环境）：**

```bash
# 方法2：手动下载
cd ~
wget https://bin.equinox.io/c/bNyj1mQVY4c/v3/ngrok-linux-amd64.zip
unzip ngrok-linux-amd64.zip
chmod +x ngrok
./ngrok config add-authtoken YOUR_AUTH_TOKEN_HERE
```

### 步骤 4：启动服务

```bash
# 确保 API 服务已启动
cd /workspace/projects
docker-compose up -d

# 验证服务
curl http://localhost:8000/health
```

### 步骤 5：启动 ngrok

```bash
# 如果安装在系统目录
ngrok http 8000

# 如果手动下载
~/ngrok http 8000
```

### 步骤 6：获取公网地址

ngrok 启动后会显示类似：

```
Session Status:                Online
Account:                       your@email.com (Plan: Free)
Version:                       3.x.x
Region:                        Asia Pacific (ap)
Latency:                       50ms

Web Interface:                 http://127.0.0.1:4040
Forwarding:                    https://a1b2-c3d4.ngrok-free.app -> http://localhost:8000
Forwarding:                    https://a1b2-c3d4-1234-5678.ngrok-free.app -> http://localhost:8000

Connections:                   ttl     opn     rt1     rt5     p50     p90
                                0       0       0.00    0.00    0.00    0.00
```

**复制 HTTPS 开头的地址**，例如：
```
https://a1b2-c3d4.ngrok-free.app
```

### 步骤 7：访问服务

打开浏览器，访问：

**API 文档：**
```
https://a1b2-c3d4.ngrok-free.app/docs
```

**健康检查：**
```
https://a1b2-c3d4.ngrok-free.app/health
```

**Web 聊天界面：**
```
https://a1b2-c3d4.ngrok-free.app/chat.html
```

### 测试 API

```bash
# 使用 curl 测试
curl -X POST https://a1b2-c3d4.ngrok-free.app/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'
```

---

## ☁️ 方案2：Railway（推荐用于生产）

### 步骤 1：准备项目

```bash
# 1. 将项目推送到 GitHub
cd /workspace/projects
git init
git add .
git commit -m "Initial commit"
# 在 GitHub 上创建仓库后
git remote add origin https://github.com/yourusername/yuanxiaoji.git
git push -u origin main
```

### 步骤 2：部署到 Railway

1. 访问 https://railway.app
2. 注册/登录
3. 点击 "New Project"
4. 选择 "Deploy from GitHub"
5. 选择你的仓库
6. Railway 会自动识别 Dockerfile
7. 点击 "Deploy"

### 步骤 3：配置环境变量

在 Railway 项目设置中：

**Settings → Variables → New Variable**

添加以下变量：

```env
COZE_WORKLOAD_IDENTITY_API_KEY=your_api_key
COZE_INTEGRATION_MODEL_BASE_URL=your_base_url
```

### 步骤 4：获取公网地址

部署完成后（约2-3分钟），Railway 会提供：

```
https://yuanxiaoji-production.up.railway.app
```

### 步骤 5：访问

打开浏览器：
```
https://yuanxiaoji-production.up.railway.app/docs
```

---

## 🏢 方案3：云服务器（阿里云/腾讯云）

### 快速部署脚本

```bash
#!/bin/bash
# cloud_deploy.sh - 云服务器快速部署

# 1. 安装 Docker
curl -fsSL https://get.docker.com | sh
systemctl enable docker
systemctl start docker

# 2. 安装 Docker Compose
apt install docker-compose -y

# 3. 创建项目目录
mkdir -p /root/yuanxiaoji
cd /root/yuanxiaoji

# 4. 上传项目文件（在本地执行）
# scp -r . root@your_server_ip:/root/yuanxiaoji/

# 5. 启动服务
docker-compose up -d

# 6. 配置防火墙
ufw allow 80
ufw allow 443
ufw allow 8000
ufw --force enable

# 7. 查看状态
docker-compose ps
```

### 本地上传项目

```bash
# 在本地电脑执行
scp -r /workspace/projects/* root@your_server_ip:/root/yuanxiaoji/
```

---

## 📱 完整示例：ngrok 5分钟部署

```bash
# ========== 步骤 1：准备环境 ==========
# 注册 ngrok 账号并获取 authtoken
# 访问：https://ngrok.com/signup

# ========== 步骤 2：安装 ngrok ==========
cd /workspace/projects
wget https://bin.equinox.io/c/bNyj1mQVY4c/v3/ngrok-linux-amd64.zip
unzip ngrok-linux-amd64.zip
chmod +x ngrok

# ========== 步骤 3：配置 ==========
# 将 YOUR_AUTH_TOKEN 替换为你的真实 token
./ngrok config add-authtoken YOUR_AUTH_TOKEN

# ========== 步骤 4：启动 API 服务 ==========
docker-compose up -d
curl http://localhost:8000/health  # 确认服务正常

# ========== 步骤 5：启动 ngrok ==========
./ngrok http 8000

# ========== 步骤 6：复制公网地址 ==========
# 在输出中找到类似：
# Forwarding: https://xxxx.ngrok-free.app

# ========== 步骤 7：测试访问 ==========
# 在浏览器中打开：
# https://xxxx.ngrok-free.app/docs
```

---

## 🔧 使用配置文件 ngrok.yml

创建 `/workspace/projects/ngrok.yml`：

```yaml
version: "2"
tunnels:
  yuanxiaoji:
    addr: 8000
    proto: http
    bind_tls: true
    inspect: true
    web_addr: 0.0.0.0:4040
    region: ap  # 亚洲区域，速度更快
```

启动：
```bash
./ngrok start --all --config ngrok.yml
```

---

## 📊 方案对比

| 特性 | ngrok | Railway | 云服务器 |
|------|-------|---------|---------|
| 部署时间 | 5分钟 | 10分钟 | 30分钟 |
| 费用 | 免费 | 免费 | ¥150/月 |
| 自定义域名 | 付费 | 免费 | 免费 |
| SSL证书 | 自动 | 自动 | 手动配置 |
| 扩展性 | 低 | 中 | 高 |
| 稳定性 | 中 | 高 | 很高 |
| 适合场景 | 开发测试 | 小规模生产 | 大规模生产 |

---

## 🎯 推荐使用场景

### 选择 ngrok 如果：
- ✅ 你需要快速测试
- ✅ 开发环境演示
- ✅ 临时访问需求
- ✅ 不需要长时间稳定运行

### 选择 Railway 如果：
- ✅ 你需要稳定的服务
- ✅ 免费方案
- ✅ 无需管理服务器
- ✅ 小规模生产环境

### 选择云服务器 如果：
- ✅ 需要高性能
- ✅ 大规模部署
- ✅ 需要完全控制
- ✅ 有预算

---

## ❓ 常见问题

### Q1: ngrok 地址会变吗？

**A:** 免费版每次重启会变化，付费版固定。建议使用固定域名（付费）或 Railway（免费固定域名）。

### Q2: ngrok 免费版有什么限制？

**A:**
- 每月流量限制：1GB
- 同时隧道数：1个
- 速度限制：较低
- 地址会变化

### Q3: Railway 免费额度够用吗？

**A:** 对于小规模应用（<1000次请求/天）完全够用。

### Q4: 如何获取稳定不变的公网地址？

**A:**
1. 购买域名（如阿里云）
2. 使用云服务器
3. 配置 DNS 解析
4. 申请免费 SSL（Let's Encrypt）

---

## 📚 更多资源

- [ngrok 官方文档](https://ngrok.com/docs)
- [Railway 文档](https://docs.railway.app)
- [Docker 部署指南](https://docs.docker.com)
- [阿里云部署教程](https://help.aliyun.com)

---

## ✅ 部署检查清单

使用 ngrok 部署后，确认以下项目：

- [ ] ngrok 成功启动
- [ ] 显示 Forwarding 地址
- [ ] 可以访问 /health
- [ ] 可以访问 /docs
- [ ] API 文档正常显示
- [ ] 可以发送测试消息
- [ ] 收到正确回复

---

**🎉 恭喜！你的元小吉智能客服已经部署到公网！**

现在任何人都可以通过公网地址与元小吉对话了！🚀
