##
## This is the powerhouse file that opens the files, stacks the
## respective data from the files (its attributes), then calls for
## histogram fits, pulls the fits and statistics, and then packages
## it into readable and small files.
##
## Updated as of 08/03/2015
## Working as of 08/03/2015
##


import ROOT as rt
import sys, random, math
import time
import os
import numpy as np

import stackNfit as snf

#opens the files for the barrel
def openEB(filename, fileList, runinfo, startfilepos, endfilepos, entries, histList1, histList2):
    rTree = rt.TChain("Tree_Optim")
    for k in range(startfilepos, endfilepos):
        if filename in fileList[k]:
            rTree.Add(fileList[k])
            print "successfully cut branch from " + fileList[k]
            #Saving run info in tuple list
            runinfo = np.vstack((runinfo, [fileList[k]]))

    #fills the histogram with data
    if isinstance(histList1[0],list) == True: #Individual barrel crystals
        if histList2 !=0:
            histList1,histList2 = snf.stackTime(rTree, entries, histList1, histList2, 1, 0)
        else:
            histList1 = snf.stackTime(rTree, entries, histList1, 0, 0, 0)
        
    else: #eta baby eta
        if histList2!=0:
            histList1, histList2 = snf.stackTimeEta(rTree, entries, histList1,histList2)
        else:
            histList1 = snf.stackTimeEta(rTree,entries,histList1,0)
    return runinfo

#opens the files for the barrel
def openEE(filename, fileList, runinfo, startfilepos, endfilepos, entries, histListp1, histListm1,histListp2,histListm2):
    rTree = rt.TChain("Tree_Optim")
    for k in range(startfilepos, endfilepos):
        if filename in fileList[k]:
            rTree.Add(fileList[k])
            print "successfully cut branch from " + fileList[k]
            #Saving run info in tuple list
            runinfo = np.vstack((runinfo, [fileList[k]]))

    #fills the histogram with data
    if histListm2 != 0: #Differentiating photon 1 and 2
        histListp1, histListm1, histListp2, histListm2 = snf.stackTime(rTree, entries,histListp1, histListm1, histListp2, histListm2)
    else:   #Combine photon 1 and 2
        histListp1, histListm1 = snf.stackTime(rTree, entries, histListp1, histListm1, 0, 0)
    return runinfo


#opens the files for the barrel
def openMass(filename, fileList, runinfo, startfilepos, endfilepos, entries, histList, histRun):
    rTree = rt.TChain("Tree_Optim")
    for k in range(startfilepos, endfilepos):
        if filename in fileList[k]:
            rTree.Add(fileList[k])
            print "successfully cut branch from " + fileList[k]
            #Saving run info in tuple list
            runinfo = np.vstack((runinfo, [fileList[k]]))

            #makes the histogram for pi0 mass
            histname = "Average Pi0 mass in Barrel for time instance (%s)" %(fileList[k])
            histtitle = "Pi0 mass (GeV) for ROOT file cluster (%s)" %(fileList[k])
            histmass = rt.TH1F(histname,histtitle,1000,0,1)
            
            #fills the mass histogram list with ROOT files oriented folder
            histmass = snf.stackMass(rTree,histmass)
            histList.append(copy.copy(histmass))
            
            #Fills large histogram for the entire run's dataset
            histRun = snf.stackMass(rTree,histRun)
    
    return runinfo, histList, histrun



