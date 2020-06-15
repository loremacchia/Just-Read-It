import sys
sys.path.insert(1, './E-Shop Dataset')
import download_Marketdataset
import craftObj
import crnnObjFlip
import os
from os.path import isfile, join
import glob

if __name__ == "__main__":
    ocrObj = crnnObjFlip.CrnnOcr()
    netBB = craftObj.CraftNet(ocrObj)
    # script to download all the imgs from a csv and analyze them (for all the files)

    # for file in os.listdir("./E-Shop Dataset/CSVmarketfiles"):
    #     if file.endswith(".csv"):
    #         path = download_Marketdataset.download_url("./CSVmarketfiles/"+file, file[:-4])
    #         image_list = []
    #         for img in os.listdir('./images/'+file[:-4]):
    #             if(img[-4:] == ".jpg" or img[-4:] == ".png"):
    #                 print(img)
    #                 netBB.evaluateBB('./images/'+file[:-4]+'/'+img)



    # script to analyze all the imgs into a folder (for us is images)
    for img in os.listdir("./images"):
        print(img)
        netBB.evaluateBB("./images/"+img)
    list_subfolders_with_paths = [f.path for f in os.scandir("./images") if f.is_dir()]
    for path in list_subfolders_with_paths:
        print(path)
        for img in os.listdir(path):
            if(img[-4:] == ".jpg" or img[-4:] == ".png"):
                print(img)
                netBB.evaluateBB(path+"/"+img)
