# 🚀 Railway 部署指南

> 10 分钟内将元小吉智能客服部署到 Railway，获得免费的固定公网地址

---

## 📋 目录

- [什么是 Railway？](#什么是-railway)
- [为什么选择 Railway？](#为什么选择-railway)
- [部署步骤](#部署步骤)
- [配置环境变量](#配置环境变量)
- [验证部署](#验证部署)
- [常见问题](#常见问题)

---

## 🎯 什么是 Railway？

Railway 是一个现代化的应用部署平台，提供：
- ✅ **完全免费**：每月 $5 免费额度
- ✅ **一键部署**：支持 Dockerfile 直接部署
- ✅ **固定域名**：提供稳定的公网地址
- ✅ **自动 HTTPS**：无需配置 SSL 证书
- ✅ **自动扩展**：根据负载自动调整
- ✅ **零运维**：无需管理服务器

---

## ✨ 为什么选择 Railway？

| 特性 | Railway | ngrok | 云服务器 |
|------|---------|-------|---------|
| 费用 | 免费（$5/月） | 免费（有限制） | ¥150/月起 |
| 固定域名 | ✅ 是 | ❌ 否 | ✅ 是 |
| HTTPS | ✅ 自动 | ✅ 自动 | 手动配置 |
| 稳定性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 部署速度 | 10分钟 | 5分钟 | 30分钟 |
| 运维 | 零运维 | 需要维护 | 需要维护 |
| 扩展性 | 自动扩展 | 无 | 手动扩展 |

---

## 📝 部署步骤

### 步骤 1：注册 Railway 账号

1. 访问：https://railway.app
2. 点击右上角的 "Login" 或 "Sign Up"
3. 使用以下方式注册：
   - GitHub 账号（推荐）
   - Google 账号
   - Email 注册

**推荐使用 GitHub 注册**，因为后续需要连接 GitHub 仓库。

---

### 步骤 2：准备 GitHub 仓库

**如果项目已经在 GitHub 上，跳到步骤 3。**

#### A. 在本地初始化 Git 仓库

```bash
cd /workspace/projects

# 初始化 Git
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: 元小吉智能客服"

# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/yuanxiaoji.git
```

#### B. 在 GitHub 上创建仓库

1. 访问：https://github.com/new
2. 仓库名：`yuanxiaoji`
3. 设置为 Public 或 Private（都可以）
4. 点击 "Create repository"

#### C. 推送到 GitHub

```bash
# 推送代码
git push -u origin main

# 或者如果使用 master 分支
git push -u origin master
```

---

### 步骤 3：在 Railway 中创建项目

1. 登录 Railway 控制台：https://railway.app
2. 点击 "New Project" 按钮
3. 选择 "Deploy from GitHub repo"

![选择 GitHub 仓库](https://docs.railway.app/images/gh_repo.png)

---

### 步骤 4：连接 GitHub 仓库

1. 在弹出页面中，找到你的 `yuanxiaoji` 仓库
2. 点击仓库名称
3. Railway 会自动扫描仓库中的配置文件（Dockerfile, Procfile 等）
4. 确认部署配置后，点击 "Deploy Now"

---

### 步骤 5：等待部署完成

Railway 会自动：
1. 拉取代码
2. 构建 Docker 镜像
3. 启动服务
4. 运行健康检查

**预计时间：2-5 分钟**

你可以看到构建日志：
```
Building...
✓ Docker image built
✓ Container started
✓ Health check passed
```

---

### 步骤 6：获取公网地址

部署完成后，Railway 会提供一个公网地址：

```
https://yuanxiaoji-production.up.railway.app
```

**这个地址是固定的，重启服务后不会改变！**

---

## ⚙️ 配置环境变量

### 步骤 1：进入项目设置

1. 在 Railway 控制台中，点击你的项目
2. 点击 "Variables" 标签

### 步骤 2：添加环境变量

点击 "New Variable"，添加以下变量：

#### 必须配置：

**1. `COZE_WORKLOAD_IDENTITY_API_KEY`**

```
your_actual_api_key_here
```

**2. `COZE_INTEGRATION_MODEL_BASE_URL`**

```
your_actual_base_url_here
```

#### 可选配置：

**3. `LOG_LEVEL`**

```
info
```

**4. `MAX_MESSAGE_HISTORY`**

```
20
```

### 步骤 3：重启服务

添加环境变量后，点击 "Redeploy" 重启服务，让新变量生效。

---

## ✅ 验证部署

### 1. 检查服务状态

在 Railway 控制台中，查看服务状态：
- Status: `Running` ✅
- Health: `Healthy` ✅

### 2. 访问 API 文档

打开浏览器，访问：

```
https://yuanxiaoji-production.up.railway.app/docs
```

你应该能看到 Swagger UI 页面。

### 3. 测试健康检查

```bash
curl https://yuanxiaoji-production.up.railway.app/health
```

预期返回：
```json
{
  "status": "ok",
  "message": "Service is running"
}
```

### 4. 测试对话功能

在 API 文档页面：
1. 展开 `/chat` 接口
2. 点击 "Try it out"
3. 输入：`{"message": "你好"}`
4. 点击 "Execute"
5. 查看响应

---

## 🌐 获取你的公网地址

Railway 提供的公网地址格式：

```
https://<project-name>-<environment>.up.railway.app
```

示例：
```
https://yuanxiaoji-production.up.railway.app
https://yuanxiaoji-staging.up.railway.app
```

### 自定义域名（可选）

如果你有自己的域名，可以配置自定义域名：

1. 在 Railway 项目设置中，点击 "Domains"
2. 点击 "New Domain"
3. 输入你的域名，如：`api.yourdomain.com`
4. 在域名 DNS 管理中添加 CNAME 记录：
   ```
   api  CNAME  <your-railway-domain>.up.railway.app
   ```
5. 等待 DNS 生效（通常 5-10 分钟）
6. Railway 会自动配置 SSL 证书

---

## 📊 监控和日志

### 查看日志

1. 在 Railway 控制台中，点击你的服务
2. 点击 "Logs" 标签
3. 实时查看应用日志

### 查看指标

1. 点击 "Metrics" 标签
2. 查看：
   - CPU 使用率
   - 内存使用率
   - 网络流量
   - 请求响应时间

### 设置告警

1. 点击 "Alerts" 标签
2. 配置告警规则：
   - CPU 使用率 > 80%
   - 内存使用率 > 90%
   - 错误率 > 5%

---

## 🔄 更新部署

### 自动部署

如果你使用 GitHub，每次 push 代码都会自动触发部署：

```bash
# 修改代码后
git add .
git commit -m "Update feature"
git push

# Railway 会自动部署
```

### 手动部署

1. 在 Railway 控制台中，点击 "Redeploy"
2. 选择最新的 commit
3. 点击 "Redeploy Now"

---

## 💰 费用说明

Railway 的免费额度：

- ✅ 每月 $5 免费额度
- ✅ 512MB 内存
- ✅ 500 小时运行时间
- ✅ 10GB 网络传输

**对于小规模应用（<1000 次请求/天），免费额度完全够用！**

如果超出免费额度，按使用量计费：
- $0.000258 / MB 内存 / 分钟
- $0.00010 / vCPU / 分钟

---

## ❓ 常见问题

### Q1: 部署失败，提示 "build failed"

**解决：**

1. 检查 Dockerfile 语法是否正确
2. 查看构建日志，找到具体错误
3. 确保所有依赖都在 requirements.txt 中
4. 检查环境变量是否配置

### Q2: 服务启动后立即崩溃

**解决：**

1. 检查日志：点击 "Logs" 标签
2. 常见原因：
   - 缺少环境变量
   - 端口配置错误
   - 依赖包版本冲突
3. 修复后重新部署

### Q3: 如何获取 COZE_WORKLOAD_IDENTITY_API_KEY？

**解决：**

这个密钥来自 Coze 平台，联系你的平台管理员获取。

### Q4: 免费额度够用吗？

**回答：**

对于以下场景，免费额度完全够用：
- 个人项目
- 测试环境
- 小规模应用（<1000 次请求/天）
- 内部工具

如果需要高并发或大规模使用，建议：
1. 优化代码，减少资源使用
2. 使用缓存
3. 升级到付费计划

### Q5: 如何备份数据？

**解决：**

Railway 提供数据持久化：
- 使用 Railway 提供的 PostgreSQL（如需）
- 定期导出数据
- 使用对象存储（如 AWS S3）

### Q6: 可以删除项目重新部署吗？

**回答：**

可以：
1. 在 Railway 控制台中，点击项目设置
2. 点击 "Delete Project"
3. 重新创建项目并部署

---

## 📚 相关文档

- [Railway 官方文档](https://docs.railway.app)
- [Railway 定价](https://railway.app/pricing)
- [Railway GitHub](https://github.com/railwayapp)
- [Dockerfile 最佳实践](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

---

## 🎉 总结

恭喜！你已经成功将元小吉智能客服部署到 Railway！

**现在你可以：**

✅ 访问稳定的公网地址  
✅ 使用自动 HTTPS  
✅ 享受零运维体验  
✅ 查看实时监控和日志  
✅ 免费使用（在额度内）  

**你的公网地址：**
```
https://yuanxiaoji-production.up.railway.app
```

**立即体验：**
```
https://yuanxiaoji-production.up.railway.app/docs
```

---

**🚀 开始你的 Railway 之旅吧！**
