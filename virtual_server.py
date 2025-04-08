# virtual_server.py
import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

class StressTestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
        # Track connections
        print(f"[+] Connection from {self.client_address[0]}")

def start_http_server(port):
    server = HTTPServer(('0.0.0.0', port), StressTestHandler)
    print(f"Virtual server running on port {port}")
    server.serve_forever()

def start_socket_server(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', port))
        s.listen(5)
        print(f"Raw socket server on port {port}")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Socket connection from {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(b"ACK")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    parser.add_argument("-m", "--mode", choices=['http', 'socket'], default='http')
    args = parser.parse_args()

    if args.mode == 'http':
        start_http_server(args.port)
    else:
        start_socket_server(args.port)
