from machine import Pin
from hcsr04 import HCSR04
from oled_1inch3_spi import OLED_1inch3
import time


sensor = HCSR04(trigger_pin=2, echo_pin=3, echo_timeout_us=28000)
OLED = OLED_1inch3()
keyA = Pin(15, Pin.IN, Pin.PULL_UP)
keyB = Pin(17, Pin.IN, Pin.PULL_UP)

speed_of_sound = 343  # m/s

while True:
    pulse_time_us = sensor.send_pulse_and_wait()
    speed_of_sound_mm_us = speed_of_sound * 1e-3
    distance = pulse_time_us * speed_of_sound_mm_us / 2

    if keyA.value() == 0 and keyB.value() == 0:
        speed_of_sound = 343
    elif keyA.value() == 0:
        speed_of_sound += 0.1
    elif keyB.value() == 0:
        speed_of_sound -= 0.1

    OLED.fill(0x0000)
    OLED.text(f"t_p: {pulse_time_us:5.0f} us", 0, 0, OLED.white)
    OLED.text(f"v_s: {speed_of_sound:4.1f} m/s", 0, 10, OLED.white)
    OLED.text(f"dist: {distance:4.0f} mm", 0, 20, OLED.white)
    OLED.show()
    time.sleep(0.2)
