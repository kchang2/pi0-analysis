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
import time, copy
import os
import stackNfit as snf
import numpy as np

from FastProgressBar import progressbar

if __name__ == "__main__":
    
    #Check and change current working directory.
    retdir = os.getcwd()
    print "Current working directory %s" % retdir
    os.chdir('..')
    startdir = retdir = os.getcwd()
    os.chdir( retdir + '/ALL_2015A_RAW_Test1/cfgFile/Fill/output/' )
    retdir = os.getcwd()
    print "Directory changed successfully %s" % retdir

    # Get list of root files in directory
    fileList = os.listdir(retdir)
    
    #creation of numpy array to store values for faster analysis(courtesy of Ben Bartlett)
    dataListf = np.array([-1.0, "root file"]) #(mass, by file [bins of 5]
    dataListr = np.array([-1.0, "week of run"]) #(mass, by run)
    
    #creates a list of histograms (for range of ROOT files)
    histList = []
    
    #creates 1 histogram for run
    histRun = rt.TH1F("Average Pi0 mass for Run 2015A","Pi0 mass (GeV) for Run 2015A",1000,0,1)
    
    #creates a list of root files used
    roofiles = []

    for k in range(0,len(fileList)):
        if "2015A_EcalNtp_" in fileList[k]:
            roofiles.append(fileList[k])
            rootFile = rt.TFile.Open(fileList[k])
            rTree = rootFile.Get("Tree_Optim")
            print "successfully cut branch from " + fileList[k]
            #rootFile.Print("v")
            
            #makes the histogram for pi0 mass
            histname = "Average Pi0 mass in Barrel for time instance (%s)" %(fileList[k])
            histtitle = "Pi0 mass (GeV) for ROOT file cluster (%s)" %(fileList[k])
            histmass = rt.TH1F(histname,histtitle,1000,0,1)
            
            #fills the mass histogram list with ROOT files oriented folder
            histmass = snf.stackMass(rTree,histmass)
            histList.append(copy.copy(histmass))
            #print histmass
            #print histList[0]

            #Fills large histogram for the entire run's dataset
            histRun = snf.stackMass(rTree,histRun)

            rootFile.Close()

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
        dataListf = np.vstack((dataListf, [massvalues[file], roofiles[file]]))
    dataListr = np.vstack((dataListr, [avemass, '2015A']))
    print avemass

    np.save("MassEBf_0T.npy", dataListf)
    np.save("MassEBr_0T.npy", dataListr)
