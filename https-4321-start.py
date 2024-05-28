import http.server
import ssl
import subprocess
import os

# Konfigurasi SSL
ssl_certfile = '/home/sora/HTTP-TO-HTTPS/certificate.crt'
ssl_keyfile = '/home/sora/HTTP-TO-HTTPS/private_key.key'
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile=ssl_certfile, keyfile=ssl_keyfile)

# Konfigurasi server HTTP dengan SSL
server_address = ('', 443)  # Port 443 untuk HTTPS

class CustomRequestHandler(http.server.SimpleHTTPRequestHandler):
    def run_php_script(self, php_file):
        """Execute the PHP script using a local PHP server"""
        try:
            output = subprocess.check_output(['php', '-S', '203.194.113.112:4321', '-t', '.', '-f', php_file], stderr=subprocess.STDOUT, universal_newlines=True)
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(output.encode('utf-8'))
        except subprocess.CalledProcessError as e:
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"PHP script execution failed:\n{e.output}".encode('utf-8'))

    def do_GET(self):
        """Handle GET requests"""
        if self.path.endswith('.php'):
            self.run_php_script(self.path)
        else:
            super().do_GET()

    def do_POST(self):
        """Handle POST requests"""
        if self.path.endswith('.php'):
            self.run_php_script(self.path)
        else:
            super().do_POST()

    def translate_path(self, path):
        """Override the translate_path method to handle .php files"""
        # Get the file extension
        _, ext = os.path.splitext(path)
        
        # If the file extension is .php, treat it as a PHP script
        if ext == '.php':
            return path
        
        # Otherwise, treat it as a static file
        return super().translate_path(path)

# Buat server HTTP dengan SSL dan custom request handler
httpd = http.server.HTTPServer(server_address, CustomRequestHandler)
httpd.socket = ssl_context.wrap_socket(httpd.socket)

# Jalankan server
httpd.serve_forever()

