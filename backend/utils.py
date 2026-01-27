import psutil
import os
import time

def get_cpu(wait_interval = 0.5):
    return psutil.cpu_percent(interval=wait_interval)

def get_mem():
    return psutil.virtual_memory().percent

# this is macOS/Linux only
def get_average():
    l1 = psutil.getloadavg()[0]
    if psutil.getloadavg()[0] != None and os.cpu_count() != None:
        cpu_usage = (l1 / os.cpu_count()) * 100
        return round(cpu_usage, 2)
    return 0

def get_bandwidth():
    old_value = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
    time.sleep(1) # Wait 1 second
    new_value = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
    bandwidth_bytes = new_value - old_value
    mbps = (bandwidth_bytes * 8) / 10**6
    return round(mbps, 3)