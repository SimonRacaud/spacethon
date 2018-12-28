import os
import time

import logging
import logzero
from logzero import logger
import cv2
import ephem # position ISS

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
sense.set_imu_config(True, False, True) # (compass_enabled, gyro_enabled, accel_enabled)

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
"""[a voir]""" formatter = logging.Formatter('%(timestamp)s - %(water)s - %(ground)s - %(cloud)s - %(other)s - %(magnetometer)s - %(accelerometer)s') # Set a custom formatter
logzero.formatter(formatter)
logzero.logfile(DIR_PATH+"/data01.csv") # Create the CSV file

# Config ephem
name = "ISS (ZARYA)"
line1 = "1 25544U 98067A   18362.36563081 -.00011736  00000-0 -17302-3 0  9998"
line2 = "2 25544  51.6377 131.0297 0002747 209.2490 215.4464 15.53700691148714"
# source : http://www.celestrak.com/NORAD/elements/stations.txt
iss = ephem.readtle(name, line1, line2)
# utilisation : print(iss.sublat, iss.sublong)
iss.compute()

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
	""" Get the value of the sensors """
	magnetometer = sense.get_compass_raw() # magnetometer
	accelerometer = sense.get_accelerometer() # accelerometer
	return (magnetometer, accelerometer)

def take_picture():
	""" Prend une photo et l'enregistre dans un fichier """
	get_latlon() # Set lat/long data in the meta data of the picture
	camera.capture(dir_path+"/image_"+str(nbImage).zfill(3)+".jpg")
	iss.compute() # mise à jour coordonnés
	nbImage += 1

def get_latitude_longitude():
	""" Get latitude/longitude and set there in the meta data of the camera """
    iss.compute() # Get the lat/long values from ephem

    long_value = [float(i) for i in str(iss.sublong).split(":")]

    if long_value[0] < 0:

        long_value[0] = abs(long_value[0])
        camera.exif_tags['GPS.GPSLongitudeRef'] = "W"
    else:
        camera.exif_tags['GPS.GPSLongitudeRef'] = "E"
    camera.exif_tags['GPS.GPSLongitude'] = '%d/1,%d/1,%d/10' % (long_value[0], long_value[1], long_value[2]*10)

    lat_value = [float(i) for i in str(iss.sublat).split(":")]

    if lat_value[0] < 0:

        lat_value[0] = abs(lat_value[0])
        camera.exif_tags['GPS.GPSLatitudeRef'] = "S"
    else:
        camera.exif_tags['GPS.GPSLatitudeRef'] = "N"

    camera.exif_tags['GPS.GPSLatitude'] = '%d/1,%d/1,%d/10' % (lat_value[0], lat_value[1], lat_value[2]*10)

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
	logger.info("%s,%s,%s,%s,%s", timestamp, water, )

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

while loop:
	update_matrix(0)
	get_loop_timestamp()
	magnetometer, accelerometer = get_sensors_value()
	take_picture()

	if not is_night():
		update_matrix(1)
		draw_area()
		analyse_picture()

	update_matrix(2)
	write_result(...)
	check_time()

##########################
## finish up the program

camera.close()