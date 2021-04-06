import time
import smbus
import os
import Gas_sensors.variables as v

ADDRESS_0                 = 0x27           # i2c Address

class Temp_Humidity_Data:
    """Store the 6 band spectral values."""

    def __init__(self, temp, humidity):
        self.temp = temp
        self.humidity = humidity

    def __iter__(self):  
        for data in ['temp', 'humidity']:
            yield getattr(self, data)

class Sparkfun_Temp(object):


    def __init__(self ,bus):
        self.i2cbus = smbus.SMBus(bus)

    def get_humidity_temperature(self):
        output = self.raw_reg(0x00,4)
        Hum_H = output[0]
        Hum_L = output[1]
        Temp_H = output[2]
        Temp_L = output[3]
        hum = Hum_H << 8 | Hum_L
        temp = Temp_H << 8 | Temp_L
        # temp = temp /4
        return Temp_Humidity_Data(temp, hum)
        # print("temp  {} humidity {}".format(temp, hum))
        
    

'''
  @brief An example of an IIC interface module
'''
class Temp_Humidity(Sparkfun_Temp): 
  def __init__(self ,bus = v.IIC_MODE,addr = v.ADDRESS):
    self.__addr = addr
    super(Temp_Humidity, self).__init__(bus)


  def write_reg(self, reg, data):
    self.i2cbus.write_i2c_block_data(self.__addr ,reg ,data)
 
  def write_cmd(self, cmd):
    self.i2cbus.write_byte(self.__addr, cmd)
  
  def raw_reg(self, reg ,len=2):
    while 1:
      try:
        rslt = self.i2cbus.read_i2c_block_data(self.__addr ,reg ,len)
        return rslt
      except:
        os.system('i2cdetect -y 1')

  def read_reg(self, reg ,len=2):
    # while 1:
    #   try:
    rslt = self.i2cbus.read_i2c_block_data(self.__addr ,reg ,len)
    dta = 0.0
    i = 0
    # print("rslt", rslt, ((rslt[1] << int(8))+rslt[0])) 
    # ((rslt[1] << int(8))+rslt[0]))
    
    for byte in range(len-1,-1,-1):
        # print("byte{}".format(byte), rslt[byte])
        dta += int(rslt[byte]) << int(8 * byte )
    return dta
    #   except:
    #     os.system('i2cdetect -y 1')



