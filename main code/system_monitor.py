import psutil
import time

def monitor_system():
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        
        print(f"CPU: {cpu_usage}% | Memory: {memory_usage}%")
        
        time.sleep(1)  # Update every second

monitor_system()
