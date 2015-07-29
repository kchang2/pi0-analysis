
##
## Tutorial for drawing a histogram plot (2D) from tree variables
## in the endcap region. We want a general time resolution to see
## which sections are affected the most.
##
## Updated as of 07/27/2015
## Running as of 07/27/2015
##
import ROOT as rt
import sys, random, math
import time
import os
import stackNfit as snf
import numpy as np

from FastProgressBar import progressbar

if __name__ == "__main__":

#creates histogram for time response
    htimep = rt.TH2F("Time Response in Endcap plus for all photons", "X vs Y",100,0,100,100,0,100)
    htimem = rt.TH2F("Time Response in Endcap minus for all photons", "X vs Y",100,0,100,100,0,100)

#creates histogram for event count
#hevent = rt.TH2F("Events in Barrel", "X vs Y",100,0,100,100,0,100)

#creation of numpy array to store values for faster analysis(courtesy of Ben Bartlett)
    dataListp = np.array([-1.0, -1.0, -1.0, -1.0]) #(photon, x, y, time response)
    dataListm = np.array([-1.0, -1.0, -1.0, -1.0]) #(photon, x, y, time response)

#creates a list of histograms
    histListp = [[0 for x in range(101)] for y in range(101)]
    histListm = [[0 for x in range(101)] for y in range(101)]

    for x in range (0,101):
        for y in range (0,101):
            histnamep = "time on plus sc (%i,%i)" %(x,y)
            histtitlep = "time response (ns) for plus crystal (%i,%i)" %(x,y)
            histnamem = "time on minus sc (%i,%i)" %(x,y)
            histtitlem = "time response (ns) for minus crystal (%i,%i)" %(x,y)

            histListp[x][y] = rt.TH1F(histnamep,histtitlep,1000,-30,30)
            histListm[x][y] = rt.TH1F(histnamem,histtitlem,1000,-30,30)


## Getting to the output files
##
    # Check current working directory.
    retdir = os.getcwd()
    print "Current working directory %s" % retdir
    
    # Now change the directory
    os.chdir('..')
    startdir = retdir = os.getcwd()
    os.chdir( retdir + '/ALL_2015A_RAW_Test1/cfgFile/Fill/output/' )
    
    # Check current working directory.
    retdir = os.getcwd()
    print "Directory changed successfully %s" % retdir


    # Get list of root files in directory
    fileList = os.listdir(retdir)
    
    for k in range(0,5):#len(fileList)): ###CHANGED###
        if "2015A_EcalNtp_" in fileList[k]:
            rootFile = rt.TFile.Open(fileList[k])
            rTree = rootFile.Get("Tree_Optim")
            print "successfully cut branch from " + fileList[k]
            #rootFile.Print("v")
            
            #fills the histogram with data
            histListp, histListm = snf.stackTime(rTree,histListp, histListm, 0, 0)
            rootFile.Close()

    #fits the histograms
    htimep = snf.fitTime(histListp,htimep)
    htimem = snf.fitTime(histListm,htimem)

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
    #    pbar = progressbar("saving data", 101).start()
    pbar = progressbar("saving data", 101).start()

    #saving all 1D histograms in tree
    f = rt.TFile("timeEB_"+str(int(time.time()))+".root","new")
    for x in range(0,len(histListp)):
        for y in range(0, len(histListp[0])):
            histListp[x][y].Write()
            histListm[x][y].Write()
            #Saving value of data in tuple list
            dataListp = np.vstack((dataListp, ["p", x, y, htimep.GetBinContent(x+1, y)]))
            dataListm = np.vstack((dataListp, ["m", x, y, htimem.GetBinContent(x+1, y)]))
        pbar.update(x+1)
    htimep.Write()
    htimem.Write()


    np.save("TimeResponseEEp_0T.npy", dataListp)
    np.save("TimeResponseEEm_0T.npy", dataListm)
    pbar.finish()



    #Tacks on histogram to canvas frame and ouputs on canvas
    c = rt.TCanvas()
    htimep.SetFillColor(0)
    htimep.Draw("colz")
    c.Print("2DTimeResponseEBp_0T.png")

    #Tacks on histogram to canvas frame and ouputs on canvas
    c = rt.TCanvas()
    htimem.SetFillColor(0)
    htimem.Draw("colz")
    c.Print("2DTimeResponseEBm_0T.png")
