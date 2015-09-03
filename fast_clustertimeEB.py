##
## This merge tree files from all the .root > 1 > and extracts all
## data, clustering them in regions of ieta. The difference between
## this and the one by one crystal is that this uses eta clustering,
## which yields faster results.
##
## Running as of 08/19/2015
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
    rootList.sort()
    rootfilename = p.runNumber + "EcalNtp_"
    
    ## Info about the Run ##
    runinfo = np.array("ROOT info") #ROOT file
    
    #Here is where it splits based on track and decision
    if p.splitPhotons == True: #separating photon 1 and 2
        fname = 'p1p2_'
        #creates histogram of time, transparency
        htime1 = rt.TH1F("Time Response in Barrel for photon 1", "Time Response vs iEta in EB for photon 1; iEta;ns",171,-85,86)
        htime2 = rt.TH1F("Time Response in Barrel for photon 2", "Time Response vs iEta in EB for photon 2; iEta;ns",171,-85,86)
        hlaser1 = rt.TH1F("Crystal Transparency in Barrel for photon 1","Laser Transparency vs iEta in EB for photon 1; iEta;Transparency",171,-85,86)
        hlaser2 = rt.TH1F("Crystal Transparency in Barrel for photon 2","Laser Transparency vs iEta in EB for photon 2; iEta;Transparency",171,-85,86)
    
        #creation of numpy array to store values for faster analysis(courtesy of Ben Bartlett)
        dataList1 = np.array([]) # 9 data entries - [eta, ieta, counts, mean, mean error, sigma, sigma error, t mean, t mean error]
        dataList2 = np.array([]) # 9 data entries - [eta, ieta, counts, time response, time response error, time resolution, time resolution error, laser transparency mean, laser transparency error]
    
        #creates a list of histograms (for range of eta)
        histList1 = [0 for eta in range(171)] #time response
        histList2 = [0 for eta in range(171)]
        transList1 = [0 for eta in range(171)] #laser transparency
        transList2 = [0 for eta in range(171)]
        
        #fills list of histograms with actual histograms, 1 for time response and 1 for transparency
        for eta in range (0,171):
            histname1 = "time on sc eta (%i) for photon 1" %(eta-85)
            histtitle1 = "time response (ns) for eta (%i) for photon 1" %(eta-85)
            histname2 = "time on sc eta (%i) for photon 2" %(eta-85)
            histtitle2 = "time response (ns) for eta (%i) for photon 2" %(eta-85)
            histList1[eta] = rt.TH1F(histname1,histtitle1,1200,-30,30)
            histList2[eta] = rt.TH1F(histname2,histtitle2,1200,-30,30)
        
            transname1 = "transparency on sc eta (%i) for photon 1" %(eta-85)
            transtitle1 = "transparency for eta (%i) for photon 1" %(eta-85)
            transname2 = "transparency on sc eta (%i) for photon 2" %(eta-85)
            transtitle2 = "transparency for eta (%i) for photon 2" %(eta-85)
            transList1[eta] = rt.TH1F(transname1,transtitle1,1000,-5,5)
            transList2[eta] = rt.TH1F(transname2,transtitle2,1000,-5,5)

        #stacks data onto the histograms
        runinfo = a.openEB(rootfilename, rootList, runinfo, bf, ef, p.numberofEntries, histList1, histList2, transList1, transList2)
    
    # No splitting, joining photon 1, photon 2 together
    else:
        fname = 'c_'
        htime = rt.TH1F("Time Response in Barrel", "Time Response vs iEta in EB; iEta;ns",171,-85,86)
        hlaser = rt.TH1F("Crystal Transparency in Barrel","Laser Transparency vs iEta in EB; iEta; Transparency",171,-85,86)
        dataList = np.array([]) # 9 data entries - [eta, ieta, counts, mean, mean error, sigma, sigma error, t mean, t mean error]
        
        #creates histogram list
        histList = [0 for eta in range(171)]
        transList = [0 for eta in range(171)]
        
        for eta in range (0,171):
            histname = "time on sc eta (%i) for all" %(eta-85)
            histtitle = "time response (ns) for eta (%i) for all" %(eta-85)
            histList[eta] = rt.TH1F(histname,histtitle,1000,-30,30)
            transname = "transparency on sc eta (%i) for all" %(eta-85)
            transtitle = "transparency for eta (%i) for all" %(eta-85)
            transList[eta] = rt.TH1F(transname,transtitle,2000,-5,5)
        
        runinfo = a.openEB(rootfilename,rootList, runinfo, bf, ef, p.numberofEntries, histList, 0, transList, 0)

    # Same procedure, going back to directory where results are printed
    retdir = os.getcwd()
    print "Current working directory %s" % retdir
    os.chdir(resultLocation + '/' + p.folderName + '/')
    folder = 'ctEB_' + fname + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    os.system('mkdir ' + folder)
    os.chdir(os.getcwd() + '/' + folder +'/')
    retdir = os.getcwd()
    print "Directory changed successfully %s" % retdir
    shutil.copytree(stardir + '/' + 'preresult package', retdir + '/QA')
#    shutil.copyfile(stardir + '/' + 'unpack.py', retdir + '/unpack.py')
    shutil.copyfile(stardir + '/' + 'setstyle.C', retdir + '/setstyle.c')
#    shutil.copyfile(stardir + '/' + 'fast_restack.py', retdir + '/fast_Restack.py')

    #saving run info to a numpy file for reference later
    np.save(p.runNumber+"EtaRunInfoEB.npy", runinfo)

    #fits the histograms and saves 1D in tree
    if p.splitPhotons == True:
        htime1, hlaser1, fitdata1, seedmap1 = snf.fitTimeEta(histList1, transList1, htime1, hlaser1, p.minStat, p.minNormal, p.includeSeedMap, p.manualHitCounterCut, "p1_", p.graphs2printEB)
        htime2, hlaser2, fitdata2, seedmap2 = snf.fitTimeEta(histList2, transList2, htime2, hlaser2, p.minStat, p.minNormal, p.includeSeedMap, p.manualHitCounterCut, "p2_", p.graphs2printEB)

        #saving all 1D histograms in tree
        a.saveEB(p.runNumber,dataList1,dataList2,histList1,histList2,transList1,transList2,htime1,htime2,hlaser1,hlaser2,fitdata1,fitdata2,seedmap1,seedmap2)

        #Tacks on histogram to canvas frame and ouputs on canvas
        a.printPrettyPictureEB(p.runNumber,htime1,htime2,hlaser1,hlaser2,seedmap1,seedmap2)

    else:
        htime, hlaser, fitdata, seedmap = snf.fitTimeEta(histList, transList, htime, hlaser, p.minStat, p.minNormal, p.includeSeedMap, p.manualHitCounterCut, "c_", p.graphs2printEB)
        a.saveEB(p.runNumber,dataList,0,histList,0,transList,0,htime,0,hlaser,0,fitdata,0,seedmap,0)

        a.printPrettyPictureEB(p.runNumber,htime,0,hlaser,0,seedmap,0)



