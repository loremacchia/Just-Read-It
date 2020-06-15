import json
import csv
import os
from urllib.request import urlretrieve


list_products = ['artworks.csv', 'beauty.csv', 'biscuits.csv', 'books.csv', 'boystops.csv', 'cerealporridge.csv',
                 'grocery.csv', 'healthpersonalcare.csv', 'homecarecleaning.csv', 'petsupplies.csv',
                 'sweetschocolate.csv', 'toysgames.csv', 'vhs.csv']


# legge il file csv e restituisce i numeri (tipo string) di riga degli URL di immagini con testo
def read_number_row_csv(csv_name):
    string_set = set()  # uso set per avere elementi unici
    print(os.getcwd())
    with open(csv_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for riga in csv_reader:
            if riga[0][0] == '#':
                riga[0] = riga[0].replace('#', '')  # elimino il cancelletto
            numb = riga[0].split('.')[0]
            string_set.add(numb)
        return string_set


# passo in ingresso il nome del file csv e il numero di url da controllare per il download (se num_url == None allora vengono prese tutte le immagini della cartella)
def download_url(csv_name, type_prod, num_url = None):
    wdir = os.getcwd()
    # Se la working directory al momento non è corretta viene cambiata per vedere E-Shop Dataset/amazon-scrape.json
    if not os.path.isfile('amazon-scrape.json'):
        os.chdir('./E-Shop Dataset')

    # Opening JSON file
    with open('amazon-scrape.json', 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)  # è un dizionario nidificato

    number_set = set(map(int, read_number_row_csv(csv_name)))
    sort_str_list = sorted(read_number_row_csv(csv_name))  # il set diventa una lista ordinata
    ind = 0  # indice utilizzato per la rinominazione delle immagini

    # Crea una cartella dove mettere tutti i download delle immagini 
    if(not os.path.isdir('../images/'+type_prod)):
        os.mkdir('../images/'+type_prod)
    os.chdir('../images/'+type_prod)
    print(number_set)

    if num_url != None: # Prende solo le prime num_url immagini del file
        # print(sorted(read_number_row_csv(csv_name)))
        for x in range(0, num_url):
            # scarico solo le immagini presenti nel file csv, quelle con testo
            if x + 1 in number_set:
                my_url = json_object[type_prod]['urls'][x]  # ottengo l'url del prodotto specificato
                my_file = my_url.split('/')
                print("Download jpg")
                # scarico l'immagine
                urlretrieve(my_url, my_file[5])
                # rinomino l'immagine con il corrispettivo nome del file csv
                os.rename(my_file[5], sort_str_list[ind] + '.jpg')
                ind += 1
                print("End.")
    else: # Prende tutte le immagini del file
        for x in number_set:
            my_url = json_object[type_prod]['urls'][x - 1]  # ottengo l'url del prodotto specificato
            my_file = my_url.split('/')
            print("Download jpg")
            # scarico l'immagine
            urlretrieve(my_url, my_file[5])
            # rinomino l'immagine con il corrispettivo nome del file csv
            os.rename(my_file[5], sort_str_list[ind] + '.jpg')
            ind += 1
            print("End.")
    os.chdir(wdir)
    return "./images/"+type_prod
    


# creo il dizionario con le scritte dei prodotti di un determinato file csv
def dictionary_dataset():
    string_set = set()  # uso set per avere elementi unici
    for file in os.listdir("CSVmarketfiles"):
        if file.endswith(".csv"):
            with open('CSVmarketfiles/'+file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for riga in csv_reader:
                    numb = riga[9]  # posizione dove c'è il testo
                    string_set.add(numb)
    return sorted(string_set)  # in output ottengo una lista ordinata di parole


if __name__ == "__main__":
    # Itera su tutti i file della cartella e scarica le relative immagini 
    for file in os.listdir("CSVmarketfiles"):
        if file.endswith(".csv"):
            download_url('CSVmarketfiles/'+file, file[:-4])
    # download_url('CSVmarketfiles/healthpersonalcare.csv', 'healthpersonalcare', 10)
    # dict = dictionary_dataset()
    # f=open('Tesseract/dictionary.txt','w')
    # for ele in dict:
    #     f.write(ele+'\n')
    
    # print(len(dictionary_dataset()))
