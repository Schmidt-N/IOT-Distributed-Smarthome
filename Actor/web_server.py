import socket

message = ""

def handle_client(client_socket):
    request = client_socket.recv(1024)
    print('Request:', request)
    
    response = f"""\
HTTP/1.1 200 OK

<!DOCTYPE html>
<html>
    <head>
        <title>ESP32 LED Control</title>
    </head>
    <body style="font-family: Arial, sans-serif; text-align: center; background-color: #f0f0f0; margin-top: 50px;">
        <h1 style="color: #4CAF50; font-size: 24px;">{message}</h1>
    </body>
    <script>
        setTimeout(() => location.reload(), 5000);
    </script>
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
