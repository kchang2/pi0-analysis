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
import time
import os
import stackNfit as snf
import numpy as np

from FastProgressBar import progressbar

if __name__ == "__main__":
    
    #creates histogram
    hmass = rt.TH1F("Pi0 Mass in Barrel", "Time Change",170,-85,85)
    
    #creation of numpy array to store values for faster analysis(courtesy of Ben Bartlett)
    dataList = np.array([-1.0, -1.0])
    
    #creates a list of histograms (for range of eta)
    histList = [0 for eta in range(171)]

    for eta in range (0,171):
        histname = "Pi0 mass on sc eta (%i) for all" %(eta-85)
        histtitle = "Pi0 mass (GeV) for eta (%i) for all" %(eta-85)
        
        histList[eta] = rt.TH1F(histname,histtitle,1000,-30,30)

    #Check and change current working directory.
    retdir = os.getcwd()
    print "Current working directory %s" % retdir
    os.chdir('..')
    startdir = retdir = os.getcwd()
    os.chdir( retdir + '/output/' )
    retdir = os.getcwd()
    print "Directory changed successfully %s" % retdir


    # Get list of root files in directory
    fileList = os.listdir(retdir)

    for k in range(0,len(fileList)):
        if "2015A_EcalNtp_" in fileList[k]:
            rootFile = rt.TFile.Open(fileList[k])
            rTree = rootFile.Get("Tree_Optim")
            print "successfully cut branch from " + fileList[k]
            #rootFile.Print("v")
            
            #fills the histogram with data
            histList = snf.stackMassEta(rTree,histList)
            rootFile.Close()

    #fits the histograms and saves 1D in tree
    hmass = snf.fitMassEta(histList,hmass)

    # Same procedure, going back to original working directory.
    retdir = os.getcwd()
    print "Current working directory %s" % retdir
    os.chdir( startdir + "/result/")
    retdir = os.getcwd()
    print "Directory changed successfully %s" % retdir
    
    #Progress bar for the saves
    pbar = progressbar("saving data", 171).start()
    
    #saving all 1D histograms in tree
    f = rt.TFile("clusterMassEB_"+str(int(time.time()))+".root","new")
    for eta in range(0,len(histList)):
        histList[eta].Write()
        #Saving value of data in tuple list
        dataList = np.vstack((dataList, [eta-85, hmass.GetBinContent(eta+1)]))
        pbar.update(i+1)
    hmass.Write()

    np.save("etaMassResponseEB_0T.npy", dataList)
    pbar.finish()
    
    
    #Tacks on histogram to canvas frame and ouputs on canvas
    htime.plotOn(frame)
    c = rt.TCanvas()
    htime.Draw()
    c.Print("etaMassResponseEB_0T.png")
