import numpy
from difflib import SequenceMatcher


def getWords():
    f = open('./crnn.pytorch-master/dictionaryLarge.txt').read()
    #f = open('dictionaryLarge.txt').read()
    parole = []
    for word in f.split():  # parole è una lista che contiene tutte le parole del dizionario
        parole.append(word)
    return parole

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

words = getWords()

if __name__ == "__main__":
    print(control_distance(None))
    print(control_distance("Hello"))
    print(control_distance("mulino"))
    print(control_distance("breen"))
