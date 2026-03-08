# ✅ Railway 部署检查清单

> 按照这个清单，确保部署成功！

---

## 📋 准备阶段

### GitHub 仓库

- [ ] 项目已在 GitHub 上
- [ ] 仓库是 Public 或 Private
- [ ] 包含以下文件：
  - [ ] `Dockerfile`
  - [ ] `Procfile`
  - [ ] `railway.toml`
  - [ ] `requirements.txt`
  - [ ] `.gitignore`
  - [ ] `src/` 目录
  - [ ] `config/` 目录

---

## 🔑 Railway 账号

- [ ] 已注册 Railway 账号
- [ ] 已登录（使用 GitHub 账号）
- [ ] 可以访问 Railway 控制台

---

## 🚀 部署步骤

### 1. 创建项目

- [ ] 点击 "New Project"
- [ ] 选择 "Deploy from GitHub repo"
- [ ] 找到并选择 `yuanxiaoji` 仓库
- [ ] 确认配置文件已自动识别
- [ ] 点击 "Deploy Now"

### 2. 等待构建

- [ ] 看到 "Building..." 状态
- [ ] 看到 "Docker image built" ✓
- [ ] 看到 "Container started" ✓
- [ ] 看到 "Health check passed" ✓
- [ ] 状态显示 "Running" ✓

### 3. 配置环境变量

- [ ] 点击 "Variables" 标签
- [ ] 添加 `COZE_WORKLOAD_IDENTITY_API_KEY`
- [ ] 添加 `COZE_INTEGRATION_MODEL_BASE_URL`
- [ ] 点击 "Redeploy" 重启服务

---

## ✅ 验证部署

### 1. 服务状态

- [ ] Status 显示 "Running" ✓
- [ ] Health 显示 "Healthy" ✓
- [ ] 无错误日志

### 2. 访问测试

- [ ] 可以访问 `/health` 端点
- [ ] 可以访问 `/docs` 页面
- [ ] 可以发送 `/chat` 请求
- [ ] 收到正确的响应

### 3. 功能测试

- [ ] 测试基础问候：{"message": "你好"}
- [ ] 测试知识库查询：{"message": "搜索沉香信息"}
- [ ] 测试工单创建：{"message": "我要投诉"}
- [ ] 测试情感分析：{"message": "今天心情不好"}

---

## 🌐 公网地址

- [ ] 获得公网地址：`https://xxxx.up.railway.app`
- [ ] 地址可以正常访问
- [ ] HTTPS 正常工作（没有证书警告）
- [ ] API 文档正常显示

---

## 📊 监控设置

- [ ] 查看过实时日志
- [ ] 查看过监控指标
- [ ] （可选）设置了告警规则
- [ ] （可选）配置了自定义域名

---

## 🎉 完成！

如果你完成了以上所有检查，恭喜你！🎊

**你现在拥有：**
- ✅ 稳定的公网地址
- ✅ 自动 HTTPS
- ✅ 免费部署
- ✅ 零运维体验

---

## 🔧 遇到问题？

### 部署失败

1. 检查构建日志，找到具体错误
2. 确认所有依赖都在 `requirements.txt` 中
3. 确认 Dockerfile 语法正确
4. 修复后重新部署

### 服务崩溃

1. 查看 "Logs" 标签
2. 确认环境变量配置正确
3. 检查端口配置
4. 重启服务

### 无法访问

1. 确认服务状态是 "Running"
2. 检查公网地址是否正确
3. 尝试访问 `/health` 端点
4. 查看日志排查问题

---

## 📚 相关文档

- [Railway 快速部署](docs/RAILWAY_QUICK_START.md)
- [Railway 部署指南](docs/RAILWAY_DEPLOYMENT_GUIDE.md)
- [公网访问指南](docs/PUBLIC_ACCESS_GUIDE.md)

---

**✅ 全部完成！开始使用你的智能客服吧！**
