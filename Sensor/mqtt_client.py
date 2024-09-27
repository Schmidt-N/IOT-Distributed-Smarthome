from umqtt.simple import MQTTClient
import ubinascii
import os
from parser import decode
import _thread
import web_server

client_id = ubinascii.hexlify(os.urandom(6)).decode('utf-8')
print("Client-ID:", client_id)

def handle_callback(topic, msg):
    decoded = decode(msg)
    if(decoded["Payload"]["Type"] == "Command"):
        web_server.message = decoded["Payload"]["Value"] #TODO schöner
    else:
        web_server.message = "Type wasn't a Command: \n" + str(decoded)

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

    _thread.start_new_thread(web_server.web_server, ())

    try:
        while True:
            client.check_msg()
    except KeyboardInterrupt:
        print("Disconnecting...")
        client.disconnect()