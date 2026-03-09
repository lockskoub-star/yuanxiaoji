# 🚀 Railway 部署完整指南（2025更新）

> 按照这个指南，10分钟内完成部署！

---

## 📋 部署前准备清单

在开始之前，确认你已完成：

- [ ] GitHub 仓库已创建：https://github.com/lockskoub-star/yuanxiaoji
- [ ] 代码已推送到 GitHub
- [ ] 已注册 Railway 账号：https://railway.app

---

## 🎯 完整部署步骤

### 第一步：访问 Railway（1分钟）

1. 打开浏览器，访问：https://railway.app
2. 使用 GitHub 账号登录（推荐）

---

### 第二步：创建项目（2分钟）

1. 点击右上角的 **"New Project"** 按钮
2. 选择 **"Deploy from GitHub repo"**
3. 在仓库列表中找到 `lockskoub-star/yuanxiaoji`
4. 点击仓库名称
5. 确认配置后，点击 **"Deploy Now"**

**Railway 会自动：**
- 识别 Dockerfile
- 识别 Procfile
- 开始构建和部署

---

### 第三步：等待部署（3-5分钟）

Railway 会自动完成以下步骤：

```
✓ 拉取代码
✓ 构建 Docker 镜像
✓ 安装依赖
✓ 启动服务
✓ 运行健康检查
```

**等待看到：**
- Status: `Running` ✓
- Health: `Healthy` ✓

---

### 第四步：配置环境变量 ⭐ 必须步骤

**重要：必须配置环境变量，否则服务无法正常工作！**

#### 4.1 进入变量配置

1. 在 Railway 项目中，点击左侧的 **"Variables"** 标签
2. 点击右上角的 **"New Variable"**

#### 4.2 添加第一个变量

**变量名：**
```
COZE_WORKLOAD_IDENTITY_API_KEY
```

**变量值：**
```
你的实际 API 密钥
```

**如何获取：**
- 联系你的 Coze 平台管理员
- 或者在 Coze 控制台中查找

#### 4.3 添加第二个变量

**变量名：**
```
COZE_INTEGRATION_MODEL_BASE_URL
```

**变量值：**
```
你的基础 URL
```

**示例：**
```
https://api.coze.cn
```

#### 4.4 可选：添加其他变量

**日志级别：**
```
LOG_LEVEL = info
```

**消息历史记录数：**
```
MAX_MESSAGE_HISTORY = 20
```

---

### 第五步：重新部署（1分钟）

配置完环境变量后：

1. 点击页面右上角的 **"Redeploy"** 按钮
2. 或者点击 **"Deploy"** → **"Redeploy"**
3. 等待 1-2 分钟，服务会自动重启

---

### 第六步：获取公网地址

部署成功后，Railway 会提供公网地址：

**点击项目名称，查看访问地址：**

```
https://yuanxiaoji-production.up.railway.app
```

---

## ✅ 验证部署

### 测试 1：健康检查

在浏览器中访问：
```
https://yuanxiaoji-production.up.railway.app/health
```

**预期返回：**
```json
{
  "status": "healthy",
  "service": "元小吉对话 API"
}
```

### 测试 2：访问 API 文档

在浏览器中访问：
```
https://yuanxiaoji-production.up.railway.app/docs
```

你应该能看到 Swagger UI 页面。

### 测试 3：发送测试消息

**使用 curl：**
```bash
curl -X POST https://yuanxiaoji-production.up.railway.app/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'
```

**在 API 文档中测试：**
1. 访问 `https://yuanxiaoji-production.up.railway.app/docs`
2. 展开 `/chat` 接口
3. 点击 "Try it out"
4. 输入：`{"message": "你好"}`
5. 点击 "Execute"
6. 查看响应

---

## 🔧 常见问题解决

### 问题 1：构建失败 - "Build failed"

**原因：**
- Dockerfile 语法错误
- 依赖包无法安装
- 构建超时

**解决方法：**

1. 查看构建日志
   - 点击项目中的 `web` 服务
   - 点击 "Build logs" 标签
   - 找到红色错误信息

2. 检查 Dockerfile
   ```bash
   # 确认 Dockerfile 语法正确
   # 确认所有依赖都在 requirements.txt 中
   ```

