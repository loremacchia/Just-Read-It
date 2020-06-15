import numpy

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
def nGram(string, jaccardCoeff = 0.6):
    global n
    global dict
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
    for j in range(len(jaccardWords)):
        dist = editDistance(jaccardWords[j], string)
        tupla = (j, dist)
        result.append(tupla)
        
    min = float('inf')
    minIndex = -1
    for j in range(len(result)):
        if min > result[j][1]:
            min = result[j][1]
            minIndex = result[j][0]
    
    if minIndex != -1:
        # print("La parola più vicina a ", string, " è ", jaccardWords[minIndex])
        return (jaccardWords[minIndex], minIndex)
    else:
        # print("La parola ", string, " non ha parole vicine nel dizionario")
        return ("",-1)

def coefficenteJaccard(str1, str2):
    str1 = set(str1)
    str2 = set(str2)
    return float(len(str1 & str2)) / len(str1 | str2)

def editDistance(x, y):
    m = len(x) +1
    n = len(y) +1
    c = numpy.zeros((m, n))
    for i in range(m):
        c[i,0] = i
    for j in range(n):
        c[0,j] = j
    for i in range(1,m):
        for j in range(1,n):
            c[i][j] = float('inf')
            if x[i-1] == y[j-1]:
                c[i][j] = c[i-1][j-1]
            if x[i-1] != y[j-1] and c[i-1][j-1] + 1 < c[i][j]:
                c[i][j] = c[i-1][j-1] + 1
            if i>=2 and j>=2 and x[i-1] == y[j-2] and x[i-2] == y[j-1] and c[i-2][j-2] + 1 < c[i][j]:
                c[i][j] = c[i-2][j-2] + 1
            if c[i-1][j] + 1 < c[i][j]:
                c[i][j] = c[i-1][j] + 1
            if c[i][j-1] + 1 < c[i][j]:
                c[i][j] = c[i][j-1] + 1
    return c[i][j]

def compareStrings(str1, str2):
    res1 = nGram(str1)
    res2 = nGram(str2)
    print(res1)
    print(res2)
    if(res1[1] > res2[1]):
        res2 += (1,)
        return res2
    res1 += (0,)
    return res1

n = 3
dict = createDictionary(n)