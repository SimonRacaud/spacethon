import cv2
import numpy as np
from matplotlib import pyplot as plt
import colorsys


image = cv2.imread("mercator-projection.jpg")

# define range of blue color in HSV
lower_green = np.array([0,8,5])
upper_green = np.array([80, 255, 255])

lower_blue = np.array([90,60,0])
upper_blue = np.array([130,255,200])

"""
lower_white = np.array([30,0,90])
upper_white = np.array([180,30,255])

lower_white = np.array([30,0,90])
upper_white = np.array([180,8,255])
"""
lower_white = np.array([30,0,0])
upper_white = np.array([180,30,255])

# Convert BGR to HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

 # Threshold the HSV image to get only blue colors
mask_b = cv2.inRange(hsv, lower_blue, upper_blue)
image[mask_b != 0] = [255,0,0]

mask_w = cv2.inRange(hsv, lower_white, upper_white)
image[mask_w != 0] = [255,255,255]

mask_g = cv2.inRange(hsv, lower_green, upper_green)
image[mask_g != 0] = [0,200,0]

# Bitwise-AND mask and original image

res_w = cv2.bitwise_and(image,image, mask=mask_w)

res_b = cv2.bitwise_and(image, image, mask= mask_b)
res_g = cv2.bitwise_and(image, image, mask= mask_g)

cv2.imshow("result", image)
#cv2.imshow("result", res)

cv2.imwrite( "result/result_mercator-projection.jpg", image);
#cv2.imwrite( "result/result_green.jpg", res_b);
#cv2.imwrite( "result/result_white.jpg", res_w);

cv2.waitKey(0)
cv2.destroyAllWindows()