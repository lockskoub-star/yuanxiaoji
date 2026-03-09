# 🚀 ngrok 部署指南

> 5分钟快速配置 ngrok，获得公网访问地址

---

## 📋 目录

1. [什么是 ngrok](#什么是-ngrok)
2. [安装 ngrok](#安装-ngrok)
3. [配置 authtoken](#配置-authtoken)
4. [启动 ngrok](#启动-ngrok)
5. [测试访问](#测试访问)
6. [常见问题](#常见问题)

---

## 🎯 什么是 ngrok？

ngrok 是一个内网穿透工具，可以将本地服务暴露到公网。

**优点：**
- ✅ 5分钟完成配置
- ✅ 速度快
- ✅ 自动 HTTPS
- ✅ 免费（有限制）

**缺点：**
- ❌ 免费版地址会变化
- ❌ 每次重启需要重新运行

---

## 📦 安装 ngrok

### 方法 1：自动安装脚本（推荐）

```bash
# 下载并安装
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update
sudo apt install ngrok
```

### 方法 2：手动下载

#### 2.1 访问下载页面

打开浏览器：https://ngrok.com/download

#### 2.2 选择 Linux 版本

下载 Linux 64-bit 版本（zip 或 tgz）

#### 2.3 解压并安装

```bash
# 解压
unzip ngrok-v3-stable-linux-amd64.zip

# 或解压 tgz
tar -xzf ngrok-v3-stable-linux-amd64.tgz

# 移动到系统目录
sudo mv ngrok /usr/local/bin/

# 设置执行权限
sudo chmod +x /usr/local/bin/ngrok

# 验证安装
ngrok version
```

### 方法 3：使用 snap（如果可用）

```bash
sudo snap install ngrok
```

---

## 🔑 配置 authtoken

### 步骤 1：注册 ngrok 账号

1. 访问：https://ngrok.com/signup
2. 使用邮箱注册（免费）
3. 验证邮箱

### 步骤 2：获取 authtoken

1. 登录 ngrok：https://dashboard.ngrok.com
2. 访问：https://dashboard.ngrok.com/get-started/your-authtoken
3. 复制你的 authtoken（类似：`2xxx...xxx...xxx`）

**示例 authtoken：**
```
2abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
```

### 步骤 3：配置 authtoken

```bash
# 将 YOUR_TOKEN 替换为你的真实 token
ngrok config add-authtoken YOUR_TOKEN
```

**示例：**
```bash
ngrok config add-authtoken 2abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
```

---

## 🚀 启动 ngrok

### 确认本地服务运行

```bash
# 检查本地服务是否运行
curl http://localhost:5000/health

# 预期返回：
# {"status":"ok","message":"Service is running"}
```

### 启动 ngrok

```bash
# 启动 ngrok，暴露 5000 端口
ngrok http 5000
```

### 查看输出

ngrok 启动后会显示类似：

```
ngrok by @inconshreveable

Session Status                Online
Account                       your@email.com (Plan: Free)
Version                       3.x.x
Region                        Asia Pacific (ap)
Latency                       50ms

Web Interface:                 http://127.0.0.1:4040
Forwarding:                    https://a1b2-c3d4.ngrok-free.app -> http://localhost:5000

Connections:                   ttl     opn     rt1     rt5     p50     p90
                                0       0       0.00    0.00    0.00    0.00
```

**复制这个 HTTPS 地址：**
```
https://a1b2-c3d4.ngrok-free.app
```

这就是你的公网访问地址！

---

## ✅ 测试访问

### 测试 1：健康检查

在浏览器中访问：
```
https://a1b2-c3d4.ngrok-free.app/health
```

**预期返回：**
```json
{
  "status": "ok",
  "message": "Service is running"
}
```

### 测试 2：API 文档

在浏览器中访问：
```
https://a1b2-c3d4.ngrok-free.app/docs
```

你应该能看到 Swagger UI 页面。

### 测试 3：发送消息

**使用 curl：**
```bash
curl -X POST https://a1b2-c3d4.ngrok-free.app/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'
```

**在 API 文档中测试：**
1. 访问 `https://a1b2-c3d4.ngrok-free.app/docs`
2. 展开 `/chat` 接口
3. 点击 "Try it out"
4. 输入：`{"message": "你好"}`
5. 点击 "Execute"
6. 查看响应

---

## 🔧 高级配置

### 使用配置文件

创建 `ngrok.yml`：

```yaml
version: "2"
authtoken: YOUR_AUTHTOKEN

tunnels:
  yuanxiaoji:
    addr: 5000
    proto: http
    bind_tls: true
    web_addr: 0.0.0.0:4040
    inspect: true
    region: ap  # 亚洲区域，速度更快
```

启动：
```bash
ngrok start --all --config ngrok.yml
```

### 固定域名（付费）

免费版的地址每次启动都会变化。如果需要固定域名：

1. 升级到付费计划
2. 购买固定域名
3. 配置自定义域名

---

## 📊 监控和日志

### 查看实时请求

访问 ngrok Web 界面：
```
http://127.0.0.1:4040
```

可以实时查看所有 HTTP 请求和响应。

### 查看日志

ngrok 会实时显示所有请求的详细信息。

---

## ❓ 常见问题

### Q1: ngrok 未安装

**解决：**
按照上面的"安装 ngrok"部分操作。

---

### Q2: 配置 authtoken 失败

**解决：**
1. 确认 token 正确
2. 确认网络连接正常
3. 重新获取 token

---

### Q3: 连接超时

**解决：**
1. 检查本地服务是否运行
2. 检查端口是否正确（应该是 5000）
3. 检查防火墙设置

---

### Q4: 地址会变吗？

**回答：**
- 免费版：每次启动都会变化
- 付费版：可以固定域名

---

### Q5: 如何停止 ngrok？

**方法 1：**
在运行 ngrok 的终端按 `Ctrl + C`

**方法 2：**
```bash
# 找到 ngrok 进程
ps aux | grep ngrok

# 杀死进程
kill <PID>
```

---

### Q6: 免费版有什么限制？

- ❌ 每月流量限制：1GB
- ❌ 同时隧道数：1个
- ❌ 地址会变化
- ❌ 速度有限制

---

## 💰 费用说明

### 免费版

- ✅ 完全免费
- ✅ 适合测试和开发
- ⚠️ 有一些限制

### 付费版

**Basic 计划：** $9.99/月
- 固定域名
- 无流量限制
- 优先支持

**Pro 计划：** $29.99/月
- 更多隧道
- 自定义域名
- 高级功能

---

## 🎯 使用场景

### 适合：
- ✅ 快速测试
- ✅ 本地开发演示
- ✅ 临时访问需求
- ✅ 不需要长期运行

### 不适合：
- ❌ 生产环境
- ❌ 高并发访问
- ❌ 需要固定域名
- ❌ 长期稳定运行

---

## 📚 相关资源

- [ngrok 官网](https://ngrok.com)
- [ngrok 文档](https://ngrok.com/docs)
- [ngrok 定价](https://ngrok.com/pricing)

---

## 🎉 总结

**快速开始：**

1. **安装 ngrok**
   ```bash
   curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
   echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
   sudo apt update
   sudo apt install ngrok
   ```

2. **配置 authtoken**
   ```bash
   ngrok config add-authtoken YOUR_TOKEN
   ```

3. **启动 ngrok**
   ```bash
   ngrok http 5000
   ```

4. **访问公网地址**
   ```
   https://xxxx-xxxx.ngrok-free.app/docs
   ```

---

**祝你使用愉快！** 🚀
