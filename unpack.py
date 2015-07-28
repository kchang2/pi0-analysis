import ROOT as rt
import sys, random, math
import os
import stackNfit as snf
import numpy as np

if __name__ == "__main__":
    
    if len(sys.argv)<2:
        print "give a file as input"
        sys.exit()

    #Check and change current working directory.
    retdir = os.getcwd()
    print "Current working directory %s" % retdir
    os.chdir('..')
    startdir = retdir = os.getcwd()
    os.chdir( retdir + '/result/' )
    retdir = os.getcwd()
    print "Directory changed successfully %s" % retdir

    #load:
    fileName = sys.argv[1]
    tuplelist = np.load(fileName)
    print tuplelist