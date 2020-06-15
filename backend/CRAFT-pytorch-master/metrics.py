import os
import json
import csv
from collections import defaultdict

def checkBB(image, newBBs, csvFile):
    jsonFile = {}
    for i in newBBs:
        jsonFile[i] = {
            "newCoords" : newBBs[i]["BB"],
            "iou" : 0,
            "word":{}
        }
    for row in csvFile:
        if row[0][0] == '#':
            row[0] = row[0].replace('#', '')
        if(row[0] == image):
            corrBB = row[1:-1]
            corrRect = [int(corrBB[0]), int(corrBB[1]), int(corrBB[2]), int(corrBB[5])]
            for i in newBBs:
                newRect = [newBBs[i]["BB"][0][0], newBBs[i]["BB"][0][1], newBBs[i]["BB"][1][0], newBBs[i]["BB"][2][1]]
                iou = intersectionOverUnion(corrRect, newRect)
                if(iou > jsonFile[i]["iou"]):
                    jsonFile[i]["iou"] = iou
                    jsonFile[i]["word"]["correct"] = row[-1:][0]
                    jsonFile[i]["word"]["new"] = newBBs[i]["strings"]
                    jsonFile[i]["word"]["newCorrected"] = newBBs[i]["stringsCorrect"]
                    jsonFile[i]["datasetCoords"] = [[int(corrBB[0]),int(corrBB[1])],[int(corrBB[2]),int(corrBB[3])],[int(corrBB[4]),int(corrBB[5])],[int(corrBB[6]),int(corrBB[7])]]
    
    return jsonFile

def intersectionOverUnion(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    interArea = abs(max((xB - xA, 0)) * max((yB - yA), 0))
    if interArea == 0:
        return 0
    boxAArea = abs((boxA[2] - boxA[0]) * (boxA[3] - boxA[1]))
    boxBArea = abs((boxB[2] - boxB[0]) * (boxB[3] - boxB[1]))
    iou = interArea / float(boxAArea + boxBArea - interArea)
    return iou

def getNameAndFolder(imagePath):
    return (imagePath[-8:], imagePath[7:-9])



if __name__ == "__main__":
    with open("CRAFT-pytorch-master/stats.json", "r") as read_file:
        stats = json.load(read_file)

    os.chdir("E-Shop Dataset/CSVmarketfiles")
    jsonFile = defaultdict(dict)
    for folder in stats:
        for file in stats[folder]:
            item = stats[folder][file]
            with open(folder + ".csv") as csv_file:
                csvReader = csv.reader(csv_file, delimiter=',')
                jsonItem = checkBB(file, item["BBs"], csvReader)
                jsonFile[folder][file] = jsonItem
    
    os.chdir("../../CRAFT-pytorch-master/")
    with open("IOU.json", "w") as write_file:
        json.dump(jsonFile, write_file, sort_keys=True, indent=4)


    