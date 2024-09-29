from umqtt.simple import MQTTClient
import ubinascii
import os
from parser import encode

client_id = ubinascii.hexlify(os.urandom(6)).decode('utf-8')
print("Client-ID:", client_id)

def mqtt_connect_pub(topic, broker_address, broker_port, user, password):
    client = MQTTClient(client_id, broker_address, port=broker_port, user=user, password=password)
    client.connect()
    return client

def mqtt_client(topic, broker_address, broker_port, user, password, temperature):
    try:
        client = mqtt_connect_pub(topic, broker_address, broker_port, user, password)
    except OSError as error:
        print(f"Error connecting to broker: {error}")
        return

    header_data = {
        "Sender": "ESP32-Sensor"
    }

    payload_data = {
        "Type": "Temperature",
        "Value": temperature 
    }

    message = encode(header_data, payload_data)
    client.publish(topic, message)