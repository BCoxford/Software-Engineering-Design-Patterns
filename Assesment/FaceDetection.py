#Ben Coxford
#------------
#Lines 7-47
#------------

#Import the frameworks and libraries
import cv2
import matplotlib.pyplot as plt
import numpy as np
import statistics 
import sys
import os, os.path
import face_recognition

class _FaceDetection(object):

    #Initialise the face detection object variables
    def __init__(self):
        self.minSize = 250; #Minimum size in pixels for a face to be detected. (Avoids smaller object being recognised)
        self.faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)

    def compareFaces(self, img1, img2):
        try:
            #Try to compare and match the faces on the two images
            encodedImage0 = face_recognition.face_encodings(img1)[0]
            encodedImage1 = face_recognition.face_encodings(img2)[0]
            result = face_recognition.compare_faces([encodedImage0], encodedImage1)
            return result[0] #Return the result
        except: #If error return -1
            return -1

    def detectSingleFace(self, img, minSize):
        #Detect a single face and return true or false if so.
        face = self.faceCascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5,minSize=(minSize, minSize),flags=cv2.CASCADE_SCALE_IMAGE)
        numberFace = len(face) #Number of faces
        if(numberFace==1):
            return True
        else:
            return False

    def rectangleFaceDetect(self, img, minSize):
        #For testing purposes, this function places a green rectangle around the faces of an image.
        face = self.faceCascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5,minSize=(minSize, minSize),flags=cv2.CASCADE_SCALE_IMAGE)
        for (x, y, w, h) in face:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        return img
