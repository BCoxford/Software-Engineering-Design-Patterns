#Ben Coxford
#------------
#Lines 8-40
#------------

#Used for testing the UVLightBox Feature

import cv2
import matplotlib.pyplot as plt
import numpy as np
import statistics 
import sys
import os, os.path

#Creates a camera with a live feed to simulate the ID Camera
camera1 = cv2.VideoCapture(0)
focus = 80
camera1.set(cv2.CAP_PROP_FOCUS, focus)
cv2.namedWindow("preview", cv2.WINDOW_NORMAL)

result = None

while 1:
        #Reads the image
        ret0, img0 = camera1.read()
        if (ret0):
            #Converts it to grayscale
            gray0 = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
            
            #Returns the binary threshold of the image (black and white)
            ret0, result = cv2.threshold(gray0,60,255,cv2.THRESH_BINARY)

            #Displays the image to the preview
            cv2.imshow("preview", result)

        #Terminates when the space bar is pressed and releases the camera.
        k = cv2.waitKey(30) & 0xff
        if k == 32:
            break
            camera1.release()
