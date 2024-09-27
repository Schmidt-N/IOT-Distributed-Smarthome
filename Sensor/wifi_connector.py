import network
import time

def connect_wifi(wifi_ssid, wifi_password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    networks = wlan.scan()

    for network1 in networks:
        ssid = network1[0].decode()
        bssid = network1[1]
        channel = network1[2]
        rssi = network1[3]
        authmode = network1[4]
    
        print(f"SSID: {ssid}, RSSI: {rssi}, Channel: {channel}, Authmode: {authmode}, bssid: {bssid}")

    wlan.connect(wifi_ssid, wifi_password)

    while not wlan.isconnected():
        print(f'Verbindung zu {wifi_ssid} wird hergestellt...')
        time.sleep(1)

    print('Mit WiFi verbunden:', wlan.ifconfig())
    return wlan.ifconfig()