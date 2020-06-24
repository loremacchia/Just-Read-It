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


class CrnnOcr(object):
    def __init__(self, model_path='./crnn.pytorch-master/data/crnn.pth'):
        self.model = crnn.CRNN(32, 1, 37, 256)
        if torch.cuda.is_available():
            self.model = self.model.cuda()
        print('loading pretrained self.model from %s' % model_path)
        self.model.load_state_dict(torch.load(model_path))
        self.alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
        self.converter = utils.strLabelConverter(self.alphabet)

    def computeOCR(self, img):
        transformer = dataset.resizeNormalize((100, 32))
        image = img.convert('L')
        image = transformer(image)
        if torch.cuda.is_available():
            image = image.cuda()
        image = image.view(1, *image.size())
        image = Variable(image)
        self.model.eval()
        preds = self.model(image)
        _, preds = preds.max(2)
        preds = preds.transpose(1, 0).contiguous().view(-1)
        preds_size = Variable(torch.IntTensor([preds.size(0)]))
        # raw_pred = self.converter.decode(preds.data, preds_size.data, raw=True)
        sim_pred = self.converter.decode(preds.data, preds_size.data, raw=False)
        return sim_pred

    def getString(self, img, bb):
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
            string = self.computeOCR(croppedPil)  # parola data dall immagine originale

            croppedRot = cv2.rotate(cropped, cv2.ROTATE_180)
            croppedPilRot = Image.fromarray(croppedRot)
            stringRot = self.computeOCR(croppedPilRot)  # parola data dall immagine ruotata di 180

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
                    string = self.computeOCR(croppedPil)

                    croppedRot = cv2.rotate(cropped, cv2.ROTATE_180)
                    croppedPilRot = Image.fromarray(croppedRot)
                    stringRot = self.computeOCR(croppedPilRot)

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

            if string1 == "" or string1 is None:
                iteration += 1
                # string = string.replace("/", "")
                cv2.imwrite("./result/wrongImg/" + string + ".jpg", cropped)
                string1 = None
            else:
                # string1 = string1.replace("/", "")
                cv2.imwrite("./result/goodImg/" + string1 + ".jpg", cropped)

            if string == "" or string is None:
                iteration += 1
                # string = string.replace("/", "")
                # ho messo come nome immagine iterator e non string
                cv2.imwrite("./result/wrongImgStr/" + str(iteration) + ".jpg", cropped)
                string1 = None
            else:
                # string = string.replace("/", "")
                cv2.imwrite("./result/goodImgStr/" + string + ".jpg", cropped)
            return string, string1

    def getStringnGram(self, img, bb):
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
            string = self.computeOCR(croppedPil)  # parola data dall immagine originale

            croppedRot = cv2.rotate(cropped, cv2.ROTATE_180)
            croppedPilRot = Image.fromarray(croppedRot)
            stringRot = self.computeOCR(croppedPilRot)  # parola data dall immagine ruotata di 180

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
                    string = self.computeOCR(croppedPil)

                    croppedRot = cv2.rotate(cropped, cv2.ROTATE_180)
                    croppedPilRot = Image.fromarray(croppedRot)
                    stringRot = self.computeOCR(croppedPilRot)

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
                cv2.imwrite("./result/wrongImg/" + string + ".jpg", cropped)
                string1 = None
            else:
                # string1 = string1.replace("/", "")
                cv2.imwrite("./result/goodImg/" + string1 + ".jpg", cropped)

            if string == "" or string is None:
                iteration += 1
                # string = string.replace("/", "")
                # ho messo come nome immagine iterator e non string
                cv2.imwrite("./result/wrongImgStr/" + str(iteration) + ".jpg", cropped)
                string1 = None
            else:
                # string = string.replace("/", "")
                cv2.imwrite("./result/goodImgStr/" + string + ".jpg", cropped)
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


if __name__ == "__main__":
    obj = CrnnOcr()
    print(obj.getString('./result/goodImg/and.jpg', ))
