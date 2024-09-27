from umqtt.simple import MQTTClient
import ubinascii
import os
from parser import encode
import _thread
import web_server
import time
import random

client_id = ubinascii.hexlify(os.urandom(6)).decode('utf-8')
print("Client-ID:", client_id)

def mqtt_connect_pub(topic, broker_address, broker_port, user, password):
    client = MQTTClient(client_id, broker_address, port=broker_port, user=user, password=password)
    client.connect()
    return client

def mqtt_client(topic, broker_address, broker_port, user, password):
    try:
        client = mqtt_connect_pub(topic, broker_address, broker_port, user, password)
    except OSError as error:
        print(f"Error connecting to broker: {error}")
        return

    _thread.start_new_thread(web_server.web_server, ())

    while (True):
        random_temp = random.randint(0, 30)

        header_data = {
            "Sender": "ESP32-Sensor",
            "Topic": topic
        }

        payload_data = {
            "Type": "Temperature",
            "Value": random_temp 
        }

        message = encode(header_data, payload_data)
        client.publish(topic, message)
        time.sleep(5)