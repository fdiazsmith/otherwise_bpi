# -*- coding:utf-8 -*-

import sys
import time
import math

from Gas_sensors.multichannel_gas import Multichannel_Gas_I2C


gases = Multichannel_Gas_I2C()

try:
    while 1:
      print(" temperature  and humidity {} ".format(gases.get_no2()))
      # print(" vol is {} ".format(gases.get_all_vol()))
      time.sleep(1)
# If keyboard Interrupt (CTRL-C) is pressed
except KeyboardInterrupt:
    print("keyboard interrupt")
    pass       # Go to next line