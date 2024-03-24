import socket
import ssl
from urllib.parse import urlparse

def parseUrl(url):
    parsed_url = urlparse(url)
    host = parsed_url.hostname
    port = parsed_url.port if parsed_url.port else 443  # Default HTTPS port
    path = parsed_url.path if parsed_url.path else "/"
    return host, port, path

# Function to make HTTPS request and retrieve HTML page
def make_https_request(url):
    # Parse the URL
    host, port, _ = parseUrl(url)
    
    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Wrap the socket with SSL/TLS
        context = ssl.create_default_context()
        secure_sock = context.wrap_socket(sock, server_hostname=host)

        # Connect to the server
        secure_sock.connect((host, port))
        # Send HTTPS request
        request = f"GET {url} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        secure_sock.sendall(request.encode())
        
        # Receive response
        response = b""
        while True:
            chunk = secure_sock.recv(4096)
            if not chunk:
                break
            response += chunk
        # Decode and return the HTML page
        html_page = response.split(b"\r\n\r\n", 1)[1]
        return html_page.decode('ISO-8859-1')
        
    finally:
        # Close the socket
        sock.close()