# IOT-Distributed-Smarthome
This repository contains the code for a university project simulating a Smart Home using a Raspberry Pi and multiple ESP32 microcontrollers. The Raspberry Pi acts as the central control unit, while the ESP32 devices manage components like lighting, temperature, and security systems.

## Setting up the development environment with VS Code
prerequisites:
- installation of NodeJS (on debian based systems: ```sudo apt install nodejs```)
- installation of Python (preinstalled on most linux machines)
- installation of VS Code

If you are working on Windows you need to install the VCP Windows Driver from
[Silabs](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers?tab=downloads). On Linux the driver should be part of the Kernel already.

To use Micropyhton downloading the firmware is required. It can be downloaded
[here](https://www.micropython.org/download/ESP32_GENERIC/).

To flash the Firmware ```esptool``` needs to be installed with:
```
pip install esptool
```
now flash the ESP32 with the Micropython firmware, where ```<PORT>``` is the Port
of the connected device and ```<PATH>``` the path of the downloaded firmware.
the port can be determined as described in [this](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/establish-serial-connection.html#check-port-on-windows) article.
```
esptool --chip esp32 --port <PORT> --baud 460800 write_flash -z 0x1000 <PATH>
```

After now opening VS Code you should be able to find the extension "pymakr" in the "Extensions" tab of VS Code and install it. Next a project can be created from the new "Pymakr" tab that should have appeared on the left side. The ESP32 now can be connected when pressing the lightning symbol after a project is created and the device is added. When now clicking on the terminal icon the VS Code terminal should connect to the ESP32.

You can check the connection by typing:
```
import sys; sys.platform
```
which should return ```'esp32'```.

After that you can write your Python code inside the ```main.py``` which is the file executed on the ESP32. In the Pymakr extension tab should be a symbol with a cloud and an arrow up. With that button you can flash the ESP32 with your written code. If the button is disabled than press the three dots and select "Stop script".

After uploading the code you can press the reset button on the device itself or the "Hard reset device" option in the three dots menu. To stop the device from running the script and press the "Stop script" option again. Now you should be able to upload you updated code.

## Installation of Mosquitto MQTT-Broker on Debian based systems

### Install Mosquitto
```
sudo apt install mosquitto mosquitto-clients
```

if not available
```
sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
sudo apt-get update
```
### Free the port of the broker with ufw
```
sudo ufw allow 1883/tcp
```
### Check if Mosquitto is running
```
sudo systemctl status mosquitto
```
### Further configuration
(<your_user> is a placeholder)
<br><br>
go to mosquitto installation directory
```
cd /etc/mosquitto
```
make config editable
```
sudo chmod +w mosquitto.conf
```
if ```passwd``` file exists
```
sudo mosquitto_passwd /etc/mosquitto/passwd <your_user>
```
if not 
```
sudo mosquitto_passwd -c /etc/mosquitto/passwd <your_user>
```
you should be prompted to type in a password. Remember to remember the password
because it will be hashed inside the ```passwd``` file
<br><br>
if ```acl``` file does not exists
```
sudo touch acl
```
own the files
```
sudo chown mosquitto: /etc/mosquitto/passwd

sudo chown mosquitto: /etc/mosquitto/acl
```
open the ```mosquitto.conf``` file (for example with ```sudo vim mosquitto.conf```) and paste following content. Do not overwrite the current contents of the file (bind_address is important to reach the broker from outside the current machine)
```
password_file /etc/mosquitto/passwd
acl_file /etc/mosquitto/acl
bind_address 0.0.0.0
```
open the acl (```sudo vim acl```) and paste following content
```
user <your_user>
topic readwrite test/topic
```
of course ```test/topic``` needs to be replaced with an actual topic, but ```test/topic``` works for the start

at the end of changing these file, the broker should be restarted with
```
sudo systemctl restart mosquitto
```

### Testing the connection
listen for messages
```
mosquitto_sub -h localhost -t test/topic -u <your_user> -P <your_password>
```
send messages
```
mosquitto_pub -h localhost -t test/topic -m "Hello, MQTT" -u <your_user> -P <your_password>
```
If you want to access the broker from another machine you need to replace localhost with the IP address of the device your broker is running on.