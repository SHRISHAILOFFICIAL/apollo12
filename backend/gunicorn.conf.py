# Gunicorn Configuration for Production
# Usage: gunicorn -c gunicorn.conf.py config.wsgi:application

import multiprocessing

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = 2  # Number of CPU cores
worker_class = "gevent"  # Async worker for high concurrency
worker_connections = 1000  # Connections per worker
max_requests = 1000  # Restart workers after 1000 requests (prevent memory leaks)
max_requests_jitter = 50  # Add randomness to prevent all workers restarting at once

# Timeouts
timeout = 120  # Worker timeout (2 minutes for long-running requests)
graceful_timeout = 30  # Time to finish requests during graceful shutdown
keepalive = 5  # Keep-alive connections

# Logging
accesslog = "-"  # Log to stdout
errorlog = "-"  # Log to stderr
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "dcet_platform"

# Server mechanics
daemon = False  # Don't daemonize (use systemd/supervisor instead)
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (uncomment for HTTPS)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Preload app for better performance
preload_app = True

# Worker lifecycle hooks
def on_starting(server):
    """Called just before the master process is initialized."""
    print("Starting Gunicorn server...")

def on_reload(server):
    """Called to recycle workers during a reload via SIGHUP."""
    print("Reloading Gunicorn server...")

def when_ready(server):
    """Called just after the server is started."""
    print(f"Gunicorn server is ready. Listening on {bind}")

def pre_fork(server, worker):
    """Called just before a worker is forked."""
    pass

def post_fork(server, worker):
    """Called just after a worker has been forked."""
    print(f"Worker spawned (pid: {worker.pid})")

def worker_exit(server, worker):
    """Called just after a worker has been exited."""
    print(f"Worker exited (pid: {worker.pid})")
