# ⚡ 本地快速开始

> 3 步在本地运行元小吉

---

## 步骤 1：启动服务

```bash
cd /workspace/projects

# 方法 1：使用脚本（推荐）
bash scripts/http_run.sh

# 方法 2：直接运行
python src/main.py -m http
```

**启动成功后，你会看到：**
```
INFO:     Uvicorn running on http://0.0.0.0:5000
```

---

## 步骤 2：访问 API 文档

**打开浏览器访问：**
```
http://localhost:5000/docs
```

---

## 步骤 3：测试对话

**在 API 文档中：**

1. 找到 `/chat` 接口
2. 点击 "Try it out"
3. 输入：`{"message": "你好"}`
4. 点击 "Execute"
5. 查看回复

---

## 📝 其他运行方式

### 使用 curl 测试

```bash
# 健康检查
curl http://localhost:5000/health

# 发送消息
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'
```

### Flow 模式（直接运行）

```bash
python src/main.py -m flow -i '{"text": "你好"}'
```

---

## 🔧 使用其他端口

```bash
# 指定端口 8000
python src/main.py -m http -p 8000

# 然后访问
http://localhost:8000/docs
```

---

## ⚠️ 停止服务

在运行的终端按 `Ctrl + C`

---

## 📚 详细文档

查看完整指南：`docs/LOCAL_RUN_GUIDE.md`

---

**就这么简单！开始使用吧！** 🚀
