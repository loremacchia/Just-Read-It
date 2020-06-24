import numpy
from difflib import SequenceMatcher

def createDictionary(n):
    dict = {}
    parole = getWords()
    for i in range(len(parole)): #ciclo su tutte le parole del lessico
        for j in range(len(parole[i]) - n + 1): #ciclo per spezzettare le parole in trigrammi
            current = parole[i][j:j + n]
            if dict.get(current) != None: #se il trigramma è già presente nel dizionario aggiungo alla sua lista la parola attuale
                dict[current].append(parole[i])
            else: #altrimenti creo una nuova lista in cui il primo elemeno è la parola attuale
                dict[current] = [parole[i]]
    return dict

def getWords():
    f = open('./crnn.pytorch-master/dictionaryLarge.txt').read()
    parole = []
    for word in f.split():  # parole è una lista che contiene tutte le parole del dizionario
        parole.append(word)
    return parole

# Usare come nGram("gigi")
def nGram(string, jaccardCoeff = 0.8):
    global n
    global dict
    if(string is not None):
        string = string.lower()
        listaParole = []
        for j in range(len(string) - n + 1):  # ciclo per spezzettare la parola in trigrammi
            current = string[j:j + n]
            if dict.get(current) != None:
                listaParole.extend(dict[current])
        jaccardWords = []
        for i in range(len(listaParole)):
            coef = coefficenteJaccard(string, listaParole[i])
            if jaccardCoeff < coef :
                jaccardWords.append(listaParole[i])
        result = []
        for word in jaccardWords:
            ratio = SequenceMatcher(None, word.lower(), string.lower()).ratio()
            if ratio > 0.9 and len(string) == len(word):
                result.append(1)
                result.append(ratio)
                result.append(string)
                result.append(word)  # word del dizionario
                return result
    result = [-1, -1, None, None]
    return result

def coefficenteJaccard(str1, str2):
    str1 = set(str1)
    str2 = set(str2)
    return float(len(str1 & str2)) / len(str1 | str2)


def control_distance(target_word):
    global words
    if target_word is None:
        return None
    result = []
    list_words = words
    for word in list_words:
        ratio = SequenceMatcher(None, word.lower(), target_word.lower()).ratio()
        if ratio > 0.9 and len(target_word) == len(word):
            print(target_word)
            print(word)
            result.append(1)
            result.append(ratio)
            result.append(target_word)
            result.append(word)  # word del dizionario
            return result

    result = [-1, -1, None, None]
    return result


n = 3
dict = createDictionary(n)
words = getWords()

if __name__ == "__main__":
    print(control_distance(None))
    print(control_distance("Hello"))
    print(control_distance("mulino"))
    print(control_distance("breen"))
    print(nGram(None))
    print(nGram("Hello"))
    print(nGram("mulino"))
    print(nGram("breen"))
