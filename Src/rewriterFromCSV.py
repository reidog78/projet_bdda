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
                print(avgVector)
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
        except:
            raise Exception("Error while loading the dataFile %s"%(self.dataFile))

    def cover(self,v, R): # v is a condition = [attName, modName, trigg]
        parts = self.vocabulary.getPartitions()
        j = 0
        i = 0
        found = False
        while not (found):
            mod = parts[j].getModalities()[i]
            if parts[j].getAttName() == v[0] and mod.getName() == v[1]:
                found = True
            elif c == parts[j].getNbModalities():
                j += 1
                c = 0
                i += 1
            else:
                c += 1
                i += 1
        return R[i]

    def dep(self,v2,R,Rv):
        return (self.cover(v2,Rv)/self.cover(v2,R))

    def assoc(self,v2,R,Rv):
        d = self.dep(v2,R,Rv)
        if d <= 1:
            a = 0
        else:
            a = 1 - (1/d)
        return a


if __name__ == "__main__":
    if len(sys.argv)  < 3:
        print("Usage: python rewriterFromCSV.py <vocfile> <dataFile>")
    else:
        if os.path.isfile(sys.argv[1]):
            voc = Vocabulary(sys.argv[1])
            if os.path.isfile(sys.argv[2]):
                rw = RewriterFromCSV(voc, sys.argv[2])
                rw.readAndFilterAndRewrite([
                    ['Distance', 'long', 0.2],
                    ['Origin', 'main', 0.6]
                ])
            else:
                print("Data file %s not found"%(sys.argv[2]))
        else:
            print("Voc file %s not found"%(sys.argv[2]))