3. 重新部署
   ```bash
   # 修复问题后，推送代码
   git add .
   git commit -m "fix: 修复构建问题"
   git push
   ```

---

### 问题 2：服务启动后立即崩溃

**原因：**
- 缺少环境变量
- 端口配置错误
- 代码运行时错误

**解决方法：**

1. 检查环境变量
   - 确认 `COZE_WORKLOAD_IDENTITY_API_KEY` 已配置
   - 确认 `COZE_INTEGRATION_MODEL_BASE_URL` 已配置

2. 查看运行日志
   - 点击项目中的 `web` 服务
   - 点击 "Logs" 标签
   - 查看错误信息

3. 修复问题并重新部署

---

### 问题 3：无法访问服务

**原因：**
- 服务未启动
- 健康检查失败
- 网络问题

**解决方法：**

1. 检查服务状态
   - Status 应该是 `Running`
   - Health 应该是 `Healthy`

2. 等待服务启动
   - 部署后可能需要 1-2 分钟启动

3. 检查公网地址
   - 确认地址正确
   - 尝试访问 `/health` 端点

---

### 问题 4：API 请求失败

**原因：**
- 环境变量配置错误
- API 密钥无效
- 网络连接问题

**解决方法：**

1. 验证环境变量
   ```bash
   # 确认变量名和值都正确
   # 变量名区分大小写
   ```

2. 检查 API 密钥
   - 确认密钥有效
   - 确认密钥没有过期

3. 查看日志
   - 查看具体的错误信息
   - 根据错误信息修复

---

## 📊 监控和维护

### 查看日志

1. 点击项目中的 `web` 服务
2. 点击 **"Logs"** 标签
3. 实时查看应用日志

### 查看指标

1. 点击 **"Metrics"** 标签
2. 查看：
   - CPU 使用率
   - 内存使用率
   - 网络流量
   - 请求响应时间

### 设置告警

1. 点击 **"Alerts"** 标签
2. 配置告警规则：
   - CPU 使用率 > 80%
   - 内存使用率 > 90%
   - 错误率 > 5%

---

## 🔄 更新部署

### 自动部署

每次推送代码到 GitHub，Railway 会自动部署：

```bash
# 修改代码
# ...

# 提交并推送
git add .
git commit -m "update: 添加新功能"
git push

# Railway 会自动部署
```

### 手动部署

1. 在 Railway 控制台，点击 **"Redeploy"**
2. 选择最新的 commit
3. 点击 **"Redeploy Now"**

---

## 💰 费用说明

### 免费额度

Railway 提供每月 **$5 免费额度**：

- ✅ 512MB 内存
- ✅ 500 小时运行时间
- ✅ 10GB 网络传输
- ✅ 适合小规模应用

### 计费方式

如果超出免费额度：

- 内存：$0.000258 / MB / 分钟
- CPU：$0.00010 / vCPU / 分钟

**对于小规模应用（<1000 次请求/天），免费额度完全够用！**

---

## 🎉 部署成功！

恭喜！你已经成功部署了元小吉智能客服！

### 你的公网地址

```
https://yuanxiaoji-production.up.railway.app
```

### 可以访问的端点

| 端点 | 说明 |
|------|------|
| `/` | API 信息 |
| `/health` | 健康检查 |
| `/docs` | API 文档 |
| `/chat` | 对话接口 |

### 下一步

1. **测试 API**
   - 访问 API 文档
   - 发送测试消息

2. **集成到应用**
   - 网站集成
   - 移动 App 集成
   - 小程序集成

3. **监控服务**
   - 查看日志
   - 监控指标
   - 设置告警

---

## 📞 获取帮助

- **Railway 文档**：https://docs.railway.app
- **Railway 定价**：https://railway.app/pricing
- **项目文档**：查看 `docs/` 目录

---

## ✅ 部署检查清单

部署完成后，确认：

- [ ] Status 显示 "Running"
- [ ] Health 显示 "Healthy"
- [ ] 可以访问 `/health` 端点
- [ ] 可以访问 `/docs` 页面
- [ ] 可以发送 `/chat` 请求
- [ ] 收到正确的响应
- [ ] 环境变量已正确配置
- [ ] 服务稳定运行

---

**🎊 恭喜，部署成功！开始使用你的智能客服吧！**
