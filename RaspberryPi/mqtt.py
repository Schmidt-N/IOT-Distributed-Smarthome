import paho.mqtt.client as mqtt
import ast
from parser import *

def connect_mqtt(CLIENT_ID, MQTT_USER, MQTT_PASSWORD, BROKER_ADDRESS, BROKER_PORT):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID)

    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_message = on_message

    client.connect(BROKER_ADDRESS, BROKER_PORT)
    return client

def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("Connected successfully")
    else:
        print("Connection failed with code", rc)

def on_publish(client, userdata, mid, reason_code, properties):
    print("Message Published with ID:", mid)

def on_message(client, userdata, msg):
    #print(f"Nachricht erhalten: {msg.payload.decode()}")
    
    try:
        message = parse(msg.payload.decode(), Message)
    except Exception as e:
        print(f"Fehler beim Parsen der Nachricht: {e}")
        return
    
    #print("Geparste Nachricht:", message.header.sender)

    header = None
    payload = None

    if isinstance(message.header, Header):
        header = message.header
    
    if isinstance(message.payload, Payload):
        payload = message.payload

    if not header:
        print("Kein Header gefunden")
        return
    if not payload:
        print("Keine Payload gefunden")
        return

    sender = header.sender

    print(f"Sender: {sender}")

    payload_type = payload.type
    payload_value = payload.value

    print(f"Payload Type: {payload_type}, Payload Value: {payload_value}")

    if payload_type == 'Temperature':
        print(payload_value)
        header_data = {
            "Sender": "RaspberryPi",
            "Topic": "actor_heat/topic"
        }

        payload_data = {
            "Type": "Command",
            "Value": "ON" if int(payload_value) <= 25 else "OFF"
        }

        command_message = encode(header_data, payload_data)
        client.publish("actor_heat/topic", command_message)
        print(f"Nachricht an actor_heat/topic gesendet:\n{command_message}")

