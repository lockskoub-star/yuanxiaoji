# 🚀 使用 ngrok 快速部署

> 最简单的部署方式，3步搞定！

---

## ⚡ 快速开始

### 方法 1：使用自动脚本（推荐）⭐

```bash
# 运行配置脚本
cd /workspace/projects
./scripts/setup_ngrok.sh
```

脚本会自动：
1. ✓ 检查本地服务
2. ✓ 安装 ngrok（如果需要）
3. ✓ 配置 authtoken
4. ✓ 启动 ngrok

**就这么简单！**

---

### 方法 2：手动配置

#### 步骤 1：注册 ngrok（1分钟）

1. 访问：https://ngrok.com/signup
2. 使用邮箱注册（免费）
3. 验证邮箱

#### 步骤 2：获取 authtoken（1分钟）

1. 登录 ngrok：https://dashboard.ngrok.com
2. 访问：https://dashboard.ngrok.com/get-started/your-authtoken
3. 复制你的 authtoken

#### 步骤 3：安装 ngrok（1分钟）

```bash
# 自动安装
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update
sudo apt install ngrok
```

#### 步骤 4：配置 authtoken（1分钟）

```bash
# 将 YOUR_TOKEN 替换为你的真实 token
ngrok config add-authtoken YOUR_TOKEN
```

#### 步骤 5：启动 ngrok（1分钟）

```bash
# 启动 ngrok
ngrok http 5000
```

#### 步骤 6：复制公网地址（即时）

ngrok 启动后会显示：

```
Forwarding: https://xxxx-xxxx.ngrok-free.app -> http://localhost:5000
```

**复制这个 HTTPS 地址！**

---

## ✅ 测试访问

### 健康检查

```
https://xxxx-xxxx.ngrok-free.app/health
```

### API 文档

```
https://xxxx-xxxx.ngrok-free.app/docs
```

### 发送消息

```bash
curl -X POST https://xxxx-xxxx.ngrok-free.app/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'
```

---

## 📝 ngrok 输出示例

```
ngrok by @inconshreveable

Session Status                Online
Account                       your@email.com (Plan: Free)
Version                       3.x.x
Region                        Asia Pacific (ap)

Web Interface:                 http://127.0.0.1:4040
Forwarding:                    https://a1b2-c3d4.ngrok-free.app -> http://localhost:5000

Connections:                   ttl     opn     rt1     rt5     p50     p90
                                0       0       0.00    0.00    0.00    0.00
```

**复制 `Forwarding` 后面的 HTTPS 地址！**

---

## 🔍 常见问题

### Q1: 如何停止 ngrok？

在运行 ngrok 的终端按 `Ctrl + C`

### Q2: 地址会变吗？

免费版每次启动都会变化。如果需要固定域名，需要升级到付费版。

### Q3: 免费版有什么限制？

- 每月流量：1GB
- 同时隧道数：1个
- 地址会变化

### Q4: 如何查看请求日志？

访问：http://127.0.0.1:4040

---

## 📚 详细文档

查看完整指南：`docs/NGROK_DEPLOYMENT_GUIDE.md`

---

## 🎯 立即开始

**使用自动脚本：**
```bash
./scripts/setup_ngrok.sh
```

**或者手动配置（5分钟）：**
1. 注册：https://ngrok.com/signup
2. 获取 token：https://dashboard.ngrok.com/get-started/your-authtoken
3. 安装 ngrok
4. 配置 token
5. 启动 ngrok
6. 复制公网地址

---

**祝你使用愉快！** 🚀
