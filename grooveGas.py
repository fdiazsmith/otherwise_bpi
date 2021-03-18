from math import pow
from time import sleep

class Gas:
    DEFAULT_I2C_ADDR = 0x08

    ADDR_IS_SET = 0  # if this is the first time to run, if 1126, set
    ADDR_FACTORY_ADC_NH3 = 2
    ADDR_FACTORY_ADC_CO = 4
    ADDR_FACTORY_ADC_NO2 = 6

    ADDR_USER_ADC_HN3 = 8
    ADDR_USER_ADC_CO = 10
    ADDR_USER_ADC_NO2 = 12
    ADDR_IF_CALI = 14  # IF USER HAD CALI

    ADDR_I2C_ADDRESS = 20

    CH_VALUE_NH3 = 1
    CH_VALUE_CO = 2
    CH_VALUE_NO2 = 3

    CMD_ADC_RES0 = 1  # NH3
    CMD_ADC_RES1 = 2  # CO
    CMD_ADC_RES2 = 3  # NO2
    CMD_ADC_RESALL = 4  # ALL CHANNEL
    CMD_CHANGE_I2C = 5  # CHANGE I2C
    CMD_READ_EEPROM = 6  # READ EEPROM VALUE, RETURN UNSIGNED INT
    CMD_SET_R0_ADC = 7  # SET R0 ADC VALUE
    CMD_GET_R0_ADC = 8  # GET R0 ADC VALUE
    CMD_GET_R0_ADC_FACTORY = 9  # GET FACTORY R0 ADC VALUE
    CMD_CONTROL_LED = 10
    CMD_CONTROL_PWR = 11

    WARMING_UP = 0xFE
    WARMING_DOWN = 0xFF
    CHANGE_I2C_ADDR = 0x55
    GM_RESOLUTION = 1023
    GM_102B = 0x01
    GM_302B = 0x03
    GM_502B = 0x05
    GM_702B = 0x07

    CO = 0
    NO2 = 1
    NH3 = 2
    C3H8 = 3
    C4H10 = 4
    CH4 = 5
    H2 = 6
    C2H5OH = 7

    adcValueR0_NH3_Buf = 0
    adcValueR0_C0_Buf = 0
    adcValueR0_NO2_Buf = 0

    def __init__(self, i2c, addr=DEFAULT_I2C_ADDR):
        self.i2c = i2c
        self.addr = addr
        self.preheat()
        # print("preheated", self.preheated)
        # self.version = self.get_version()

    def write(self, cmd):
        self.i2c.write_byte_data(self.addr, 0, cmd)
        sleep(0.001)
    
    def read(self, cmd):
        return self.i2c.read_byte_data(self.addr, cmd)
   
    def read_block(self, cmd, nbytes=2):
        raw = self.i2c.read_i2c_block_data(self.addr, cmd, nbytes)
        dta = 0
        # print("reading block list ", raw)
        for byte in raw:
            dta = dta * 256 + int(byte)
        sleep(0.001)
        return dta

    def calcVol(self,  adc):
        return (adc * 3.3) / self.GM_RESOLUTION
    
    def preheat(self):
        self.write(self.WARMING_UP)
        self.preheated = True
        return True
    
    #not super sure if this is the right call for it
    def setAddress(self, newAddr ):
        self.i2c.write_i2c_block_data(self.addr,0, [self.CHANGE_I2C_ADDR, newAddr] )
        self.addr = newAddr
        return True
    
    # get reading from gas sensor
    def getGM102B(self):
        if not self.preheated:
            self.preheat()
        
        self.write(self.GM_102B)
        data = self.read_block(self.GM_102B, 4)
        # print("getting reading from sensor getGM102B", data)
        return data 
    
    # get reading from gas sensor
    def getGM302B(self):
        if not self.preheated:
            self.preheat()
        
        self.write(self.GM_302B)
        data = self.read_block(self.GM_302B, 4)
        # print("getting reading from sensor getGM302B", data)
        return data
    
    # get reading from gas sensor
    def getGM502B(self):
        if not self.preheated:
            self.preheat()
        
        self.write(self.GM_502B)
        data = self.read_block(self.GM_502B, 4)
        # print("getting reading from sensor getGM502B", data)
        return data
    
    # get reading from gas sensor
    def getGM702B(self):
        if not self.preheated:
            self.preheat()
        
        self.write(self.GM_702B)
        data = self.read_block(self.GM_702B, 4)
        # print("getting reading from sensor getGM702B", data)
        return data
    def close(self):
        self.i2c.close()


