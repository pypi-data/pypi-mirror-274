import os
import sys
import shutil
import logging
import json
import ssl
import webbrowser
from concurrent.futures import ThreadPoolExecutor
from http.server import SimpleHTTPRequestHandler
import socketserver
import signal
from time import time
from functools import wraps
import subprocess
from io import BytesIO
import pkg_resources
import mimetypes  # Import mimetypes

# Placeholder for generate_self_signed_cert function
def generate_self_signed_cert(certfile, keyfile, cert_config):
    # Implement the function or import it if defined elsewhere
    pass

# Load configuration
def load_config(config_file='config.json'):
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        logging.error(f"Configuration file {config_file} not found.")
        raise
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from {config_file}.")

config = load_config()

# Ensure htdocs and downloads directories exist
def ensure_directories():
    htdocs_dir = config.get('htdocs_dir', 'htdocs')
    downloads_dir = config.get('downloads_dir', os.path.join(htdocs_dir, 'downloads'))

    os.makedirs(htdocs_dir, exist_ok=True)
    os.makedirs(downloads_dir, exist_ok=True)

    # Copy HTML files if they don't exist
    for filename in ['index.html', 'upload.html', 'download.html']:
        if not os.path.exists(os.path.join(htdocs_dir, filename)):
            resource_path = pkg_resources.resource_filename(__name__, f'htdocs/{filename}')
            shutil.copy(resource_path, htdocs_dir)

ensure_directories()

# Define the HTTP request handler
class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.entry_point = kwargs.pop('entry_point', 'index.html')
        self.executor = kwargs.pop('executor', None)
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == '/':
            self.path = '/' + self.entry_point
        elif self.path == '/list-downloads':
            self.list_downloads()
        elif self.path.startswith('/downloads/'):
            self.serve_download()
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/upload':
            self.handle_file_upload()
        else:
            self.send_error(404, "File not found")

    def serve_download(self):
        file_path = self.path.lstrip('/')
        full_path = os.path.join(config.get('htdocs_dir', 'htdocs'), file_path)
        if os.path.exists(full_path) and os.path.isfile(full_path):
            mime_type, _ = mimetypes.guess_type(full_path)
            self.send_response(200)
            self.send_header("Content-Type", mime_type or "application/octet-stream")
            self.send_header("Content-Disposition", f'attachment; filename="{os.path.basename(full_path)}"')
            self.send_header("Content-Length", str(os.path.getsize(full_path)))
            self.end_headers()
            with open(full_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404, "File not found")

    def list_downloads(self):
        try:
            files = os.listdir(config.get('downloads_dir', 'htdocs/downloads'))
            files = [f for f in files if os.path.isfile(os.path.join(config.get('downloads_dir', 'htdocs/downloads'), f))]
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = json.dumps({"files": files})
            self.wfile.write(response.encode())
        except Exception as e:
            self.send_error(500, "Internal server error")

    def handle_file_upload(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        boundary = self.headers['Content-Type'].split("=")[1].encode()
        parts = body.split(boundary)

        for part in parts:
            if b'Content-Disposition' in part:
                headers, content = part.split(b'\r\n\r\n', 1)
                headers = headers.decode()
                filename = headers.split('filename="')[1].split('"')[0]
                filepath = os.path.join(config.get('downloads_dir', 'htdocs/downloads'), filename)
                with open(filepath, 'wb') as f:
                    f.write(content.rstrip(b'\r\n--'))

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        response = BytesIO()
        response.write(b"File uploaded successfully")
        self.wfile.write(response.getvalue())

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def send_error(self, code, message=None):
        self.error_message_format = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Error response</title>
        </head>
        <body>
            <h1>Error response</h1>
            <p>Error code: %(code)d</p>
            <p>Message: %(message)s</p>
        </body>
        </html>
        '''
        super().send_error(code, message)

    def log_message(self, format, *args):
        with open(config.get('log_file', 'server.log'), "a") as log_file:
            log_file.write("%s - - [%s] %s\n" %
                           (self.client_address[0],
                            self.log_date_time_string(),
                            format % args))

def run_server():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    try:
        port = config.get('port', 8080)
        entry_point = config.get('entry_point', 'index.html')
        use_https = config.get('use_https', False)
        certfile = config.get('certfile', 'cert.pem')
        keyfile = config.get('keyfile', 'key.pem')
        cert_config = config.get('cert_config', {})

        if use_https:
            generate_self_signed_cert(certfile, keyfile, cert_config)

        with ThreadPoolExecutor() as executor:
            handler = lambda *args, **kwargs: CustomHTTPRequestHandler(*args, entry_point=entry_point, executor=executor, **kwargs)
            with socketserver.ThreadingTCPServer(("", port), handler) as httpd:
                if use_https:
                    httpd.socket = ssl.wrap_socket(httpd.socket, certfile=certfile, keyfile=keyfile, server_side=True)
                    logging.info(f"Serving on port {port} with HTTPS")
                    webbrowser.open(f'https://localhost:{port}/{entry_point}')
                else:
                    logging.info(f"Serving on port {port}")
                    webbrowser.open(f'http://localhost:{port}/{entry_point}')

                # Handle graceful shutdown on Ctrl-C
                def signal_handler(sig, frame):
                    logging.info('Shutting down server...')
                    httpd.shutdown()
                    sys.exit(0)

                signal.signal(signal.SIGINT, signal_handler)
                httpd.serve_forever()
    except Exception as e:
        logging.error(f"Failed to start server: {e}")

if __name__ == "__main__":
    run_server()
