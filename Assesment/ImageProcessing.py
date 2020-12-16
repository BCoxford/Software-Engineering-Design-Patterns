#Ben Coxford
#------------
#Lines 6-27
#------------

import cv2
import matplotlib.pyplot as plt
import numpy as np
import statistics 
import sys
import os, os.path

class _ImageProcessing(object):

    def __init__(self):
        self.lastImg = None;

    #Converts the image to its grayscale version and returns the image
    def convertToGrayScale(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.lastImg = img
        return img

    #Converts the image to its black and white binary self using the binary thresholding
    #This produced better results that that of otsu's thresholding
    def convertToBinary(self, img):
        return cv2.threshold(img,60,255,cv2.THRESH_BINARY)
