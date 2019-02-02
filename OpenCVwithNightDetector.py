import numpy as np
import cv2

img = cv2.imread('Test/night.jpg')
##OpenCV Quantization Color

Z = img.reshape((-1,3))

# convert to np.float32
Z = np.float32(Z)

# define criteria, number of clusters(K) and apply kmeans()
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 32
ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

# Now convert back into uint8, and make original image
center = np.uint8(center)
res = center[label.flatten()]
image = res.reshape((img.shape))

##Treatment of the image

height, width, channels = image.shape
image = image[0:height, 140:530]
exit = True
counter = 0
oldPix = image[0,0]
nextPix = image[0,0]
green = np.array([0,255,0])
white = np.array([255,255,255])
blue = np.array([255,0,0])


#initialisation function

#this function will check if the pixel is in the range
def isInColorRange(bvr,bvr1,bvr2):
    if(bvr[0]<=bvr2[0] and bvr[0]>=bvr1[0] and bvr[1]<=bvr2[1] and bvr[1]>=bvr1[1] and bvr[2]<=bvr2[2] and bvr[2]>=bvr1[2]):
        return True
    else :
        return False


#This function will verify the equality of the color between 2 pixel        
def isEgal(bvr1,bvr2):
    if(bvr1[0] == bvr2[0] and bvr1[1] == bvr2[1] and bvr1[2] == bvr2[2]):
        return True
    else:
        return False

#this function will check if there a color around a pixel
def checkIfThereAreColorInRangeOfPixel(color,i,o):
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
    

    
height, width, channels = image.shape
imagePixSize = height*width
            
# initialisation of the interval between the color
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

# Main Algorithm
counterBlackPixel= 0
isItTheNight = False
#check if the pixel is in a rage and will change his color consequently
for i in range(0,height):
    for o in range(0,width):
        if(counterBlackPixel>= imagePixSize/2):
            print("It's the night !")
            isItTheNight = False
            break
        if(isInColorRange(image[i,o],lower_white,upper_white)):
            image[i,o] = [255,255,255]
        
        elif(isInColorRange(image[i,o],lower_green,upper_green)):
            image[i,o] = [0,255,0]
            
        elif(isInColorRange(image[i,o],lower_green2,upper_green2)):
            image[i,o] = [0,255,0]
           
        elif(isInColorRange(image[i,o],lower_blue,upper_blue)):
            image[i,o] = [255,0,0]
            
        elif(isInColorRange(image[i,o],lower_green3,upper_green3)):
            image[i,o] = [0,255,0]
        
        elif(isInColorRange(image[i,o],lower_white2,upper_white2)):
            image[i,o] = [255,255,255]
        elif(isInColorRange(image[i,o],[0,0,0],[60,50,20])):
            counterBlackPixel+=1
            
        
#this algorithm will remove the cloud or the non threat pixel in the ocean or in a plane.
        
        if(isEgal(image[i,o],green) and isEgal(oldPix,green)==False and isEgal(oldPix,blue)==False):
            exit = True
            while exit:
                counter+=1
                if(o-counter>=0):
    
                    if (isEgal(image[i,o-counter],green) and checkIfThereAreColorInRangeOfPixel(blue,i,o)):
                        for u in range (0,counter):
                            image[i,o-u] = green
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
    
                    if (isEgal(image[i,o-counter],blue) and checkIfThereAreColorInRangeOfPixel(green,i,o)):
                        for u in range (0,counter):
                            image[i,o-u] = blue
                        exit = False
                    elif(isEgal(image[i,o-counter],green)):
                        exit = False
                else:
                    exit=False
        elif(isEgal(image[i,o],green) and isEgal(image[i,o-2],green)==False and isEgal(image[i,o-2],blue)==False):
            image[i,o-1] = green
            image[i,o-2]= blue        



    
#This part will detect the coast between the blue and the green
blank_image = np.zeros((height,width,3), np.uint8)

oldPix = image[0,0]
Pix = np.array([0,0,0])
for i in range(0,height-1) :
    for o in range(0,width-1) :
        Pix = image[i,o]
        if((Pix[0]== 255 and Pix[1]==0 and Pix[2]==0) and(oldPix[0]== 0 and oldPix[1]==255 and oldPix[2]==0) or (Pix[0]== 0 and Pix[1]==255 and Pix[2]==0) and(oldPix[0]== 255 and oldPix[1]==0 and oldPix[2]==0) ):
            blank_image[i,o]= [200,50,10]
        oldPix = image[i,o]
            
for o in range(0,width-1) :
    for i in range(0,height-1) :      
        Pix = image[i,o]
        if((Pix[0]== 255 and Pix[1]==0 and Pix[2]==0) and(oldPix[0]== 0 and oldPix[1]==255 and oldPix[2]==0) or (Pix[0]== 0 and Pix[1]==255 and Pix[2]==0) and(oldPix[0]== 255 and oldPix[1]==0 and oldPix[2]==0) ):
            blank_image[i,o]= [200,50,10]
        oldPix = image[i,o]

#Show the result and save it 
cv2.imshow('res2',image)
cv2.imshow("Coast",blank_image)
cv2.waitKey(0)
cv2.destroyAllWindows()