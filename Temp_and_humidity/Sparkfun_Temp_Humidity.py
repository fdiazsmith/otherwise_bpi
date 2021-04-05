import time
import smbus
import os

ADDRESS_0                 = 0x27           # i2c Address

class Sparkfun_Temp(object):
    __key      = 0.0            # oxygen key value
    __count    = 0              # acquisition count
    __txbuf      = [0]          # iic send buffer
    __oxygendata = [0]*101      # ozone data

    def __init__(self ,bus):
        self.i2cbus = smbus.SMBus(bus)

    def get_humidity_temperature(self):
        output = self.read_reg(0x00 ,4)
        Hum_H = output[0]
        Hum_L = output[1]
        Temp_H = output[2]
        Temp_L = output[3]
        hum = Hum_H << 8 | Hum_L
        temp = Temp_H << 8 | Temp_L
        # temp = temp /4
        print("temp  {} humidity {}".format(temp, hum))
        
    
'''
  @brief An example of an IIC interface module
'''
class Temp_Humidity(Sparkfun_Temp): 
  def __init__(self ,bus ,addr):
    self.__addr = addr;
    super(Temp_Humidity, self).__init__(bus)

  '''
    @brief writes data to a register
    @param reg register address
    @param value written data
  '''
  def write_reg(self, reg, data):
    self.i2cbus.write_i2c_block_data(self.__addr ,reg ,data)

  '''
    @brief read the data from the register
    @param reg register address
    @param value read data
  '''
  def read_reg(self, reg ,len):
    while 1:
      try:
        rslt = self.i2cbus.read_i2c_block_data(self.__addr ,reg ,len)
        return rslt
      except:
        os.system('i2cdetect -y 1')


# pass in the bus number and the address
temp = Temp_Humidity(0x01, 0x27)

if __name__ == "__main__":
    try:
        while True:
            temp.get_humidity_temperature()
            time.sleep(1)
    except KeyboardInterrupt:

        print("Keyboard interrupt")
    finally:

        print('Program finished')