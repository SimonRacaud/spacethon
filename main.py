"""
	SPACETHON an AstroPI Project
		2018-2019
	
	Authors: GAZEAU Lucas, RACAUD Simon

	---

	Note: 
"""

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
		Global variables/constants
"""
### CONSTANTS
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
TIME_LOOP = 000 # duration of a loop
TIME_STOP = 000 # duration from which the program stop

### VARIABLES
loop = True
picture_ID = 1
row_ID = 1
start_program_time = int(time.time()) # timestamp when the program has started (in second)
start_loop_time = 0 # timestamp when the loop has started

""" 
		Config peripherals
"""
### CAMERA
camera = PiCamera()
camera.resolution = (640,480)

### SENSEHAT
sense = SenseHat()
sense.set_imu_config(True, False, True) # (compass_enabled, gyro_enabled, accel_enabled)

##	Matrix led
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

### Logfile parameters
logzero.logfile(DIR_PATH+"/data01.csv") # Create the CSV file
"""
# Set a custom formatter
formatter = logging.Formatter('%(timestamp)s - %(water)s - %(ground)s - %(cloud)s - %(other)s - %(magnetometer)s - %(accelerometer)s') # Set a custom formatter
logzero.formatter(formatter)
"""
logger.info("ROW,Time_Stamp,Picture_Number,Water,Ground,Cloud,MagX,MagY,MagZ,Acce_Pitch,Acce_Roll,AcceYaw")

### Config ephem (A REMPLACER !!!!)
name = "ISS (ZARYA)"
line1 = "1 25544U 98067A   18362.36563081 -.00011736  00000-0 -17302-3 0  9998"
line2 = "2 25544  51.6377 131.0297 0002747 209.2490 215.4464 15.53700691148714"
# source : http://www.celestrak.com/NORAD/elements/stations.txt
iss = ephem.readtle(name, line1, line2)
# utilisation : print(iss.sublat, iss.sublong)
iss.compute()

""" 
		[FUNCTIONS]
"""

def update_matrix(state):
	""" Update the state of the matrix led. """
	if state == 0:
		sh.set_pixels(img1)
	elif state == 1:
		sh.set_rotation(90)
	else:
		sh.set_rotation(270)

"""
		GET main data
"""

def get_sensors_value():
	""" Get the value of the sensors 
	"""
	magnetometer = sense.get_compass_raw() # magnetometer [x, y, z] Floats representing the magnetic intensity of the axis in microteslas (µT)
	accelerometer = sense.get_accelerometer() # accelerometer [pitch, roll, yaw] Floats representing the angle of the axis in degrees.
	return (magnetometer, accelerometer)

def take_picture():
	""" Prend une photographie et l'enregistre dans un nouveau fichier. 
	"""
	get_latitude_longitude() # Set lat/long data in the meta data of the picture
	camera.capture(dir_path+"/image_"+str(picture_ID).zfill(3)+".jpg")
	iss.compute() # mise à jour coordonnés
	picture_ID += 1

def get_latitude_longitude():
	""" Get latitude/longitude and set there in the meta data of the camera 
		Récupérer la position en longitude et latitude de l'ISS afin de l'écrire dans les métadonnées des prises de vues.
	"""
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
	""" Détecter si la luminosité d'une image est suffisante. """
	pass

def draw_area():
	""" Traiter l'image prise par l'astro pi afin d'identifier les sufaces de terre, d'eau et de nuage.

	"""
	sense.get_compass()	# gets the direction of North from the magnetometer in degrees.
	pass

def analyse_picture(img):
	""" Récupérer le % d'eau, de terre, de nuage et de surface x sur l'image traité par draw_area().
		Parcours de l'image pixel par pixel en récupérant le nombres de pixels bleu(eau), vert(terre), blanc(nuage, neige).
	"""
	blue = 0  # Eau
	green = 0 # Terre
	white = 0 # Nuage, Neige
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			r, g, b = im[i, j]
			if b > 200 and r < 50 and g < 50:					# Ecarts à revoir
				blue += 1
			elif b < 50 and r < 50 and g > 200:
				green += 1
			elif b > 200 and r > 200 and g > 200:
				white += 1
	number_pixel = img.shape[0] * img.shape[1]
	percentage_blue = (blue / number_pixel) * 100
	percentage_green = (green / number_pixel) * 100
	percentage_white = (white / number_pixel) * 100

"""
		Finish up the loop
"""

def write_result(water, ground, cloud, magnetometer, accelerometer):
	""" Write data in the CSV file 
		Ecrire les données récupéré durant la boucle sur une nouvelle ligne du fichier CSV.
	"""	
	# ROW, Time_Stamp, Picture_Number, Water, Ground, Cloud, MagX, MagY, MagZ, Acce_Pitch, Acce_Roll, AcceYaw
	logger.info("%s,%s,image_%s.jpg,%s,%s,%s,%s,%s,%s,%s,%s,%s", row_ID, start_loop_time, str(picture_ID).zfill(3), water, ground, cloud, magnetometer[0], magnetometer[1], magnetometer[2], accelerometer[0], accelerometer[1], accelerometer[2])
	row_ID+=1;

def check_time():
	""" Check if the program must be stopped 
		Si le temps d'execution à dépassé la limite : arreter le programme
	"""
	now = int(time.time()) # in second
	# 3h == 10,800 seconds
	if (now - start_time) >= TIME_STOP:
		# Stopper le programme
		loop = False
	else:
		wait()

def wait():
	""" Wait before start again  
		Call by : check_time()
		Attendre que la durée TIME_LOOP se soit écoulé avant de commencer la prochaine boucle.
	"""
	now = time.time()
	if (now - start_loop_time) < TIME_LOOP:
		time.sleep(TIME_LOOP - (now - start_loop_time))


##########################
## in progress

while loop:
	update_matrix(0)
	start_loop_time = time.time()
	magnetometer, accelerometer = get_sensors_value()
	take_picture()

	if not is_night():
		update_matrix(1)
		draw_area()
		analyse_picture()

	update_matrix(2)
	write_result(water, ground, cloud, magnetometer, accelerometer)
	check_time()

##########################
## finish up the program

camera.close()