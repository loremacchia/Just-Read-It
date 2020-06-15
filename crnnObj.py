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

iteration = 0

class CrnnOcr(object):
    def __init__(self, model_path = './crnn.pytorch-master/data/crnn.pth'):
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
        (x,y,w,h) = cv2.boundingRect(bb) # returns (x,y,w,h) of the rect
        cropped = img[y: y + h, x: x + w]    
        if h > w:
            cropped = cv2.rotate(cropped, cv2.ROTATE_90_CLOCKWISE)
        if(len(cropped[0]) > 0):
            cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
            cropped_pil = Image.fromarray(cropped)
            string = self.computeOCR(cropped_pil)
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
                w += 12
                h += 12
                cropped = img[y: y + h, x: x + w]
                if h > w:
                    cropped = cv2.rotate(cropped, cv2.ROTATE_90_CLOCKWISE)
                cropped_pil = Image.fromarray(cropped)  
                string = self.computeOCR(cropped_pil)
                string1 = editDistance.nGram(string)  
            if(string1 == "" or string1 == None):
                iteration += 1
                string = string.replace("/","")
                cv2.imwrite("./result/wrongImg/" + string + ".jpg",cropped)
                string1 = None
            else:
                string1 = string1.replace("/","")
                cv2.imwrite("./result/goodImg/"+string1+".jpg", cropped)
            if(string == "" or string == None):
                string = string.replace("/","")
                cv2.imwrite("./result/wrongImgStr/" + string + ".jpg",cropped)
                string1 = None
            else:
                string = string.replace("/","")
                cv2.imwrite("./result/goodImgStr/"+string+".jpg", cropped)
            return (string, string1)
        else:
            iteration += 1
            cv2.imwrite("./result/wrongImg/" + str(iteration) + ".jpg",cropped)
            return (None, None)

if __name__ == "__main__":
    obj = CrnnOcr()
    print(obj.getString('./data/5.jpg',))
