import pytesseract
import torch
from torch.autograd import Variable
import utils
import dataset
from PIL import Image
import cv2
import models.crnn as crnn
import numpy as np
import os
import csv
import editDistance
import calculateDistance

iteration = 0



def computeOCR(img):
    image = np.array(img)[:, :, ::-1].copy() 
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
    return data

def getString(img, bb):
    global iteration
    (x, y, w, h) = cv2.boundingRect(bb)  # returns (x,y,w,h) of the rect
    cropped = img[y: y + h, x: x + w]
    if h > w:
        cropped = cv2.rotate(cropped, cv2.ROTATE_90_CLOCKWISE)

    if cropped is None or len(cropped) <= 0 or len(cropped[0]) <= 0:  # MOD
        if cropped is None:
            return None, None
        iteration += 1
        # cv2.imwrite("./result/wrongImg/" + str(iteration) + ".jpg", cropped)
        return None, None

    elif len(cropped[0]) > 0:
        cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
        croppedPil = Image.fromarray(cropped)
        string = computeOCR(croppedPil)  # parola data dall immagine originale

        croppedRot = cv2.rotate(cropped, cv2.ROTATE_180)
        croppedPilRot = Image.fromarray(croppedRot)
        stringRot = computeOCR(croppedPilRot)  # parola data dall immagine ruotata di 180

        # res = editDistance.compareStrings(string, stringRot)
        res_not_rotate = calculateDistance.control_distance(string)
        res_rotate = calculateDistance.control_distance(stringRot)
        res = comparison_rotate(res_not_rotate, res_rotate)
        if res is not None:
            if res == res_rotate:
                string = stringRot
                img = cv2.rotate(img, cv2.ROTATE_180)  # ??????
                cropped = croppedRot
            # STRING1 È CON EDITDISTANCE/CALCULATEDISTANCE
            string1 = res[3]  # in res[2] cè la parola target in res[3] la parola del dizionario più vicina

        else:
            if x - 6 > 0:
                x -= 6
            else:
                x = 0
            if y - 6 > 0:
                y -= 6
            else:
                y = 0
            w += 12
            h += 12
            cropped = img[y: y + h, x: x + w]
            if h > w:
                cropped = cv2.rotate(cropped, cv2.ROTATE_90_CLOCKWISE)
            if len(cropped[0]) > 0:
                cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
                croppedPil = Image.fromarray(cropped)
                string = computeOCR(croppedPil)

                croppedRot = cv2.rotate(cropped, cv2.ROTATE_180)
                croppedPilRot = Image.fromarray(croppedRot)
                stringRot = computeOCR(croppedPilRot)

                # res = editDistance.compareStrings(string, stringRot)
                res_not_rotate = calculateDistance.control_distance(string)
                res_rotate = calculateDistance.control_distance(stringRot)
                res = comparison_rotate(res_not_rotate, res_rotate)
                if res is not None:
                    if res == res_rotate:
                        string = stringRot
                        img = cv2.rotate(img, cv2.ROTATE_180)  # ??????
                        cropped = croppedRot
                    string1 = res[3]  # in res[2] cè la parola target in res[3] la parola del dizionario più vicina

                else:
                    string1 = None

        if(string1 == "" or string1 is None):
            iteration += 1
            # string = string.replace("/", "")
            # cv2.imwrite("./result/wrongImg/" + string + ".jpg", cropped)
            string1 = None
        
        if(string == "" or string is None):
            iteration += 1
            # string = string.replace("/", "")
            # ho messo come nome immagine iterator e non string
            # cv2.imwrite("./result/wrongImgStr/" + str(iteration) + ".jpg", cropped)
            string1 = None
        
        return string, string1

def getStringnGram( img, bb):
    global iteration
    (x, y, w, h) = cv2.boundingRect(bb)  # returns (x,y,w,h) of the rect
    cropped = img[y: y + h, x: x + w]
    if h > w:
        cropped = cv2.rotate(cropped, cv2.ROTATE_90_CLOCKWISE)
    if(cropped is None or len(cropped) <= 0 or len(cropped[0]) <= 0):  # MOD
        if cropped is None:
            return None, None
        iteration += 1
        # cv2.imwrite("./result/wrongImg/" + str(iteration) + ".jpg", cropped)
        return None, None

    elif (len(cropped[0]) > 0):
        cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
        croppedPil = Image.fromarray(cropped)
        string = computeOCR(croppedPil)  # parola data dall immagine originale

        croppedRot = cv2.rotate(cropped, cv2.ROTATE_180)
        croppedPilRot = Image.fromarray(croppedRot)
        stringRot = computeOCR(croppedPilRot)  # parola data dall immagine ruotata di 180

        # res = editDistance.compareStrings(string, stringRot)
        res_not_rotate = calculateDistance.nGram(string)
        res_rotate = calculateDistance.nGram(stringRot)
        res = comparison_rotate(res_not_rotate, res_rotate)
        if res is not None:
            if res == res_rotate:
                string = stringRot
                img = cv2.rotate(img, cv2.ROTATE_180)  # ??????
                cropped = croppedRot
            # STRING1 È CON EDITDISTANCE/CALCULATEDISTANCE
            string1 = res[3]  # in res[2] cè la parola target in res[3] la parola del dizionario più vicina
        else:
            if x - 6 > 0:
                x -= 6
            else:
                x = 0
            if y - 6 > 0:
                y -= 6
            else:
                y = 0
            w += 12
            h += 12
            cropped = img[y: y + h, x: x + w]
            if h > w:
                cropped = cv2.rotate(cropped, cv2.ROTATE_90_CLOCKWISE)
            if len(cropped[0]) > 0:
                cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
                croppedPil = Image.fromarray(cropped)
                string = computeOCR(croppedPil)

                croppedRot = cv2.rotate(cropped, cv2.ROTATE_180)
                croppedPilRot = Image.fromarray(croppedRot)
                stringRot = computeOCR(croppedPilRot)

                # res = editDistance.compareStrings(string, stringRot)
                res_not_rotate = calculateDistance.nGram(string)
                res_rotate = calculateDistance.nGram(stringRot)
                res = comparison_rotate(res_not_rotate, res_rotate)
                if res is not None:
                    if res == res_rotate:
                        string = stringRot
                        img = cv2.rotate(img, cv2.ROTATE_180)  # ??????
                        cropped = croppedRot
                    string1 = res[3]  # in res[2] cè la parola target in res[3] la parola del dizionario più vicina

                else:
                    string1 = None

        if string1 == "" or string1 is None:
            iteration += 1
            # string = string.replace("/", "")
            # cv2.imwrite("./result/wrongImg/" + string + ".jpg", cropped)
            string1 = None
        

        if string == "" or string is None:
            iteration += 1
            # string = string.replace("/", "")
            # ho messo come nome immagine iterator e non string
            # cv2.imwrite("./result/wrongImgStr/" + str(iteration) + ".jpg", cropped)
            string1 = None
        
        return string, string1


# per confrontare tra il risultato di calculateDistance con e senza rotazione dell immagine
def comparison_rotate(not_rotate, rotate):
    if not_rotate is None:
        return rotate
    elif rotate is None:
        return not_rotate
    # alla posizione 0 mi indica se la parola è stata trovata o meno
    if not_rotate[0] > rotate[0]:
        return not_rotate
    elif not_rotate[0] < rotate[0]:
        return rotate
    else:
        # alla posizione 1 c'è il ratio
        if not_rotate[1] >= rotate[1]:
            return not_rotate
        elif not_rotate[1] < rotate[1]:
            return rotate




                        
                        
