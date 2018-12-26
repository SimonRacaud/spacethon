import cv2
import numpy as np
from matplotlib import pyplot as plt
import colorsys


image = cv2.imread("france.jpg")


# define range of blue color in HSV
lower_green = np.array([0,8,5])
upper_green = np.array([90, 255, 255])

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

upper_black = np.array([50,50,50])
lower_black = np.array([0,0,0])



# Convert BGR to HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    


# Threshold the HSV image to get only blue colors
mask_black = cv2.inRange(hsv, lower_black, upper_black)
image[mask_black != 0] = [0,200,0]
hsv[mask_black != 0] = [0,200,0]


mask_g = cv2.inRange(hsv, lower_green, upper_green)
image[mask_g != 0] = [0,200,0]
hsv[mask_g != 0] = [0,200,0]

mask_b = cv2.inRange(hsv, lower_blue, upper_blue)
image[mask_b != 0] = [255,0,0]
hsv[mask_b != 0] = [255,0,0]

mask_w = cv2.inRange(hsv, lower_white, upper_white)
image[mask_w != 0] = [255,255,255]
hsv[mask_w != 0] = [255,255,255]


blank_image = np.zeros((480,633,3), np.uint8)
oldPix = image[0,0]
Pix = np.array([0,0,0])
for i in range(0,479) :
    for o in range(0,632) :
        Pix = image[i,o]
        if((Pix[0]== 255 and Pix[1]==0 and Pix[2]==0) and(oldPix[0]== 0 and oldPix[1]==200 and oldPix[2]==0) or (Pix[0]== 0 and Pix[1]==200 and Pix[2]==0) and(oldPix[0]== 255 and oldPix[1]==0 and oldPix[2]==0) or (Pix[0]== 0 and Pix[1]==200 and Pix[2]==0 and oldPix[0]== 255 and oldPix[1]==255 and oldPix[2]==255)):
           blank_image[i,o]= [200,50,10]
        oldPix = image[i,o]



# Bitwise-AND mask and original image

#res_w = cv2.bitwise_and(image,image, mask=mask_w)

#res_b = cv2.bitwise_and(image, image, mask= mask_b)
#res_g = cv2.bitwise_and(image, image, mask= mask_g)


cv2.imshow("result", blank_image)
#cv2.imshow("result", res)

cv2.imwrite( "result_mercator-projection.jpg", image);
cv2.imwrite("test.jpg", blank_image)
#cv2.imwrite( "result/result_green.jpg", res_b);
#cv2.imwrite( "result/result_white.jpg", res_w);

cv2.waitKey(0)
cv2.destroyAllWindows()