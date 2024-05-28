import http.server
import ssl

# Konfigurasi SSL
ssl_certfile = '/home/sora/HTTP-TO-HTTPS/certificate.crt'
ssl_keyfile = '/home/sora/HTTP-TO-HTTPS/private_key.key'
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile=ssl_certfile, keyfile=ssl_keyfile)

# Konfigurasi server HTTP dengan SSL
server_address = ('', 443)  # Port 443 untuk HTTPS
http_handler = http.server.SimpleHTTPRequestHandler

# Buat server HTTP dengan SSL
httpd = http.server.HTTPServer(server_address, http_handler)
httpd.socket = ssl_context.wrap_socket(httpd.socket)

# Jalankan server
httpd.serve_forever()

# <port> --bind <IP address>
