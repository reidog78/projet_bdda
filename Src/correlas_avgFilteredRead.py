import sys
from vocabulary import *
from rewriterFromCSV import *

vocFile = "./../Data/FlightsVoc2.txt"
dataFile = "./../Data/extrait_2008.csv"


if __name__ == "__main__": # Usage: python correlas_avgFilteredRead.py <attName1,modName1,trigg1> <attName2,modName2,trigg2> ...
    conditions = [sys.argv[i].split(",") for i in range(1,int(len(sys.argv)))]
    for c in conditions:
        c[2] = float(c[2])
    voc = Vocabulary(vocFile)
    rw = RewriterFromCSV(voc, dataFile)
    Rv = rw.avgVector(rw.rewrite(rw.filteredRead(conditions)))
    R = rw.avgVector(rw.rewrite(rw.read()))
    sVoc = rw.schemasVoc()
    partitions = sVoc[0]
    modalities = sVoc[1]
    entetes = ["attrName","modName","deg","correl"]
    f = open('correls_avgFilteredRead.csv', 'w')
    ligneEntete = ",".join(entetes) + "\n"
    f.write(ligneEntete)
    for i in range(len(Rv)):
            attrName = partitions[i]
            modName = modalities[i]
            deg = str(Rv[i])
            correl = str(rw.assoc([attrName,modName], R, Rv))
            ligne = ",".join([attrName, modName, deg, correl]) + "\n"
            f.write(ligne)

    f.close()


