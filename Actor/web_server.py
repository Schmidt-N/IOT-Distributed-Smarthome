import socket

def handle_client(client_socket):
    request = client_socket.recv(1024)
    print('Request:', request)
    
    response = f"""\
HTTP/1.1 200 OK

<!DOCTYPE html>
<html>
    <head><title>ESP32 LED Control</title></head>
    <body>
        <h1>123</h1>
    </body>
</html>
"""
    client_socket.send(response)
    client_socket.close()

def web_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    server_socket = socket.socket()
    server_socket.bind(addr)
    server_socket.listen(1)
    print('Listening on', addr)

    while True:
        try:
            client_socket, client_addr = server_socket.accept()
            print('Client connected from', client_addr)
            handle_client(client_socket)
        except Exception as e:
            print('Error handling client:', e)
