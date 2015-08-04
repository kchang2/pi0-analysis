import ROOT as rt
import sys, random, math
import os
import numpy as np

if __name__ == "__main__":
    
    if len(sys.argv)<2:
        print "give a file as input"
        sys.exit()

#load:
    fileName = sys.argv[1]
    tuplelist = np.load(fileName)
    print tuplelist