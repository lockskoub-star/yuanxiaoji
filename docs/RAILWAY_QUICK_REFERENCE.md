# 🚀 Railway 快速部署参考

> 3 分钟快速参考

---

## ⚡ 快速开始

### 1️⃣ 访问 Railway

```
https://railway.app
```

---

### 2️⃣ 创建项目

1. New Project → Deploy from GitHub
2. 选择 `lockskoub-star/yuanxiaoji`
3. Deploy Now

---

### 3️⃣ 配置环境变量

**Variables 标签 → New Variable**

```
COZE_WORKLOAD_IDENTITY_API_KEY = 你的API密钥
COZE_INTEGRATION_MODEL_BASE_URL = 你的基础URL
```

点击 **Redeploy**

---

## ✅ 验证

**健康检查：**
```
https://yuanxiaoji-production.up.railway.app/health
```

**API 文档：**
```
https://yuanxiaoji-production.up.railway.app/docs
```

**测试对话：**
```bash
curl -X POST https://yuanxiaoji-production.up.railway.app/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'
```

---

## 🔍 常见问题

| 问题 | 解决方法 |
|------|---------|
| 构建失败 | 查看构建日志，修复后重新推送 |
| 服务崩溃 | 检查环境变量是否配置 |
| 无法访问 | 等待 1-2 分钟，服务启动中 |

---

## 📚 详细文档

- 完整指南：`docs/RAILWAY_DEPLOYMENT_COMPLETE.md`
- 快速教程：`docs/RAILWAY_QUICK_START.md`
- 检查清单：`docs/RAILWAY_CHECKLIST.md`

---

**立即开始部署！** 🚀
