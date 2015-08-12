
##
## Tutorial for drawing a histogram plot (2D) from tree variables
## in the endcap region. We want a general time resolution to see
## which sections are affected the most.
##
## Updated as of 08/03/2015
## NOT Running as of 08/03/2015
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
    
    #creation of numpy array to store values for faster analysis(courtesy of Ben Bartlett). Note in Endcap, we don't differentiate with splitPhotons -> they are all saved in their respective plus and minus sections.
    dataListp = np.array(["plus or minus", -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0]) #(photon, x, y, counts, mean, mean error, sigma, sigma error, t mean, t mean error)
    dataListm = np.array(["plus or minus", -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0]) #(photon, x, y, counts, time response, time response error, time resolution, time resolution error, laser transparency mean, laser transparency error)
    
    if p.splitPhotons == True:
        fname = 'p1p2_'
        #creates histogram for time response
        htimep1 = rt.TH2F("Time Response in Endcap plus for photon 1", "Time Response in EE+ for photon 1; iX;iY;ns",101,0,101,101,0,101)
        htimep2 = rt.TH2F("Time Response in Endcap plus for photon 2", "Time Response in EE+ for photon 2; iX;iY;ns",101,0,101,101,0,101)
        htimem1 = rt.TH2F("Time Response in Endcap minus for photon 1", "Time Response in EE- for photon 1; iX;iY;ns",101,0,101,101,0,101)
        htimem2 = rt.TH2F("Time Response in Endcap minus for photon 2", "Time Response in EE- for photon 2; iX;iY;ns",101,0,101,101,0,101)
        #creates histogram for laser response
        hlaserp1 = rt.TH2F("Transparency in Endcap plus for photon 1", "Transparency in EE+ for photon 1; iX;iY;Transparency Factor",101,0,101,101,0,101)
        hlaserp2 = rt.TH2F("Transparency in Endcap plus for photon 2", "Transparency in EE+ for photon 2; iX;iY;Transparency Factor",101,0,101,101,0,101)
        hlaserm1 = rt.TH2F("Transparency in Endcap minus for photon 1", "Transparency in EE- for photon 1; iX;iY;Transparency Factor",101,0,101,101,0,101)
        hlaserm2 = rt.TH2F("Transparency in Endcap minus for photon 2", "Transparency in EE- for photon 2; iX;iY;Transparency Factor",101,0,101,101,0,101)
    
        #creates a list of histograms
        histListp1 = [[0 for x in range(101)] for y in range(101)]
        histListm1 = [[0 for x in range(101)] for y in range(101)]
        histListp2 = [[0 for x in range(101)] for y in range(101)]
        histListm2 = [[0 for x in range(101)] for y in range(101)]

        transListp1 = [[0 for x in range(101)] for y in range(101)]
        transListm1 = [[0 for x in range(101)] for y in range(101)]
        transListp2 = [[0 for x in range(101)] for y in range(101)]
        transListm2 = [[0 for x in range(101)] for y in range(101)]

    
        #fills the 2D histogram with 1D histograms
        for x in range (0,101):
            for y in range (0,101):
                histnamep1 = "time on plus sc (%i,%i) for photon 1" %(x,y)
                histtitlep1 = "time response (ns) for plus crystal (%i,%i) for photon 1" %(x,y)
                histnamem1 = "time on minus sc (%i,%i) for photon 1" %(x,y)
                histtitlem1 = "time response (ns) for minus crystal (%i,%i) for photon 1" %(x,y)
                histnamep2 = "time on plus sc (%i,%i) for photon 2" %(x,y)
                histtitlep2 = "time response (ns) for plus crystal (%i,%i) for photon 2" %(x,y)
                histnamem2 = "time on minus sc (%i,%i) for photon 2" %(x,y)
                histtitlem2 = "time response (ns) for minus crystal (%i,%i) for photon 2" %(x,y)
                histListp1[x][y] = rt.TH1F(histnamep1,histtitlep1,1200,-30,30)
                histListm1[x][y] = rt.TH1F(histnamem1,histtitlem1,1200,-30,30)
                histListp2[x][y] = rt.TH1F(histnamep2,histtitlep2,1200,-30,30)
                histListm2[x][y] = rt.TH1F(histnamem2,histtitlem2,1200,-30,30)
    
                transnamep1 = "transparency on plus sc (%i,%i) for photon 1" %(x,y)
                transtitlep1 = "transparency for plus crystal (%i,%i) for photon 1" %(x,y)
                transnamem1 = "transparency on minus sc (%i,%i) for photon 1" %(x,y)
                transtitlem1 = "transparency for minus crystal (%i,%i) for photon 1" %(x,y)
                transnamep2 = "transparency on plus sc (%i,%i) for photon 2" %(x,y)
                transtitlep2 = "transparency for plus crystal (%i,%i) for photon 2" %(x,y)
                transnamem2 = "transparency on minus sc (%i,%i) for photon 2" %(x,y)
                transtitlem2 = "transparency for minus crystal (%i,%i) for photon 2" %(x,y)
                transListp1[x][y] = rt.TH1F(transnamep1,transtitlep1,1000,-5,5)
                transListm1[x][y] = rt.TH1F(transnamem1,transtitlem1,1000,-5,5)
                transListp2[x][y] = rt.TH1F(transnamep2,transtitlep2,1000,-5,5)
                transListm2[x][y] = rt.TH1F(transnamem2,transtitlem2,1000,-5,5)

        #stack data on histograms
        runinfo = a.openEE(rootfilename,rootList,runinfo,bf,ef,p.numberofEntries,histListp1, histListm1,histListp2,histListm2,transListp1,transListm1,transListp2,transListm2)
    else:
        fname = 'c_'
        htimep = rt.TH2F("Time Response in Endcap plus for all photons", "Time Response in EE+; iX;iY;ns",101,0,101,101,0,101)
        htimem = rt.TH2F("Time Response in Endcap minus for all photons", "Time Response in EE-; iX;iY;ns",100,0,101,101,0,101)
        hlaserp = rt.TH2F("Transparency in Endcap plus for all photons", "Transparency in EE+; iX;iY;Transparency Factor",101,0,101,101,0,101)
        hlaserm = rt.TH2F("Transparency in Endcap minus for all photons", "Transparency in EE-; iX;iY;Transparency Factor",101,0,101,101,0,101)

        histListp = [[0 for x in range(101)] for y in range(101)]
        histListm = [[0 for x in range(101)] for y in range(101)]
        transListp = [[0 for x in range(101)] for y in range(101)]
        transListm = [[0 for x in range(101)] for y in range(101)]

        for x in range (0,101):
            for y in range (0,101):
                histnamep = "time on plus sc (%i,%i)" %(x,y)
                histtitlep = "time response (ns) for plus crystal (%i,%i)" %(x,y)
                histnamem = "time on minus sc (%i,%i)" %(x,y)
                histtitlem = "time response (ns) for minus crystal (%i,%i)" %(x,y)
                histListp[x][y] = rt.TH1F(histnamep,histtitlep,1000,-30,30)
                histListm[x][y] = rt.TH1F(histnamem,histtitlem,1000,-30,30)

                transnamep = "transparency on plus sc (%i,%i)" %(x,y)
                transtitlep = "transparency for plus crystal (%i,%i)" %(x,y)
                transnamem = "transparency on minus sc (%i,%i)" %(x,y)
                transtitlem = "transparency for minus crystal (%i,%i)" %(x,y)
                transListp[x][y] = rt.TH1F(transnamep,transtitlep,1000,-5,5)
                transListm[x][y] = rt.TH1F(transnamem,transtitlem,1000,-5,5)

        runinfo = a.openEE(rootfilename,rootList,runinfo,bf,ef,p.numberofEntries,histListp, histListm, 0, 0, transListp, transListm, 0, 0)

    # Same procedure, going back to directory where results are printed
    retdir = os.getcwd()
    print "Current working directory %s" % retdir
    os.chdir(resultLocation + '/' + p.folderName + '/')
    folder = 'ctEE_' + fname + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    os.system('mkdir ' + folder)
    os.chdir(os.getcwd() + '/' + folder +'/')
    retdir = os.getcwd()
    print "Directory changed successfully %s" % retdir
    shutil.copyfile(stardir + '/' + 'unpack.py', retdir + '/unpack.py')
    
    #saving run info to a numpy file for reference later
    np.save(p.runNumber+"ClusterRunInfoEE.npy", runinfo)

    if p.splitPhotons == True:
        htimep1, hlaserp1, fitdatap1, seedmapp1 = snf.fitTime(histListp1,transListp1,htimep1,hlaserp1,p.minStat,p.includeHitCounter,p.manualHitCounterCut,"pp1_")
        htimem1, hlaserm1, fitdatam1, seedmapm1 = snf.fitTime(histListm1,transListm1,htimem1,hlaserm1,p.minStat,p.includeHitCounter,p.manualHitCounterCut,"mp1_")
        htimep2, hlaserp2, fitdatap2, seedmapp2 = snf.fitTime(histListp2,transListp2,htimep2,hlaserp2,p.minStat,p.includeHitCounter,p.manualHitCounterCut,"pp2_")
        htimem2, hlaserm2, fitdatam2, seedmapm2 = snf.fitTime(histListm2,transListm2,htimem2,hlaserm2,p.minStat,p.includeHitCounter,p.manualHitCounterCut,"mp2_")

        #saving all 1D histograms in tree
        a.saveEE(p.runNumber,dataListp,dataListm,histListp1,histListp2,histListm1,histListm2,transListp1,transListp2,transListm1,transListm2,htimep1,htimep2,htimem1,htimem2,hlaserp1,hlaserp2,hlaserm1,hlaserm2,fitdatap1,fitdatap2,fitdatam1,fitdatam2,seedmapp1,seedmapm1,seedmapp2,seedmapm2)
    
        #Tacks on histogram to canvas frame and ouputs on canvas
        a.printPrettyPictureEE(p.runNumber,htimep1,htimep2,htimem1,htimem2,hlaserp1,hlaserp2,hlaserm1,hlaserm2,seedmapp1,seedmapm1,seedmapp2,seedmapm2)
    else:
        htimep,hlaserp,fitdatap,seedmapp = snf.fitTime(histListp,transListp,htimep,hlaserp,p.minStat,p.includeHitCounter,p.manualHitCounterCut,"pc_")
        htimem,hlaserm,fitdatam,seedmapm = snf.fitTime(histListm,transListm,htimem,hlaserm,p.minStat,p.includeHitCounter,p.manualHitCounterCut,"mc_")

        #saving all 1D histograms in tree
        a.saveEE(p.runNumber,dataListp,dataListm,histListp,0,histListm,0,transListp,0,transListm,0,htimep,0,htimem,0,hlaserp,0,hlaserm,0,fitdatap,0,fitdatam,0,seedmapp,0,seedmapm,0)

        #Tacks on histogram to canvas frame and ouputs on canvas
        a.printPrettyPictureEE(p.runNumber,htimep,0,htimem,0,hlaserp,0,hlaserm,0,seedmapp,seedmapm,0,0)
