#!/usr/bin/env python

import time, os

HIGH = "1"
LOW =  "0"
INPUT = "0"
OUTPUT = "1"
INPUT_PU = "8"
SERIAL = "3"

def GPIO_MODE(pin, mode): # set pin mode - INPUT or OUTPUT
	file = open('/sys/devices/virtual/misc/gpio/mode/gpio' +str(pin), 'r+')
	file.write(mode)
	file.close()

def GPIO_DATA(pin, data): # set pin data - LOW or HIGH
	file = open('/sys/devices/virtual/misc/gpio/pin/gpio' +str(pin), 'r+')
	file.write (data)
	file.close()

def GPIO_STATUS(pin): # read pin status LOW or HIGH and return value as integer
	file = open('/sys/devices/virtual/misc/gpio/pin/gpio' +str(pin), 'r+')
	file.seek(0)
	status = file.read()
	file.close()
	return int(status)

def GPIO_PWM(pin, value): # set value of PWM chanel
	file = open('/sys/class/leds/pwm' +str(pin) +'/max_brightness', 'r')
	max_value = int(file.read())
	file.close()
	if value > max_value:
		value = max_value
	if value < 0:
		value = 0
	os.system('echo ' +str(value) +' >' +'/sys/class/leds/pwm' +str(pin) +'/brightness')
	
def GPIO_PWM_read(pin): # read PWM chanel value
	file = open('/sys/class/leds/pwm' +str(pin) +'/brightness', 'r')
	value = file.read()
	file.close()
	return int(value)

def GPIO_ADC(pin): # read ADC chanel(pin) value and return as integer
	file = open('/proc/adc' +str(pin), 'r')
	value = file.read().split(':')[1].strip()
	file.close()
	return int(value)
