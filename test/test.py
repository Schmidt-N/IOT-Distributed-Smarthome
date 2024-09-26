import paho.mqtt.client as mqtt
from pypeg2 import *

# MQTT Setup
BROKER = "192.168.225.152"
TOPIC = "actor_heat/topic"
#CLIENT_ID = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()

Symbol.regex = re.compile(r"[\w\s]+")

class Key(str):
    grammar = name(), "=", restline, endl

class Header(Namespace):
    grammar = "[", "Header", "]", endl, maybe_some(Key)

class Payload(Namespace):
    grammar = "[", "Payload", "]", endl, maybe_some(Key)

class Message(Namespace):
    grammar = maybe_some(Header), maybe_some(Payload)

def connect_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="client_id")
    client.username_pw_set("user", "password")
    # Assign the callback functions
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_message = on_message

    # Connect to the MQTT broker
    client.connect(BROKER, 1883)
    return client

def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("Connected successfully")
    else:
        print("Connection failed with code", rc)

# Define the on_publish callback function
def on_publish(client, userdata, mid, reason_code, properties):
    print("Message Published with ID:", mid)

def on_message(client, userdata, msg):
    print(f"Nachricht erhalten: {msg.payload.decode()}")

    # Nachricht parsen
    message = parse(msg.payload.decode(), Message)

    # Verarbeitung der Nachricht
    sender = message["Header"]["Sender"]
    message_id = message["Header"]["MessageID"]
    payloads = message["Payload"]

    print(f"Sender: {sender}, MessageID: {message_id}")

    for payload in payloads:
        print(f"Payload Type: {payload['Type']}, Payload Value: {payload['Value']}")

    for payload in payloads:
       if payload['Type'] == 'Temperature' and float(payload['Value']) > 25:
           # Nachricht an den ESP32-Schalter senden, wenn die Temperatur > 25 ist
           header_data = {
               "Sender": "RaspberryPi",
               "Receiver": "ESP32-Switch",
               "MessageID": "456"
           }

           payload_data = [
               {"Type": "Command", "Value": "TurnOn"}
           ]

           command_message = build_message(header_data, payload_data)
           # Nachricht an den ESP32-Schalter senden
           client.publish("action_heat/topic", command_message)
           print(f"Nachricht an action_heat/topic gesendet:\n{command_message}")

def build_message(header, payloads):
    """
    Baut eine Nachricht im gewünschten Format zusammen.
    
    :param header: Ein Dictionary mit den Header-Informationen (Sender, Receiver, MessageID)
    :param payloads: Eine Liste von Dictionaries, die die Payload-Daten enthalten (Type, Value)
    :return: Die formatierte Nachricht als String
    """
    # Header-Sektion zusammenbauen
    message = "[Header]\n"
    for key, value in header.items():
        message += f"{key}={value}\n"
    
    # Payload-Sektionen zusammenbauen
    for payload in payloads:
        message += "\n[Payload]\n"
        for key, value in payload.items():
            message += f"{key}={value}\n"
    
    return message.strip()


# Test mit einer Beispielnachricht
def main():
    client = connect_mqtt()

    # Start the loop
    client.loop_start()  # Use loop_start() for non-blocking

    header_data = {
        "Sender": "RaspberryPi",
        "Topic": "actor_heat/topic"
    }

    payload_data = [
        {"Type": "Command", "Value": "ON"}
    ]

    # Nachricht erstellen
    message = build_message(header_data, payload_data)
    # Publish the message to the specified topic
    result = client.publish(TOPIC, message)

    # Check if the message was published successfully
    status = result.rc
    
    if status == mqtt.MQTT_ERR_SUCCESS:
        print(f"Message published to topic `{TOPIC}`: {message}")
    else:
        print(f"Failed to publish message to topic `{TOPIC}`")

    # Stop the loop and disconnect from the broker
    client.loop_stop()
    client.disconnect()

# Programm starten
if __name__ == "__main__":
    main()

