import sys
from vocabulary import *
from rewriterFromCSV import *

vocFile = "./../Data/FlightsVoc2.txt"
dataFile = "./../Data/extrait_2008.csv"


if __name__ == "__main__": # Usage: python avgFilteredRead.py <attName1,modName1,trigg1> <attName2,modName2,trigg2> ...
    conditions = [sys.argv[i].split(",") for i in range(1,int(len(sys.argv)-1))]
    for c in conditions:
        c[2] = float(c)
    voc = Vocabulary(vocFile)
    rw = RewriterFromCSV(voc, dataFile)
    res = rw.rewrite(rw.filteredRead(conditions))
    avg = rw.avgVector(res)

    sV = rw.schemasVoc()
    partitions = sV[0]
    modalities = sV[1]
    entetes = ["attrName","modName","deg"]
    f = open('avgFilteredRead.csv', 'w')
    ligneEntete = ",".join(entetes) + "\n"
    f.write(ligneEntete)
    for i in range(len(avg)):
            attrName = partitions[i]
            modName = modalities[i]
            deg = str(avg[i])
            ligne = ",".join([attrName, modName, deg]) + "\n"
            f.write(ligne)

    f.close()


