##
## This merge tree files from all the .root > 1 > extracts to all
## data, mapping to 1 to 1 crystals. This is the more comprehensive
## result, but runs much slower.
##
## Updated as of 07/24/2015
## Running as of 07/23/2015
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

    # Check current working directory.
    stardir = os.getcwd()
    print "Current working directory %s" % stardir
    
    # Now change the directory
    os.chdir(p.rootFileLocation)
    
    # Check current working directory.
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
        htime1 = rt.TH2F("Time Response in Barrel for photon 1", "iPhi vs. iEta",170,-85,85,360,0,360)
        htime2 = rt.TH2F("Time Response in Barrel for photon 2", "iPhi vs. iEta",170,-85,85,360,0,360)

        #creation of numpy array for faster analysis(courtesy of Ben Bartlett)
        dataList1 = np.array([-1.0, -1.0, -1.0]) #(eta, phi, time response)
        dataList2 = np.array([-1.0, -1.0, -1.0]) #(eta, phi, time response)

        #creates a list of histograms
        histList1 = [[0 for phi in range(361)] for eta in range(171)]
        histList2 = [[0 for phi in range(361)] for eta in range(171)]

        #fills each coordinate with a histogram!
        for eta in range (0,171):
            for phi in range (0,361):
                histname1 = "time on sc (%i,%i) for photon 1" %(eta-85,phi)
                histtitle1 = "time response (ns) for crystal (%i,%i) for photon 1" %(eta-85,phi)
                histname2 = "time on sc (%i,%i) for photon 2" %(eta-85,phi)
                histtitle2 = "time response (ns) for crystal (%i,%i) for photon 2" %(eta-85,phi)
                histList1[eta][phi] = rt.TH1F(histname1,histtitle1,1000,-30,30)
                histList2[eta][phi] = rt.TH1F(histname2,histtitle2,1000,-30,30)

        #stacks data onto the histograms
        a.openEB(nof,rootfilename,fileList, p.numberofEntries, histList1, histList2)

    # No splitting, joining photon 1,photon 2 together
    else:
        htime = rt.TH2F("Time Response in Barrel", "iPhi vs. iEta",170,-85,85,360,0,360)
        dataList = np.array([-1.0, -1.0, -1.0]) #(eta, phi, time response)
        histList = [[0 for phi in range(361)] for eta in range(171)]

        for eta in range (0,171):
            for phi in range (0,361):
                histname = "time on sc (%i,%i)" %(eta-85,phi)
                histtitle = "time response (ns) for crystal (%i,%i)" %(eta-85,phi)
                histList[eta][phi] = rt.TH1F(histname,histtitle,1000,-30,30)

        a.openEB(nof,rootfilename,fileList, p.numberofEntries, histList, 0)

    # Same procedure, going to results directory.
    retdir = os.getcwd()
    print "Current working directory %s" % retdir
    os.chdir(p.resultPath + '/' + p.folderName + '/')
    folder = 'itEB'+str(int(time.time()))
    os.system('mkdir ' + folder)
    os.chdir(os.getcwd() + '/' + folder +'/')
    retdir = os.getcwd()
    print "Directory changed successfully %s" % retdir

    #fits the histograms and saves 1D in tree
    if p.splitPhotons == True:
        htime1, fitdata1 = snf.fitTime(histList1,htime1)
        htime2, fitdata2 = snf.fitTime(histList2,htime2)
        a.saveEB(p.runNumber,dataList1,dataList2,histList1,histList2,htime1,htime2,fitdata1,fitdata2)
        np.save("TimeResponseEB1_0T.npy", dataList1)
        np.save("TimeResponseEB2_0T.npy", dataList2)

        #Tacks on histogram to canvas frame and ouputs on canvas
        a.printPrettyPictureEB(p.runNumber,htime1,htime2)
    else:
        htime, fitdata = snf.fitTime(histList,htime)
        a.saveEB(p.runNumber,dataList,0,histList,0,htime,0,fitdata,0)
        np.save("TimeResponseEB_0T.npy", dataList)
        
        a.printPrettyPictureEB(p.runNumber,htime1,0)