#saves the histograms, fits, and others for the barrel
def saveEB(runNumber, dataList1, dataList2, histList1, histList2, htime1,htime2,fitdata1,fitdata2,seedmap1,seedmap2):
    if isinstance(histList1[0],list) == True: #Individual barrel crystals
        if histList2 !=0:
            f = rt.TFile(runNumber+"IndivTimeEB_p1.root","new")
            for eta in range(0,len(histList1)):
                for phi in range(0, len(histList1[0])):
                    histList1[eta][phi].Write()
                    #Saving value of data in tuple list
                    dataList1 = np.vstack((dataList1, [eta-85, phi, fitdata1[eta][phi][0],fitdata1[eta][phi][1],fitdata1[eta][phi][2],fitdata1[eta][phi][3]]))
            htime1.Write()
            if seedmap1 != 0:
                seedmap1.Write()
            f.Close()

            f2 = rt.TFile(runNumber+"IndivTimeEB_p2.root","new")
            for eta in range(0,len(histList2)):
                for phi in range(0, len(histList2[0])):
                    histList2[eta][phi].Write()
                    #Saving value of data in tuple list
                    dataList2 = np.vstack((dataList2, [eta-85, phi, fitdata2[eta][phi][0],fitdata2[eta][phi][1],fitdata2[eta][phi][2],fitdata2[eta][phi][3]]))
            htime2.Write()
            if seedmap1 != 0:
                seedmap2.Write()
            f2.Close()
    
            np.save(runNumber+"TimeResponseEB_p1.npy", dataList1)
            np.save(runNumber+"TimeResponseEB_p2.npy", dataList2)
        else:
            #saving all 1D histograms in tree
            f = rt.TFile(runNumber+"IndivTimeEB_c.root","new")
            for eta in range(0,len(histList1)):
                for phi in range(0, len(histList1[0])):
                    histList1[eta][phi].Write()
                    #Saving value of data in tuple list
                    dataList1 = np.vstack((dataList1, [eta-85, phi, fitdata1[eta][phi][0],fitdata1[eta][phi][1],fitdata1[eta][phi][2],fitdata1[eta][phi][3]]))
            htime1.Write()
            if seedmap1 != 0:
                seedmap1.Write()
            f.Close()

            np.save("TimeResponseEB_c.npy", dataList1)
    else:
        if histList2 !=0:
            f = rt.TFile(runNumber+"ClusterTimeEB_p1.root","new")
            for eta in range(0,len(histList1)):
                histList1[eta].Write()
                #Saving value of data in tuple list
                dataList1 = np.vstack((dataList1, [eta-85, fitdata1[eta][0],fitdata1[eta][1],fitdata1[eta][2],fitdata1[eta][3]]))
            htime1.Write()
            if seedmap1 != 0:
                seedmap1.Write()
            f.Close()
        
            f2 = rt.TFile(runNumber+"ClusterTimeEB_p2.root","new")
            for eta in range(0,len(histList2)):
                histList2[eta].Write()
                #Saving value of data in tuple list
                dataList2 = np.vstack((dataList2, [eta-85, fitdata2[eta][0],fitdata2[eta][1],fitdata2[eta][2],fitdata2[eta][3]]))
            htime2.Write()
            if seedmap1 != 0:
                seedmap2.Write()
            f2.Close()
            
            #saving all data into a numpy file for analyzing later
            np.save(runNumber+"EtaTimeResponseEB_p1.npy", dataList1)
            np.save(runNumber+"EtaTimeResponseEB_p2.npy", dataList2)
        else:
            f = rt.TFile(runNumber+"ClusterTimeEB_c.root","new")
            for eta in range(0,len(histList1)):
                histList1[eta].Write()
                #Saving value of data in tuple list
                dataList1 = np.vstack((dataList1, [eta-85, fitdata1[eta][0],fitdata1[eta][1],fitdata1[eta][2],fitdata1[eta][3]]))
            htime1.Write()
            if seedmap1 != 0:
                seedmap1.Write()
            f.Close()
            
            #saving all data into a numpy file for analyzing later
            np.save(runNumber+"EtaTimeResponseEB_c.npy", dataList1)


