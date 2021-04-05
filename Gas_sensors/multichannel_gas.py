import Gas_sensors.variables as v
import smbus
import os
import time

GM_702B = 0x07 # oxigen

class CO2(object):
    def __init__(self):
        pass
    def co2(self):
        print("co2 class")
        rslt = self.interpret_reg(register ,2)
        print("register", int(rslt) )

class Multichannel_Gas(object):
  __key      = 0.0            # co2 key value
  __count    = 0              # acquisition count
  __txbuf      = [0]          # iic send buffer
  __co2data = [0]*101      # ozone data
  def __init__(self ,bus):
    self.i2cbus = smbus.SMBus(bus)
    super(Multichannel_Gas, self).__init__()
  '''
    @brief get flash value
  '''
  def get_flash(self, register):
    # rslt = self.read_reg(register ,2)
    rslt = self.interpret_reg(register ,4)
    
    # print("register", rslt[1],rslt[0])
    # print("register", bin(rslt[1]),bin(rslt[0]))
    # print("register", bin(rslt[1] << int(8)) ,bin(rslt[0]))
    # print("register", bin((rslt[1] << int(8))+rslt[0]))
    # print("register", ((rslt[1] << int(8))+rslt[0]))
    print("register", int(rslt) )

    # if rslt == 0:
    #   self.__key = (20.9 / 120.0)
    # else:
    #   self.__key = (float(rslt[0]) / 1000.0)
    # time.sleep(0.1)
  
  '''
    @brief calibrate key value
    @param vol co2 content
    @param mv  the value marked on the sensor
  '''
  def calibrate(self ,vol ,mv):
    self.__txbuf[0] = int(vol * 10)
    if (mv < 0.000001) and (mv > (-0.000001)):
      self.write_reg(USER_SET_REGISTER ,self.__txbuf)
    else:
      self.__txbuf[0] = int((vol / mv) * 1000)
      self.write_reg(AUTUAL_SET_REGISTER ,self.__txbuf)

  '''
    @brief read the co2 data ,units of vol
    @param collectnum Collect the number
    @return  Oxygen concentration, (units %)
  '''
  def get_co2_data(self ,collectnum = v.COLLECT_NUMBER):
    self.get_flash(GM_702B)
    # if collectnum > 0:
    #   for num in range(collectnum ,1 ,-1):
    #     self.__co2data[num-1] = self.__co2data[num-2]
    #   rslt = self.read_reg(OXYGEN_DATA_REGISTER ,3)
    #   self.__co2data[0] = self.__key * (float(rslt[0]) + float(rslt[1]) / 10.0 + float(rslt[2]) / 100.0)
    #   if self.__count < collectnum:
    #     self.__count += 1
    #   return self.get_average_num(self.__co2data ,self.__count)
    # elif (collectnum > 100) or (collectnum <= 0):
    #   return -1

  ''' 
    @brief get the average of the co2 data ,units of vol
    @param barry ozone data group
    @param Len The number of data
    @return  Oxygen concentration, (units %)
  '''
  def get_average_num(self ,barry ,Len):
    temp = 0.0
    for num in range (0 ,Len):
      temp += barry[num]
    return (temp / float(Len))

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

  def interpret_reg(self, reg ,len):
    # while 1:
    #   try:
    rslt = self.i2cbus.read_i2c_block_data(self.__addr ,reg ,len)
    dta = 0.0
    i = 0
    print("rslt", rslt, ((rslt[1] << int(8))+rslt[0])) 
    # ((rslt[1] << int(8))+rslt[0]))
    
    for byte in range(len-1,-1,-1):
        print("byte", byte, rslt[byte])
        dta += int(rslt[byte]) << int(8 * byte )
    return dta
    #   except:
    #     os.system('i2cdetect -y 1')
