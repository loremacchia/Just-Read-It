import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

with open('IOU.json', 'r') as openfile:
    json_object = json.load(openfile)

with open('stats.json', 'r') as openfile:
    json_time = json.load(openfile)

# threshold for IOU
threshold = 0.9


# to find the correct word extracted from the annotations
def find_correct_word(category, img, numb):
    img_names = json_object[category]  # image names in dictionary format
    numb_dict = img_names[img]  # numbers that identify bb in the images
    return numb_dict[numb]['word'].get('correct')

def evaluate_proc_time():

    tot_bb = 0
    dict_result = {}  # dizionario  num bb - proc time
    dict_totalnum = {}  # dizionario num bb - quantità di quel num bb

    for i in range(0, len(json_time)):
        category = list(json_time)[i]
        img_names = json_time[category]  # nomi delle immagini in formato dizionario
        for img in list(img_names):
            numb_dict = img_names[img]
            tot_bb = 0
            proc_time = float(numb_dict.get('procTime'))

            for numb in list(numb_dict['BBs']):
                tot_bb += 1
            # print(proc_time)
            if len(dict_result) == 0:
                dict_result[tot_bb] = proc_time
                dict_totalnum[tot_bb] = 1
            if tot_bb in list(dict_result.keys()):
                dict_result[tot_bb] = dict_result.get(tot_bb) + proc_time
                dict_totalnum[tot_bb] = dict_totalnum.get(tot_bb) + 1
            else:
                dict_result[tot_bb] = proc_time
                dict_totalnum[tot_bb] = 1

    print(dict_result)
    print(dict_totalnum)

    keys = list(dict_result.keys())
    final = {}
    for i in keys:
        x = dict_result.get(i)
        y = dict_totalnum.get(i)
        final[i] = (x / y)
    # sorted_final è final ordinata: chiave numero di bb dell immagine, valore media del relativo proc_time
    sorted_final = {k: v for k, v in sorted(final.items(), key=lambda item: item[0])}
    print('miku')
    print(sorted_final)
    # plt.plot(list(sorted_final.values()), list(sorted_final.keys()))
    plt.plot(list(sorted_final.keys()), list(sorted_final.values()))  # valori assi invertiti
    # plotting points as a scatter plot
    # plt.scatter(list(sorted_final.keys()), list(sorted_final.values()))

    # plt.ylabel(sorted())
    plt.xlabel('x - axis')
    plt.ylabel('y - axis')
    plt.title('proc time')
    plt.show()


# PER TESSERACT, usato in evaluate_OCRtime()
def evaluate_tesseract_time():
    dict_result = {}  # dictionary number word characters - ocr time
    dict_totalnum = {}  # dictionary number word characters - quantity of that number word characters
    tot_proc_time = tot_ocr_time = 0
    tot_num_img = tot_words = 0
    for i in range(0, len(json_time)):
        category = list(json_time)[i]
        img_names = json_time[category]  # image names
        for img in list(img_names):
            tot_num_img += 1
            numb_dict = img_names[img]
            tot_proc_time += float(numb_dict.get('procTime'))

            for numb in list(numb_dict['BBs']):
                tot_words += 1
                actual_word = find_correct_word(category, img, numb)
                actual_ocrtime = float(numb_dict['BBs'][numb].get('ocrTimeTess'))

                if actual_word is None:
                    continue
                if len(dict_result) == 0:
                    dict_result[len(actual_word)] = actual_ocrtime
                    dict_totalnum[len(actual_word)] = 1
                    continue
                if len(actual_word) in list(dict_result.keys()):
                    dict_result[len(actual_word)] = dict_result.get(len(actual_word)) + actual_ocrtime
                    dict_totalnum[len(actual_word)] = dict_totalnum.get(len(actual_word)) + 1
                else:
                    dict_result[len(actual_word)] = actual_ocrtime
                    dict_totalnum[len(actual_word)] = 1

                # print(float(numb_dict['BBs'][numb].get('ocrTime')))
                # print(len(numb_dict['BBs'][numb].get('strings')))
                tot_ocr_time += float(numb_dict['BBs'][numb].get('ocrTimeTess'))

    print(dict_result)
    print(dict_totalnum)
    keys = list(dict_result.keys())
    final = {}
    for i in keys:
        x = dict_result.get(i)
        y = dict_totalnum.get(i)
        final[i] = (x / y)
    # sorted_final è final ordinata, chiave: numero di lettere nella parola, valore: media del relativo ocr_time
    sorted_final = {k: v for k, v in sorted(final.items(), key=lambda item: item[0])}
    #print(sorted_final)
    tesseract_finale = [list(sorted_final.keys()), list(sorted_final.values())]
    return tesseract_finale
    # plt.plot(list(sorted_final.keys()), list(sorted_final.values()))


