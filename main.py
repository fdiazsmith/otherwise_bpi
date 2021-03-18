#!/usr/bin/env python
from smbus2 import SMBus
from grooveGas import Gas
print("OTHERWISE sensing")
# Open i2c bus 1 and read one byte from address 80, offset 0
# bus = SMBus(1)
# b = bus.read_byte_data(0x08, 0x01)
# print(b)
# bus.close()

i2c = SMBus(1)

g = Gas(i2c)
def main():
    '''
    Main program function
    '''

    gm1 = g.getGM102B()
    gm1v= g.calcVol(gm1) 
    gm3 = g.getGM302B()
    gm3v= g.calcVol(gm3) 
    gm5 = g.getGM502B()
    gm5v= g.calcVol(gm5) 
    gm7 = g.getGM702B()
    gm7v= g.calcVol(gm7) 
    print("NO2:{: <20}    C2H5OH:{: <20}   VOC:{: <20}   CO:{: <20}".format(gm1v,gm3v,gm5v,gm7v))


if __name__ == "__main__":
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print("Keyboard interrupt")
    finally:
        print('Program finished')
        g.close()

