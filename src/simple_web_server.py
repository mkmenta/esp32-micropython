import socket


class SimpleWebServer:
    def __init__(self, ip):
        self.ip = ip
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, 80))  # Bind to port 80 (HTTP)
        self.server_socket.listen(5)  # Listen for connections
        self._handlers = {}
    #
    def start(self):
        print(f"Starting web server on http://{self.ip}:80")
        while True:
            conn, addr = self.server_socket.accept()
            print("Client connected from:", addr)
            request = conn.recv(1024).decode('utf-8')
            print("Request:", request)
            method, path_args = request.split(' ')[0], request.split(' ')[1]
            # Extract path args
            path_args = path_args.split('?')
            path = path_args[0]
            query = path_args[1] if len(path_args) > 1 else ''
            # Convert query to dict
            query_dict = dict(q.split('=') for q in query.split('&') if '=' in q)
            # Check if a handler exists for this method and path
            handler = self._handlers.get((method, path))
            if handler:
                response = handler(query_dict)
            else:
                # Return not found response
                response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<h1>404 Not Found</h1>"
            # Send response
            print("Response:", response)
            conn.send(response.encode())
            conn.close()
    #
    def add_handler(self, method, path, handler_function):
        """Add a handler for a specific method and path."""
        assert method in ['GET', 'POST', 'PUT', 'DELETE'], "Method must be one of GET, POST, PUT, DELETE"
        self._handlers[(method, path)] = handler_function


if __name__ == "__main__":
    import json

    # Example of usage
    def hello_world_handler(query):
        """Example handler for the /hello_world endpoint."""
        return "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Hello, World!</h1>"

    def json_handler(query):
        """Example handler that returns a JSON response."""
        json_data = json.dumps({'received_query': query})
        return f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{json_data}"

    sws = SimpleWebServer(IFCONFIG[0])  # Use the IP address (not mask) from IFCONFIG
    sws.add_handler('GET', '/hello_world', hello_world_handler)
    sws.add_handler('GET', '/json', json_handler)
    sws.start()
