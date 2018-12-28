import cv2 
import numpy as np 

img = cv2.imread('input/france.jpg',0) 
rows,cols = img.shape 

print(rows, cols)
"""
for i in range(rows): 
    for j in range(cols): 
     k = x[i,j] 
     print k 
"""
while i < rows:
	while j < cols:
		R = image[i, j][0]
		j+=2
	i+=2