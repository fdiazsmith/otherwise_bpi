# -*- coding:utf-8 -*-

import sys
import time
import math

from Gas_sensors.multichannel_gas import Multichannel_Gas_I2C


gases = Multichannel_Gas_I2C()

try:
    while 1:
      co2_data = gases.co2()
    #   print("c02 concentration is %4.2f %%vol"%co2_data)
      time.sleep(1)
# If keyboard Interrupt (CTRL-C) is pressed
except KeyboardInterrupt:
    print("keyboard interrupt")
    pass       # Go to next line