##
## Version 0.0.0
## Draws histogram plot (1D) of the time from tree variables. This is
## the first step into making analysis. It will draw a histogram plot
## of all the time responses of every event that occurred, regardless
## of location. This checkt to see if all the tree variables are
## holding the right data.
##
## Updated as of 07/27/2015
## Running as of 07/23/2015
##
import ROOT as rt
import sys, random, math
import os

from FastProgressBar import progressbar

if __name__ == "__main__":
#    if len(sys.argv)<2 or ('.root' not in sys.argv[1]):
#        print "give a root file as input"
#        sys.exit()
#
#    fileName = sys.argv[1]
#    rootFile = rt.TFile.Open(fileName)
#    rTree = rootFile.Get("Tree_Optim")
#    rootFile.Print("v")


    #Check and change current working directory.
    retdir = os.getcwd()
    print "Current working directory %s" % retdir
    os.chdir('..')
    startdir = retdir = os.getcwd()
    os.chdir( retdir + '/output/' )
    retdir = os.getcwd()
    print "Directory changed successfully %s" % retdir
    

    #Draws the Canvas Frame
    #t = rt.RooRealVar("t","t (ns)",-1,1)
    #frame = t.frame(rt.RooFit.Title("Timing Response of Pi0"))


    #creates histogram
    htime = rt.TH1F("time", "time (ns)",1000,-30,30)


    # Get list of root files in directory
    fileList = os.listdir(retdir)


    for k in range(0,len(fileList)):
        if "2015A_" in fileList[k]:
            rootFile = rt.TFile.Open(fileList[k])
            rTree = rootFile.Get("Tree_Optim")
            print "successfully cut branch from " + fileList[k]

            #fills in histograms with data
            nentries = rTree.GetEntries()
            
            #creates a progress bar
            pbar = progressbar("Stacking", nentries).start()
            
            for i in range(0, nentries):
                rTree.GetEntry(i)
                #if rTree.STr2_NPi0_rec==0: break
                #print "\nrec =", rTree.STr2_NPi0_rec
                for rec in range(0,rTree.STr2_NPi0_rec):
                    htime.Fill(rTree.STr2_Time_1[rec])
                    #print "time =", rTree.STr2_Time_1[rec]
                    #print "ieta =", rTree.STr2_iEta_1[rec]
                    #print "iphi =", rTree.STr2_iPhi_1[rec]
                pbar.update(i+1)
            pbar.finish()

    #Tacks on histogram to canvas frame and ouputs on canvas
    #htime.plotOn(frame)
    c = rt.TCanvas()
    htime.Draw()
    htime.SetXTitle("Time (ns)")
    htime.SetYTitle("Count")
    c.SetLogy()
    c.Print("timeResponseHistogram.png")

    #rt.TBrowser()
    #rTree.StartViewer()
