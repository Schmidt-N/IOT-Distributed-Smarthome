from umqtt.simple import MQTTClient
import ubinascii
import os
from parser import decode

client_id = ubinascii.hexlify(os.urandom(6)).decode('utf-8')
print("Client-ID:", client_id)

def handle_callback(topic, msg):
    decoded = decode(msg)
    print(decoded)
    print(decoded["Header"])

def mqtt_connect_sub(topic, broker_address, broker_port, user, password):
    client = MQTTClient(client_id, broker_address, port=broker_port, user=user, password=password)
    client.set_callback(handle_callback)
    client.connect()
    client.subscribe(topic)
    print(f"Subscribed to topic: {topic}")
    return client

def mqtt_client(topic, broker_address, broker_port, user, password):
    try:
        client = mqtt_connect_sub(topic, broker_address, broker_port, user, password)
    except OSError as error:
        print(f"Error connecting to broker: {error}")
        return

    try:
        while True:
            client.check_msg()
    except KeyboardInterrupt:
        print("Disconnecting...")
        client.disconnect()