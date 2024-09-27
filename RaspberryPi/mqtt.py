import paho.mqtt.client as mqtt
from messages import *

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
    print(f"Nachricht erhalten: {msg.payload.decode()}")

    message = parse(msg.payload.decode(), Message)

    sender = message["Header"]["Sender"]
    message_id = message["Header"]["MessageID"]
    payloads = message["Payload"]

    print(f"Sender: {sender}, MessageID: {message_id}")

    for payload in payloads:
        print(f"Payload Type: {payload['Type']}, Payload Value: {payload['Value']}")

    for payload in payloads:
       if payload['Type'] == 'Temperature' and float(payload['Value']) > 25:
           header_data = {
               "Sender": "RaspberryPi",
               "Receiver": "ESP32-Switch",
               "MessageID": "456"
           }

           payload_data = [
               {"Type": "Command", "Value": "TurnOn"}
           ]

           command_message = build_message(header_data, payload_data)
           client.publish("action_heat/topic", command_message)
           print(f"Nachricht an action_heat/topic gesendet:\n{command_message}")