import os
import numpy as np
import cv2

files = os.listdir("./input")

for file in files:
	path = "./input/"+file
	img = cv2.imread(path)

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
	res2 = res.reshape((img.shape))


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

	def isInGray(bvr):
	    ecart = 10
	    if(bvr[0]<= bvr[1]+ecart and bvr[0]>= bvr[1]-ecart and bvr[0]<= bvr[2]+ecart and bvr[0]>= bvr[2]-ecart and bvr[1]<= bvr[0]+ecart and bvr[1]>= bvr[0]-ecart and bvr[1]<= bvr[2]+ecart and bvr[1]>= bvr[2]-ecart and bvr[2]<= bvr[0]+ecart and bvr[2]>= bvr[0]-ecart and bvr[2]<=bvr[1]+ecart and bvr[2]>= bvr[1]-ecart):
	        return True
	    elif(isInColorRange(bvr,30,0,0,180,30,255)):
	        return True

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
	    
	def isCloud(color,i,o):
	    if(color[i,o]<20):
	        return True
	    else:
	        return False

	hsv = res2#[200:700, 400:800]
	height, width, channels = hsv.shape

	            

	lower_blue = np.array([60,50,20])
	upper_blue = np.array([140,125,110])

	lower_green = np.array([90,100,110])
	upper_green = np.array([130,130,140])

	lower_green2 = np.array([150,170,185])
	upper_green2 = np.array([180,210,220])

	lower_white = np.array([100,125,110])
	upper_white = np.array([255,255,255])



	mask_b = cv2.inRange(hsv, lower_blue, upper_blue)
	hsv[mask_b != 0] = [255,0,0]

	mask_g = cv2.inRange(hsv, lower_green, upper_green)
	hsv[mask_g != 0] = [0,255,0]

	mask_g = cv2.inRange(hsv, lower_green2, upper_green2)
	hsv[mask_g != 0] = [0,255,0]


	mask_w = cv2.inRange(hsv, lower_white, upper_white)
	hsv[mask_w != 0] = [255,255,255]
	    

	image = hsv

	# Algo inplane cloud or bad pixel remover
	exit = True
	decrementer = 0
	oldPix = image[0,0]
	nextPix = image[0,0]
	green = np.array([0,200,0])
	white = np.array([255,255,255])
	blue = np.array([255,0,0])
	for i in range(0,height) :
	    for o in range(0,width) :
	            
	        if(isEgal(image[i,o],green) and isEgal(oldPix,green)==False and isEgal(oldPix,blue)==False):
	            exit = True
	            while exit:
	                decrementer+=1
	                #print("o = " + str(o) + "decrementer = "+ str(decrementer))
	                #print(o-decrementer)
	                # print(decrementer)
	                if(o-decrementer>=0):
	    
	                    if (isEgal(image[i,o-decrementer],green) and checkIfThereAreColorInRangeOfPixel(blue,i,o)):
	                        for u in range (0,decrementer):
	                            image[i,o-u] = green
	                        exit = False
	                    elif(isEgal(image[i,o-decrementer],blue)):
	                        #for u in range (0,decrementer):
	                            #image[i,o-u] = blue
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
	    
	                    if (isEgal(image[i,o-decrementer],blue) and checkIfThereAreColorInRangeOfPixel(green,i,o)):
	                        for u in range (0,decrementer):
	                            image[i,o-u] = blue
	                        exit = False
	                    elif(isEgal(image[i,o-decrementer],green)):
	                        #print("exit")
	                        exit = False
	                else:
	                    #print("test")
	                    exit=False
	        elif(isEgal(image[i,o],green) and isEgal(image[i,o-2],green)==False and isEgal(image[i,o-2],blue)==False):
	            image[i,o-1] = green
	            image[i,o-2]= blue    

	        

	        
	    
	        
	blank_image = np.zeros((height,width,3), np.uint8)

	oldPix = image[0,0]
	Pix = np.array([0,0,0])
	for i in range(0,height-1) :
	    for o in range(0,width-1) :
	        Pix = image[i,o]
	        if((Pix[0]== 255 and Pix[1]==0 and Pix[2]==0) and(oldPix[0]== 0 and oldPix[1]==200 and oldPix[2]==0) or (Pix[0]== 0 and Pix[1]==200 and Pix[2]==0) and(oldPix[0]== 255 and oldPix[1]==0 and oldPix[2]==0) ):
	            blank_image[i,o]= [200,50,10]
	        oldPix = image[i,o]
	            
	for o in range(0,width-1) :
	    for i in range(0,height-1) :      
	        Pix = image[i,o]
	        if((Pix[0]== 255 and Pix[1]==0 and Pix[2]==0) and(oldPix[0]== 0 and oldPix[1]==200 and oldPix[2]==0) or (Pix[0]== 0 and Pix[1]==200 and Pix[2]==0) and(oldPix[0]== 255 and oldPix[1]==0 and oldPix[2]==0) ):
	            blank_image[i,o]= [200,50,10]
	        oldPix = image[i,o]

	cv2.imwrite( "./input/"+file+"_1.jpg", image)
	print(file)