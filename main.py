import time
import math
import random

from Oxygen_sensor import *

from OSC.server import Server
from OSC.client import Client
from Gas_sensors.multichannel_gas import Multichannel_Gas_I2C
    

if __name__ == "__main__":
    now = time.time()
    oxygen = DFRobot_Oxygen_IIC()
    osc_server = Server()
    osc_client = Client()

    gas_sensor = Multichannel_Gas_I2C()
    # setup stuff that should happen once
    try:
        while True:
            # loopforever
            
            if time.time() - now > 1:
                print("seconds")
                oxygen_data = oxygen.get_oxygen_data()
                gases = gas_sensor.get_all_vol()

                for gas in gases:
                    # do this with bundle eventually
                    osc_client.send_message("/{}".format(gas), gases[gas] )

                now = time.time()
                
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        osc_server.close()
    finally:
        print('Program finished')

        
