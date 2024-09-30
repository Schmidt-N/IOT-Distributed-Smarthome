from init import *
from mqtt import *

def main():
    client = connect_mqtt(CLIENT_ID, MQTT_USER, MQTT_PASSWORD, BROKER_ADDRESS, BROKER_PORT)
    client.subscribe(TOPIC_SENSOR)
    client.loop_forever()
    
if __name__ == "__main__":
    main()

