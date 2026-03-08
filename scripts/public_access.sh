#!/bin/bash

################################################################################
# 元小吉智能客服 - 公网访问部署脚本
# 支持两种方案：
#   1. 内网穿透（ngrok）- 快速临时方案
#   2. 云服务器部署 - 稳定生产方案
################################################################################

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# 检查服务是否运行
check_service() {
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        log_info "✓ API 服务运行正常 (http://localhost:8000)"
        return 0
    else
        log_error "✗ API 服务未运行，请先启动服务"
        return 1
    fi
}

# 方案1：使用 ngrok 内网穿透
setup_ngrok() {
    log_step "=== 方案1：使用 ngrok 内网穿透 ==="
    log_info "这个方案适合快速测试，无需云服务器"

    # 检查 ngrok 是否安装
    if ! command -v ngrok &> /dev/null; then
        log_warn "ngrok 未安装，正在安装..."

        # 检测系统架构
        ARCH=$(uname -m)
        OS=$(uname -s | tr '[:upper:]' '[:lower:]')

        if [[ "$ARCH" == "x86_64" ]]; then
            NGROK_ARCH="amd64"
        elif [[ "$ARCH" == "aarch64" ]]; then
            NGROK_ARCH="arm64"
        else
            log_error "不支持的架构: $ARCH"
            exit 1
        fi

        NGROK_VERSION="v3"
        NGROK_URL="https://bin.equinox.io/c/bNyj1mQVY4c/${NGROK_VERSION}/ngrok-${OS}-${NGROK_ARCH}.zip"

        log_info "下载 ngrok..."
        wget -q --show-progress "$NGROK_URL" -O /tmp/ngrok.zip || {
            log_error "下载 ngrok 失败"
            log_info "请手动下载: https://ngrok.com/download"
            exit 1
        }

        log_info "解压 ngrok..."
        unzip -q /tmp/ngrok.zip -d /tmp/
        sudo mv /tmp/ngrok /usr/local/bin/

        log_info "设置 ngrok 权限..."
        sudo chmod +x /usr/local/bin/ngrok

        rm -f /tmp/ngrok.zip

        log_info "ngrok 安装完成！"
    fi

    # 创建 ngrok 配置
    log_info "创建 ngrok 配置..."
    cat > "${PROJECT_ROOT}/ngrok.yml" << 'EOF'
version: "2"
authtoken: YOUR_AUTH_TOKEN
tunnels:
  yuanxiaoji:
    addr: 8000
    proto: http
    bind_tls: true
    web_addr: 0.0.0.0:4040
    inspect: true
    domain: ""
EOF

    log_info "ngrok 配置文件已创建: ${PROJECT_ROOT}/ngrok.yml"

    # 检查是否已配置 authtoken
    if grep -q "YOUR_AUTH_TOKEN" "${PROJECT_ROOT}/ngrok.yml"; then
        echo ""
        log_warn "⚠️  需要配置 ngrok authtoken"
        echo ""
        echo "请按以下步骤操作："
        echo "  1. 访问 https://ngrok.com/signup 注册账号"
        echo "  2. 登录后获取 authtoken: https://dashboard.ngrok.com/get-started/your-authtoken"
        echo "  3. 运行: ngrok config add-authtoken YOUR_AUTH_TOKEN"
        echo "  4. 修改 ${PROJECT_ROOT}/ngrok.yml 中的 authtoken"
        echo ""
        read -p "是否现在配置 authtoken? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            read -p "请输入你的 ngrok authtoken: " TOKEN
            ngrok config add-authtoken "$TOKEN"
            sed -i "s/YOUR_AUTH_TOKEN/$TOKEN/g" "${PROJECT_ROOT}/ngrok.yml"
        fi
    fi

    # 启动 ngrok
    log_info "启动 ngrok 内网穿透..."
    log_warn "按 Ctrl+C 停止 ngrok"

    ngrok http 8000 --log=stdout
}

# 方案2：云服务器部署
setup_cloud() {
    log_step "=== 方案2：云服务器部署 ==="
    log_info "这个方案适合生产环境，稳定可靠"

    cat << 'EOF'

┌─────────────────────────────────────────────────────────────┐
│                  云服务器部署指南                              │
├─────────────────────────────────────────────────────────────┤
│  推荐云服务商：                                                │
│    • 阿里云（ECS）：https://www.aliyun.com/product/ecs      │
│    • 腾讯云（CVM）：https://cloud.tencent.com/product/cvm    │
│    • 华为云（ECS）：https://www.huaweicloud.com/product/ecs  │
│    • 阿里云轻量应用服务器：¥60/月起                           │
│    • 腾讯云轻量应用服务器：¥50/月起                           │
├─────────────────────────────────────────────────────────────┤
│  部署步骤：                                                    │
│  1. 购买云服务器（推荐配置：2核4G，带宽5M）                    │
│  2. 安装 Docker 和 Docker Compose                            │
│  3. 上传部署包到服务器                                         │
│  4. 运行 docker-compose up -d                                │
│  5. 配置域名（可选）                                           │
│  6. 配置 SSL 证书（推荐使用 Let's Encrypt）                   │
├─────────────────────────────────────────────────────────────┤
│  预计费用：                                                    │
│    • 服务器：¥50-100/月                                       │
│    • 带宽：¥30-100/月                                         │
│    • 域名：¥50-100/年                                         │
│    总计：¥150-300/月                                          │
└─────────────────────────────────────────────────────────────┘

EOF

    read -p "是否查看详细的云部署文档? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cat "${PROJECT_ROOT}/DEPLOYMENT_README.md"
    fi
}

