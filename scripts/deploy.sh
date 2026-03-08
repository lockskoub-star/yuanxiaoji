#!/bin/bash
# ========================================
# 元小吉智能客服 - 自动部署脚本
# ========================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 主函数
main() {
    echo "=========================================="
    echo "   🚀 元小吉智能客服 - 自动部署"
    echo "=========================================="
    echo ""

    # 检查 Docker 是否安装
    if ! command_exists docker; then
        log_error "Docker 未安装，请先安装 Docker"
        log_info "安装命令: curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh"
        exit 1
    fi

    if ! command_exists docker-compose; then
        log_error "Docker Compose 未安装，请先安装 Docker Compose"
        log_info "安装命令: apt install -y docker-compose"
        exit 1
    fi

    # 检查 .env 文件
    if [ ! -f ".env" ]; then
        log_warning ".env 文件不存在，正在创建..."
        cp .env.example .env
        log_warning "请编辑 .env 文件，配置你的环境变量"
        log_info "编辑命令: nano .env"
        exit 1
    fi

    log_info "开始部署..."
    echo ""

    # 停止旧容器
    log_info "停止旧容器..."
    docker-compose down 2>/dev/null || true

    # 构建镜像
    log_info "构建 Docker 镜像..."
    docker-compose build --no-cache

    # 启动服务
    log_info "启动服务..."
    docker-compose up -d

    # 等待服务启动
    log_info "等待服务启动..."
    sleep 10

    # 检查服务状态
    log_info "检查服务状态..."
    docker-compose ps

    # 测试服务
    log_info "测试服务健康检查..."
    if curl -f http://localhost:8000/health >/dev/null 2>&1; then
        log_success "服务启动成功！"
    else
        log_error "服务启动失败，请检查日志"
        log_info "查看日志: docker-compose logs agent"
        exit 1
    fi

    echo ""
    echo "=========================================="
    echo "   🎉 部署完成！"
    echo "=========================================="
    echo ""
    echo "📱 访问地址："
    echo "   - 本地: http://localhost:8000"
    echo "   - 健康检查: http://localhost:8000/health"
    echo "   - API 文档: http://localhost:8000/docs"
    echo ""
    echo "📝 常用命令："
    echo "   - 查看日志: docker-compose logs -f"
    echo "   - 重启服务: docker-compose restart"
    echo "   - 停止服务: docker-compose down"
    echo "   - 查看状态: docker-compose ps"
    echo ""
    echo "=========================================="
}

# 执行主函数
main
