import socket
from mqtt_client import mqtt_client

message = ""

def handle_client(client_socket, topic, BROKER_ADDRESS, BROKER_PORT, MQTT_USER, MQTT_PASSWORD):
    request = client_socket.recv(1024)
    request = str(request)
    input_value = ''
    if 'GET /?input=' in request:
        input_value = request.split('GET /?input=')[1].split(' ')[0]
        input_value = input_value.replace('%20', ' ')

        temperature = 0

        try:
            temperature = int(input_value)

            if temperature < -273 or temperature > 100:
                print("Error:", temperature, "ist nicht zwischen -273°C und 100°C!")
            else:
                mqtt_client(topic, BROKER_ADDRESS, BROKER_PORT, MQTT_USER, MQTT_PASSWORD, temperature)

        except ValueError:
            print("Error:", input_value, "ist keine Zahl!")
        
    html = f"""<!DOCTYPE html>
<html>
    <head> <title>ESP32 Temperatureingabe</title> </head>
    <body>
        <h1>Temperatur eingeben (in &deg;C)</h1>
        <form action="/" method="get">
            <input type="number" name="input">
            <input type="submit" value="Absenden">
        </form>
        <p>Zuletzt eingegebene Temperatur: {input_value}</p>
    </body>
</html>
"""

    client_socket.send('HTTP/1.1 200 OK\n')
    client_socket.send('Content-Type: text/html\n')
    client_socket.send('Connection: close\n\n')
    client_socket.sendall(html)
    client_socket.close()

def web_server(topic, BROKER_ADDRESS, BROKER_PORT, MQTT_USER, MQTT_PASSWORD):
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    server_socket = socket.socket()
    server_socket.bind(addr)
    server_socket.listen(1)
    print('Listening on', addr)

    while True:
        try:
            client_socket, client_addr = server_socket.accept()
            print('Client connected from', client_addr)
            handle_client(client_socket, topic, BROKER_ADDRESS, BROKER_PORT, MQTT_USER, MQTT_PASSWORD)
        except Exception as e:
            print('Error handling client:', e)
