import Gas_sensors.variables as v
import smbus
import os
import time
import math

GM_702B = 0x07 # oxigen

class CO2:
    __count    = 0              # acquisition count
    __co2data = [0]*101      # ozone data
    
    _R0 = 3.21
    _sensorValue = 0.0
    _volt = 0
    _RS_gas = 0
    _ratio = 0
    _log_ppm = 0 
    _ppm = 0


    def volt(self):
      self._volt =  (self._sensorValue/1024)*3.3
      # print("XXXXX",self._sensorValue)
      return self._volt

    def RS_gas(self):
      self.volt()
      self._RS_gas = (3.3-self._volt)/self._volt
      return self._RS_gas

    def ratio(self):
      self.RS_gas()
      self._ratio =  self._RS_gas/self._R0
      return self.ratio
    
    def log_ppm(self):
      self.ratio()
      self._log_ppm = ( math.log10(self._ratio) * - 2.82) - 0.12
      return self._log_ppm

    def ppm(self, sensor_eval):
      self._sensorValue = sensor_eval()
      self.log_ppm()
      PPM = math.pow(10,self._log_ppm)
      return PPM

class NO2(CO2):
  _R0 = 1.07
  def log_ppm(self):
      self.ratio()
      self._log_ppm = ( math.log10(self._ratio) * - 1.9) - 0.2
      return self._log_ppm

class Multichannel_Gas(object):
  _GM_102B = 0x01 # NO2
  _GM_302B = 0x03 # C2H5OH 

  _GM_502B = 0x05 # VOC
  _GM_702B = 0x07 # CO2

  _CHANGE_I2C_ADDR = 0x55
  _WARMING_UP = 0xFE
  _WARMING_DOWN  = 0xFF
  _is_preheated = False

  def __init__(self ,bus):
    self.i2cbus = smbus.SMBus(bus)
    super(Multichannel_Gas, self).__init__()
    self.__co2 = CO2()
    self.__no2 = NO2()
  '''
    @brief get flash value
  '''
  def get_flash(self, register):
    # rslt = self.read_reg(register ,2)
    rslt = self.read_reg(register ,4)
    
    # print("register", rslt[1],rslt[0])
    # print("register", bin(rslt[1]),bin(rslt[0]))
    # print("register", bin(rslt[1] << int(8)) ,bin(rslt[0]))
    # print("register", bin((rslt[1] << int(8))+rslt[0]))
    # print("register", ((rslt[1] << int(8))+rslt[0]))
    print("register", int(rslt) )

  '''
    @brief returns raw output from the I2C 
    @return  a number the break out is putting out
  '''
  def preheat(self):
    if not self._is_preheated:
      self.write_cmd(self._WARMING_UP)
      self._is_preheated = True
    return self._is_preheated
  
  def cooldown(self):
    self.write_cmd(self._WARMING_DOWN)
    self._is_preheated = False
    return self._is_preheated

  def calc_vol(self, gas):
    return (gas * 3.3) / 1024

  def get_GM_102B(self):
    self.preheat()
    return self.read_reg(self._GM_102B)
  
  def get_GM_302B(self):
    self.preheat()
    return self.read_reg(self._GM_302B)
  
  def get_GM_502B(self):
    self.preheat()
    return self.read_reg(self._GM_502B)
  
  def get_GM_702B(self):
    self.preheat()
    return self.read_reg(self._GM_702B)
  
  def get_all(self):
    return {"CO2": self.get_GM_702B(), "VOC": self.get_GM_502B(), "C2H5OH": self.get_GM_302B(), "NO2": self.get_GM_102B() }
  
  def get_all_vol(self):
    return {"CO2": self.calc_vol(self.get_GM_702B()), "VOC": self.calc_vol(self.get_GM_502B()), "C2H5OH": self.calc_vol(self.get_GM_302B()), "NO2": self.calc_vol(self.get_GM_102B()) }

  def get_co2(self):
    return self.__co2.ppm(self.get_GM_702B )
  
  def get_no2(self):
    return self.__no2.ppm(self.get_GM_102B )


'''
  @brief An example of an IIC interface module
'''
class Multichannel_Gas_I2C(Multichannel_Gas): 
  def __init__(self ,bus = v.IIC_MODE,addr = v.ADDRESS):
    self.__addr = addr
    super(Multichannel_Gas_I2C, self).__init__(bus)

  '''
    @brief writes data to a register
    @param reg register address
    @param data written data
  '''
  def write_reg(self, reg, data):
    self.i2cbus.write_i2c_block_data(self.__addr ,reg ,data)
  '''
    @brief sends byte to a register
    @param cmd register address
  '''
  def write_cmd(self, cmd):
    self.i2cbus.write_byte(self.__addr, cmd)

  '''
    @brief read the data from the register
    @param reg register address
    @param value read data
  '''
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
