#! /usr/bin/env python2

import serial
import os
import time


def open_serial_port():
	if os.name == 'nt':
		ser = serial.Serial('COM3', baudrate = 9600, timeout = 1)
	else:
		ser = serial.Serial('/dev/ttyUSB0', baudrate = 9600, timeout = 1)
	return ser

def read_meteoData(serialPort):
	ser = serialPort
	data = ser.readline().split()
	#while not data: 
	#	data = ser.readline().split() 
	if data:
		data[0] = '%.1f' % float(data[0])
		data[1] = '%.0f' % float(data[1])
		data[2] = '%.2f' % float(data[2])
	ser.reset_input_buffer()
	return data


