##
## This program confirms that we stored our .npy files
## correctly. That way, any information modified and any
## calculations done using the .npy files should match directly
## to any SAME modifications done with the .root files (with the
## same respective histogram [99% the TH2F one])
##
## Running as of 09/22/2015

import ROOT as rt
import sys, random, math
import time, datetime
import os, shutil
import numpy as np

sys.path.insert(1, '/Users/kaichang/Desktop/analysis/') #this will get changed in fastAnalysis to appropriate location.
import parameters as p
import stackNfit as snf

def fill(f, hist_t, hist_l, hist_d):
    for x in range(len(f)):
        for y in range(len(f[0])):
            #time response
            hist_t.Fill(x,y,float(f[x][y][5])) #response mean
            hist_t.SetBinError(x+1,y+1,float(f[x][y][6])) #response uncertainty
            #laser transparency
            hist_l.Fill(x,y,float(f[x][y][9])) #transparency mean
            hist_l.SetBinError(x+1,y+1,float(f[x][y][10])) #transparency uncertainty
            #seed density plot
            hist_d.Fill(x,y,float(f[x][y][4])) #seed count
    return hist_t, hist_l, hist_d


def save(hist_t,hist_l,hist_d):
    hist_t.SetAxisRange(-5., 5.,"Z")
    hist_t.Draw("colz")
    hist_t.GetYaxis().SetTitleOffset(1.1)
    hist_t.GetZaxis().SetTitleOffset(1.1)
    c.Print("TR_EEp.png")
    hist_l.SetAxisRange(-0, 1,"Z")
    hist_l.Draw("colz")
    hist_l.GetYaxis().SetTitleOffset(1.1)
    hist_l.GetZaxis().SetTitleOffset(1.25)
    c.Print("LS_EEp.png")
    hist_d.SetMinimum(0.)
    hist_d.Draw("colz")
    hist_d.GetYaxis().SetTitleOffset(1.1)
    hist_d.GetZaxis().SetTitleOffset(1.1)
    c.Print("SD_EEp.png")


if __name__ == "__main__":
    
    numpyList = [] #list of root files from result, should at max 2
    retdir = os.getcwd()
    #os.chdir('/Users/kaichang/Desktop/result/analyze')
    fileList = os.listdir('.') #list of files in the result folder
    
    #finds all the .npy files
    for file in fileList:
        if '.npy' in file and 'data' in file:
            numpyList.append(file)

    if len(numpyList) == 0:
        print "sorry, no .npy files in folder"
        exit()

    #difference histograms (htdp = *h*istgram of *t*ime response *d*ifference, plus)
    htdp = rt.TH2F("TR in EE+", "TR in EE+; iX;iY;ns",101,0,101,101,0,101) #first column or row is 0
    htdm = rt.TH2F("TR in EE-", "TR in EE-; iX;iY;ns",101,0,101,101,0,101)
    hldp = rt.TH2F("Transparency in EE+", "Transparency in EE+; iX;iY;Relative Transparency",101,0,101,101,0,101)
    hldm = rt.TH2F("Transparency n EE-", "Transparency in EE-; iX;iY;Relative Transparency",101,0,101,101,0,101)
    hddp = rt.TH2F("SPD in EE+", "SPD in EE+; iX;iY;Photon Counts",101,0,101,101,0,101)
    hddm = rt.TH2F("SPD in EE-", "SPD in EE-; iX;iY;Photon Counts",101,0,101,101,0,101)


    for numpyfile in numpyList:
        if "2015A" and "EEp" in numpyfile:
            fA_p = np.load(numpyfile)
        if "2015A" and "EEm" in numpyfile:
            fA_m = np.load(numpyfile)
        if "2015B" and "EEp" in numpyfile:
            fB_p = np.load(numpyfile)
        if "2015B" and "EEm" in numpyfile:
            fB_m = np.load(numpyfile)
        if "2015C" and "EEp" in numpyfile:
            fC_p = np.load(numpyfile)
        if "2015C" and "EEm" in numpyfile:
            fC_m = np.load(numpyfile)

    htdp,hldp,hddp = fill(fA_p,htdp,hldp,hddp)


    #creates permanent canvas, only need to do ONCE.
    rt.gROOT.LoadMacro('setstyle.c')
    rt.gROOT.Macro('setstyle.c')
    c = rt.TCanvas("c","c",600,500)
    c.cd()

    os.chdir(retdir)
    save(htdp,hldp,hddp)
