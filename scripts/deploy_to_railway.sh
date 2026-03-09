#!/bin/bash

################################################################################
# Railway 部署脚本
# 自动配置并部署到 Railway
################################################################################

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# 日志函数
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step() { echo -e "${BLUE}[STEP]${NC} $1"; }

# 检查 Git 仓库
check_git() {
    log_step "检查 Git 仓库..."
    if [ ! -d ".git" ]; then
        log_error "这不是一个 Git 仓库"
        log_info "请先初始化 Git 仓库"
        exit 1
    fi

    # 检查远程仓库
    if ! git remote get-url origin > /dev/null 2>&1; then
        log_error "未配置远程仓库"
        log_info "请先添加远程仓库：git remote add origin <repository-url>"
        exit 1
    fi

    log_info "✓ Git 仓库配置正确"
    git remote -v
}

# 检查是否已推送
check_pushed() {
    log_step "检查代码是否已推送..."

    if git log origin/main..main > /dev/null 2>&1; then
        log_warn "有未推送的提交"
        log_info "正在推送代码..."
        git push origin main
    else
        log_info "✓ 代码已推送到 GitHub"
    fi
}

# 显示部署信息
show_deployment_info() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║              Railway 部署准备完成                          ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo ""
    log_info "仓库地址："
    echo "  $(git remote get-url origin)"
    echo ""
    log_info "下一步："
    echo "  1. 访问 https://railway.app"
    echo "  2. 登录账号（推荐使用 GitHub）"
    echo "  3. 点击 'New Project'"
    echo "  4. 选择 'Deploy from GitHub repo'"
    echo "  5. 选择 yuanxiaoji 仓库"
    echo "  6. 点击 'Deploy Now'"
    echo ""
    log_info "部署后配置环境变量："
    echo "  1. 点击 'Variables' 标签"
    echo "  2. 添加以下变量："
    echo ""
    echo "     COZE_WORKLOAD_IDENTITY_API_KEY = 你的API密钥"
    echo "     COZE_INTEGRATION_MODEL_BASE_URL = 你的基础URL"
    echo ""
    echo "  3. 点击 'Redeploy'"
    echo ""
    log_warn "注意：必须配置环境变量，否则服务无法正常工作！"
    echo ""
}

# 主函数
main() {
    log_info "开始 Railway 部署准备..."
    echo ""

    # 检查 Git 仓库
    check_git

    # 检查推送状态
    check_pushed

    # 显示部署信息
    show_deployment_info

    # 询问是否打开 Railway
    echo ""
    read -p "是否现在打开 Railway 网站？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if command -v xdg-open > /dev/null; then
            xdg-open https://railway.app
        elif command -v open > /dev/null; then
            open https://railway.app
        else
            log_info "请手动打开浏览器访问：https://railway.app"
        fi
    fi
}

# 运行主函数
main
