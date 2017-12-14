import multiprocessing

bind = "0.0.0.0"
workers = multiprocessing.cpu_count() * 2 + 1
loglevel = "info"
timeout = 90
