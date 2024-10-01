# IOT-Distributed-Smarthome
This repository contains the code for a university project simulating a Smart Home using a Raspberry Pi and multiple ESP32 microcontrollers. The Raspberry Pi acts as the central control unit, while the ESP32 devices manage components like lighting, temperature, and security systems.

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