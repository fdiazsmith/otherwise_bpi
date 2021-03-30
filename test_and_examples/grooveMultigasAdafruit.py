'''
BREADCRUMS
-[Tutorial to creare I2C lib](https://learn.adafruit.com/porting-an-arduino-library-to-circuitpython-vl6180x-distance-sensor?view=all)
- has dependencies on [Adafruit CircuitPython libraries](https://learn.adafruit.com/circuitpython-basics-i2c-and-spi/i2c-devices). 
-[more detail explanation of I2C](https://learn.adafruit.com/circuitpython-basics-i2c-and-spi/i2c-devices)
'''
import board
import busio as io
i2c = io.I2C(board.SCL, board.SDA)

while not i2c.try_lock():
    pass
[hex(x) for x in i2c.scan()]
i2c.writeto(0x08, bytes([0x01]), stop=False)
result = bytearray(4)
i2c.readfrom_into(0x08, result)
print(hex(result[0]))