from init import *
from pypeg import *
from mqtt import *

def main():
    client = connect_mqtt(CLIENT_ID, MQTT_USER, MQTT_PASSWORD, BROKER_ADDRESS, BROKER_PORT)

    client.loop_start()

    header_data = {
        "Sender": "RaspberryPi",
        "Topic": "actor_heat/topic"
    }

    payload_data = [
        {"Type": "Command", "Value": "ON"}
    ]

    message = build_message(header_data, payload_data)
    result = client.publish(TOPIC_ACTOR, message)

    status = result.rc
    
    if status == mqtt.MQTT_ERR_SUCCESS:
        print(f"Message published to topic `{TOPIC_ACTOR}`: {message}")
    else:
        print(f"Failed to publish message to topic `{TOPIC_ACTOR}`")

    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    main()

