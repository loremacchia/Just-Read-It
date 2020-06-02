import cv2;
import numpy as np;
import pytesseract
import os
import csv
import editDistance

iteration = 0

def getTXT(parent, img):
    txtPath = "result/"+parent+"/res_"+img+".txt"
    return open(txtPath,"r")

def getString(image, bb):
    global iteration
    img = cv2.imread(image)
    (x,y,w,h) = cv2.boundingRect(bb) # returns (x,y,w,h) of the rect
    cropped = img[y: y + h, x: x + w]    
    if h > w:
        cropped = cv2.rotate(cropped, cv2.ROTATE_90_CLOCKWISE)
    if(not cropped.all()):
        print("starttt")
        string = new_ocr(cropped)
        string1 = editDistance.nGram(string)
        if(string1 == "" or string1 == None):
            if(x - 6 > 0):
                x -= 6
            else:
                x = 0
            if(y - 6 > 0):
                y -= 6
            else:
                y = 0
            print(x,y,w,h)
            w += 12
            h += 12
            cropped = img[y: y + h, x: x + w]
            if h > w:
                cropped = cv2.rotate(cropped, cv2.ROTATE_90_CLOCKWISE)  
            string = new_ocr(cropped)
            string1 = editDistance.nGram(string)  
        if(string1 == "" or string1 == None):
            iteration += 1
            string = string.replace("/","")
            cv2.imwrite("wrongImg/" + string + ".jpg",cropped)
            return (string, None)
        else:
            string1 = string1.replace("/","")
            cv2.imwrite("goodImg/"+string1+".jpg", cropped)
            return (string, string1)
    else:
        iteration += 1
        cv2.imwrite("wrongImg/" + str(iteration) + ".jpg",cropped)
        return (None, None)

def new_ocr(image):
    # Grayscale, Gaussian blur, Otsu's threshold
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Morph open to remove noise and invert image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening

    # Perform text extraction
    data = pytesseract.image_to_string(invert, lang='eng', config='--psm 8')
    print(data)
    return data


if __name__ == "__main__":
    os.chdir("CRAFT-pytorch-master/")
    print(os.getcwd())
    for dirs in os.listdir("images"):
        print(dirs)
        dirImg = "images/"+dirs
        dirRes = "result/"+dirs
        if(os.path.isdir(dirImg) and os.path.isdir(dirRes)):
            for file in os.listdir(dirImg):
                if file.endswith(".jpg"):
                    img = file[:-4]
                    txt = getTXT(dirs, img)
                    for bb in txt:
                        boundingBox = bb.split(',')
                        boundingBox[len(boundingBox)-1] = boundingBox[len(boundingBox)-1][:-1]
                        retString = getString(dirImg+"/"+file, list(map(int, boundingBox)))
                        
                        
