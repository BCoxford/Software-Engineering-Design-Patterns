#Ben Coxford
#------------
#Lines 7-31
#------------

#Import frameworks and libraries
import cv2
import matplotlib.pyplot as plt
import numpy as np
import sys
import os, os.path

class _FeatureMatching(object):

    def __init__(self):
        self.matches = 0;

    #Match the images and produce a number
    def Match(self, img1, img2):
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        sift = cv2.xfeatures2d.SIFT_create() #Sift descriptor

        #Detect and calculate the matches
        kp1, des1 = sift.detectAndCompute(img1,None)
        kp2, des2 = sift.detectAndCompute(img2,None)
        bf = cv2.BFMatcher() #Brute force method
        matches = bf.knnMatch(des1,des2, k=2)
        self.matches = len(matches) #Set the number of matches

    def getMatch(self): #Return the number of matches
        return self.matches