#saves the histograms, fits, and others for the barrel
def saveEE(runNumber,dataListp,dataListm,histListp1,histListp2,histListm1,histListm2,htimep1,htimep2,htimem1,htimem2,fitdatap1,fitdatap2,fitdatam1,fitdatam2,seedmapp1,seedmapm1,seedmapp2,seedmapm2):
    if histListp2 != 0: #2 photons
        f = rt.TFile(runNumber+"IndivTimeEEp_p1p2.root","new")
        for x in range(0,len(histListp1)):
            for y in range(0, len(histListp1[0])):
                histListp1[x][y].Write()
                histListp2[x][y].Write()
                #Saving value of data in tuple list
                dataListp = np.vstack((dataListp, ["p1", x, y, fitdatap1[x][y][0],fitdatap1[x][y][1],fitdatap1[x][y][2],fitdatap1[x][y][3]]))
                dataListp = np.vstack((dataListp, ["p2", x, y, fitdatap2[x][y][0],fitdatap2[x][y][1],fitdatap2[x][y][2],fitdatap2[x][y][3]]))
        htimep1.Write()
        htimep2.Write()
        if seedmapp1 != 0:
            seedmapp1.Write()
        if seedmapp2 !=0:
            seedmapp2.Write()
        f.Close()
            
        f2 = rt.TFile(runNumber+"IndivTimeEEm_p1p2.root","new")
        for x in range(0,len(histListm1)):
            for y in range(0, len(histListm1[0])):
                histListm1[x][y].Write()
                histListm2[x][y].Write()
                #Saving value of data in tuple list
                dataListm = np.vstack((dataListm, ["m1", x, y, fitdatam1[x][y][0],fitdatam1[x][y][1],fitdatam1[x][y][2],fitdatam1[x][y][3]]))
                dataListm = np.vstack((dataListm, ["m2", x, y, fitdatam2[x][y][0],fitdatam2[x][y][1],fitdatam2[x][y][2],fitdatam2[x][y][3]]))
        htimem1.Write()
        htimem2.Write()
        if seedmapm1 != 0:
            seedmapm1.Write()
        if seedmapm2 !=0:
            seedmapm2.Write()
        f2.Close()
        
        np.save(runNumber+"TimeResponseEEp_p1p2.npy", dataListp)
        np.save(runNumber+"TimeResponseEEm_p1p2.npy", dataListm)
    else:
        f = rt.TFile(runNumber+"IndivTimeEEm_c.root","new")
        for x in range(0,len(histListp1)):
            for y in range(0, len(histListp1[0])):
                histListp1[x][y].Write()
                dataListp = np.vstack((dataListp, ["p", x, y, fitdatap1[x][y][0],fitdatap1[x][y][1],fitdatap1[x][y][2],fitdatap1[x][y][3]]))
        htimep1.Write()
        if seedmapp1 != 0:
            seedmapp1.Write()
        f.Close()
        
        f2 = rt.TFile(runNumber+"IndivTimeEEp_c.root","new")
        for x in range(0,len(histListm1)):
            for y in range(0, len(histListm1[0])):
                histListm1[x][y].Write()
                dataListm = np.vstack((dataListm, ["m", x, y, fitdatam1[x][y][0],fitdatam1[x][y][1],fitdatam1[x][y][2],fitdatam1[x][y][3]]))
        htimem1.Write()
        if seedmapm1 != 0:
            seedmapm1.Write()
        f2.Close()

        #saving all data into a numpy file for analyzing later
        np.save(runNumber+"TimeResponseEEp_c.npy", dataListp)
        np.save(runNumber+"TimeResponseEEm_c.npy", dataListm)


