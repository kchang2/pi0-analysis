##
## This merge tree files from all the .root > 1 > and extracts all
## data, clustering them in regions of ieta. The difference between
## this and the one by one crystal is that this uses eta clustering,
## which yields faster results.
##
## Updated as of 08/03/2015
## Running as of 08/03/2015
##
import ROOT as rt
import sys, random, math
import time, datetime
import os, shutil
import numpy as np

import stackNfit as snf
import parameters as p
import fast_assemble as a

from FastProgressBar import progressbar

if __name__ == "__main__":
    #Check and change current working directory.
    stardir = os.getcwd()
    print "Current working directory %s" % stardir
    if p.runFormat == 'L':
        os.chdir(p.resultPathLocal + folderName + '/')
    else:
        os.chdir(resultPathLXPLUS + folderName + '/')
    retdir = os.getcwd()
    print "Directory changed successfully %s" % retdir

    if isEE = True: #endcap analysis
#EE+, EE-
        #rip images into 1 folder (time response + transparency)
        #fit all crystals photon 1 and 2 TOGETHER in 1 plot (response vs time, transparency vs time, response vs. transparency)
        ######fit all crystals photons 1 and 2 SEPARATRELY in 1 plot
        #rip all images in 1 folder
    else: #barrel analysis
#eta
#individual