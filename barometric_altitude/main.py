from machine import Pin
from oled_1inch3_spi import OLED_1inch3
from lps22hbtr import LPS22HB
from ina219 import INA219
import time

# calculate barometric altitude based on the following formula:
# https://www.weather.gov/media/epz/wxcalc/pressureAltitude.pdf
def calculate_pressure_altitude(pressure: float, p0: float = 1013.25) -> float:
    altitude = 0.3048 * 145_366.45 * (1 - pow(pressure / p0, 0.190_284))
    return altitude


OLED = OLED_1inch3()
lps22hb = LPS22HB()
keyA = Pin(15, Pin.IN, Pin.PULL_UP)
keyB = Pin(17, Pin.IN, Pin.PULL_UP)
# Create an ADS1115 ADC (16-bit) instance.
ina219 = INA219(addr=0x43)

ref_pressure = 1013.25

while True:
    data = lps22hb.read_sensor()
    pressure = data["pressure"]
    temperature = data["temperature"]
    altitude = calculate_pressure_altitude(pressure, ref_pressure)
    if keyA.value() == 0 and keyB.value() == 0:
        ref_pressure = 1013.25
    elif keyA.value() == 0:
        ref_pressure += 0.1
    elif keyB.value() == 0:
        ref_pressure -= 0.1
    # voltage on V- (load side)
    bus_voltage = ina219.getBusVoltage_V()
    # INA219 measures bus voltage on the load side. So PSU voltage = bus_voltage + shunt_voltage
    P = (bus_voltage - 3) / 1.2 * 100
    if P < 0:
        P = 0
    elif P > 100:
        P = 100

    OLED.fill(0x0000)
    OLED.text(f"p : {pressure:7.2f} hPa", 0, 0, OLED.white)
    OLED.text(f"T : {temperature:7.2f} degC", 0, 10, OLED.white)
    OLED.text(f"h : {altitude:7.2f} m", 0, 20, OLED.white)
    OLED.text(f"p0: {ref_pressure:7.2f} hPa", 0, 30, OLED.white)
    OLED.text(f"Bat: {bus_voltage:4.2f} V, {P:.0f}%", 0, 50, OLED.white)
    OLED.show()
    time.sleep(0.27)
