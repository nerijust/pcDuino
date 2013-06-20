#!/usr/bin/env python
#
# blinking_led.py
# gpio test code for pcduino ( http://www.pcduino.com )
# 
# nerijust.com

import time, os
from gpio import *


GPIO_MODE(2, OUTPUT) # make GPIO2 pin an output
GPIO_DATA(2, LOW)    # set it LOW

while(1):
    GPIO_DATA(2, HIGH) # set GPIO2 pin HIGH
    time.sleep(2)      # wait 2 sec.
    GPIO_DATA(2, LOW)  # set GPIO2 pin LOW
    time.sleep(2)      # wait 2 sec.


