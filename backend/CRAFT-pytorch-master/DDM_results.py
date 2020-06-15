import json
import pandas as pd
import matplotlib.pyplot as plt


with open('EyesForBlind/CRAFT-pytorch-master/IOU.json', 'r') as openfile:
    json_object = json.load(openfile)


def iou_threshold():
    threshold = 0.7
    # indici usati per i risultati
    tot_words = iou_words = iou_find_true = not_iou_find_true = num_newBB = 0
    final_result = []  # contiene il numero di parole correttamente riconosciute per ogni categoria
    correct_words = []  # contiene le parole correttamente riconosciute
    for i in range(0, len(json_object)):
        category = list(json_object)[i]
        img_names = json_object[category]  # nomi delle immagini in formato dizionario
        for img in list(img_names):
            numb_dict = img_names[img]  # numeri che identificano i bb nelle immagini
            for numb in list(numb_dict):
                tot_words += 1

                if numb_dict[numb]['iou'] >= threshold:
                    iou_words += 1  # indice delle parole con iou >= della soglia
                    if numb_dict[numb]['word'].get('correct') == numb_dict[numb]['word'].get('newCorrected'):
                        iou_find_true += 1
                        correct_words.append(numb_dict[numb]['word'].get('newCorrected'))
                        final_result.append(category)
                else:
                    if len(numb_dict[numb]['word']) != 0:  # usato perchè ci sono parole senza bb del dataset di partenz
                        if numb_dict[numb]['word'].get('correct') == numb_dict[numb]['word'].get('newCorrected'):
                            not_iou_find_true += 1
                            correct_words.append(numb_dict[numb]['word'].get('newCorrected'))
                            final_result.append(category)
                    else:
                        num_newBB += 1  # indice per le parole senza bb del dataset originale

    print('tot words: %d' % tot_words)
    print('words without original dataset bounding box: %d' % num_newBB)
    print('words with iou more than treshold: %d' % iou_words)
    print('correct words with iou more than treshold: %d' % iou_find_true)
    print('correct words with iou less then treshold: %d' % not_iou_find_true)
    print(correct_words)
    print('precision: %f' % (iou_find_true / tot_words))  # num parole corrette riconosciute / num parole totali
    print('recall: %f' % (iou_find_true / iou_words))  # num parole corrette riconosciute / num parole corrette

    print(final_result)
    pd.Series(final_result).value_counts().plot(kind='bar')
    plt.show()


if __name__ == "__main__":
    iou_threshold()
