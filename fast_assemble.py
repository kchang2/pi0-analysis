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
            histList = snf.stackTime(rTree, entries, histList, 0, 0, 0)
        
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
        histListp, histListm = snf.stackTime(rTree, entries, histListp, histListm, 0, 0)
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
def saveEB(runNumber, dataList1, dataList2, histList1, histList2, htime1,htime2,fitdata1,fitdata2):
    if isinstance(histList1[0],list) == True: #Individual barrel crystals
        if histList2 !=0:
            f = rt.TFile(runNumber+"IndivtimeEB1.root","new")
            for eta in range(0,len(histList1)):
                for phi in range(0, len(histList1[0])):
                    histList1[eta][phi].Write()
                    #Saving value of data in tuple list
                    dataList1 = np.vstack((dataList1, [eta-85, phi, fitdata1[eta][phi][0],fitdata1[eta][phi][1],fitdata1[eta][phi][2],fitdata1[eta][phi][3]]))
            htime1.Write()
            f.Close()

            f2 = rt.TFile(runNumber+"IndivtimeEB2.root","new")
            for eta in range(0,len(histList2)):
                for phi in range(0, len(histList2[0])):
                    histList2[eta][phi].Write()
                    #Saving value of data in tuple list
                    dataList2 = np.vstack((dataList2, [eta-85, phi, fitdata2[eta][phi][0],fitdata2[eta][phi][1],fitdata2[eta][phi][2],fitdata2[eta][phi][3]]))
            htime2.Write()
            f2.Close()
    
            np.save(runNumber+"TimeResponseEB1_0T.npy", dataList1)
            np.save(runNumber+"TimeResponseEB2_0T.npy", dataList2)
        else:
            #saving all 1D histograms in tree
            f = rt.TFile(runNumber+"IndivtimeEB.root","new")
            for eta in range(0,len(histList)):
                for phi in range(0, len(histList[0])):
                    histList[eta][phi].Write()
                    #Saving value of data in tuple list
                    dataList1 = np.vstack((dataList1, [eta-85, phi, fitdata1[eta][phi][0],fitdata1[eta][phi][1],fitdata1[eta][phi][2],fitdata1[eta][phi][3]]))
            htime.Write()
            f.Close()

            np.save("TimeResponseEB_0T.npy", dataList)
    else:
        if histList2 !=0:
            f = rt.TFile(runNumber+"clustertimeEB1.root","new")
            for eta in range(0,len(histList1)):
                histList1[eta].Write()
                #Saving value of data in tuple list
                dataList1 = np.vstack((dataList1, [eta-85, fitdata1[eta][0],fitdata1[eta][1],fitdata1[eta][2],fitdata1[eta][3]]))
            htime1.Write()
            f.Close()
        
            f2 = rt.TFile(runNumber+"clustertimeEB2.root","new")
            for eta in range(0,len(histList2)):
                histList2[eta].Write()
                #Saving value of data in tuple list
                dataList2 = np.vstack((dataList2, [eta-85, fitdata2[eta][0],fitdata2[eta][1],fitdata2[eta][2],fitdata2[eta][3]]))
            htime2.Write()
            f2.Close()
            
            #saving all data into a numpy file for analyzing later
            np.save(runNumber+"etaTimeResponseEB1_0T.npy", dataList1)
            np.save(runNumber+"etaTimeResponseEB2_0T.npy", dataList2)
        else:
            f = rt.TFile(runNumber+"clustertimeEBAll.root","new")
            for eta in range(0,len(histList1)):
                histList1[eta].Write()
                #Saving value of data in tuple list
                dataList1 = np.vstack((dataList, [eta-85, fitdata1[eta][0],fitdata1[eta][1],fitdata1[eta][2],fitdata1[eta][3]]))
            htime1.Write()
            f.Close()
            
            #saving all data into a numpy file for analyzing later
            np.save(runNumber+"etaTimeResponseEBAll_0T.npy", dataList1)


