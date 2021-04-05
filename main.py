import time
import math
import random

from Oxygen_sensor import *

from OSC.server import Server
from OSC.client import Client

    

if __name__ == "__main__":
    now = time.time()
    oxygen = DFRobot_Oxygen_IIC()
    osc_server = Server()
    osc_client = Client()
    # setup stuff that should happen once
    try:
        while True:
            # loopforever
            
            if time.time() - now > 1:
                print("seconds")
                oxygen_data = oxygen.get_oxygen_data()
                osc_client.send_message("/oxygen", oxygen_data )
                now = time.time()
                
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        osc_server.close()
    finally:
        print('Program finished')

        
