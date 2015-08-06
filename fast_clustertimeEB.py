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
        #creates histogram of time
        htime1 = rt.TH1F("Time Response in Barrel for photon 1", "Time Response vs iEta in EB for photon 1; iEta;ns",171,-85,86)
        htime2 = rt.TH1F("Time Response in Barrel for photon 2", "Time Response vs iEta in EB for photon 2; iEta;ns",171,-85,86)
    
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
            histList1[eta] = rt.TH1F(histname1,histtitle1,1200,-30,30)
            histList2[eta] = rt.TH1F(histname2,histtitle2,1200,-30,30)

        #stacks data onto the histograms
        runinfo = a.openEB(rootfilename, rootList, runinfo, bf, ef, p.numberofEntries, histList1, histList2)
    
    # No splitting, joining photon 1, photon 2 together
    else:
        fname = 'c_'
        htime = rt.TH1F("Time Response in Barrel for all photons", "Time Response vs iEta in EB; iEta;ns",171,-85,86)
        dataList = np.array([-1.0, -1.0, -1.0, -1.0, -1.0]) #[eta, mean, mean error, sigma, sigma error]
        
        #creates histogram list
        histList = [0 for eta in range(171)]
        
        for eta in range (0,171):
            histname = "time on sc eta (%i) for all" %(eta-85)
            histtitle = "time response (ns) for eta (%i) for all" %(eta-85)
            histList[eta] = rt.TH1F(histname,histtitle,1000,-30,30)
        runinfo = a.openEB(rootfilename,rootList, runinfo, bf, ef, p.numberofEntries, histList, 0)

    # Same procedure, going back to directory where results are printed
    retdir = os.getcwd()
    print "Current working directory %s" % retdir
    os.chdir(resultLocation + '/' + p.folderName + '/')
    folder = 'ctEB_' + fname + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    os.system('mkdir ' + folder)
    os.chdir(os.getcwd() + '/' + folder +'/')
    retdir = os.getcwd()
    print "Directory changed successfully %s" % retdir
    shutil.copyfile(stardir + '/' + 'unpack.py', retdir + '/unpack.py')
    
    #saving run info to a numpy file for reference later
    np.save(p.runNumber+"EtaRunInfoEB.npy", runinfo)

    #fits the histograms and saves 1D in tree
    if p.splitPhotons == True:
        htime1, fitdata1, seedmap1 = snf.fitTimeEta(histList1,htime1,p.minStat,p.includeHitCounter,p.manualHitCounterCut,"p1_")
        htime2, fitdata2, seedmap2 = snf.fitTimeEta(histList2,htime2,p.minStat,p.includeHitCounter,p.manualHitCounterCut,"p2_")

        #saving all 1D histograms in tree
        a.saveEB(p.runNumber,dataList1,dataList2,histList1,histList2,htime1,htime2,fitdata1,fitdata2,seedmap1,seedmap2)

        #Tacks on histogram to canvas frame and ouputs on canvas
        a.printPrettyPictureEB(p.runNumber,htime1,htime2,seedmap1,seedmap2)

    else:
        htime, fitdata, seedmap = snf.fitTimeEta(histList,htime,p.minStat,p.includeHitCounter,p.manualHitCounterCut,"c_")
        a.saveEB(p.runNumber,dataList,0,histList,0,htime,0,fitdata,0,seedmap,0)

        a.printPrettyPictureEB(p.runNumber,htime,0,seedmap,0)