# calcola ocr time DELLA RETE CRNN e le medie totali di ocr e proc time
def evaluate_OCRtime():
    dict_result = {}  # dizionario numero lettere parola - ocr time
    dict_totalnum = {}  # dizionario numero lettere parola - quantità di quel numero lettere parola
    tot_proc_time = tot_ocr_time = 0
    tot_num_img = tot_words = 0
    for i in range(0, len(json_time)):
        category = list(json_time)[i]
        img_names = json_time[category]  # nomi delle immagini in formato dizionario
        for img in list(img_names):
            tot_num_img += 1
            numb_dict = img_names[img]
            tot_proc_time += float(numb_dict.get('procTime'))

            for numb in list(numb_dict['BBs']):
                tot_words += 1
                actual_word = numb_dict['BBs'][numb].get('strings')
                actual_ocrtime = float(numb_dict['BBs'][numb].get('ocrTime'))

                if actual_word is None:
                    continue
                if len(dict_result) == 0:
                    dict_result[len(actual_word)] = actual_ocrtime
                    dict_totalnum[len(actual_word)] = 1
                    continue
                if len(actual_word) in list(dict_result.keys()):
                    dict_result[len(actual_word)] = dict_result.get(len(actual_word)) + actual_ocrtime
                    dict_totalnum[len(actual_word)] = dict_totalnum.get(len(actual_word)) + 1
                else:
                    dict_result[len(actual_word)] = actual_ocrtime
                    dict_totalnum[len(actual_word)] = 1

                # print(float(numb_dict['BBs'][numb].get('ocrTime')))
                # print(len(numb_dict['BBs'][numb].get('strings')))
                tot_ocr_time += float(numb_dict['BBs'][numb].get('ocrTime'))

    print('average process time: %f' % (tot_proc_time / tot_num_img) + ' s')
    print('average ocr time: %f' % (tot_ocr_time / tot_words) + ' s')
    print(dict_result)
    print(dict_totalnum)
    keys = list(dict_result.keys())
    final = {}
    for i in keys:
        x = dict_result.get(i)
        y = dict_totalnum.get(i)
        final[i] = (x / y)
    # sorted_final è final ordinata, chiave: numero di lettere nella parola, valore: media del relativo ocr_time
    sorted_final = {k: v for k, v in sorted(final.items(), key=lambda item: item[0])}
    plt.plot(list(sorted_final.keys()), list(sorted_final.values()))
    # plt.plot(evaluate_tesseract_time()[0], evaluate_tesseract_time()[1], label='Tempo Ocr tesseract')
    plt.xlabel('# Caratteri')
    plt.ylabel('Tempo di processamento (s)')
    # plt.title('Confronto tempo Ocr della CRNN e tempo Ocr del tesseract')
    plt.title('Tempo di riconoscimento CRNN')
    # plt.legend()
    plt.show()


