import uuid
import re

def load_env_file(filepath):
    env = {}
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    env[key.strip()] = value.strip()
    except OSError:
        print("Could not open the .env file")
    return env

def get_mac_address():
    mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    print(mac)
    return mac

env_vars = load_env_file('.env')
MQTT_USER = env_vars.get("MQTT_USER")
MQTT_PASSWORD = env_vars.get("MQTT_PASSWORD")

BROKER_ADDRESS = env_vars.get("BROKER_ADDRESS")
BROKER_PORT = int(env_vars.get("BROKER_PORT"))

TOPIC_ACTOR = "actor_heat/topic"
TOPIC_SENSOR = "sensor_heat/topic"

CLIENT_ID = get_mac_address()
