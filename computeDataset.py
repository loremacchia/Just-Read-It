import sys
sys.path.insert(1, './E-Shop Dataset')
import download_Marketdataset
import craftObj
import crnnObj
import os
from os.path import isfile, join
import glob

if __name__ == "__main__":
    ocrObj = crnnObj.CrnnOcr()
    netBB = craftObj.CraftNet(ocrObj)
    for file in os.listdir("./E-Shop Dataset/CSVmarketfiles"):
        if file.endswith(".csv"):
            print(os.getcwd())
            path = download_Marketdataset.download_url("./CSVmarketfiles/"+file, file[:-4])
            print(os.getcwd())
            
            image_list = []
            print("speroz")
            for img in os.listdir('./images/'+file[:-4]): #assuming gif
                print("fronge")
                print(img)
                netBB.evaluateBB('./images/'+file[:-4]+'/'+img)