# calcola i risultati USANDO TESSERACT
def iou_threshold_tesseract():
# groundThruth.txt is the list of words in  dataset annotations
    ground = open("groundThruth.txt", "r")
    # elimino il \n dalle parole nella lista
    ground_thruth0 = [line.rstrip('\n') for line in ground]
    ground_thruth = []
    words_in_grand_and_output = 0
    for w in ground_thruth0:
        w = w.lower()
        ground_thruth.append(w)

    categoryCounter = {}
    # indici usati per i risultati
    tot_words = iou_words = not_iou_words = iou_find_true = not_iou_find_true = num_newBB = none_words = 0
    final_result = []  # contiene il numero di parole correttamente riconosciute per ogni categoria
    correct_words = []  # contiene le parole correttamente riconosciute
    for i in range(0, len(json_object)):
        category = list(json_object)[i]
        img_names = json_object[category]
        categoryCounter[category] = 0
        img_names = json_object[category]  # nomi delle immagini in formato dizionario
        for img in list(img_names):
            numb_dict = img_names[img]  # numeri che identificano i bb nelle immagini
            for numb in list(numb_dict):
                tot_words += 1
                if numb_dict[numb]['word'].get('newCorrectedTesseract') is None:
                    capo = 0
                elif numb_dict[numb]['word'].get('newCorrectedTesseract').lower() in ground_thruth:
                    words_in_grand_and_output += 1

                if numb_dict[numb]['iou'] >= threshold:
                    iou_words += 1  # indice delle parole con iou >= della soglia
                    if numb_dict[numb]['word'].get('newCorrectedTesseract') is None:
                        none_words += 1
                    elif numb_dict[numb]['word'].get('correct').lower() == numb_dict[numb]['word'].get(
                            'newCorrectedTesseract').lower():
                        categoryCounter[category] += 1
                        iou_find_true += 1
                        correct_words.append(numb_dict[numb]['word'].get('newCorrectedTesseract'))
                        final_result.append(category)
                else:
                    not_iou_words += 1
                    if len(numb_dict[numb]['word']) != 0:  # usato perchè ci sono parole senza bb del dataset di partenz
                        if numb_dict[numb]['word'].get('newCorrectedTesseract') is None:
                            none_words += 1
                        elif numb_dict[numb]['word'].get('correct').lower() == numb_dict[numb]['word'].get(
                                'newCorrectedTesseract').lower():
                            categoryCounter[category] += 1
                            not_iou_find_true += 1
                            correct_words.append(numb_dict[numb]['word'].get('newCorrectedTesseract'))
                            final_result.append(category)
                    else:
                        num_newBB += 1  # indice per le parole senza bb del dataset originale
    
    print('TESSERACT')
    print('tot words: %d' % tot_words)
    print('words without original dataset bounding box: %d' % num_newBB)
    print('words with iou more than treshold: %d' % iou_words)
    print('words without iou more than treshold: %d' % not_iou_words)
    print('correct words found with iou more than treshold: %d' % iou_find_true)
    print('correct words found with iou less then treshold: %d' % not_iou_find_true)
    print('tot correct words found: %d' % len(correct_words))  # totale parole corrette sotto e sopra la soglia iou
    # print(sorted(correct_words))
    print('words without recognition: %d' % none_words)
    # precision: num parole corrette riconosciute / num parole totali
    print('precision: %f' % ((iou_find_true + not_iou_find_true) / (tot_words - num_newBB)))
    # recall: num parole corrette riconosciute / num parole corrette
    # print('recall: %f' % ((iou_find_true + not_iou_find_true) / 4480))
    print('recall iou more iou tresh: %f' % (iou_find_true / iou_words))
    print('recall iou less iou tresh: %f' % (not_iou_find_true / (not_iou_words - num_newBB)))
    print('words in ground_truth and in the tesseract output: %s' % words_in_grand_and_output)
    print(categoryCounter)
    # print(final_result)
    pd.Series(final_result).value_counts().plot(kind='bar')
    plt.xlabel('e-commerce product categories')
    plt.ylabel('correct words')
    plt.title('Correct words found in all product categories')
    #plt.show()

    # calcola i risultati del progetto


