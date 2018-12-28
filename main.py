import os
import time

import logging
import logzero
from logzero import logger
import cv2

from sense_hat import SenseHat
from picamera import PiCamera


""" 
		Global variables
"""
# CONSTANTS
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
TIME_LOOP = 000 # duration of a loop
TIME_STOP = 000 # duration from which the program stop

loop = True
nbImage = 1
start_program_time = int(time.time()) # timestamp when the program has started (in second)
start_loop_time = 0 # timestamp when the loop has started

# CAMERA
camera = PiCamera()
camera.resolution = (640,480)

# SENSEHAT
sh = SenseHat()

# 	Matrix led
# 		Colors
g = [0,50,0]
o = [0,0,0]
#		Define a simple image
img1 = [
	g,g,g,g,g,g,g,g,
	o,g,o,o,o,o,g,o,
	o,o,g,o,o,g,o,o,
	o,o,o,g,g,o,o,o,
	o,o,o,g,g,o,o,o,
	o,o,g,g,g,g,o,o,
	o,g,g,g,g,g,g,o,
	g,g,g,g,g,g,g,g,
]

# Logfile parameters
formatter = logging.Formatter('%(name)s - %(asctime)-15s - %(levelname)s: %(message)s') # Set a custom formatter
logzero.formatter(formatter)

####

def update_matrix(state):
	""" Update the state of the matrix led """
	if state == 0:
		sh.set_pixels(img1)
	elif state == 1:
		sh.set_rotation(90)
	else:
		sh.set_rotation(270)

"""
		GET main data
"""

def get_loop_timestamp():
	""" Get the timestap when the loop has started """
	start_loop_time = time.time()

def get_sensors_value():
	pass

def take_picture():
	""" Prend une photo et l'enregistre dans un fichier """
	camera.capture(dir_path+"/image_"+str(nbImage).zfill(3)+".jpg")
	nbImage += 1

"""
		OPENCV
"""

def is_night():
	pass

def draw_area():
	pass

def analyse_picture():
	pass

"""
		finish up the loop
"""

def write_result(timestamp, water, ground, cloud, other, magnetometer, accelerometer):
	""" Write data in the CSV file """
	# Save the data to the file
	logger.info("%s,%s", humidity, temperature, )

def check_time():
	""" check if the program must be stopped """
	now = int(time.time()) # in second
	# 3h == 10,800 seconds
	if (now - start_time) >= TIME_STOP:
		# Stopper le programme
		loop = False
	else:
		wait()

def wait():
	""" Wait before start again  """
	now = time.time()
	if (now - start_loop_time) < TIME_LOOP:
		time.sleep(TIME_LOOP - (now - start_loop_time))


##########################
## in progress

logzero.logfile(DIR_PATH+"/data01.csv") # Create the CSV file

while loop:
	update_matrix(0)
	get_loop_timestamp()
	get_sensors_value()
	take_picture()

	if not is_night():
		update_matrix(1)
		draw_area()
		analyse_picture()

	update_matrix(2)
	write_result()
	check_time()

##########################
## finish up the program

camera.close()