# 方案3：使用平台部署（Vercel/Railway）
setup_platform() {
    log_step "=== 方案3：使用云平台部署 ==="
    log_info "适合快速部署，无需管理服务器"

    cat << 'EOF'

┌─────────────────────────────────────────────────────────────┐
│                云平台部署方案                                  │
├─────────────────────────────────────────────────────────────┤
│  推荐平台：                                                    │
│    • Railway：https://railway.app (推荐，支持 Docker)        │
│      - 免费额度：$5/月                                       │
│      - 支持自定义域名                                         │
│      - 一键部署 Docker                                        │
│    • Render：https://render.com                              │
│      - 免费额度：$7/月                                       │
│      - 支持 Docker 和 Python                                 │
│    • Fly.io：https://fly.io                                  │
│      - 免费额度：3个应用                                      │
│      - 全球边缘节点                                           │
├─────────────────────────────────────────────────────────────┤
│  Railway 部署步骤：                                            │
│  1. 注册账号：https://railway.app                            │
│  2. 新建项目 → Deploy from Dockerfile                         │
│  3. 上传 Dockerfile 和项目文件                               │
│  4. 配置环境变量                                              │
│  5. 部署完成后获得公网 URL                                    │
│  6. （可选）绑定自定义域名                                     │
├─────────────────────────────────────────────────────────────┤
│  优点：                                                       │
│    • 零运维                                                    │
│    • 自动扩展                                                  │
│    • 全球 CDN                                                  │
│    • 免费额度可用                                              │
├─────────────────────────────────────────────────────────────┤
│  缺点：                                                       │
│    • 免费额度有限                                              │
│    • 不适合高并发场景                                           │
└─────────────────────────────────────────────────────────────┘

EOF
}

# 显示菜单
show_menu() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║         元小吉智能客服 - 公网访问部署菜单                   ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo ""
    echo "请选择部署方案："
    echo ""
    echo "  1️⃣  内网穿透（ngrok）"
    echo "     └─ 适合快速测试，无需服务器，5分钟内完成"
    echo "     └─ 免费（有限制）"
    echo ""
    echo "  2️⃣  云服务器部署"
    echo "     └─ 适合生产环境，稳定可靠"
    echo "     └─ ¥150-300/月"
    echo ""
    echo "  3️⃣  云平台部署（Railway）"
    echo "     └─ 适合快速部署，零运维"
    echo "     └─ 免费额度可用"
    echo ""
    echo "  4️⃣  查看当前公网访问状态"
    echo ""
    echo "  0️⃣  退出"
    echo ""
}

# 查看公网访问状态
check_public_access() {
    log_step "=== 检查公网访问状态 ==="

    # 检查 ngrok
    if pgrep -f "ngrok" > /dev/null; then
        log_info "✓ ngrok 正在运行"
        log_info "  查看状态: http://localhost:4040"
        log_info "  获取公网URL: curl http://localhost:4040/api/tunnels"
    else
        log_warn "✗ ngrok 未运行"
    fi

    # 检查服务
    if check_service; then
        log_info "✓ API 服务运行正常"
    else
        log_error "✗ API 服务未运行"
    fi
}

# 主函数
main() {
    # 检查服务是否运行
    if ! check_service; then
        log_error "请先启动 API 服务："
        echo "  cd ${PROJECT_ROOT}"
        echo "  docker-compose up -d"
        echo "  或"
        echo "  python -m src.api_server"
        exit 1
    fi

    while true; do
        show_menu
        read -p "请输入选项 [0-4]: " choice

        case $choice in
            1)
                setup_ngrok
                ;;
            2)
                setup_cloud
                ;;
            3)
                setup_platform
                ;;
            4)
                check_public_access
                ;;
            0)
                log_info "退出"
                exit 0
                ;;
            *)
                log_error "无效选项，请重新输入"
                ;;
        esac

        echo ""
        read -p "按 Enter 继续..."
    done
}

# 运行主函数
main
