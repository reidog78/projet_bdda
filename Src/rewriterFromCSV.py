#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import sys
from vocabulary import *
from flight import Flight

class RewriterFromCSV(object):

    def __init__(self, voc, df):
        """
        Translate a dataFile using a given vocabulary
        """
        self.vocabulary = voc
        self.dataFile = df

    # Loads data from defined file name
    # Returns an Array of Flights representing all data

    def read (self):
        try:
            with open(self.dataFile, 'r') as source:
                res = []
                for line in source:
                    line = line.strip()
                    if line != "" and line[0] != "#":
                        f = Flight(line, self.vocabulary)
                        res.append(f)
            return res
        except:
            raise Exception("Error while loading the dataFile %s"%(self.dataFile))



    def filteredRead (self, conditions): # conditions comme liste de conditions chacune de la forme [attName, modName, trigg]
        try:
            with open(self.dataFile, 'r') as source:
                res = []
                for line in source:
                    line = line.strip()
                    if line != "" and line[0] != "#":
                        f = Flight(line, self.vocabulary)
                        if f.satisfaisant(conditions):
                            res.append(f)
            return res
        except:
            raise Exception("Error while loading the dataFile %s"%(self.dataFile))

    def rewrite (self, data):
        res = []
        for f in data:
            res.append(f.rewrite())
        return res

    def avgVector (self, rewrData):
        vect = rewrData[0]

        for i in range(1, len(rewrData)):
            for x in range(len(vect)):
                vect[x] = ((vect[x] * i) + rewrData[i][x]) / (i+1)

        return vect

    def readAndRewrite(self):
        try:
            with open(self.dataFile, 'r') as source:
                avgVector = []
                lineNum = 0
                for line in source:
                    line = line.strip()
                    if line != "" and line[0] != "#":

                        f = Flight(line,self.vocabulary)
                        rewr = f.rewrite()

                        if lineNum == 0:
                            avgVector = rewr
                        else:
                            for x in range(len(avgVector)):
                                avgVector[x] = (avgVector[x] * lineNum + rewr[x]) / (lineNum + 1)
                        lineNum = lineNum + 1


                        #print(rewr)
                print('Vecteur moyen')
                return(avgVector)
        except:
            raise Exception("Error while loading the dataFile %s"%(self.dataFile))

    def readAndFilterAndRewrite(self, conditions) :
        res = []
        avgVector = []
        try:
            with open(self.dataFile, 'r') as source:
                for line in source:
                    line = line.strip()
                    if line != "" and line[0] != "#":
                        f = Flight(line,self.vocabulary)

                        if f.satisfaisant(conditions):
                            res.append(f)
                            print(f.rewrite())
                print(len(res))
            for i in range(len(res[0].rewrite())):
                avgVector.append(sum([f.rewrite()[i] for f in res])/len(res))
            print(avgVector)
            return avgVector
        except:
            raise Exception("Error while loading the dataFile %s"%(self.dataFile))

    def cover(self,v2, R): # v2 pattern is [attName, modName]

        sVoc = self.schemasVoc()
        partitions = sVoc[0]
        modalities = sVoc[1]
        i_part = partitions.index(v2[0])
        i = i_part
        while modalities[i] != v2[1]:
            i += 1
        return R[i]

    def dep(self,v2,R,Rv):
        cRv = self.cover(v2,Rv)
        cR = self.cover(v2,R)
        if cR == 0:
            d = 0
        else :
            d = cRv/cR
        return d

    def assoc(self,v2,R,Rv): # correlation entre v2 (un terme de Rv) et le terme v de Rv utilisé pour le filtrage
        d = self.dep(v2,R,Rv)
        if d <= 1:
            a = 0
        else:
            a = 1 - (1/d)
        return a

    def schemasVoc(self): # retourne 2 listes (partitions et modalities) de longueur = nombre de modalities = longueur vecteur reecriture
        voc = self.vocabulary
        parts = list(voc.getPartitions())
        modalities = parts[0].getModNames()
        partitions = [parts[0].getAttName()] * parts[0].getNbModalities()
        for i in range(1,len(parts)):
            modalities += parts[i].getModNames()
            partitions += [parts[i].getAttName()] * parts[i].getNbModalities()
        return partitions,modalities


if __name__ == "__main__":
    if len(sys.argv)  < 3:
        print("Usage: python rewriterFromCSV.py <vocfile> <dataFile>")
    else:
        if os.path.isfile(sys.argv[1]):
            voc = Vocabulary(sys.argv[1])
            if os.path.isfile(sys.argv[2]):
                rw = RewriterFromCSV(voc, sys.argv[2])
                R = rw.avgVector(rw.rewrite(rw.read()))
                condition = ['Distance', 'long', 0.2]
                Rv = rw.avgVector(rw.rewrite(rw.filteredRead([
                    condition])))
                a = rw.assoc(["DepTime","afternoon"],R,Rv)
                print("R = ", R)
                print("Rv = ", Rv)
                print("a = ", a)
            else:
                print("Data file %s not found"%(sys.argv[2]))
        else:
            print("Voc file %s not found"%(sys.argv[2]))
