#Joel Guest Lines 3-92

import unittest
import cv2
import numpy as np

import Camera
import DateValidation
import TrainingClass
import FaceDetection
import FeatureMatching
import ImagePool
import ProgramCode

#Tests each subsystem with example data and the expected outcomes.

class TestSubsystems(unittest.TestCase):

    #Tests if an image can be read from the camera
    def testReadImg(self):
        camera = Camera._Camera(0)
        camera.start()
        ret, img = camera.readImg()
        self.assertTrue(ret)

    #Tests the full camera
    def testFullCamera(self):
        camera = Camera._Camera(0)
        camera.start()
        ret, img = camera.readImg()
        camera.stop()

    #Tests if an ID card returns valid dates
    def testDate(self):
        date = DateValidation._DateValidation()
        imgPath = "TestImages/TestID.jpg"
        img = cv2.imread(imgPath, 0)
        a, b, c = False, False, False
        for i in range(0,50):
            a, b, c = date.readText(img)
        self.assertTrue(a)
        self.assertTrue(b)
        self.assertTrue(c)

    #Test the training data to get the number of matches and the mean
    def testTrainData(self):
        train = TrainingClass._TrainData()
        self.assertEqual(train.getMatch(), [1700,2848,2383,3176])
        self.assertEqual(train.getMean(), 2526.75)

    #Test if two faces can be matched
    def testFaceDetection(self):
        imgPath = "TestImages/TestFace.jpg"
        img = cv2.imread(imgPath, 0)

        imgPath = "TestImages/TestFace2.jpg"
        img2 = cv2.imread(imgPath, 0)

        face = FaceDetection._FaceDetection()
        self.assertTrue(face.detectSingleFace(img,300))
        self.assertTrue(face.compareFaces(img,img2))

    #Tests if the number of matches returned on the test data is between the given range
    #Any errors matching or using invalid images will produce a lower number of matches.
    def testFeatureMatching(self):
        imgPath = "TestImages/TestBlob.png"
        img = cv2.imread(imgPath, 0)

        imgPath = "TestImages/TestBlob2.png"
        img2 = cv2.imread(imgPath, 0)

        match = FeatureMatching._FeatureMatching()
        match.Match(img,img2)
        self.assertTrue(400 <= match.getMatch() <= 4000)

    #Tests if the image pool can aquire an image and return the correct image
    def testImagePool(self):
        imgPath = "images/img_1.png"
        img = cv2.imread(imgPath, 0)

        pool = ImagePool._ImagePool()

        image = pool.acquire(1)

        np.testing.assert_array_almost_equal(image.getImage(), img, 2)

        image.reset()

        pool.release(image)        
            
if __name__ == '__main__':
    unittest.main()
