import ROOT as rt
import sys, random, math
import time
import os
import numpy as np

import stackNfit as snf

def openEB(numofFiles, filename, fileList, entries, histList1, histList2):
    for k in range(0, numofFiles):
        if filename in fileList[k]:
            rootFile = rt.TFile.Open(fileList[k])
            rTree = rootFile.Get("Tree_Optim")
            print "successfully cut branch from " + fileList[k]
            #rootFile.Print("v")
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
            rootFile.Close()

def saveEB(runNumber, dataList1, dataList2, histList1, histList2, htime1,htime2,fitdata1,fitdata2):
    if isinstance(histList1[0],list) == True: #Individual barrel crystals
        if histList2 !=0:
            f = rt.TFile(runNumber+"IndivtimeEB1_"+str(int(time.time()))+".root","new")
            for eta in range(0,len(histList1)):
                for phi in range(0, len(histList1[0])):
                    histList1[eta][phi].Write()
                    #Saving value of data in tuple list
                    dataList1 = np.vstack((dataList1, [eta-85, phi, htime1.GetBinContent(eta+1, phi)]))
            np.delete(dataList1,0)
            htime1.Write()

            f2 = rt.TFile(runNumber+"IndivtimeEB2_"+str(int(time.time()))+".root","new")
            for eta in range(0,len(histList2)):
                for phi in range(0, len(histList2[0])):
                    histList2[eta][phi].Write()
                    #Saving value of data in tuple list
                    dataList2 = np.vstack((dataList2, [eta-85, phi, htime2.GetBinContent(eta+1, phi)]))
            np.delete(dataList2,0)
            htime2.Write()
        else:
            #saving all 1D histograms in tree
            f = rt.TFile(runNumber+"IndivtimeEB"+str(int(time.time()))+".root","new")
            for eta in range(0,len(histList)):
                for phi in range(0, len(histList[0])):
                    histList[eta][phi].Write()
                    #Saving value of data in tuple list
                    dataList = np.vstack((dataList, [eta-85, phi, htime.GetBinContent(eta+1, phi)]))
            np.delete(dataList,0)
            htime.Write()
    else:
        if histList2 !=0:
            f = rt.TFile(runNumber+"clustertimeEB1_"+str(int(time.time()))+".root","new")
            for eta in range(0,len(histList1)):
                histList1[eta].Write()
                #Saving value of data in tuple list
                dataList1 = np.vstack((dataList1, [eta-85, fitdata1[eta][0],fitdata1[eta][1],fitdata1[eta][2],fitdata1[eta][3]]))
            htime1.Write()
        
            f2 = rt.TFile(runNumber+"clustertimeEB2_"+str(int(time.time()))+".root","new")
            for eta in range(0,len(histList2)):
                histList2[eta].Write()
                #Saving value of data in tuple list
                dataList2 = np.vstack((dataList2, [eta-85, fitdata2[eta][0],fitdata2[eta][1],fitdata2[eta][2],fitdata2[eta][3]]))
            htime2.Write()
        else:
            f = rt.TFile(runNumber+"clustertimeEBAll_"+str(int(time.time()))+".root","new")
            for eta in range(0,len(histList1)):
                histList1[eta].Write()
                #Saving value of data in tuple list
                dataList1 = np.vstack((dataList, [eta-85, fitdata1[eta][0],fitdata1[eta][1],fitdata1[eta][2],fitdata1[eta][3]]))
            htime1.Write()

def printPrettyPictureEB(runNumber,htime1,htime2):
    if type(htime1) != rt.TH1F:
        if htime2 != 0:
            c1 = rt.TCanvas()
            htime1.SetFillColor(0)
            htime1.Draw("colz")
            c1.Print(runNumber+"_IndivTimeResponseEB1_0T.png")

            c2 = rt.TCanvas()
            htime2.SetFillColor(0)
            htime2.Draw("colz")
            c2.Print(runNumber+"_IndivTimeResponseEB2_0T.png")
        else:
            c = rt.TCanvas()
            htime.SetFillColor(0)
            htime.Draw("colz")
            c.Print(runNumber+"_IndivTimeResponseEB_0T.png")

    else:
        if htime2 != 0:
            c1 = rt.TCanvas()
            #htime1.GetYaxis().SetRangeUser(-1,1) #hist->GetYaxis()->SetRangeUser(min value, max value)
            htime1.Draw()
            c1.Print(runNumber+"_etaTimeResponseEB1_0T.png")
    
            c2 = rt.TCanvas()
            htime2.Draw()
            c2.Print(runNumber+"_etaTimeResponseEB2_0T.png")
        else:
            c = rt.TCanvas()
            htime.Draw()
            c.Print(runNumber+"_etaTimeResponseEBAll_0T.png")


