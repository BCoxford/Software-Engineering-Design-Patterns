#Ben Coxford
#------------
#Lines 11-65 (excluding 22-46)
#------------

#Joel Guest
#------------
#Lines 22-46
#------------

#Import frameworks
import pytesseract
import datetime

class _DateValidation(object):

    #Initialise date verification
    def __init__(self):
        self.text = []
        self.endRead = False #Have three distinct dates been found?

    def checkDate(self):
        #stores current date in date format
        currentDate = datetime.date.today()
        currentDate = currentDate.strftime("%d.%m.%Y")

        #Sets all dates to false
        validDOB = False
        validIssue = False
        validExpiry = False

        #sorts the dates in reverse order
        sortedDates = sorted(self.text, reverse=True)

        #If all dates are valid and in date the variables are changed to true
        if (datetime.datetime.strptime(sortedDates[0], "%d.%m.%Y") < datetime.datetime.strptime(currentDate, "%d.%m.%Y")):
            validDOB = True

        if (datetime.datetime.strptime(sortedDates[1], "%d.%m.%Y") < datetime.datetime.strptime(currentDate, "%d.%m.%Y")):
            validIssue = True

        if (datetime.datetime.strptime(sortedDates[2], "%d.%m.%Y")  > datetime.datetime.strptime(currentDate, "%d.%m.%Y")):
            validExpiry = True

        #Variables are returned
        return validDOB, validIssue, validExpiry

    def readText(self, imgID):
        #If three dates have not been found
        if self.endRead == False:
            #Read the text from the image
            pytesseract.pytesseract.tesseract_cmd = '/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'
            text = pytesseract.image_to_string(imgID)

            #Split the text by spaces
            data = text.split()

            for i in data:
                #For each item in the array
                try:
                    #Attempt to test if its in the correct format
                    datetime.datetime.strptime(i, '%d.%m.%Y')
                    if(i not in self.text): #If the same date is not in the array
                        #Split the date and extract its year
                        x = i.split(".")
                        date = datetime.datetime.now()
                        #If the year is within 30 years of the current date
                        
                        if(int(x[2]) > (int(date.year)-30) and int(x[2]) < (int(date.year)+30)):
                            #Append it to the array of dates
                            self.text.append(i)
                except:
                    continue
                
        if(self.text): #If the array is initialised
            if(len(self.text) == 3): #If the array length is equal to three
                self.endRead = True #Set value to true as all three dates are collected
                return self.checkDate() #Return if the date are valid

        return False, False, False #Return false if three dates are not found
