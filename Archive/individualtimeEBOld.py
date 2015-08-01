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

    for k in range(0,len(fileList)):
        if "2015A_EcalNtp_" in fileList[k]:
            rootFile = rt.TFile.Open(fileList[k])
            rTree = rootFile.Get("Tree_Optim")
            print "successfully cut branch from " + fileList[k]
            #rootFile.Print("v")
                   
            #fills the histogram with data
#            histList = snf.stackTime(rTree,histList, 0, 0, 0)
            histList1,histList2 = snf.stackTime(rTree,histList1, histList2, 1, 0)
            rootFile.Close()


    #fits the histograms
#    htime = snf.fitTime(histList,htime)
    htime1 = snf.fitTime(histList1,htime1)
    htime2 = snf.fitTime(histList2,htime2)

## Getting back to program file
##
    # Check current working directory.
    retdir = os.getcwd()
    print "Current working directory %s" % retdir
    
    # Now change the directory
    os.chdir( startdir + '/result/')
    
    # Check current working directory.
    retdir = os.getcwd()
    print "Directory changed successfully %s" % retdir

    #Progress bar for the saves
#    pbar = progressbar("saving data", 171).start()
    pbar = progressbar("saving data", 342).start()

    #saving all 1D histograms in tree
#    f = rt.TFile("timeEB"+str(int(time.time()))+".root","new")
#    for eta in range(0,len(histList)):
#        for phi in range(0, len(histList[0])):
#            histList[eta][phi].Write()
#            #Saving value of data in tuple list
#            dataList = np.vstack((dataList, [eta-85, phi, htime.GetBinContent(eta+1, phi)]))
#        pbar.update(eta+1)
#    np.delete(dataList,0)
#    htime.Write()

    f = rt.TFile("timeEB1_"+str(int(time.time()))+".root","new")
    for eta in range(0,len(histList1)):
        for phi in range(0, len(histList1[0])):
            histList1[eta][phi].Write()
            #Saving value of data in tuple list
            dataList1 = np.vstack((dataList1, [eta-85, phi, htime1.GetBinContent(eta+1, phi)]))
        pbar.update(eta+1)
    np.delete(dataList1,0)
    htime1.Write()

    f = rt.TFile("timeEB2_"+str(int(time.time()))+".root","new")
    for eta in range(0,len(histList2)):
        for phi in range(0, len(histList2[0])):
            histList2[eta][phi].Write()
            #Saving value of data in tuple list
            dataList2 = np.vstack((dataList2, [eta-85, phi, htime2.GetBinContent(eta+1, phi)]))
        pbar.update(eta+1)
    np.delete(dataList2,0)
    htime2.Write()


#    np.save("TimeResponseEB_0T.npy", dataList)
    np.save("TimeResponseEB1_0T.npy", dataList1)
    np.save("TimeResponseEB2_0T.npy", dataList2)
    pbar.finish()


    #Tacks on histogram to canvas frame and ouputs on canvas
    #htime.plotOn(frame)
#    c = rt.TCanvas()
#    htime.SetFillColor(0)
#    htime.Draw("colz")
#    c.Print("2DTimeResponseEB_0T.png")

    c1 = rt.TCanvas()
    htime1.SetFillColor(0)
    htime1.Draw("colz")
    c1.Print("2DTimeResponseEB1_0T.png")

    c2 = rt.TCanvas()
    htime2.SetFillColor(0)
    htime2.Draw("colz")
    c2.Print("2DTimeResponseEB2_0T.png")

