import network
import time
import ubinascii
from umqtt.simple import MQTTClient

# MQTT Setup
BROKER = "192.168.225.152"
TOPIC = "actor_heat/topic"
#CLIENT_ID = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()

def connect_mqtt():
    client = MQTTClient("CLIENT_ID", BROKER, port=1883, user="user", password="password")
    client.connect()
    return client

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
    header_data = {
        "Sender": "RaspberryPi",
        "Topic": "actor_heat/topic"
    }

    payload_data = [
        {"Type": "Command", "Value": "ON"}
    ]

    # Nachricht erstellen
    message = build_message(header_data, payload_data)

    client = connect_mqtt()
    client.publish(TOPIC, message)
    client.disconnect()

# Programm starten
if __name__ == "__main__":
    main()

