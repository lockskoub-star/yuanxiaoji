import multiprocessing
import os

# 服务器绑定
bind = os.getenv("HOST", "0.0.0.0") + ":" + os.getenv("PORT", "8000")

# Worker 进程数量
workers = multiprocessing.cpu_count() * 2 + 1

# Worker 类型
worker_class = "uvicorn.workers.UvicornWorker"

# 每个 Worker 的最大并发请求数
worker_connections = 1000

# 每个 Worker 处理的最大请求数（超过后会重启 Worker，防止内存泄漏）
max_requests = 1000
max_requests_jitter = 50

# 超时设置
timeout = 120
keepalive = 5

# 日志配置
accesslog = "/app/logs/access.log"
errorlog = "/app/logs/error.log"
loglevel = os.getenv("LOG_LEVEL", "info")

# 进程名称
proc_name = "yuanxiaoji_agent"

# 守护进程
daemon = False

# PID 文件
pidfile = "/app/logs/gunicorn.pid"

# 用户和组
user = None
group = None

# 临时目录
tmp_upload_dir = "/tmp"

# 启用访问日志
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'
