# 🚀 公网部署包

## 📦 包含内容

✅ **部署指南**：`DEPLOYMENT_GUIDE.md` - 完整的部署文档
✅ **快速开始**：`QUICK_START.md` - 5分钟快速部署
✅ **Docker 配置**：Dockerfile, docker-compose.yml, nginx.conf
✅ **部署脚本**：`scripts/deploy.sh` - 一键部署
✅ **监控脚本**：`scripts/monitor.sh` - 服务监控
✅ **环境配置**：`.env.example` - 环境变量模板

---

## 🎯 快速开始

### 第1步：准备服务器
```bash
# 购买云服务器（推荐配置）
# - 2核 CPU
# - 4GB 内存
# - Ubuntu 20.04/22.04
```

### 第2步：安装 Docker
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
apt install -y docker-compose
```

### 第3步：上传项目
```bash
scp -r /workspace/projects root@your_server_ip:/root/
```

### 第4步：配置环境
```bash
ssh root@your_server_ip
cd /root/projects
cp .env.example .env
nano .env
```

### 第5步：一键部署
```bash
./scripts/deploy.sh
```

---

## 📝 配置清单

必须配置的环境变量：
- [ ] `COZE_WORKLOAD_IDENTITY_API_KEY` - Coze API Key
- [ ] `SECRET_KEY` - 随机安全密钥
- [ ] `ALLOWED_ORIGINS` - 允许的域名

可选配置：
- [ ] 域名和 HTTPS
- [ ] 数据库连接
- [ ] Redis 缓存
- [ ] 监控告警

---

## 🔍 部署后检查

```bash
# 1. 检查服务
docker-compose ps

# 2. 检查健康
curl http://localhost:8000/health

# 3. 测试 API
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'

# 4. 查看日志
docker-compose logs -f
```

---

## 🛠️ 常用命令

```bash
# 部署
./scripts/deploy.sh

# 监控
./scripts/monitor.sh

# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 停止服务
docker-compose down

# 更新服务
docker-compose pull
docker-compose up -d
```

---

## 📊 访问地址

部署成功后，可以通过以下地址访问：

| 服务 | 地址 |
|------|------|
| API 接口 | `http://your_server_ip:8000` |
| 健康检查 | `http://your_server_ip:8000/health` |
| API 文档 | `http://your_server_ip:8000/docs` |
| 聊天界面 | `http://your_server_ip:8000/static/chat.html` |

---

## 🔒 安全建议

1. **配置 HTTPS**：使用 Let's Encrypt 免费 SSL 证书
2. **设置防火墙**：只开放 80、443 端口
3. **定期更新**：及时更新系统和依赖
4. **监控日志**：定期检查错误日志
5. **备份数据**：定期备份配置和数据

---

## 📞 技术支持

查看详细文档：
- `DEPLOYMENT_GUIDE.md` - 完整部署指南
- `QUICK_START.md` - 快速开始
- `ACCESS_GUIDE.md` - 访问指南

---

**祝您部署顺利！** 🎉
