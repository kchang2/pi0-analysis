##
## This merge tree files from all the .root > 1 > extracts to all
## data, mapping to 1 to 1 crystals. This is the more comprehensive
## result, but runs much slower.
##
## Updated as of 08/04/2015
## Running as of 08/04/2015
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

    #Here is where it splits based on track and decision
    if p.splitPhotons == True:
        fname = 'p1p2_'
        #creates histogram
        htime1 = rt.TH2F("Time Response in Barrel for photon 1", "Time Response in EB for photon 1; iEta;iPhi;ns",170,-85,85,360,0,360)
        htime2 = rt.TH2F("Time Response in Barrel for photon 2", "Time Response in EB for photon 2; iEta;iPhi;ns",170,-85,85,360,0,360)

        #creation of numpy array for faster analysis(courtesy of Ben Bartlett)
        dataList1 = np.array([-1.0, -1.0, -1.0, -1.0, -1.0, -1.0]) #(eta, phi, mean, mean error, sigma, sigma error)
        dataList2 = np.array([-1.0, -1.0, -1.0, -1.0, -1.0, -1.0]) #(eta, phi, time response, time response error, time resolution, time resolution error)

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
                histList1[eta][phi] = rt.TH1F(histname1,histtitle1,1200,-30,30)
                histList2[eta][phi] = rt.TH1F(histname2,histtitle2,1200,-30,30)

        #stacks data onto the histograms
        runinfo = a.openEB(rootfilename, rootList, runinfo, bf, ef, p.numberofEntries, histList1, histList2)

    # No splitting, joining photon 1,photon 2 together
    else:
        fname = 'c_'
        htime = rt.TH2F("Time Response in Barrel", "Time Response in Barrel; iEta;iPhi;ns",170,-85,85,360,0,360)
        dataList = np.array([-1.0, -1.0, -1.0, -1.0, -1.0, -1.0]) #(eta, phi, time response, time response error, time resolution, time resolution error)
        histList = [[0 for phi in range(361)] for eta in range(171)]

        for eta in range (0,171):
            for phi in range (0,361):
                histname = "time on sc (%i,%i)" %(eta-85,phi)
                histtitle = "time response (ns) for crystal (%i,%i)" %(eta-85,phi)
                histList[eta][phi] = rt.TH1F(histname,histtitle,1000,-30,30)

        runinfo = a.openEB(rootfilename,rootList, runinfo, bf, ef, p.numberofEntries, histList, 0)

    # Same procedure, going to results directory.
    retdir = os.getcwd()
    print "Current working directory %s" % retdir
    os.chdir(resultLocation + '/' + p.folderName + '/')
    folder = 'itEB_'+ fname + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    os.system('mkdir ' + folder)
    os.chdir(os.getcwd() + '/' + folder +'/')
    retdir = os.getcwd()
    print "Directory changed successfully %s" % retdir
    shutil.copyfile(stardir + '/' + 'unpack.py', retdir + '/unpack.py')
    
    #saving run info to a numpy file for reference later
    np.save(p.runNumber+"IndivRunInfoEB.npy", runinfo)

    #fits the histograms and saves 1D in tree
    if p.splitPhotons == True:
        htime1, fitdata1, seedmap1 = snf.fitTime(histList1,htime1,p.minStat,p.includeHitCounter,p.manualHitCounterCut,"p1_")
        htime2, fitdata2, seedmap2 = snf.fitTime(histList2,htime2,p.minStat,p.includeHitCounter,p.manualHitCounterCut,"p2_")
        
        #saving all 1D and 2D histogram(s) in tree
        a.saveEB(p.runNumber,dataList1,dataList2,histList1,histList2,htime1,htime2,fitdata1,fitdata2,seedmap1,seedmap2)

        #Tacks on histogram to canvas frame and ouputs on canvas
        a.printPrettyPictureEB(p.runNumber,htime1,htime2,seedmap1,seedmap2)
    else:
        htime, fitdata, seedmap = snf.fitTime(histList,htime,p.minStat,p.includeHitCounter,p.manualHitCounterCut,"c_")
        a.saveEB(p.runNumber,dataList,0,histList,0,htime,0,fitdata,0,seedmap,0)
        
        a.printPrettyPictureEB(p.runNumber,htime,0,seedmap,0)

