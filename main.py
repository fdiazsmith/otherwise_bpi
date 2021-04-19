import time
import math
import random

from Oxygen_sensor import *

from OSC.server import Server
from OSC.client import Client
from Gas_sensors.multichannel_gas import Multichannel_Gas_I2C

from as7262 import AS7262




if __name__ == "__main__":
    now = time.time()
    oxygen = DFRobot_Oxygen_IIC()
    osc_server = Server()
    osc_client = Client()

    gas_sensor = Multichannel_Gas_I2C()

    as7262 = AS7262()

    as7262.set_gain(64)
    as7262.set_integration_time(17.857)
    as7262.set_measurement_mode(2)
    as7262.set_illumination_led(1)
    print('Program running')
    # setup stuff that should happen once
    try:
        while True:
            # loopforever
            
            if time.time() - now > 1:
               
                oxygen_data = oxygen.get_oxygen_data()
                gases = gas_sensor.get_all_vol()

                for gas in gases:
                    # do this with bundle eventually
                    osc_client.send_message("/{}".format(gas), gases[gas] )
                osc_client.send_message("/O2", oxygen_data )
                
                values = as7262.get_calibrated_values()


                osc_client.send_message("/Red", values.red )
                osc_client.send_message("/Orange", values.orange )
                osc_client.send_message("/Yellow", values.yellow )
                osc_client.send_message("/Green", values.green )
                osc_client.send_message("/Blue", values.blue )
                osc_client.send_message("/Violet", values.violet )

                now = time.time()
                
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        as7262.set_measurement_mode(3)
        as7262.set_illumination_led(0)
        osc_server.close()
    finally:
        print('Program finished')

        