#saves the histograms, fits, and others for the barrel
def saveEE(runNumber,dataListp,dataListm,histListp1,histListp2,histListm1,histListm2,htimep1,htimep2,htimem1,htimem2,fitdatap1,fitdatap2,fitdatam1,fitdatam2):
    if histListp2 != 0: #2 photons
        f = rt.TFile(runNumber+"IndivtimeEEp.root","new")
        for x in range(0,len(histListp1)):
            for y in range(0, len(histListp1[0])):
                histListp1[x][y].Write()
                histListp2[x][y].Write()
                #Saving value of data in tuple list
                dataListp = np.vstack((dataListp, ["p1", x, y, fitdatap1[x][y][0],fitdatap1[x][y][1],fitdatap1[x][y][2],fitdatap1[x][y][3]]))
                dataListp = np.vstack((dataListp, ["p2", x, y, fitdatap2[x][y][0],fitdatap2[x][y][1],fitdatap2[x][y][2],fitdatap2[x][y][3]]))
        htimep1.Write()
        htimep2.Write()
        f.Close()
            
        f2 = rt.TFile(runNumber+"IndivtimeEEm.root","new")
        for x in range(0,len(histListm1)):
            for y in range(0, len(histListm1[0])):
                histListm1[x][y].Write()
                histListm2[x][y].Write()
                #Saving value of data in tuple list
                dataListm = np.vstack((dataListm, ["m1", x, y, fitdatam1[x][y][0],fitdatam1[x][y][1],fitdatam1[x][y][2],fitdatam1[x][y][3]]))
                dataListm = np.vstack((dataListm, ["m2", x, y, fitdatam2[x][y][0],fitdatam2[x][y][1],fitdatam2[x][y][2],fitdatam2[x][y][3]]))
        htimem1.Write()
        htimem2.Write()
        f2.Close()
        
        np.save(runNumber+"TimeResponseEEp.npy", dataListp)
        np.save(runNumber+"TimeResponseEEm.npy", dataListm)
    else:
        f = rt.TFile(runNumber+"IndivtimeEEp_c.root","new")
        for x in range(0,len(histListp1)):
            for y in range(0, len(histListp1[0])):
                histListp1[x][y].Write()
                dataListp = np.vstack((dataListp, ["p", x, y, fitdatap1[x][y][0],fitdatap1[x][y][1],fitdatap1[x][y][2],fitdatap1[x][y][3]]))
        htimep.Write()
        f.Close()
        
        f2 = rt.TFile(runNumber+"IndivtimeEEm_c.root","new")
        for x in range(0,len(histListm1)):
            for y in range(0, len(histListm1[0])):
                histListm1[x][y].Write()
                dataListm = np.vstack((dataListm, ["m", x, y, fitdatam1[x][y][0],fitdatam1[x][y][1],fitdatam1[x][y][2],fitdatam1[x][y][3]]))
        htimem.Write()
        f2.Close()

        #saving all data into a numpy file for analyzing later
        np.save(runNumber+"TimeResponseEEp_c.npy", dataListp)
        np.save(runNumber+"TimeResponseEEm_c.npy", dataListm)


#draws the graphs you want to see and saves them as .png in respective folders
def printPrettyPictureEB(runNumber,htime1,htime2):
    #Gets rid of legend
    rt.gStyle.SetOptStat(0)
    if type(htime1) != rt.TH1F:
        if htime2 != 0:
            c1 = rt.TCanvas()
            htime1.SetFillColor(0)
            htime1.SetAxisRange(-5., 5.,"Z")
            htime1.Draw("colz")
            c1.Print(runNumber+"IndivTimeResponseEB1_0T.png")

            c2 = rt.TCanvas()
            htime2.SetFillColor(0)
            htime2.SetAxisRange(-5., 5.,"Z")
            htime2.Draw("colz")
            c2.Print(runNumber+"IndivTimeResponseEB2_0T.png")
        else:
            c = rt.TCanvas()
            htime.SetFillColor(0)
            htime.SetAxisRange(-5., 5.,"Z")
            htime.Draw("colz")
            c.Print(runNumber+"IndivTimeResponseEB_0T.png")
    else:
        if htime2 != 0:
            c1 = rt.TCanvas()
            htime1.GetYaxis().SetRangeUser(-1,1) #hist->GetYaxis()->SetRangeUser(min value, max value)
            htime1.Draw()
            c1.Print(runNumber+"etaTimeResponseEB1_0T.png")
    
            c2 = rt.TCanvas()
            htime2.Draw()
            c2.Print(runNumber+"etaTimeResponseEB2_0T.png")
        else:
            c = rt.TCanvas()
            htime.Draw()
            c.Print(runNumber+"etaTimeResponseEBAll_0T.png")

#draws the graphs you want to see and saves them as .png in respective folders
def printPrettyPictureEE(runNumber,htimep1,htimep2,htimem1,htimem2):
    if type(htimep2) == rt.TH2F:
        c1 = rt.TCanvas()
        htimep1.SetFillColor(0)
        htimep1.SetAxisRange(-5., 5.,"Z")
        htimep1.Draw("colz")
        c1.Print(runNumber+"IndivTimeResponseEEp1.png")
            
        c2 = rt.TCanvas()
        htimep2.SetFillColor(0)
        htimep2.SetAxisRange(-5., 5.,"Z")
        htimep2.Draw("colz")
        c2.Print(runNumber+"IndivTimeResponseEEp2.png")
    
        c3 = rt.TCanvas()
        htimem1.SetFillColor(0)
        htimem1.SetAxisRange(-5., 5.,"Z")
        htimem1.Draw("colz")
        c3.Print(runNumber+"IndivTimeResponseEEm1.png")
        
        c4 = rt.TCanvas()
        htimem2.SetFillColor(0)
        htimem2.SetAxisRange(-5., 5.,"Z")
        htimem2.Draw("colz")
        c4.Print(runNumber+"IndivTimeResponseEEm2.png")
    else:
        c = rt.TCanvas()
        htimep.SetFillColor(0)
        htimep.SetAxisRange(-5., 5.,"Z")
        htimep.Draw("colz")
        c.Print(runNumber+"IndivTimeResponseEEp_c.png")

        c2 = rt.TCanvas()
        htimem.SetFillColor(0)
        htimem.SetAxisRange(-5., 5.,"Z")
        htimem.Draw("colz")
        c2.Print(runNumber+"IndivTimeResponseEEm_c.png")
