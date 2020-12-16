#Joel Guest Code Lines
#-----------------
#Lines 7-50
#-----------------

#imports libraries
import os, os.path
import cv2
import numpy as np
import matplotlib.pyplot as plt

#Inage directory
path = "/images"

#inmage pool class initialised
class _ImagePool(object):
    def __init__(self):
        
        #initialises 3 reusable objects
        self._reusables = [Reusable() for _ in range(3)]

    #function sets image number and returns the image
    def acquire(self, number):
            img = self._reusables.pop()
            img.setImage(number)
            return img

    #Releases object back into the pool
    def release(self, reusable):
        reusable.reset()
        self._reusables.append(reusable)


#initialises reusable class
class Reusable:
    def __init__(self):
        self._img = None
        
    #Opens the image
    def setImage(self, number):
        imgPath = "images/img_" + str(number) + ".png"
        self._img = cv2.imread(imgPath, 0)

    #Resets the object
    def reset(self):
        self.__img = None
        
    #Returns the image
    def getImage(self):
        return self._img
