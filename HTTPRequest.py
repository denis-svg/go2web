import socket
import ssl
from urllib.parse import urlparse

def parseUrl(url):
    parsed_url = urlparse(url)
    host = parsed_url.hostname
    port = parsed_url.port if parsed_url.port else 443  # Default HTTPS port
    path = parsed_url.path if parsed_url.path else "/"
    return host, port, path

# Function to make HTTPS request and retrieve HTML or JSON content
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
        
        # Extract response headers
        headers, _, body = response.partition(b"\r\n\r\n")
        content_type = None
        for header in headers.split(b"\r\n"):
            if header.startswith(b"Content-Type:"):
                content_type = header.decode().split(";")[0]
                break

        # Handle response based on content type
        if content_type == "Content-Type: application/json":
            # Decode JSON content and return
            import json
            return json.loads(body.decode())
        elif content_type == "Content-Type: text/html":
            # Decode HTML content and return
            return body.decode('ISO-8859-1')
        else:
            # Unsupported content type
            raise ValueError(f"Unsupported content type: {content_type}")

    finally:
        # Close the socket
        sock.close()

if __name__ == "__main__":
    # Example usage: Make a request and handle both JSON and HTML content
    json_response = make_https_request("https://jsonplaceholder.typicode.com/posts/1")
