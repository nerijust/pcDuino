#!/usr/bin/env python
#
# ntc_temp_read.py
# Mesure temperature with NTC termistor for pcduino ( http://www.pcduino.com )
# 
# nerijust.com
# https://github.com/nerijust/pcDuino.git

import time, os, math
from gpio import *
from math import log

def loop():
	V_in = 3.3 #voltage in to voltage divider
	ADC_resoliution = V_in/4096 #12 bit resolution in V (use chanel A2 - A5)
	R_nom = 1000 #nominal NTC termistor resistance at nominal temperature (25 deg Celsius)
	R_sec = 1000 #resistance of second resistor in voltage divider
	T_nom = 25 + 273.15 #nominal temperature in Kelvin
	B = 3730 #from datasheet device specific constant in Kelvin

	while(1):
		os.system('clear') #clear terminal window on linux
		V_out = GPIO_ADC(3)*ADC_resoliution #voltage out of voltage divider
		R_actual = ((V_in*R_sec) / (V_in - V_out)) - R_sec #actual NTC termistor resistance
		log_value = R_actual/R_nom #log function value for next formula
		temp_K = (B * T_nom)/(B + (math.log(log_value) * T_nom)) #actual temperature in Kelvin
		temp = temp_K - 273.15 #actual temperature in Celsius

		print 'temperature: ', "%.2f" % temp, 'deg C'
		time.sleep(1)      # wait 1 sec.
		
def main():
	loop()

main()
