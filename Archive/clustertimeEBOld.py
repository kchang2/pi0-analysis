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
import parameter as *

from FastProgressBar import progressbar

if __name__ == "__main__":
    
    if splitPhotons == True:
    
    else:
        htime = rt.TH1F("Time Response in Barrel for all photons", "Eta relation",170,-85,85)
        dataList = np.array([-1.0, -1.0])
        histList = [0 for eta in range(171)]
        histname = "time on sc eta (%i) for all" %(eta-85)
        histtitle = "time response (ns) for eta (%i) for all" %(eta-85)

        histList[eta] = rt.TH1F(histname,histtitle,1000,-30,30)


    
    #creates histogram
    htime1 = rt.TH1F("Time Response in Barrel for photon 1", "Eta relation",170,-85,85)
    htime2 = rt.TH1F("Time Response in Barrel for photon 2", "Eta relation",170,-85,85)
    
    #creation of numpy array to store values for faster analysis(courtesy of Ben Bartlett)
    dataList1 = np.array([-1.0, -1.0])
    dataList2 = np.array([-1.0, -1.0])

    #creates a list of histograms (for range of eta)
    histList1 = [0 for eta in range(171)]
    histList2 = [0 for eta in range(171)]
    for eta in range (0,171):

        histname1 = "time on sc eta (%i) for photon 1" %(eta-85)
        histtitle1 = "time response (ns) for eta (%i) for photon 1" %(eta-85)
        histname2 = "time on sc eta (%i) for photon 2" %(eta-85)
        histtitle2 = "time response (ns) for eta (%i) for photon 2" %(eta-85)
        histList1[eta] = rt.TH1F(histname1,histtitle1,1000,-30,30)
        histList2[eta] = rt.TH1F(histname2,histtitle2,1000,-30,30)
        

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

    for k in range(0,len(fileList)):
        if "2015A_EcalNtp_" in fileList[k]:
            rootFile = rt.TFile.Open(fileList[k])
            rTree = rootFile.Get("Tree_Optim")
            print "successfully cut branch from " + fileList[k]
            #rootFile.Print("v")
            
            #fills the histogram with data
            #histList = snf.stackTimeEta(rTree,histList,0)
            histList1, histList2 = snf.stackTimeEta(rTree,histList1,histList2)
            rootFile.Close()

    #fits the histograms and saves 1D in tree
#    htime = snf.fitTimeEta(histList,htime)
    htime1 = snf.fitTimeEta(histList1,htime1)
    htime2 = snf.fitTimeEta(histList2,htime2)

    # Same procedure, going back to original working directory.
    retdir = os.getcwd()
    print "Current working directory %s" % retdir
    os.chdir( startdir + "/result/")
    retdir = os.getcwd()
    print "Directory changed successfully %s" % retdir

    #Progress bar for the saves
#    pbar = progressbar("saving data", 171).start()
    pbar = progressbar("saving data", 342).start()

    #saving all 1D histograms in tree
#    f = rt.TFile("clustertimeEBAll_"+str(int(time.time()))+".root","new")
#    for eta in range(0,len(histList)):
#        histList[eta].Write()
#        #Saving value of data in tuple list
#        dataList = np.vstack((dataList, [eta-85, htime.GetBinContent(eta+1)]))
#        pbar.update(i+1)
#    htime.Write()

    f = rt.TFile("clustertimeEB1_"+str(int(time.time()))+".root","new")
    for eta in range(0,len(histList1)):
        histList1[eta].Write()
        #Saving value of data in tuple list
        dataList1 = np.vstack((dataList1, [eta-85, htime1.GetBinContent(eta+1)]))
        pbar.update(eta+1)
    htime1.Write()

    f = rt.TFile("clustertimeEB2_"+str(int(time.time()))+".root","new")
    for eta in range(0,len(histList2)):
        histList2[eta].Write()
        #Saving value of data in tuple list
        dataList2 = np.vstack((dataList2, [eta-85, htime2.GetBinContent(eta+1)]))
        pbar.update(eta+1)
    htime2.Write()

#    np.save("etaTimeResponseEBAll_0T.npy", dataList)
    np.save("A_etaTimeResponseEB1_0T.npy", dataList1)
    np.save("A_etaTimeResponseEB2_0T.npy", dataList2)
    pbar.finish()


    #Tacks on histogram to canvas frame and ouputs on canvas
    #htime.plotOn(frame)
#    c = rt.TCanvas()
#    htime.Draw()
#    c.Print("etaTimeResponseEBAll_0T.png")

    c1 = rt.TCanvas()
#    htime1.GetYaxis().SetRangeUser(-1,1) #hist->GetYaxis()->SetRangeUser(min value, max value)
    htime1.Draw()
    c1.Print("A_etaTimeResponseEB1_0T.png")

    c2 = rt.TCanvas()
    htime2.Draw()
    c2.Print("A_etaTimeResponseEB2_0T.png")

