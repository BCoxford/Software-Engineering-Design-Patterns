#Ben Coxford
#------------
#Lines 6-34
#------------

#Import frameworks and libraries
import cv2
import matplotlib.pyplot as plt
import numpy as np
import statistics 
import sys
import os, os.path

class _Camera(object): #Camera subsystem (2 subsystems created)
    def __init__(self, cameraNumber):
        #Initialise cameras instance variables
        self.camera = None
        self.cameraNumber = cameraNumber
        self.focus = 80
        self.ret = None
        self.img = None

    def start(self):
        #Start the video capture and set the focus
        self.camera = cv2.VideoCapture(self.cameraNumber)
        self.camera.set(cv2.CAP_PROP_FOCUS, self.focus)

    def adjustFocus(self, focus):
        #Adjust the focus
        self.focus = focus
        self.camera.set(cv2.CAP_PROP_FOCUS, self.focus)

    def readImg(self):
        #Read the current frame as an image
        self.ret, self.img = self.camera.read()
        return self.ret, self.img

    def stop(self):
        #Stop the and release the camera
        self.camera.release()
