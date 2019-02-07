# -*- coding: utf-8 -*
"""
	SPACETHON Team - AstroPI contest
		2018-2019
	
	Authors: GAZEAU Lucas, RACAUD Simon
	
	---
	# tag debug: !!remove!!
    Debug: 	* ok - 	Voir comptage pixel bleu/vert apres suppression des nuages.
			* Définir les constantes TIME_LOOP=20s et TIME_STOP=10660s
            * ok -	Rognage image
"""

import os
import time

import logging
import logzero
from logzero import logger
import numpy as np
import cv2
import ephem

from sense_hat import SenseHat
from picamera import PiCamera


""" 
		Global variables/constants
"""
### CONSTANTS
DIR_PATH = os.path.dirname(os.path.realpath(__file__)) # path of the program
TIME_LOOP = 30 # duration of a loop
TIME_STOP = 000 # duration from which the program must stop

### VARIABLES
loop = True
picture_ID = 0 # Picture number (for the picture name)
row_ID = 1 # Row number (csv file)
start_program_time = int(time.time()) # timestamp when the program has started (in second)
start_loop_time = 0 # timestamp when the loop has started

###############
### FOR OPENCV
green = np.array([0,255,0])
white = np.array([255,255,255])
blue = np.array([255,0,0])
# Initialisation of the interval between the color
lower_blue = np.array([60,50,20])
upper_blue = np.array([160,130,110])

lower_green = np.array([70,70,70])
upper_green = np.array([155,145,145])

lower_green2 = np.array([130,145,160])
upper_green2 = np.array([155,160,175])

lower_white = np.array([140,125,110])
upper_white = np.array([205,200,200])


lower_white2 = np.array([210,210,210])
upper_white2 = np.array([255,255,255])

lower_green3 = np.array([170,200,210])
upper_green3 = np.array([200,235,240])

lower_green4 = np.array([90,85,84])
upper_green4 = np.array([110,110,110])

""" 
		Init and Config library
"""
### CAMERA
camera = PiCamera()

### SENSEHAT
sense = SenseHat()
sense.set_imu_config(True, False, False) # (compass_enabled, gyro_disabled, accel_disabled)

##	Matrix led
# Colors
g = [0,50,0]
r = [50,0,0]
b = [0,0,50]
o = [0,0,0]
# Define simple images
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
img2 = [
    r,r,r,r,r,r,r,r,
    o,r,o,o,o,o,r,o,
    o,o,r,o,o,r,o,o,
    o,o,o,r,r,o,o,o,
    o,o,o,r,r,o,o,o,
    o,o,r,r,r,r,o,o,
    o,r,r,r,r,r,r,o,
    r,r,r,r,r,r,r,r,
]
img3 = [
    b,b,b,b,b,b,b,b,
    o,b,o,o,o,o,b,o,
    o,o,b,o,o,b,o,o,
    o,o,o,b,b,o,o,o,
    o,o,o,b,b,o,o,o,
    o,o,b,b,b,b,o,o,
    o,b,b,b,b,b,b,o,
    b,b,b,b,b,b,b,b,
]

### Logfile parameters
logzero.logfile(DIR_PATH+"/data01.csv") # Create the CSV file

# Set a custom formatter and insert the first line.
formatter = logging.Formatter('[%(asctime)s] :%(message)s') # !!remove!!
logzero.formatter(formatter) # !!remove!!
logger.info(",ROW,Time_Stamp,Picture_Number,Water,Ground,Cloud,MagX,MagY,MagZ,Longitude,Latitude")

### Config ephem (A REMPLACER !!!!)
name = "ISS (ZARYA)"
line1 = "1 25544U 98067A   18362.36563081 -.00011736  00000-0 -17302-3 0  9998"
line2 = "2 25544  51.6377 131.0297 0002747 209.2490 215.4464 15.53700691148714"
# source : http://www.celestrak.com/NORAD/elements/stations.txt
iss = ephem.readtle(name, line1, line2)
iss.compute()

"""
		# FUNCTION #
"""

def update_matrix(state):
    """ Update the image displayed by the matrix led """
    if state == 0:
        sense.set_pixels(img1)
    elif state == 1:
        sense.set_pixels(img2)
    elif state == 2:
        sense.set_pixels(img3)
    else:
        sense.set_pixels(img1)
        sense.set_rotation(180)

