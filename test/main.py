# main.py -- put your code here!
import network
import socket
import time
import machine
import _thread  # For multithreading
from umqtt.simple import MQTTClient
import ubinascii
import os

broker = "insert-broker-address-here"
client_id = ubinascii.hexlify(os.urandom(6)).decode('utf-8')
print(client_id)
topic = b"test/topic"  # The same topic to subscribe to
port = 1883
mqtt_user = "user"
mqtt_password = "password"

# WiFi-Konfiguration
ssid = 'insert-ssid-here'
password = 'insert-password-here'

# LED-Pin-Konfiguration
led_pin = machine.Pin(2, machine.Pin.OUT)

# WLAN-Verbindung herstellen
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    networks = wlan.scan()

    for network1 in networks:
        ssid1 = network1[0].decode()  # SSID of the network
        bssid = network1[1]          # MAC address
        channel = network1[2]        # Channel number
        rssi = network1[3]           # Signal strength
        authmode = network1[4]       # Authentication mode
    
        # Display details
        print(f"SSID: {ssid1}, RSSI: {rssi}, Channel: {channel}, Authmode: {authmode}, bssid: {bssid}")

    wlan.connect(ssid, password)

    while not wlan.isconnected():
        print(f'Verbindung zu {ssid} wird hergestellt...')
        time.sleep(1)

    print('Mit WiFi verbunden:', wlan.ifconfig())
    return wlan.ifconfig()

# Function to handle incoming HTTP requests
def handle_client(client_socket):
    request = client_socket.recv(1024)
    print('Request:', request)
    
    # Send HTTP response
    response = """\
HTTP/1.1 200 OK

<!DOCTYPE html>
<html>
    <head><title>ESP32 LED Control</title></head>
    <body>
        <h1>Hello from ESP32</h1>
    </body>
</html>
"""
    client_socket.send(response)
    client_socket.close()

# Function to start the web server
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

# Function to blink the LED
def blink_led():
    while True:
        led_pin.value(1)
        print("Turning ON...")
        time.sleep(1)
        led_pin.value(0)
        print("Turning OFF...")
        time.sleep(1)

def mqtt_callback(topic, msg):
    print("Received message:", msg, "on topic:", topic)

# Connect and subscribe
def mqtt_connect_sub():
    client = MQTTClient(client_id, broker, port=port, user=mqtt_user, password=mqtt_password)
    client.set_callback(mqtt_callback)
    client.connect()
    client.subscribe(topic)
    print(f"Subscribed to topic: {topic}")
    return client

def mqtt_server():
    try:
        client = mqtt_connect_sub()
    except OSError as error:
        print(f"Error connecting to broker: {error}")
        return

    try:
        while True:
            # Wait for a message and check for any pending messages
            client.check_msg()
            # Do other tasks here if needed
    except KeyboardInterrupt:
        print("Disconnecting...")
        client.disconnect()

# Hauptprogramm
def main():
    # Versuche, WiFi-Verbindung herzustellen
    ip_config = connect_wifi()
    print("IP-Adresse des ESP32:", ip_config[0])

    # Start the web server in a separate thread
    _thread.start_new_thread(web_server, ())

    #_thread.start_new_thread(mqtt_connect_sub, ())
    # Main function
    
    _thread.start_new_thread(mqtt_server, ())
   
    # Continue blinking the LED in the main thread
    blink_led()

if __name__ == "__main__":
    main()
