import csv
import json
from PIL import Image
import os


# legge il file csv e restituisce le righe corrispondenti al img_name e al img_text per ricavare i BB
def get_row_csv(csv_name, img_name, img_text):
    annotation_list = []  # una lista perchè nella stessa immagine ci sono parole ripetute
    with open(csv_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for riga in csv_reader:
            # print(riga)
            if riga[0][0] == '#':
                riga[0] = riga[0].replace('#', '')  # elimino il cancelletto
            if riga[0] == img_name and riga[9] == img_text:
                annotation_list.append(riga)
        return annotation_list


# ritorna i BB dei caratteri della parola e salva le immagini dei char
def get_crop_img(csv_name, img_name, img_text):
    is_vertical = False  # mi indica se il testo da tagliare è in verticale o orizzontale
    ann_list = get_row_csv(csv_name, img_name, img_text)
    # print(ann_list)
    first_img = ann_list[0]  # se c'è più di un testo uguale, prendo per ora il primo

    im = Image.open(csv_name[:-4] + "/" + first_img[0])  # gli passo il nome dell immagine

    left = int(first_img[1])  # 1.1
    bottom = int(first_img[4])  # 2.2 sarebbe la linea bassa orizzontale
    right = int(first_img[3])  # 2.1
    top = int(first_img[6])  # 3.2 sarebbe la linea alta orizzontale
    if top - bottom > right - left:
        dim_x = top - bottom
        is_vertical = True
    else:
        dim_x = right - left

    os.chdir('../')
    #im1 = im.crop((left, bottom, right, top))  # per vedere il bb della parola
    #im1.show()

    # Opening JSON file
    with open('charLength.json', 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)  # è un dizionario

    os.chdir('CSVmarketfiles/')

    # print(json_object)
    somma = 0  # indica la somma dei valori delle lettere che formano il testo
    for letter in img_text:
        somma = somma + json_object[letter]

    charBB = []  # array che andrà a contenere i charBB
    i = 0  # serve per il nome dell immagine
    for letter in img_text:
        crop_dim = json_object[letter] * dim_x / somma
        if is_vertical:
            bottom = top - crop_dim  # vado dall'alto verso il basso
        else:
            right = left + crop_dim
        charBB.append([letter, left, bottom, right, bottom, right, top, left, top])  # scrivo il char e il BB del char

        im1 = im.crop((left, bottom, right, top))
        if is_vertical:
            top = bottom
            im1 = im1.rotate(270)  # ruoto l'immagine
        else:
            left = right

        im1.save('new_img_' + str(i) + letter + img_name)  # salvo l'immagine del carattere
        i += 1

    return charBB


if __name__ == "__main__":
    os.chdir('E-Shop Dataset/CSVmarketfiles/')
    #print(get_crop_img('healthpersonalcare.csv', '0027.jpg', 'ACIDOPHILUS'))
    print(get_crop_img('healthpersonalcare.csv', '0005.jpg', 'HEALTH'))
    print(get_crop_img('grocery.csv', '0017.jpg', 'COINTREAU'))  # bb non rettangolare, risultato non preciso
