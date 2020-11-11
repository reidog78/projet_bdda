import sys
from vocabulary import *
from rewriterFromCSV import *

vocFile = "./../Data/FlightsVoc2.txt"
dataFile = "./../Data/extrait_2008.csv"


if __name__ == "__main__": # Usage: python avgRead.py

    voc = Vocabulary(vocFile)
    rw = RewriterFromCSV(voc, dataFile)
    res = rw.rewrite(rw.read())
    avg = rw.avgVector(res)

    print(avg)
    sV = rw.schemasVoc()
    partitions = sV[0]
    modalities = sV[1]

    entetes = ["attrName","modName","deg"]
    f = open('avgRead.csv', 'w')
    ligneEntete = ",".join(entetes) +"\n"
    f.write(ligneEntete)
    for i in range(len(avg)):
            attrName = partitions[i]
            modName = modalities[i]
            deg = str(avg[i])
            ligne = ",".join([attrName, modName, deg]) +"\n"
            f.write(ligne)

    f.close()
