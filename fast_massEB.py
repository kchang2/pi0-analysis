##
## This merge tree files from all the .root > 1 > and extracts all
## data, clustering them in regions of ieta. The difference between
## this and the one by one crystal is that this uses eta clustering,
## which yields faster results.
##
## Updated as of 07/28/2015
## NOT Running as of 07/28/2015
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
    
    #input comes in from the fastAnalysis as [script, path of ROOT file, path of Result directory, starting position in the list of files in the 'path of ROOT file', ending position in the list of files in 'path of ROOT file']
    fileLocation = sys.argv[1]
    resultLocation = sys.argv[2]
    bf = int(sys.argv[3])
    ef = int(sys.argv[4])
    
    
    #Check and change current working directory.
    stardir = os.getcwd()
    print "Current working directory %s" % stardir
    os.chdir(fileLocation)
    retdir = os.getcwd()
    print "Directory changed successfully %s" % retdir

    ## Root file path and file name you analyze ##
    rootList = os.listdir(fileLocation)
    rootfilename = p.runNumber + "EcalNtp_"
    
    ## Info about the Run ##
    runinfo = np.array("ROOT info") #ROOT file

    #creation of numpy array to store values for faster analysis(courtesy of Ben Bartlett)
    dataListf = np.array([-1.0, "root file"]) #(mass, by file [bins of 5]
    dataListr = np.array([-1.0, "week of run"]) #(mass, by run)
    
    #creates a list of histograms (corresponding to) and root files used
    histList = []
    runinfo = []
    
    #creates 1 histogram for run
    histRun = rt.TH1F("Average Pi0 mass for select run","Pi0 mass (GeV) for select run",1000,0,1)

    #fit
    runinfo, histList, histRun = a.openMass(rootfilename, rootList, runinfo, bf, ef, p.numberofEntries,histList, histRun)

    # Same procedure, going back to directory where results are printed
    retdir = os.getcwd()
    print "Current working directory %s" % retdir
    os.chdir(resultLocation + '/' + p.folderName + '/')
    folder = 'massEB' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    os.system('mkdir ' + folder)
    os.chdir(os.getcwd() + '/' + folder +'/')
    retdir = os.getcwd()
    print "Directory changed successfully %s" % retdir
    shutil.copyfile(stardir + '/' + 'unpack.py', retdir + '/unpack.py')



    #fits the histograms and saves 1D in tree
    massvalues = snf.fitMassROOT(histList)
    avemass = snf.fitMass(histRun)

    # Same procedure, going back to original working directory.
    retdir = os.getcwd()
    print "Current working directory %s" % retdir
    os.chdir( startdir + "/result/")
    retdir = os.getcwd()
    print "Directory changed successfully %s" % retdir

    #saving all 1D histograms in tree
    f = rt.TFile("MassEBAll_"+str(int(time.time()))+".root","new")
    for file in range(0,len(histList)):
        histList[file].Write()
        histRun.Write()
        #Saving value of data in tuple list
        dataListf = np.vstack((dataListf, [massvalues[file], runinfo[file]]))
    dataListr = np.vstack((dataListr, [avemass, '2015A']))
    print avemass

    np.save("MassEBf_0T.npy", dataListf)
    np.save("MassEBr_0T.npy", dataListr)
