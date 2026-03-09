#!/bin/bash

################################################################################
# ngrok 快速配置和启动脚本
################################################################################

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step() { echo -e "${BLUE}[STEP]${NC} $1"; }

# 检查本地服务
check_local_service() {
    log_step "检查本地服务..."

    if curl -s http://localhost:5000/health > /dev/null 2>&1; then
        log_info "✓ 本地服务运行正常 (http://localhost:5000)"
        return 0
    else
        log_error "✗ 本地服务未运行"
        log_info "请先启动服务："
        echo "  python src/main.py"
        return 1
    fi
}

# 检查 ngrok 是否已安装
check_ngrok() {
    log_step "检查 ngrok 安装..."

    if command -v ngrok &> /dev/null; then
        log_info "✓ ngrok 已安装"
        ngrok version
        return 0
    else
        log_warn "✗ ngrok 未安装"
        return 1
    fi
}

# 安装 ngrok
install_ngrok() {
    log_step "安装 ngrok..."

    echo ""
    log_info "选择安装方式："
    echo "  1. 自动安装（推荐）"
    echo "  2. 手动下载"
    echo ""
    read -p "请选择 [1-2]: " choice

    case $choice in
        1)
            log_info "正在自动安装 ngrok..."
            curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
            echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
            sudo apt update
            sudo apt install -y ngrok
            log_info "✓ ngrok 安装完成"
            ;;
        2)
            log_info "请手动下载和安装 ngrok"
            echo ""
            echo "1. 访问: https://ngrok.com/download"
            echo "2. 下载 Linux 64-bit 版本"
            echo "3. 解压并安装:"
            echo "   unzip ngrok-v3-stable-linux-amd64.zip"
            echo "   sudo mv ngrok /usr/local/bin/"
            echo "   sudo chmod +x /usr/local/bin/ngrok"
            echo ""
            read -p "安装完成后按 Enter 继续..."
            ;;
        *)
            log_error "无效选择"
            exit 1
            ;;
    esac
}

# 配置 authtoken
configure_authtoken() {
    log_step "配置 authtoken..."

    echo ""
    log_warn "⚠️  需要配置 ngrok authtoken"
    echo ""
    echo "请按以下步骤操作："
    echo "  1. 访问 https://ngrok.com/signup 注册（免费）"
    echo "  2. 登录后访问: https://dashboard.ngrok.com/get-started/your-authtoken"
    echo "  3. 复制你的 authtoken"
    echo ""
    read -p "请输入你的 ngrok authtoken: " TOKEN

    if [ -z "$TOKEN" ]; then
        log_error "authtoken 不能为空"
        exit 1
    fi

    log_info "正在配置 authtoken..."
    ngrok config add-authtoken "$TOKEN"
    log_info "✓ authtoken 配置完成"
}

# 启动 ngrok
start_ngrok() {
    log_step "启动 ngrok..."
    echo ""
    log_info "正在启动 ngrok，暴露端口 5000..."
    log_warn "按 Ctrl+C 停止 ngrok"
    echo ""

    ngrok http 5000
}

# 主函数
main() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║              ngrok 快速配置和启动                        ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo ""

    # 检查本地服务
    if ! check_local_service; then
        exit 1
    fi

    echo ""

    # 检查 ngrok
    if ! check_ngrok; then
        install_ngrok
    fi

    echo ""

    # 检查是否已配置 authtoken
    if ! ngrok config check > /dev/null 2>&1; then
        configure_authtoken
    else
        log_info "✓ authtoken 已配置"
        read -p "是否重新配置 authtoken? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            configure_authtoken
        fi
    fi

    echo ""
    log_info "配置完成！"
    echo ""

    # 启动 ngrok
    start_ngrok
}

# 运行主函数
main
