#Ben Coxford
#------------
#Lines 27-29
#------------

#Joel Guest
#------------
#Lines 12-51 (excluding 27-29)
#------------

#imports library
import statistics
import sys
import os, os.path
import cv2
import matplotlib.pyplot as plt
import numpy as np

#saves training data to data files
class _TrainData(object):
    def __init__(self):
        self.fileName = "dataFile.txt"
        self.path = "images/"
        self.data = self.getMatch()

    #Writes the image to the directory and sets the name to img_'image number'
    def saveImage(self, image):
        numberOfImg = len(os.listdir(self.path)) #Number of images in the directory
        cv2.imwrite(self.path+"img_"+str(numberOfImg)+".png", image)

    #Appends the number of matches plus one to the file
    def addMatch(self, numberOfMatches):
        file = open(self.fileName, "a")
        file.write(","+str(numberOfMatches+1))
        file.close()
        
    #Reads the file and seperates the number of matches
    def getMatch(self):
        file = open(self.fileName, "r")
        self.data = file.readline().split(",")
        file.close()
        self.data = [int(i) for i in self.data]
        return self.data
    
    #Gets the average number of matc hes from the file and returns value
    def getMean(self):
        self.data = self.getMatch()
        if(self.data):
            mean = statistics.mean(self.data)
            return mean
        return False
    
        
