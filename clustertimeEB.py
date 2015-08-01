##
## This merge tree files from all the .root > 1 > and extracts all
## data, clustering them in regions of ieta. The difference between
## this and the one by one crystal is that this uses eta clustering,
## which yields faster results.
##
## Updated as of 07/23/2015
## Working as of 07/23/2015
##
import ROOT as rt
import sys, random, math
import time
import os
import numpy as np

import stackNfit as snf
import parameters as p
import assemble as a

from FastProgressBar import progressbar

if __name__ == "__main__":
    
    #Check and change current working directory.
    stardir = os.getcwd()
    print "Current working directory %s" % stardir
    os.chdir(p.rootFileLocation)
    retdir = os.getcwd()
    print "Directory changed successfully %s" % retdir
    
    # Get list of root files in directory
    fileList = os.listdir(retdir)
    
    # Root file name
    rootfilename = p.runNumber + "EcalNtp_"
    
    # number of files to analyze
    if p.numberofFiles == -1:
        nof = len(fileList)
    else:
        nof = p.numberofFiles

    #Here is where it splits based on track and decision
    if p.splitPhotons == True:
        #creates histogram
        htime1 = rt.TH1F("Time Response in Barrel for photon 1", "Eta relation",170,-85,85)
        htime2 = rt.TH1F("Time Response in Barrel for photon 2", "Eta relation",170,-85,85)
    
        #creation of numpy array to store values for faster analysis(courtesy of Ben Bartlett)
        dataList1 = np.array([-1.0, -1.0, -1.0, -1.0, -1.0]) #[eta, mean, mean error, sigma, sigma error]
        dataList2 = np.array([-1.0, -1.0, -1.0, -1.0, -1.0]) #[eta, time response, time response error, time resolution, time resolution error]
    
        #creates a list of histograms (for range of eta)
        histList1 = [0 for eta in range(171)]
        histList2 = [0 for eta in range(171)]
        
        #fills list of histograms with actual histograms
        for eta in range (0,171):
            histname1 = "time on sc eta (%i) for photon 1" %(eta-85)
            histtitle1 = "time response (ns) for eta (%i) for photon 1" %(eta-85)
            histname2 = "time on sc eta (%i) for photon 2" %(eta-85)
            histtitle2 = "time response (ns) for eta (%i) for photon 2" %(eta-85)
            histList1[eta] = rt.TH1F(histname1,histtitle1,1000,-30,30)
            histList2[eta] = rt.TH1F(histname2,histtitle2,1000,-30,30)

        #stacks data onto the histograms
        a.openEB(nof,rootfilename,fileList, p.numberofEntries, histList1, histList2)
    
    # No splitting, joining photon 1,photon 2 together
    else:
        htime = rt.TH1F("Time Response in Barrel for all photons", "Eta relation",170,-85,85)
        dataList = np.array([-1.0, -1.0])
        histList = [0 for eta in range(171)]
        histname = "time on sc eta (%i) for all" %(eta-85)
        histtitle = "time response (ns) for eta (%i) for all" %(eta-85)
        for eta in range (0,171):
            histList[eta] = rt.TH1F(histname,histtitle,1000,-30,30)
        a.openEB(nof,rootfilename,fileList, p.numberofEntries, histList, 0)

    # Same procedure, going back to directory where results are printed
    retdir = os.getcwd()
    print "Current working directory %s" % retdir
    os.chdir(p.resultPath + '/' + p.folderName + '/')
    folder = 'ctEB'+str(int(time.time()))
    os.system('mkdir ' + folder)
    os.chdir(os.getcwd() + '/' + folder +'/')
    retdir = os.getcwd()
    print "Directory changed successfully %s" % retdir

    #fits the histograms and saves 1D in tree
    if p.splitPhotons == True:
        htime1, fitdata1 = snf.fitTimeEta(histList1,htime1)
        htime2, fitdata2 = snf.fitTimeEta(histList2,htime2)

        #saving all 1D histograms in tree
        a.saveEB(p.runNumber,dataList1,dataList2,histList1,histList2,htime1,htime2,fitdata1,fitdata2)
        #saving all data into a numpy file for analyzing later
        np.save("A_etaTimeResponseEB1_0T.npy", dataList1)
        np.save("A_etaTimeResponseEB2_0T.npy", dataList2)

        #Tacks on histogram to canvas frame and ouputs on canvas
        a.printPrettyPictureEB(p.runNumber,htime1,htime2)

    else:
        htime, fitdata = snf.fitTimeEta(histList,htime)
        a.saveEB(p.runNumber,dataList,0,histList,0,htime,0,fitdata,0)
        np.save("etaTimeResponseEBAll_0T.npy", dataList)

        a.printPrettyPictureEB(p.runNumber,htime,0)