#RISULTATI USANDO CRNN
def iou_threshold():
    ground = open("groundThruth.txt", "r")
    # elimino il \n dalle parole nella lista
    ground_thruth0 = [line.rstrip('\n') for line in ground]
    ground_thruth = []
    words_in_grand_and_output = 0
    for w in ground_thruth0:
        w = w.lower()
        ground_thruth.append(w)

    categoryCounter = {}
    # indici usati per i risultati
    tot_words = iou_words = not_iou_words = iou_find_true = not_iou_find_true = num_newBB = none_words = 0
    final_result = []  # contiene il numero di parole correttamente riconosciute per ogni categoria
    correct_words = []  # contiene le parole correttamente riconosciute
    for i in range(0, len(json_object)):
        category = list(json_object)[i]
        img_names = json_object[category]
        categoryCounter[category] = 0
        img_names = json_object[category]  # nomi delle immagini in formato dizionario
        for img in list(img_names):
            numb_dict = img_names[img]  # numeri che identificano i bb nelle immagini
            for numb in list(numb_dict):
                tot_words += 1
                if numb_dict[numb]['word'].get('newCorrected') is None:
                    capo = 0
                elif numb_dict[numb]['word'].get('newCorrected').lower() in ground_thruth:
                    words_in_grand_and_output += 1

                if numb_dict[numb]['iou'] >= threshold:
                    iou_words += 1  # indice delle parole con iou >= della soglia
                    if numb_dict[numb]['word'].get('newCorrected') is None:
                        none_words += 1
                    elif numb_dict[numb]['word'].get('correct').lower() == numb_dict[numb]['word'].get(
                            'newCorrected').lower():
                        categoryCounter[category] += 1
                        iou_find_true += 1
                        correct_words.append(numb_dict[numb]['word'].get('newCorrected'))
                        final_result.append(category)
                else:
                    not_iou_words += 1
                    if len(numb_dict[numb]['word']) != 0:  # usato perchè ci sono parole senza bb del dataset di partenz
                        if numb_dict[numb]['word'].get('newCorrected') is None:
                            none_words += 1
                        elif numb_dict[numb]['word'].get('correct').lower() == numb_dict[numb]['word'].get(
                                'newCorrected').lower():
                            categoryCounter[category] += 1
                            not_iou_find_true += 1
                            correct_words.append(numb_dict[numb]['word'].get('newCorrected'))
                            final_result.append(category)
                    else:
                        num_newBB += 1  # indice per le parole senza bb del dataset originale

    print('tot words: %d' % tot_words)
    print('words without original dataset bounding box: %d' % num_newBB)
    print('words with iou more than treshold: %d' % iou_words)
    print('words without iou more than treshold: %d' % not_iou_words)
    print('correct words found with iou more than treshold: %d' % iou_find_true)
    print('correct words found with iou less then treshold: %d' % not_iou_find_true)
    print('tot correct words found: %d' % len(correct_words))  # totale parole corrette sotto e sopra la soglia iou
    # print(sorted(correct_words))
    print('words without recognition: %d' % none_words)
    # precision: num parole corrette riconosciute / num parole totali
    print('precision: %f' % ((iou_find_true + not_iou_find_true) / (tot_words - num_newBB)))
    # recall: num parole corrette riconosciute / num parole corrette
    # print('recall: %f' % ((iou_find_true + not_iou_find_true) / 4480))
    print('recall iou more iou tresh: %f' % (iou_find_true / iou_words))
    print('recall iou less iou tresh: %f' % (not_iou_find_true / (not_iou_words - num_newBB)))
    print('words in ground_truth and in the net output: %s' % words_in_grand_and_output)
    print(categoryCounter)
    # print(final_result)
    pd.Series(final_result).value_counts().plot(kind='bar')
    plt.xlabel('e-commerce product categories')
    plt.ylabel('correct words')
    plt.title('Correct words found in all product categories')
    #plt.show()


def printHist():

    
    x = ['artworks', 'beauty', 'biscuits', 'books', 'boystops', 'cerealporridge', 'grocery', 'healthpersonalcare', 'homecarecleaning', 'petsupplies', 'sweetschocolate', 'toysgames', 'vhs']
    yDat = [257, 489, 254, 813, 72, 549, 358, 212, 505, 167, 316, 170, 318]
    yTess = [31, 32, 16, 106, 15, 68, 11, 29, 54, 33, 25, 25, 18]
    yCRNN = [91,244, 124, 512, 38, 331, 183, 138, 327, 104, 140, 100, 186]
  
    fig, ax = plt.subplots()  
    width = 0.75 # the width of the bars 
    ind = np.arange(len(x))  # the x locations for the groups
    rectDat = ax.bar(ind + 0.5 - width/2, yDat, width/3, label='Dataset')
    rectCRNN = ax.bar(ind + 0.5 - width/6, yCRNN, width/3, label='CRNN')
    rectTess = ax.bar(ind + 0.5 + width/6, yTess, width/3, label='Tesseract')
    ax.set_xticks(ind+width/2)
    ax.set_xticklabels(x, rotation = 30, rotation_mode="anchor", ha="right")
    ax.set_title('Parole trovate per categoria')
    ax.set_xlabel('Categoria')
    ax.set_ylabel('# Parole trovate') 
    ax.legend() 

    def autolabelCRNN(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            idx = 0
            for i in range(len(yCRNN)):
                if(yCRNN[i] == height):
                    idx = i
                    break

            ax.annotate('{}%'.format('%.0f'%(height*100/yDat[i])),
                        xy=(rect.get_x() + 0.13  + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    def autolabelTess(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            idx = 0
            for i in range(len(yTess)):
                if(yTess[i] == height):
                    idx = i
                    break

            ax.annotate('{}%'.format('%.0f'%(height*100/yDat[i])),
                        xy=(rect.get_x() + 0.13 + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
    autolabelCRNN(rectCRNN)
    autolabelTess(rectTess)
    plt.show()

if __name__ == "__main__":
    # evaluate_proc_time()
    # evaluate_OCRtime()
    # iou_threshold()
    # iou_threshold_tesseract()
    # plt.show()
    printHist()