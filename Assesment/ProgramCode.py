#Ben Coxford Code Lines
#-----------------
#Lines 14-212 (excluding joel's code lines 51, 108-127, 164-188)
#-----------------


#Joel Guest Code Lines
#-----------------
#Lines 51, 108-127, 164-188
#-----------------


#Import all relevant frameworks and classes
import cv2 #Image Processing Library
import matplotlib.pyplot as plt
import numpy as np
import statistics 
import sys
import os, os.path
import face_recognition #Face matching library
import pytesseract #Text detection library
import datetime

#Subsystem Classes
import DateValidation
import Camera
import ImageProcessing
import FaceDetection
import FeatureMatching
import ImagePool
import TrainingClass

class IDSystem(): #System
    def __init__(self):
        #Initiate system and subsystems
        self.__Camera_1 = Camera._Camera(1)
        self.__Camera_2 = Camera._Camera(0)
        self.__FaceDetection = FaceDetection._FaceDetection()
        self.__FeatureMatching = FeatureMatching._FeatureMatching()
        self.__ImageProcessing = ImageProcessing._ImageProcessing()
        self.__DateValidation = DateValidation._DateValidation()
        self.__ImagePool = ImagePool._ImagePool()
        self.__Training = TrainingClass._TrainData()

        #Pipeline passes
        self.passA = -1
        self.passB = -1
        self.passC = -1

        #Indicator when button pressed
        self.turnt = False

        #Date boolean checks
        self.ValidDOB = False
        self.ValidIssue = False
        self.ValidExpiry = False

        #ID Verification check
        self.ImagePass = False

    #Start the system
    def startSystem(self):
        cv2.namedWindow("preview", cv2.WINDOW_NORMAL) #Create a new window named preview
        cv2.setWindowProperty('preview', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN) #Set to fullscreen

        self.__Camera_1.start() #Initialise camera 1
        self.__Camera_2.start() #Initialise camera 2

        #Loop until the algorithm breaks
        while(True):
            retCustomer, frameCustomer = self.__Camera_1.readImg() #Read image of customers view
            retID, frameID = self.__Camera_2.readImg() #Read image of ID

            if(retCustomer and retID): #If the images are accepted
                
                #Pipeline test 1 = match face
                if(self.passA == -1):

                    #Detect if there is one face on both the ID and customer view 
                    error = self.__FaceDetection.detectSingleFace(frameID, 300)
                    error2 = self.__FaceDetection.detectSingleFace(frameCustomer, 300)

                    #If there is one face detected
                    if(error != False and error2 != False):
                        result = self.__FaceDetection.compareFaces(frameCustomer, frameID) #Compare faces and return the result
                        if(result == True): #If the faces match
                            self.passA = True
                        elif(result == False): #If the faces do match
                            self.passA = False

                #Pipeline test 2 = test dates
                if(self.passB == -1):
                    ret, image = self.__ImageProcessing.convertToBinary(frameID)
                    self.validDOB, self.validIssue, self.validExpiry = self.__DateValidation.readText(image)
                    if(self.validDOB != False):
                        self.passB = True

                #Pipeline test 3 = test UV light
                if(self.passB != -1 and self.passA != -1 and self.turnt == True):
                    if(self.passC == -1):
                        #Convert image to grayscale and then to binary
                        grayID = self.__ImageProcessing.convertToGrayScale(frameID)
                        binaryID = self.__ImageProcessing.convertToBinary(grayID)

                        #From tuple get the binary data
                        binaryImage = binaryID[1]

                        matches = [] #List of match counts

                        #Number of images in the directory.
                        numberOfImg = len(os.listdir("images/"))

                        #loops from 1 to number of image
                        for i in range(1,numberOfImg):
                            #retrievs an object from the object pool
                            img = self.__ImagePool.acquire(i)
                            image = img.getImage()

                            #matches the features of both images
                            self.__FeatureMatching.Match(binaryImage, image)
                            match = self.__FeatureMatching.getMatch()

                            #Append the number of matches to the list of match counts
                            matches.append(match)

                            #Releases object back to the object pool
                            self.__ImagePool.release(img)

                        matchList = self.__Training.getMean() #Gets the mean average from the data set

                        if(matches): #If there is any matches
                            meanMatches = statistics.mean(matches) #Calculate the average match count

                            if(meanMatches > (matchList*0.8)): #If the number of matches is above 80% of the average match count
                                self.__Training.saveImage(binaryID[1]) #Save the new image to the data set
                                self.__Training.addMatch(meanMatches) #Add the new average number of matches to the data.
                                self.ImagePass = True #Set image pass to true (ID verified)

                        self.passC = True #Image has been processed

                #Set borders for ID image
                borderType = cv2.BORDER_CONSTANT
                top = bottom = int(0.01 * frameID.shape[0])
                left = right = int(0.005 * frameID.shape[1])
                borderColour = [0,0,0]
                frameID = cv2.copyMakeBorder(frameID, top, bottom, left, right, borderType, None, borderColour)
                
                #Flips the ID image
                frameCustomer = cv2.flip(frameCustomer, 1)

                #Gets the height and width of the window.
                x, y, width, height = cv2.getWindowImageRect("preview")

                #Copies and resizes the image (width, height)
                projectedImage = frameCustomer.copy()
                projectedID = cv2.resize(frameID, (300, 200))
                
                #Places the new resized ID image to the customer view. (y,y_max), (x,x_max)
                projectedImage[50:250, width-525:width-225,:] = projectedID

                #stores status to display when face has been recognised
                status = "Recognising face and checking dates..."
                
                if(self.passA != -1 and self.passB != -1 and self.passC != -1 and self.turnt == True): # if the algoritmn has finished
                    #If statements determine what message to output
                    if(self.passA):
                        if(self.passC != -1 and self.ImagePass):
                            if(self.validDOB):
                                if(self.validIssue):
                                    if(self.validExpiry):
                                        status = "ID Verified"
                                    else:
                                        status = "ID has expired."
                                else:
                                    status = "ID issue date is invalid"
                            else:
                                status = "The age limit has not been reached"
                        else:
                            status = "The ID card was not validated"
                    else:
                        status = "We could not match your face to the ID card"
                else:
                    if(self.passA != -1):
                        status = "Face Recongised, "
                    if(self.passB == True):
                        status = status + "Dates Found, "
                    if(self.passC == True):
                        status = "ID Verified "

                #Output text and place it on the projected image.  
                cv2.putText(projectedImage, status, (width-525, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)

                #Display the projected image to the screen
                cv2.imshow("preview", projectedImage)

            #Key interrupts
            k = cv2.waitKey(30) & 0xff
            if k == 32: #If the spacebar is pressed, terminate the program
                self.__Camera_1.stop()
                self.__Camera_2.stop()
                cv2.destroyAllWindows()
                break
            if k == 13: #If the enter button is pressed, set turnt to true
                self.turnt = True

#Main function
def main():
    system = IDSystem()
    system.startSystem()

if __name__ == "__main__":
    main()
