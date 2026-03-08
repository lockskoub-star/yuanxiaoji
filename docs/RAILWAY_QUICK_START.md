# ⚡ Railway 快速部署（10分钟版）

> 最简单的部署方式，10分钟搞定！

---

## 🚀 快速开始

### 第一步：准备 GitHub 仓库（1分钟）

```bash
# 1. 初始化 Git
cd /workspace/projects
git init
git add .
git commit -m "Initial commit"

# 2. 在 GitHub 创建新仓库：yuanxiaoji

# 3. 推送到 GitHub
git remote add origin https://github.com/YOUR_USERNAME/yuanxiaoji.git
git branch -M main
git push -u origin main
```

---

### 第二步：在 Railway 创建项目（2分钟）

1. **访问**：https://railway.app
2. **登录**：使用 GitHub 账号登录
3. **新建项目**：点击 "New Project"
4. **选择仓库**：点击 "Deploy from GitHub repo"
5. **选择你的仓库**：找到 `yuanxiaoji` 并点击

---

### 第三步：配置环境变量（2分钟）

1. **进入设置**：在 Railway 控制台点击 "Variables"
2. **添加变量**：

**变量 1：**
```
名称：COZE_WORKLOAD_IDENTITY_API_KEY
值：你的API密钥
```

**变量 2：**
```
名称：COZE_INTEGRATION_MODEL_BASE_URL
值：你的基础URL
```

3. **重启服务**：点击 "Redeploy"

---

### 第四步：等待部署（3分钟）

Railway 会自动：
- ✓ 构建镜像
- ✓ 启动服务
- ✓ 健康检查

**等待 2-3 分钟，看到 Status: Running 即可**

---

### 第五步：访问服务（1分钟）

**复制你的公网地址：**
```
https://yuanxiaoji-production.up.railway.app
```

**打开浏览器访问：**
```
https://yuanxiaoji-production.up.railway.app/docs
```

---

## ✅ 验证

### 测试 1：健康检查

```bash
curl https://yuanxiaoji-production.up.railway.app/health
```

### 测试 2：发送消息

```bash
curl -X POST https://yuanxiaoji-production.up.railway.app/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'
```

---

## 🎯 完成！

**你现在拥有：**
- ✅ 稳定的公网地址
- ✅ 自动 HTTPS
- ✅ 免费部署
- ✅ 零运维

**你的公网地址：**
```
https://yuanxiaoji-production.up.railway.app
```

**API 文档：**
```
https://yuanxiaoji-production.up.railway.app/docs
```

---

## 📞 遇到问题？

查看完整文档：[Railway 部署指南](docs/RAILWAY_DEPLOYMENT_GUIDE.md)

---

**🎉 恭喜，部署成功！**
