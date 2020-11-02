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

    def readAndFilter(self, conditions) :
        res = []
        try:
            with open(self.dataFile, 'r') as source:
                for line in source:
                    line = line.strip()
                    if line != "" and line[0] != "#":
                        f = Flight(line,self.vocabulary)

                        if f.satisfaisant(conditions):
                            res.append(f)
                            #print(f.rewrite())
                print(len(res))
        except:
            raise Exception("Error while loading the dataFile %s"%(self.dataFile))


if __name__ == "__main__":
    if len(sys.argv)  < 3:
        print("Usage: python rewriterFromCSV.py <vocfile> <dataFile>")
    else:
        if os.path.isfile(sys.argv[1]):
            voc = Vocabulary(sys.argv[1])
            if os.path.isfile(sys.argv[2]):
                rw = RewriterFromCSV(voc, sys.argv[2])
                rw.readAndFilter([
                    ['Distance', 'long', 0.2],
                    ['Origin', 'big', 0.9]
                ])
            else:
                print("Data file %s not found"%(sys.argv[2]))
        else:
            print("Voc file %s not found"%(sys.argv[2]))
