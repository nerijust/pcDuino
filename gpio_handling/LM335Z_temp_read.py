#!/usr/bin/env python
#
# LMZ335Z_temp_read.py
# Mesure temperature with LM335Z for pcduino ( http://www.pcduino.com )
# 
# nerijust.com
# https://github.com/nerijust/pcDuino.git

import time, os
from gpio import *

def loop():
	V_in = 3.3 #voltage in to voltage divider
	ADC_resoliution = V_in/4095 #12 bit resolution in V
	
	while(1):
		os.system('clear') #clear terminal window on linux
		V_out = GPIO_ADC(3)*ADC_resoliution #voltage out of voltage divider
		temp_K = V_out*1000/10 #actual temperature in Kelvin
		temp = temp_K - 273.15 #actual temperature in Celsius

		print 'temperature: ', "%.2f" % temp, 'deg C' #print temperature in terminal window
		time.sleep(1)      # wait 1 sec.
		
def main():
	loop()

main()
