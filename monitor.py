# monitor.py
import psutil
import time
import os

def monitor_resources(server_pid):
    server_process = psutil.Process(server_pid)
    
    while True:
        try:
            # Network connections
            conns = len(server_process.connections())
            
            # Resource usage
            cpu = server_process.cpu_percent()
            mem = server_process.memory_info().rss / (1024 ** 2)  # MB
            
            # Clear and print
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Connections: {conns} | CPU: {cpu:.1f}% | Memory: {mem:.2f}MB")
            
            time.sleep(0.5)
            
        except (psutil.NoSuchProcess, KeyboardInterrupt):
            break

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python monitor.py <SERVER_PID>")
        sys.exit(1)
    
    monitor_resources(int(sys.argv[1]))
