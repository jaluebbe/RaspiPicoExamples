# code based on examples provided by Waveshare for the Pico-10DOF-IMU
import time
from machine import I2C

# i2c address
LPS22HB_I2C_ADDRESS = 0x5C
#
LPS_ID = 0xB1
# Register
LPS_INT_CFG = 0x0B  # Interrupt register
LPS_THS_P_L = 0x0C  # Pressure threshold registers
LPS_THS_P_H = 0x0D
LPS_WHO_AM_I = 0x0F  # Who am I
LPS_CTRL_REG1 = 0x10  # Control registers
LPS_CTRL_REG2 = 0x11
LPS_CTRL_REG3 = 0x12
LPS_FIFO_CTRL = 0x14  # FIFO configuration register
LPS_REF_P_XL = 0x15  # Reference pressure registers
LPS_REF_P_L = 0x16
LPS_REF_P_H = 0x17
LPS_RPDS_L = 0x18  # Pressure offset registers
LPS_RPDS_H = 0x19
LPS_RES_CONF = 0x1A  # Resolution register
LPS_INT_SOURCE = 0x25  # Interrupt register
LPS_FIFO_STATUS = 0x26  # FIFO status register
LPS_STATUS = 0x27  # Status register
LPS_PRESS_OUT_XL = 0x28  # Pressure output registers
LPS_PRESS_OUT_L = 0x29
LPS_PRESS_OUT_H = 0x2A
LPS_TEMP_OUT_L = 0x2B  # Temperature output registers
LPS_TEMP_OUT_H = 0x2C
LPS_RES = 0x33  # Filter reset register


class LPS22HB(object):
    def __init__(self, address=LPS22HB_I2C_ADDRESS):
        self._address = address
        self._bus = I2C(1)
        self.LPS22HB_RESET()  # Wait for reset to complete
        # BDU, ODR 75Hz, LP ODR/20
        self._write_byte(LPS_CTRL_REG1, 0b0_101_11_1_0)

    def LPS22HB_RESET(self):
        Buf = self._read_u16(LPS_CTRL_REG2)
        Buf |= 0x04
        self._write_byte(LPS_CTRL_REG2, Buf)  # SWRESET Set 1
        while Buf:
            Buf = self._read_u16(LPS_CTRL_REG2)
            Buf &= 0x04

    def _read_byte(self, cmd):
        rec = self._bus.readfrom_mem(int(self._address), int(cmd), 1)
        return rec[0]

    def _read_u16(self, cmd):
        LSB = self._bus.readfrom_mem(int(self._address), int(cmd), 1)
        MSB = self._bus.readfrom_mem(int(self._address), int(cmd) + 1, 1)
        return (MSB[0] << 8) + LSB[0]

    def _write_byte(self, cmd, val):
        self._bus.writeto_mem(int(self._address), int(cmd), bytes([int(val)]))

    def read_sensor(self):
        response = {}
        u8Buf = [0, 0, 0]
        u8Buf[0] = self._read_byte(LPS_PRESS_OUT_XL)
        u8Buf[1] = self._read_byte(LPS_PRESS_OUT_L)
        u8Buf[2] = self._read_byte(LPS_PRESS_OUT_H)
        response["pressure"] = (
            (u8Buf[2] << 16) + (u8Buf[1] << 8) + u8Buf[0]
        ) / 4096.0
        u8Buf[0] = self._read_byte(LPS_TEMP_OUT_L)
        u8Buf[1] = self._read_byte(LPS_TEMP_OUT_H)
        response["temperature"] = ((u8Buf[1] << 8) + u8Buf[0]) / 100.0
        return response


if __name__ == "__main__":
    lps22hb = LPS22HB()
    while True:
        time.sleep(0.1)
        print(lps22hb.read_sensor())