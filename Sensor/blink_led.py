import time
import machine

led_pin = machine.Pin(2, machine.Pin.OUT)

def blink_led():
    led_pin.value(1)
    time.sleep(0.5)
    led_pin.value(0)