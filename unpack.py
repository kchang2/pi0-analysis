##
## Simple quick code to print out whatever
## npy files gets produced by the package.
## This can be used as an example or framework
## into more analysis.
##
## Imported into EVERY result folder that gets
## produced. Not really all results though..
##
##
## Running as of 08/19/2015 (MM/DD/YYYY)
##
##

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