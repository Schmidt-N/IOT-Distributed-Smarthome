# main.py -- put your code here!
import network
import machine
import time

# WiFi-Konfiguration
ssid = 'IOT-Distributed' #TODO SSID of Rasperypi Wlan
password = '' #TODO Password of Rasperypi Wlan

# LED-Pin-Konfiguration
led_pin = machine.Pin(2, machine.Pin.OUT)

# WLAN-Verbindung herstellen
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while not wlan.isconnected():
        print('Verbindung zu WiFi wird hergestellt...')
        time.sleep(1)

    print('Mit WiFi verbunden:', wlan.ifconfig())
    return wlan.ifconfig()

# Hauptprogramm
def main():
    # Versuche, WiFi-Verbindung herzustellen
    ip_config = connect_wifi()
    print("IP-Adresse des ESP32:", ip_config[0])

    while True:
        led_pin.value(1)
        print("Turning ON...")
        time.sleep(1)
        led_pin.value(0)
        print("Turning OFF...")
        time.sleep(1)

if __name__ == "__main__":
    main()