def get_sensors_value():
	""" Get the value of the magnetometer (at the beginning of the loop) """
	magnetometer = sense.get_compass_raw() # magnetometer [x, y, z] Floats representing the magnetic intensity of the axis in microteslas (µT)
	angleNorth = sense.get_compass() # Angle in degree
	return (magnetometer, angleNorth)

def take_picture(picture_ID):
	""" Take two pictures and save they in a new file """
	# First image : with high resolution
	picture_ID += 1
	camera.resolution = (2592,1944)
	imageName1 = "image_"+str(picture_ID).zfill(3)+".jpg";
	camera.capture(DIR_PATH+"/"+imageName1)
	# Second image : with low resolution for opencv
	picture_ID += 1
	camera.resolution = (320,240)
	imageName2 = "image_"+str(picture_ID).zfill(3)+".jpg";
	camera.capture(DIR_PATH+"/"+imageName2)

	return (imageName1, imageName2)

def get_latitude_longitude():
    """ Get the location (latitude/longitude) """
    iss.compute()
    return (iss.sublong, iss.sublat)


""" ##############################################
	##	OPENCV
"""

### opencv_analysis() => subfunctions

def isInColorRange(bvr,bvr1,bvr2):
    """ This function will check if the pixel is in the range """
    if(bvr[0]<=bvr2[0] and bvr[0]>=bvr1[0] and bvr[1]<=bvr2[1] and bvr[1]>=bvr1[1] and bvr[2]<=bvr2[2] and bvr[2]>=bvr1[2]):
        return True
    else:
        return False
      
def isEgal(bvr1,bvr2):
    """ This function will verify the equality of the color between 2 pixel """
    if(bvr1[0] == bvr2[0] and bvr1[1] == bvr2[1] and bvr1[2] == bvr2[2]):
        return True
    else:
        return False

def checkIfThereAreColorInRangeOfPixel(color,i,o, image, height, width):
    """ This function will check if there a color around a pixel """
    for y in range(0,10):
        if(i+y < height):
            if(isEgal(image[i+y,o],color)):
                return False
            if(isEgal(image[i-y,o],color)):
                return False
        if(o+y < width):
            if(isEgal(image[i,o+y],color)):
                return False        
            if(isEgal(image[i,o-y],color)):
                return False   
    return True

###

