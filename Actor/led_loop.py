import time
import machine

led_pin = machine.Pin(2, machine.Pin.OUT)
def blink_led():
    while True:
        led_pin.value(1)
        print("Turning ON...")
        time.sleep(1)
        led_pin.value(0)
        print("Turning OFF...")
        time.sleep(1)