#draws the graphs you want to see and saves them as .png in respective folders
def printPrettyPictureEB(runNumber,htime1,htime2,seedmap1,seedmap2):
    #Gets rid of legend
    rt.gStyle.SetOptStat(0)
    
    if type(htime1) != rt.TH1F: #Individual crystals
        if htime2 != 0:
            c1 = rt.TCanvas()
            htime1.SetAxisRange(-5., 5.,"Z")
            htime1.Draw("colz")
            c1.Print(runNumber+"IndivTimeResponseEB_p1.png")

            c2 = rt.TCanvas()
            htime2.SetAxisRange(-5., 5.,"Z")
            htime2.Draw("colz")
            c2.Print(runNumber+"IndivTimeResponseEB_p2.png")
        else:
            c = rt.TCanvas()
            htime1.SetAxisRange(-5., 5.,"Z")
            htime1.Draw("colz")
            c.Print(runNumber+"IndivTimeResponseEB_c.png")
    else:
        if htime2 != 0:
            c1 = rt.TCanvas()
            htime1.Draw("E1")
            c1.Print(runNumber+"EtaTimeResponseEB_p1.png")
            c2 = rt.TCanvas()
            htime2.Draw("E1")
            c2.Print(runNumber+"EtaTimeResponseEB_p2.png")

        else:
            c = rt.TCanvas()
            htime1.Draw("E1")
            c.Print(runNumber+"EtaTimeResponseEB_c.png")

    if seedmap1 != 0: #print 1 seed map
        s1 = rt.TCanvas()
        seedmap1.Draw("colz")
        s1.Print(runNumber+"SeedDensityEB.png")
        if seedmap2 != 0: #print both seed maps
            s2 = rt.TCanvas()
            seedmap2.Draw("colz")
            s2.Print(runNumber+"SeedDensityEB_p2.png")



#draws the graphs you want to see and saves them as .png in respective folders
def printPrettyPictureEE(runNumber,htimep1,htimep2,htimem1,htimem2,seedmapp1,seedmapm1,seedmapp2,seedmapm2):
    #Gets rid of legend
    rt.gStyle.SetOptStat(0)
    
    if type(htimep2) == rt.TH2F:
        c1 = rt.TCanvas()
        htimep1.SetAxisRange(-5., 5.,"Z")
        htimep1.Draw("colz")
        c1.Print(runNumber+"IndivTimeResponseEEp_p1.png")
            
        c2 = rt.TCanvas()
        htimep2.SetAxisRange(-5., 5.,"Z")
        htimep2.Draw("colz")
        c2.Print(runNumber+"IndivTimeResponseEEp_p2.png")
    
        c3 = rt.TCanvas()
        htimem1.SetAxisRange(-5., 5.,"Z")
        htimem1.Draw("colz")
        c3.Print(runNumber+"IndivTimeResponseEEm_p1.png")
        
        c4 = rt.TCanvas()
        htimem2.SetAxisRange(-5., 5.,"Z")
        htimem2.Draw("colz")
        c4.Print(runNumber+"IndivTimeResponseEEm_p2.png")
    else:
        c = rt.TCanvas()
        htimep1.SetAxisRange(-5., 5.,"Z")
        htimep1.Draw("colz")
        c.Print(runNumber+"IndivTimeResponseEEp_c.png")

        c2 = rt.TCanvas()
        htimem1.SetAxisRange(-5., 5.,"Z")
        htimem1.Draw("colz")
        c2.Print(runNumber+"IndivTimeResponseEEm_c.png")

    if seedmapp1 != 0: #print 1 seed map
        s1 = rt.TCanvas()
        seedmapp1.Draw("colz")
        s1.Print(runNumber+"SeedDensityEEp.png")
        if seedmapp2 != 0: #print both seed maps
            s2 = rt.TCanvas()
            seedmapp2.Draw("colz")
            s2.Print(runNumber+"SeedDensityEEp_p2.png")
    if seedmapm1 !=0: #print1 seed map
        s3 = rt.TCanvas()
        seedmapm1.Draw("colz")
        s3.Print(runNumber+"SeedDensityEEm.png")
        if seedmapm2 !=0: #print1 seed map
            s4 = rt.TCanvas()
            seedmapm2.Draw("colz")
            s4.Print(runNumber+"SeedDensityEEm_p2.png")

