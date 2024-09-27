from env_loader import load_env_file
from wifi_connector import connect_wifi
from mqtt_client import mqtt_client

env_vars = load_env_file('.env')

WIFI_SSID = env_vars.get("WIFI_SSID")
WIFI_PASSWORD = env_vars.get("WIFI_PASSWORD")
BROKER_ADDRESS = env_vars.get("BROKER_ADDRESS")
MQTT_USER = env_vars.get("MQTT_USER")
MQTT_PASSWORD = env_vars.get("MQTT_PASSWORD")
BROKER_PORT = env_vars.get("BROKER_PORT")

topic = b"sensor_heat/topic"

def main():
    ip_config = connect_wifi(WIFI_SSID, WIFI_PASSWORD)
    print("IP-Adresse des ESP32:", ip_config[0])
    mqtt_client(topic, BROKER_ADDRESS, BROKER_PORT, MQTT_USER, MQTT_PASSWORD)

if __name__ == "__main__":
    main()
