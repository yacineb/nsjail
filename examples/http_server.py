#!/usr/bin/env python3
"""
Simple HTTP Server: Single route server on port 8000
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import socket

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Single route - respond to any path
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        
        response = f"Hello from sandbox!\nPath: {self.path}\nServer: Simple HTTP Server\nPort: 8000"
        self.wfile.write(response.encode())

def get_local_ip():
    """Get local IP address"""
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except:
        return "127.0.0.1"

def main():
    port = 8000
    local_ip = get_local_ip()
    
    print(f"🚀 Starting simple HTTP server...")
    print(f"📍 Address: {local_ip}:{port}")
    print(f"🌐 URL: http://{local_ip}:{port}")
    print(f"📡 Single route: Any path will work")
    print("=" * 50)
    
    try:
        server = HTTPServer(('0.0.0.0', port), SimpleHandler)
        print(f"✅ Server started successfully!")
        print(f"⏹️  Press Ctrl+C to stop")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹️  Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    main() 