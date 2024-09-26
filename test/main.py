# main.py -- put your code here!
import network
import socket
import time
import machine
import _thread  # For multithreading
from umqtt.simple import MQTTClient
import ubinascii
import os

def load_env_file(filepath):
    env = {}
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    env[key.strip()] = value.strip()
    except OSError:
        print("Could not open the .env file")
    return env

env_vars = load_env_file('.env')

WIFI_SSID = env_vars.get("WIFI_SSID")
WIFI_PASSWORD = env_vars.get("WIFI_PASSWORD")
BROKER_ADDRESS = env_vars.get("BROKER_ADDRESS")
MQTT_USER = env_vars.get("MQTT_USER")
MQTT_PASSWORD = env_vars.get("MQTT_PASSWORD")
BROKER_PORT = env_vars.get("BROKER_PORT")

#broker = "192.168.225.149"
client_id = ubinascii.hexlify(os.urandom(6)).decode('utf-8')
print(client_id)
topic = b"actor_heat/topic"  # The same topic to subscribe to
#port = 1883
#mqtt_user = "user"
#mqtt_password = "password"

# WiFi-Konfiguration
#ssid = "Mark's S24+"
#password = 'eehk4u4z6vefnqm'

# LED-Pin-Konfiguration
led_pin = machine.Pin(2, machine.Pin.OUT)

# WLAN-Verbindung herstellen
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    networks = wlan.scan()

    for network1 in networks:
        ssid = network1[0].decode()  # SSID of the network
        bssid = network1[1]          # MAC address
        channel = network1[2]        # Channel number
        rssi = network1[3]           # Signal strength
        authmode = network1[4]       # Authentication mode
    
        # Display details
        print(f"SSID: {ssid}, RSSI: {rssi}, Channel: {channel}, Authmode: {authmode}, bssid: {bssid}")

    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    while not wlan.isconnected():
        print(f'Verbindung zu {WIFI_SSID} wird hergestellt...')
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

def handle_callback(topic, msg):
    print(msg)
    #decoded = decode(msg)
    #print(decoded)

def decode(msg):
    # Entfernt führende und nachfolgende Leerzeichen und Zeilenumbrüche
    lines = msg.strip().split("\n")
    
    parsed_data = {
        "Header": {},
        "Payloads": []
    }

    current_section = None
    current_payload = None

    for line in lines:
        line = line.strip()
        
        # Überspringe leere Zeilen oder Kommentare
        if not line or line.startswith(";"):
            continue
        
        # Überprüfe, ob es eine neue Sektion ist ([Header] oder [Payload])
        if line.startswith("[") and line.endswith("]"):
            section_name = line[1:-1]
            if section_name == "Header":
                current_section = "Header"
            elif section_name == "Payload":
                current_section = "Payload"
                current_payload = {}
                parsed_data["Payloads"].append(current_payload)
            continue
        
        # Verarbeite Schlüssel-Wert-Paare
        if "=" in line:
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            
            if current_section == "Header":
                parsed_data["Header"][key] = value
            elif current_section == "Payload" and current_payload is not None:
                current_payload[key] = value
    
    return parsed_data

# Connect and subscribe
def mqtt_connect_sub():
    print(BROKER_ADDRESS)
    print(BROKER_PORT)
    print(MQTT_USER)
    print(MQTT_PASSWORD)
    client = MQTTClient(client_id, BROKER_ADDRESS, port=BROKER_PORT, user=MQTT_USER, password=MQTT_PASSWORD)
    client.set_callback(handle_callback)
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
    
    #_thread.start_new_thread(mqtt_server, ())
   
    # Continue blinking the LED in the main thread
    mqtt_server()

if __name__ == "__main__":
    main()
