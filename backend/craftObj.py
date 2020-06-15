import sys
import os
import time
import argparse

sys.path.insert(1, './CRAFT-pytorch-master')
sys.path.insert(1, './crnn.pytorch-master')

import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
from torch.autograd import Variable

from PIL import Image

import cv2
from skimage import io
import numpy as np
import craft_utils
import imgproc 
import file_utils
import json
import zipfile
import crnnObj
from collections import defaultdict
from craft import CRAFT
from collections import OrderedDict


def copyStateDict(state_dict):
    if list(state_dict.keys())[0].startswith("module"):
        start_idx = 1
    else:
        start_idx = 0
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        name = ".".join(k.split(".")[start_idx:])
        new_state_dict[name] = v
    return new_state_dict

def str2bool(v):
    return v.lower() in ("yes", "y", "true", "t", "1")

def getNameAndFolder(imagePath):
    return (imagePath[-8:], imagePath[8:-9])


# Parameters
# imageFolder = "images/"
# image_list, _, _ = file_utils.get_files(imageFolder)

result_folder = './result/'
if not os.path.isdir(result_folder):
    os.mkdir(result_folder)

isCuda = True
trained_model = "./CRAFT-pytorch-master/craft_mlt_25k.pth"
show_time = True
canvas_size = 1280
mag_ratio = 1.5
text_thresholdVal = 0.7
link_thresholdVal = 0.4
low_textVal = 0.4
polyVal = False
isTest = True


class CraftNet(object):
    def __init__(self, ocrObj):
        self.net = CRAFT()    
        print('Loading weights from checkpoint (' + trained_model + ')')
        if isCuda:
            self.net.load_state_dict(copyStateDict(torch.load(trained_model)))
        else:
            self.net.load_state_dict(copyStateDict(torch.load(trained_model, map_location='cpu')))
        if isCuda:
            self.net = self.net.cuda()
            self.net = torch.nn.DataParallel(self.net)
            cudnn.benchmark = False 
        self.net.eval()
        self.jsonFile = defaultdict(dict)
        self.ocrObj = ocrObj

    def test_net(self, image, text_threshold, link_threshold, low_text, cuda, poly, refine_net=None):
        t0 = time.time()

        # resize
        img_resized, target_ratio, size_heatmap = imgproc.resize_aspect_ratio(image, canvas_size, interpolation=cv2.INTER_LINEAR, mag_ratio=mag_ratio)
        ratio_h = ratio_w = 1 / target_ratio

        # preprocessing
        x = imgproc.normalizeMeanVariance(img_resized)
        x = torch.from_numpy(x).permute(2, 0, 1)    # [h, w, c] to [c, h, w]
        x = Variable(x.unsqueeze(0))                # [c, h, w] to [b, c, h, w]
        if cuda:
            x = x.cuda()

        # forward pass
        with torch.no_grad():
            y, feature = self.net(x)

        # make score and link map
        score_text = y[0,:,:,0].cpu().data.numpy()
        score_link = y[0,:,:,1].cpu().data.numpy()

        # refine link
        if refine_net is not None:
            with torch.no_grad():
                y_refiner = refine_net(y, feature)
            score_link = y_refiner[0,:,:,0].cpu().data.numpy()

        t0 = time.time() - t0
        t1 = time.time()

        # Post-processing
        boxes, polys = craft_utils.getDetBoxes(score_text, score_link, text_threshold, link_threshold, low_text, poly)

        # coordinate adjustment
        boxes = craft_utils.adjustResultCoordinates(boxes, ratio_w, ratio_h)
        polys = craft_utils.adjustResultCoordinates(polys, ratio_w, ratio_h)
        for k in range(len(polys)):
            if polys[k] is None: polys[k] = boxes[k]

        t1 = time.time() - t1

        # render results (optional)
        render_img = score_text.copy()
        render_img = np.hstack((render_img, score_link))
        ret_score_text = imgproc.cvt2HeatmapImg(render_img)

        # if show_time : print("\ninfer/postproc time : {:.3f}/{:.3f}".format(t0, t1))

        return boxes, polys, ret_score_text


    def evaluateBB(self, image_path):
        print(image_path)
        image = imgproc.loadImage(image_path)
        t = time.time()
        tnew = t
        bboxes, polys, score_text = self.test_net(image, text_thresholdVal, link_thresholdVal, low_textVal, isCuda, polyVal)
        deltaTime = time.time() - tnew
        words = []
        # # save image with BB
        # filename, file_ext = os.path.splitext(os.path.basename(image_path))
        # real_folder = result_folder + '/' + image_path.replace('images', '').replace(filename + file_ext, '')
        # file_utils.saveResult(image_path, image[:,:,::-1], polys, dirname=real_folder)
        if(isTest):
            curImg = {
                "BBs" : defaultdict(dict),
                "pretrained" : "MLT",
                "procTime" : deltaTime,
                "OCR" : "CRNN",
            }
        for i in range(len(polys)):
            tnew = time.time()
            incorrect, correct = self.ocrObj.getString(image, polys[i])
            print(incorrect, correct)
            words.append((incorrect,correct))
            if(isTest):
                curImg["BBs"][i] = {
                    "BB" : polys[i].tolist(),
                    "strings" : incorrect,
                    "stringsCorrect" : correct,
                    "ocrTime" : time.time() - tnew
                }
        if(isTest):
            name, folder = getNameAndFolder(image_path)
            self.jsonFile[folder][name] = curImg
            with open("./CRAFT-pytorch-master/stats.json", "w") as write_file:
                json.dump(self.jsonFile, write_file, sort_keys=True, indent=4)
        # return polys
        corr = ""
        incorr = ""
        for w in words:
            corr.join(w[1] + "  ")
            incorr.join(w[0] + "  ")
        print(corr)
        print(incorr)
        return words


if __name__ == "__main__":
    ocrObj = crnnObj.CrnnOcr()
    netBB = CraftNet(ocrObj)
    netBB.evaluateBB("images/beauty/0027.jpg")