def opencv_analysis(imageName):
    """ Traiter l'image prise par l'astro pi afin d'identifier les surfaces de terre, d'eau et de nuage.
		Process the picture to identify the area (ground, water, cloud)
    """
    image = cv2.imread(DIR_PATH+"/"+imageName)

    ## Treatment of the image
    height, width, channels = image.shape
    image = image[0:height, 84:width-96]
    exit = True
    counter = 0
    oldPix = image[0,0]
    nextPix = image[0,0]

    height, width, channels = image.shape
    imagePixSize = height*width
                
    # Main Algorithm
    counterBlackPixel= 0
    isItTheNight = False

    # Check if the pixel is in a rage and will change his color consequently
    print("02.5: PHASE 1") # debug : !!remove!!
    blue_pixel = 0
    green_pixel = 0
    white_pixel = 0
    for i in range(0,height):
        for o in range(0,width):
            if(counterBlackPixel>= imagePixSize/2):
                print("It's the night !") # debug : !!remove!!
                isItTheNight = False
                return 0 ## Analyse impossible, Fin de la fonction
                #break
            if(isInColorRange(image[i,o],lower_white,upper_white)):
                #image[i,o] = [255,255,255]
                white_pixel += 1
            elif(isInColorRange(image[i,o],lower_green,upper_green)):
                #image[i,o] = [0,255,0]
                green_pixel += 1
            elif(isInColorRange(image[i,o],lower_green2,upper_green2)):
                #image[i,o] = [0,255,0]
                green_pixel += 1
            elif(isInColorRange(image[i,o],lower_blue,upper_blue)):
                #image[i,o] = [255,0,0]
                blue_pixel += 1
            elif(isInColorRange(image[i,o],lower_green3,upper_green3)):
                #image[i,o] = [0,255,0]
                green_pixel += 1
            elif(isInColorRange(image[i,o],lower_white2,upper_white2)):
                #image[i,o] = [255,255,255]
                white_pixel += 1
            elif(isInColorRange(image[i,o],[0,0,0],[60,50,20])):
                counterBlackPixel+=1
                   
        # This algorithm will remove the cloud or the non threat pixel in the ocean or in a plane.
            
            if(isEgal(image[i,o],green) and isEgal(oldPix,green)==False and isEgal(oldPix,blue)==False):
                exit = True
                while exit:
                    counter+=1
                    if(o-counter>=0):
                        if (isEgal(image[i,o-counter],green) and checkIfThereAreColorInRangeOfPixel(blue,i,o, image, height, width)):
                            #for u in range (0,counter):
                                #image[i,o-u] = green
                            green_pixel += counter
                            exit = False
                        elif(isEgal(image[i,o-counter],blue)):
                            exit = False
                    else:
                        exit=False
                            
                counter = 0
            elif(isEgal(image[i,o],blue) and isEgal(oldPix,green)==False and isEgal(oldPix,blue)==False):
                exit = True
                while exit:
                    counter+=1
                    if(o-counter>=0):
                        if (isEgal(image[i,o-counter],blue) and checkIfThereAreColorInRangeOfPixel(green,i,o, image, height, width)):
                            #for u in range (0,counter):
                                #image[i,o-u] = blue
                            blue_pixel += counter
                            exit = False
                        elif(isEgal(image[i,o-counter],green)):
                            exit = False
                    else:
                        exit=False
            elif(isEgal(image[i,o],green) and isEgal(image[i,o-2],green)==False and isEgal(image[i,o-2],blue)==False):
                image[i,o-1] = green
                image[i,o-2] = blue 
                green_pixel += 1
                blue_pixel += 1       

    print("02.5: PHASE 2") # debug : !!remove!!

    # Save the result (!!! debug !!! ) !!remove!!
    cv2.imwrite(DIR_PATH+"/cv_"+imageName, image)

    # Calculate the percentage of water, cloud and ground in the image
    number_pixel = height * width
    percentage_blue = round((blue_pixel / number_pixel) * 100, 3)
    percentage_green = round((green_pixel / number_pixel) * 100, 3)
    percentage_white = round((white_pixel / number_pixel) * 100, 3)
    
    print("\nPercentage %B %G %W") # !!remove!!
    print(percentage_blue)
    print(percentage_green)
    print(percentage_white) 
    #
    return (percentage_blue, percentage_green, percentage_white)

"""
		Finish up the loop
"""

def write_result(row_ID, imageName, water, ground, cloud, magnetometer, angleNorth, location):
	""" Write data in the CSV file """	
	# ROW, Time_Stamp, formatedTime, Picture_Name, %Water, %Ground, %Cloud, MagX, MagY, MagZ, angleNorth, longitude, latitude
	logger.info(",%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s", row_ID, start_loop_time, time.asctime(time.localtime(start_loop_time)), imageName, water, ground, cloud, magnetometer["x"], magnetometer["y"], magnetometer["z"], angleNorth, location[0], location[1])
	row_ID+=1;

def check_time(start_time):
	""" Check if the program must be stopped """
	now = int(time.time()) # current time in second

	if (now - start_time) >= TIME_STOP:
		# Stop the program
		loop = False
	else:
		wait()

def wait():
	""" Wait before start a new loop again  
		Call by : check_time()
		Wait that the duration TIME_LOOP is pass before to start a new loop
	"""
	now = time.time()
	if (now - start_loop_time) < TIME_LOOP:
		time.sleep(TIME_LOOP - (now - start_loop_time))


##########################
## in progress

while loop:
    print("01: START") # debug : !!remove!!
    update_matrix(0)
    start_loop_time = time.time()
    magnetometer, angleNorth = get_sensors_value()
    nameImage = take_picture(picture_ID)
    location = get_latitude_longitude()

	# OpenCV
    print("02: OPENCV") # debug : !!remove!!
    update_matrix(1)
    result = opencv_analysis(nameImage[1])

    # Write the results in a loop
    print("03: FINISH") # debug : !!remove!!
    update_matrix(2)

    if result != 0:
        write_result(row_ID, nameImage[1], result[0], result[1], result[2], magnetometer, angleNorth, location)
    else:
        write_result(row_ID, nameImage[1], 0, 0, 0, magnetometer, angleNorth, location) # During the night

    print(time.time() - start_loop_time) # !!remove!!

    check_time(start_loop_time) # Check if the three hours are almost up.

##########################
## finish up the program

camera.close()
