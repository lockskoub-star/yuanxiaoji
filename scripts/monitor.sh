#!/bin/bash
# ========================================
# 元小吉智能客服 - 服务监控脚本
# ========================================

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_success() {
    echo -e "${GREEN}[OK]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_warning() {
    echo -e "${YELLOW}[WARN]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

# 检查服务健康
check_health() {
    local url=$1
    local name=$2

    if curl -f -s "$url" >/dev/null 2>&1; then
        log_success "$name 服务正常"
        return 0
    else
        log_error "$name 服务异常"
        return 1
    fi
}

# 检查 Docker 容器
check_docker() {
    log_info "检查 Docker 容器状态..."

    docker ps --filter "name=yuanxiaoji" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "无运行中的容器"
}

# 检查服务资源
check_resources() {
    log_info "检查服务资源使用情况..."

    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}" yuanxiaoji_agent yuanxiaoji_nginx 2>/dev/null || echo "无法获取资源信息"
}

# 检查日志错误
check_logs() {
    log_info "检查最近的错误日志..."

    if [ -f "/workspace/projects/logs/error.log" ]; then
        local error_count=$(tail -100 /workspace/projects/logs/error.log 2>/dev/null | grep -i error | wc -l)
        if [ $error_count -gt 0 ]; then
            log_warning "发现 $error_count 个错误，最近的错误："
            tail -20 /workspace/projects/logs/error.log | grep -i error | tail -5
        else
            log_success "最近没有发现错误"
        fi
    fi
}

# 主监控循环
monitor() {
    local check_interval=60

    log_info "开始监控服务，检查间隔: ${check_interval}秒"
    echo ""

    while true; do
        echo "=========================================="
        date '+%Y-%m-%d %H:%M:%S'
        echo "=========================================="

        check_health "http://localhost:8000/health" "Agent API"
        check_docker
        check_resources
        check_logs

        echo ""
        log_info "下一次检查: ${check_interval}秒后..."
        echo ""

        sleep $check_interval
    done
}

# 单次检查
check_once() {
    log_info "执行单次健康检查..."
    echo ""

    check_health "http://localhost:8000/health" "Agent API"
    check_docker
    check_resources

    echo ""
}

# 显示帮助
show_help() {
    cat << EOF
元小吉智能客服 - 监控脚本

用法:
  $0 [选项]

选项:
  monitor     持续监控服务（默认）
  once        执行单次检查
  help        显示此帮助信息

示例:
  $0 monitor     # 持续监控
  $0 once        # 单次检查
EOF
}

# 主函数
main() {
    case "${1:-monitor}" in
        monitor)
            monitor
            ;;
        once)
            check_once
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "未知选项: $1"
            show_help
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"
