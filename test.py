import cv2
import numpy as np
from matplotlib import pyplot as plt


def deletePix(b1,v1,r1,b2,v2,r2):
    lower = np.array([b1,v1,r1])
    upper = np.array([b2,v2,r2])
    mask = cv2.inRange(hsv, lower, upper)
    image[mask != 0] = [255,0,0]
    hsv[mask != 0] = [255,0,0]

def isInColorRange(bvr,b1,v1,r1,b2,v2,r2):
    if(bvr[0]<=b2 and bvr[0]>=b1 and bvr[1]<=v2 and bvr[1]>=v1 and bvr[2]<=r2 and bvr[2]>=r1):
        return True
    else :
        return False
        
def isEgal(bvr1,bvr2):
    if(bvr1[0] == bvr2[0] and bvr1[1] == bvr2[1] and bvr1[2] == bvr2[2]):
        return True
    else:
        return False
    

image = cv2.imread("amerique.jpg")


# define range of blue color in HSV
lower_green = np.array([0,8,5])
upper_green = np.array([90, 255, 255])

lower_blue = np.array([70,50,0])
upper_blue = np.array([242,255,200])

lower_white = np.array([30,0,0])
upper_white = np.array([180,30,255])

upper_black = np.array([50,70,30])
lower_black = np.array([0,0,0])



# Convert BGR to HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    


# Threshold the HSV image to get only blue colors
deletePix(65,60,80,115,115,110)

mask_g = cv2.inRange(hsv, lower_green, upper_green)
image[mask_g != 0] = [0,200,0]
hsv[mask_g != 0] = [0,200,0]

mask_b = cv2.inRange(hsv, lower_blue, upper_blue)
image[mask_b != 0] = [255,0,0]
hsv[mask_b != 0] = [255,0,0]

mask_w = cv2.inRange(hsv, lower_white, upper_white)
image[mask_w != 0] = [255,255,255]
hsv[mask_w != 0] = [255,255,255]



# Algo inplane cloud or bad pixel remover
height, width, channels = image.shape
exit = True
decrementer = 0
oldPix = image[0,0]
nextPix = image[0,0]
green = np.array([0,200,0])
white = np.array([255,255,255])
blue = np.array([255,0,0])
for i in range(0,height) :
    for o in range(0,width) :
        #if(isInColorRange(image[i,o],0,150,0,50,200,50) and ((isInColorRange(oldPix,0,150,0,50,200,50)==False) or (isInColorRange(oldPix,200,0,0,255,30,30)==False))):
        
        if(isEgal(image[i,o],green) and isEgal(oldPix,green)==False and isEgal(oldPix,blue)==False):
            exit = True
            while exit:
                decrementer+=1
                #print("o = " + str(o) + "decrementer = "+ str(decrementer))
                #print(o-decrementer)
               # print(decrementer)
                if(o-decrementer>=0):

                    if (isEgal(image[i,o-decrementer],green)):
                        for u in range (0,decrementer):
                            image[i,o-u] = green
                        exit = False
                    elif(isEgal(image[i,o-decrementer],blue)):
                        for u in range (0,decrementer):
                            image[i,o-u] = blue
                        exit = False
                else:
                    #print("test")
                    exit=False
                    
            decrementer = 0
        elif(isEgal(image[i,o],blue) and isEgal(oldPix,green)==False and isEgal(oldPix,blue)==False):
            exit = True
            while exit:
                decrementer+=1
                #print("o = " + str(o) + "decrementer = "+ str(decrementer))
                #print(o-decrementer)
                #print(decrementer)
                if(o-decrementer>=0):

                    if (isEgal(image[i,o-decrementer],blue)  or o-decrementer == 0):
                        for u in range (0,decrementer):
                            image[i,o-u] = blue
                        exit = False
                    elif(isEgal(image[i,o-decrementer],green)):
                        #print("exit")
                        exit = False
                else:
                    #print("test")
                    exit=False
                    
        oldPix = image[i,o]
        decrementer = 0
        


#Coast cleaner algo

for i in range(0,height-1) :
    for o in range(0,width-1) :

        if(o <width):
            nextPix = image[i,o+1]

            if(isEgal(image[i,o],green) and isEgal(nextPix,green)==False and isEgal(nextPix,blue)==False):
                exit = True
                while exit:
                    decrementer+=1
                    #print("o = " + str(o) + "decrementer = "+ str(decrementer))
                    #print(o-decrementer)
                # print(decrementer)
                    if(o+decrementer<=width-1):
                        if (isEgal(image[i,o+decrementer],green)):
                            for u in range (0,decrementer):
                                image[i,o+u] = green
                            exit = False
                        elif(isEgal(image[i,o+decrementer],blue)):
                            for u in range (0,decrementer):
                                image[i,o+u] = blue
                            exit = False
                    else:
                        #print("test")
                        exit=False
                    
                decrementer = 0
            elif(isEgal(image[i,o],blue) and isEgal(nextPix,green)==False and isEgal(nextPix,blue)==False):
                exit = True
                while exit:
                    decrementer+=1
                    #print("o = " + str(o) + "decrementer = "+ str(decrementer))
                    #print(o-decrementer)
                    #print(decrementer)
                    if(o+decrementer<=width-1):

                        if (isEgal(image[i,o+decrementer],blue) or o+decrementer== width-1):
                            for u in range (0,decrementer):
                                image[i,o+u] = blue
                            exit = False
                        elif(isEgal(image[i,o+decrementer],green)):
                            #print("exit")
                            exit = False
                    else:
                        #print("test")
                        exit=False
        else:
            break            
        decrementer = 0




blank_image = np.zeros((height,width,3), np.uint8)
oldPix = image[0,0]
Pix = np.array([0,0,0])
for i in range(0,height-1) :
    for o in range(0,width-1) :
        Pix = image[i,o]
        if((Pix[0]== 255 and Pix[1]==0 and Pix[2]==0) and(oldPix[0]== 0 and oldPix[1]==200 and oldPix[2]==0) or (Pix[0]== 0 and Pix[1]==200 and Pix[2]==0) and(oldPix[0]== 255 and oldPix[1]==0 and oldPix[2]==0) ):
           blank_image[i,o]= [200,50,10]
        oldPix = image[i,o]




cv2.imshow("result", blank_image)
cv2.imshow("resultat", image)

cv2.imwrite( "result_mercator-projection.jpg", image);
cv2.imwrite("test.jpg", blank_image)
#cv2.imwrite( "result/result_green.jpg", res_b);
#cv2.imwrite( "result/result_white.jpg", res_w);

cv2.waitKey(0)
cv2.destroyAllWindows()