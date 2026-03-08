#!/bin/bash

################################################################################
# 快速启动 ngrok 内网穿透（一键部署到公网）
################################################################################

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# 检查服务
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    log_warn "API 服务未运行，尝试启动..."
    docker-compose up -d > /dev/null 2>&1 || {
        log_warn "Docker 启动失败，尝试使用 Python..."
        python -m src.api_server &
        sleep 3
    }

    if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
        log_warn "服务启动中，请稍候..."
        sleep 5
    fi
fi

log_info "✓ API 服务已启动"

# 检查 ngrok
if ! command -v ngrok &> /dev/null; then
    log_warn "正在安装 ngrok..."

    ARCH=$(uname -m)
    OS=$(uname -s | tr '[:upper:]' '[:lower:]')

    [[ "$ARCH" == "x86_64" ]] && NGROK_ARCH="amd64" || NGROK_ARCH="arm64"

    wget -q --show-progress "https://bin.equinox.io/c/bNyj1mQVY4c/v3/ngrok-${OS}-${NGROK_ARCH}.zip" -O /tmp/ngrok.zip
    unzip -q /tmp/ngrok.zip -d /tmp/
    sudo mv /tmp/ngrok /usr/local/bin/
    sudo chmod +x /usr/local/bin/ngrok
    rm -f /tmp/ngrok.zip

    log_info "✓ ngrok 安装完成"
fi

# 检查配置
if ! ngrok config check > /dev/null 2>&1; then
    echo ""
    log_warn "⚠️  首次使用需要配置 ngrok authtoken"
    echo ""
    echo "1. 访问 https://ngrok.com/signup 注册（免费）"
    echo "2. 登录后获取 authtoken: https://dashboard.ngrok.com/get-started/your-authtoken"
    echo ""
    read -p "请输入你的 ngrok authtoken: " TOKEN
    ngrok config add-authtoken "$TOKEN"
    log_info "✓ 配置完成"
fi

log_info "正在启动 ngrok 内网穿透..."
echo ""
log_info "🌐 公网访问地址将在下面显示"
echo ""
log_warn "按 Ctrl+C 停止 ngrok"
echo ""

ngrok http 8000
