#!/usr/bin/env python3
import http.server
import socketserver
import json
import os
import base64
from urllib.parse import urlparse, parse_qs
import mimetypes

PORT = 8000
IMG_DIR = os.path.join(os.path.dirname(__file__), 'img')

# Create img directory if it doesn't exist
os.makedirs(IMG_DIR, exist_ok=True)

class UploadHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve static files from current directory
        if self.path.endswith('/'):
            self.path = '/index.html'
        return super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            data = json.loads(body.decode('utf-8'))
            image_type = data.get('type')  # 'gallery' or 'fact'
            index = data.get('index')
            image_data = data.get('data')  # base64 string
            
            if not all([image_type, index is not None, image_data]):
                self.send_error(400, 'Missing required fields')
                return
            
            # Generate filename
            filename = f"{image_type}_{index}.png"
            filepath = os.path.join(IMG_DIR, filename)
            
            # Decode and save image
            try:
                # Remove data:image/png;base64, prefix if present
                if image_data.startswith('data:'):
                    image_data = image_data.split(',')[1]
                
                image_bytes = base64.b64decode(image_data)
                with open(filepath, 'wb') as f:
                    f.write(image_bytes)
                
                # Return success response
                response = {
                    'success': True,
                    'filename': filename,
                    'url': f'/img/{filename}'
                }
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                self.send_error(500, f'Error saving image: {str(e)}')
        except json.JSONDecodeError:
            self.send_error(400, 'Invalid JSON')

    def do_DELETE(self):
        # Handle image deletion
        path = urlparse(self.path).path
        if path.startswith('/img/'):
            filename = os.path.basename(path)
            filepath = os.path.join(IMG_DIR, filename)
            
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
                    response = {'success': True}
                else:
                    response = {'success': False, 'error': 'File not found'}
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                self.send_error(500, f'Error deleting image: {str(e)}')

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

if __name__ == '__main__':
    Handler = UploadHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Server running at http://127.0.0.1:{PORT}/")
        print(f"Image directory: {IMG_DIR}")
        httpd.serve_forever()
