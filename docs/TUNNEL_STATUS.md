# 🔍 localtunnel 隧道状态说明

## 当前状态

localtunnel 服务目前遇到连接问题，无法稳定运行。

## 问题详情

```
Error: connection refused: localtunnel.me:34067 (check your firewall settings)
```

## 原因分析

localtunnel 的公共服务器可能：
1. 临时不可用
2. 防火墙阻止了连接
3. 网络配置问题

## 解决方案

### 方案 1：使用 ngrok（推荐）⭐

ngrok 更稳定，速度更快：

```bash
# 1. 注册账号
https://ngrok.com/signup

# 2. 获取 authtoken
https://dashboard.ngrok.com/get-started/your-authtoken

# 3. 安装 ngrok
wget https://bin.equinox.io/c/bNyj1mQVY4c/v3/ngrok-linux-amd64.zip
unzip ngrok-linux-amd64.zip
chmod +x ngrok

# 4. 配置
./ngrok config add-authtoken YOUR_TOKEN_HERE

# 5. 启动
./ngrok http 5000
```

### 方案 2：使用 Railway（免费且稳定）

1. 访问 https://railway.app
2. 新建项目
3. 连接 GitHub 仓库
4. 配置环境变量
5. 部署完成

### 方案 3：等待 localtunnel 恢复

localtunnel 的服务可能会自动恢复，稍后再试。

## 当前本地服务

**本地服务仍然正常运行**：

```bash
# 访问本地 API
curl http://localhost:5000/health
# 返回：{"status":"ok","message":"Service is running"}

# 访问本地 API 文档
http://localhost:5000/docs
```

## 建议

**强烈建议使用 ngrok 或 Railway**：
- ✅ 更稳定
- ✅ 速度更快
- ✅ 可靠性更高
- ✅ 更好的支持

需要帮助配置 ngrok 吗？
