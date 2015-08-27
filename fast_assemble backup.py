##
## This is the powerhouse file that opens the files, stacks the
## respective data from the files (its attributes), then calls for
## histogram fits, pulls the fits and statistics, and then packages
## it into readable and small files.
##
## Running as of 08/19/2015
##


import ROOT as rt
import sys, random, math
import time
import os
import numpy as np

import stackNfit as snf

#opens the files for the barrel
def openEB(filename, fileList, runinfo, startfilepos, endfilepos, entries, histList1, histList2, transList1, transList2):
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
            histList1, histList2, transList1, transList2 = snf.stackTime(rTree, entries, histList1, histList2, 1, 0, transList1,transList2, 0, 0)
        else:
            histList1, transList1 = snf.stackTime(rTree, entries, histList1, 0, 0, 0, transList1, 0, 0, 0)
        
    else: #eta baby eta
        if histList2!=0:
            histList1, histList2, transList1, transList2 = snf.stackTimeEta(rTree, entries, histList1, histList2, transList1, transList2)
        else:
            histList1, transList1 = snf.stackTimeEta(rTree, entries, histList1, 0, transList1, 0)
    return runinfo

#opens the files for the barrel
def openEE(filename, fileList, runinfo, startfilepos, endfilepos, entries, histListp1, histListm1, histListp2, histListm2, transListp1, transListm1, transListp2, transListm2):
    rTree = rt.TChain("Tree_Optim")
    for k in range(startfilepos, endfilepos):
        if filename in fileList[k]:
            rTree.Add(fileList[k])
            print "successfully cut branch from " + fileList[k]
            #Saving run info in tuple list
            runinfo = np.vstack((runinfo, [fileList[k]]))

    #fills the histogram with data
    if histListm2 != 0: #Differentiating photon 1 and 2
        histListp1, histListm1, histListp2, histListm2, transListp1, transListm1, transListp2, transListm2 = snf.stackTime(rTree, entries, histListp1, histListm1, histListp2, histListm2, transListp1, transListm1, transListp2, transListm2)
    else:   #Combine photon 1 and 2
        histListp1, histListm1, transListp1, transListm1 = snf.stackTime(rTree, entries, histListp1, histListm1, 0, 0, transListp1, transListm1, 0, 0)
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
def saveEB(runNumber, dataList1, dataList2, histList1, histList2, transList1, transList2, htime1, htime2, hlaser1, hlaser2, fitdata1, fitdata2, seedmap1, seedmap2):
    if isinstance(histList1[0],list) == True: #Individual barrel crystals
        if histList2 !=0:
            f = rt.TFile(runNumber+"IndivTimeEB_p1.root","new")
            for eta in range(0,len(histList1)):
                for phi in range(0, len(histList1[0])):
                    histList1[eta][phi].Write()
                    transList1[eta][phi].Write()
                    #Saving value of data in tuple list
                    dataList1 = np.append(dataList1, [0, eta-85, phi, fitdata1[eta][phi][0],fitdata1[eta][phi][1],fitdata1[eta][phi][2],fitdata1[eta][phi][3],fitdata1[eta][phi][4],fitdata1[eta][phi][5],fitdata1[eta][phi][6]])
            htime1.Write()
            hlaser1.Write()
            if seedmap1 != 0:
                seedmap1.Write()
            f.Close()

            f2 = rt.TFile(runNumber+"IndivTimeEB_p2.root","new")
            for eta in range(0,len(histList2)):
                for phi in range(0, len(histList2[0])):
                    histList2[eta][phi].Write()
                    transList2[eta][phi].Write()
                    #Saving value of data in tuple list
                    dataList2 = np.append(dataList2, [0, eta-85, phi, fitdata2[eta][phi][0],fitdata2[eta][phi][1],fitdata2[eta][phi][2],fitdata2[eta][phi][3],fitdata2[eta][phi][4],fitdata2[eta][phi][5],fitdata1[eta][phi][6]])
            htime2.Write()
            hlaser2.Write()
            if seedmap1 != 0:
                seedmap2.Write()
            f2.Close()
    
            dataList1.shape = (171,361,10)
            dataList2.shape = (171,361,10)
            np.save(runNumber+"dataEB_p1.npy", dataList1)
            np.save(runNumber+"dataEB_p2.npy", dataList2)
        else:
            #saving all 1D histograms in tree
            f = rt.TFile(runNumber+"IndivTimeEB_c.root","new")
            for eta in range(0,len(histList1)):
                for phi in range(0, len(histList1[0])):
                    histList1[eta][phi].Write()
                    transList1[eta][phi].Write()
                    #Saving value of data in tuple list
                    dataList1 = np.append(dataList1, [0, eta-85, phi, fitdata1[eta][phi][0],fitdata1[eta][phi][1],fitdata1[eta][phi][2],fitdata1[eta][phi][3],fitdata1[eta][phi][4],fitdata1[eta][phi][5],fitdata1[eta][phi][6]])
            htime1.Write()
            hlaser1.Write()
            if seedmap1 != 0:
                seedmap1.Write()
            f.Close()

            dataList1.shape = (171,361,10)
            np.save("dataEB_c.npy", dataList1)
    else: #clustertimeEB
        if histList2 !=0:
            f = rt.TFile(runNumber+"ClusterTimeEB_p1.root","new")
            for eta in range(0,len(histList1)):
                histList1[eta].Write()
                transList1[eta].Write()
                #Saving value of data in tuple list
                dataList1 = np.append(dataList1, [0, eta-85, fitdata1[eta][0],fitdata1[eta][1],fitdata1[eta][2],fitdata1[eta][3],fitdata1[eta][4],fitdata1[eta][5],fitdata1[eta][6]])
            htime1.Write()
            hlaser1.Write()
            if seedmap1 != 0:
                seedmap1.Write()
            f.Close()
        
            f2 = rt.TFile(runNumber+"ClusterTimeEB_p2.root","new")
            for eta in range(0,len(histList2)):
                histList2[eta].Write()
                transList2[eta].Write()
                #Saving value of data in tuple list
                dataList2 = np.append(dataList2, [0, eta-85, fitdata2[eta][0],fitdata2[eta][1],fitdata2[eta][2],fitdata2[eta][3],fitdata2[eta][4],fitdata2[eta][5],fitdata1[eta][6]])
            htime2.Write()
            hlaser2.Write()
            if seedmap1 != 0:
                seedmap2.Write()
            f2.Close()
            
            #formatting and saving all data into a numpy file for analyzing later
            dataList1.shape = (171,9)
            dataList2.shape = (171,9)
            np.save(runNumber+"EtadataEB_p1.npy", dataList1)
            np.save(runNumber+"EtadataEB_p2.npy", dataList2)
        else:
            f = rt.TFile(runNumber+"ClusterTimeEB_c.root","new")
            for eta in range(0,len(histList1)):
                histList1[eta].Write()
                #Saving value of data in tuple list
                dataList1 = np.append(dataList1, [0, eta-85, fitdata1[eta][0],fitdata1[eta][1],fitdata1[eta][2],fitdata1[eta][3],fitdata1[eta][4],fitdata1[eta][5],fitdata1[eta][6]])
            htime1.Write()
            hlaser1.Write()
            if seedmap1 != 0:
                seedmap1.Write()
            f.Close()
            
            #formatting and saving all data into a numpy file for analyzing later
            dataList1.shape = (171,9)
            np.save(runNumber+"EtadataEB_c.npy", dataList1)


#saves the histograms, fits, and others for the barrel
def saveEE(runNumber,dataListp,dataListm,histListp1,histListp2,histListm1,histListm2,transListp1,transListp2,transListm1,transListm2,htimep1,htimep2,htimem1,htimem2,hlaserp1,hlaserp2,hlaserm1,hlaserm2,fitdatap1,fitdatap2,fitdatam1,fitdatam2,seedmapp1,seedmapp2,seedmapm1,seedmapm2):
    if histListp2 != 0: #2 photons
        f = rt.TFile(runNumber+"IndivTimeEEp_p1p2.root","new")
        for x in range(0,len(histListp1)):
            for y in range(0, len(histListp1[0])):
                histListp1[x][y].Write()
                histListp2[x][y].Write()
                transListp1[x][y].Write()
                transListp2[x][y].Write()
                #Saving value of data in tuple list
                dataListp = np.append(dataListp, [0, "p1", x, y, fitdatap1[x][y][0],fitdatap1[x][y][1],fitdatap1[x][y][2],fitdatap1[x][y][3],fitdatap1[x][y][4],fitdatap1[x][y][5],fitdatap1[x][y][6]])
                dataListp = np.append(dataListp, [0, "p2", x, y, fitdatap2[x][y][0],fitdatap2[x][y][1],fitdatap2[x][y][2],fitdatap2[x][y][3],fitdatap2[x][y][4],fitdatap2[x][y][5],fitdatap2[x][y][6]])
        htimep1.Write()
        htimep2.Write()
        hlaserp1.Write()
        hlaserp2.Write()
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
                transListm1[x][y].Write()
                transListm2[x][y].Write()
                #Saving value of data in tuple list
                dataListm = np.append(dataListm, [0, "m1", x, y, fitdatam1[x][y][0],fitdatam1[x][y][1],fitdatam1[x][y][2],fitdatam1[x][y][3],fitdatam1[x][y][4],fitdatam1[x][y][5],fitdatam1[x][y][6]])
                dataListm = np.append(dataListm, [0, "m2", x, y, fitdatam2[x][y][0],fitdatam2[x][y][1],fitdatam2[x][y][2],fitdatam2[x][y][3],fitdatam2[x][y][4],fitdatam2[x][y][5],fitdatam2[x][y][6]])
        htimem1.Write()
        htimem2.Write()
        hlaserm1.Write()
        hlaserm2.Write()
        if seedmapm1 != 0:
            seedmapm1.Write()
        if seedmapm2 !=0:
            seedmapm2.Write()
        f2.Close()
        
        dataListp.shape = (101,101,2,11)
        dataListm.shape = (101,101,2,11)
        np.save(runNumber+"dataEEp_p1p2.npy", dataListp)
        np.save(runNumber+"dataEEm_p1p2.npy", dataListm)
    else:
        f = rt.TFile(runNumber+"IndivTimeEEp_c.root","new")
        for x in range(0,len(histListp1)):
            for y in range(0, len(histListp1[0])):
                histListp1[x][y].Write()
                transListp1[x][y].Write()
                dataListp = np.append(dataListp, [0, "p", x, y, fitdatap1[x][y][0],fitdatap1[x][y][1],fitdatap1[x][y][2],fitdatap1[x][y][3],fitdatap1[x][y][4],fitdatap1[x][y][5],fitdatap1[x][y][6]])
        htimep1.Write()
        hlaserp1.Write()
        if seedmapp1 != 0:
            seedmapp1.Write()
        f.Close()
        
        f2 = rt.TFile(runNumber+"IndivTimeEEm_c.root","new")
        for x in range(0,len(histListm1)):
            for y in range(0, len(histListm1[0])):
                histListm1[x][y].Write()
                transListm1[x][y].Write()
                dataListm = np.append(dataListm, [0, "m", x, y, fitdatam1[x][y][0],fitdatam1[x][y][1],fitdatam1[x][y][2],fitdatam1[x][y][3],fitdatam1[x][y][4],fitdatam1[x][y][5],fitdatam1[x][y][6]])
        htimem1.Write()
        hlaserm1.Write()
        if seedmapm1 != 0:
            seedmapm1.Write()
        f2.Close()

        #formatting and saving all data into a numpy file for analyzing later
        dataListp.shape = (101,101,11)
        dataListm.shape = (101,101,11)
        np.save(runNumber+"dataEEp_c.npy", dataListp)
        np.save(runNumber+"dataEEm_c.npy", dataListm)


#draws the graphs you want to see and saves them as .png in respective folders
def printPrettyPictureEB(runNumber,htime1,htime2,hlaser1,hlaser2,seedmap1,seedmap2):
    #Gets rid of legend
    rt.gStyle.SetOptStat(0)
    os.system('.x setstyle.c')
    
    if type(htime1) != rt.TH1F: #Individual crystals
        if htime2 != 0:
            c1 = rt.TCanvas()
            htime1.SetAxisRange(-5., 5.,"Z")
            htime1.Draw("colz")
            c1.Print(runNumber+"IndivTimeResponseEB_p1.png")
            hlaser1.SetAxisRange(0., 1.,"Z")
            hlaser1.Draw("colz")
            c1.Print(runNumber+"IndivLaserTransparencyEB_p1.png")
            c1.Close()

            c2 = rt.TCanvas()
            htime2.SetAxisRange(-5., 5.,"Z")
            htime2.Draw("colz")
            c2.Print(runNumber+"IndivTimeResponseEB_p2.png")
            hlaser2.SetAxisRange(0., 1.,"Z")
            hlaser2.Draw("colz")
            c2.Print(runNumber+"IndivLaserTransparencyEB_p2.png")
            c2.Close()
        else:
            c = rt.TCanvas()
            htime1.SetAxisRange(-5., 5.,"Z")
            htime1.Draw("colz")
            c.Print(runNumber+"IndivTimeResponseEB_c.png")
            hlaser1.SetAxisRange(0., 1.,"Z")
            hlaser1.Draw("colz")
            c.Print(runNumber+"IndivLaserTransparencyEB_c.png")
            c.Close()
    else:
        if htime2 != 0:
            c1 = rt.TCanvas()
            htime1.SetAxisRange(-85,85,"X")
            htime1.Draw("E1")
            c1.Print(runNumber+"EtaTimeResponseEB_p1.png")
            hlaser1.SetAxisRange(0., 1.,"Y")
            hlaser1.Draw("colz")
            c1.Print(runNumber+"EtaLaserTransparencyEB_p1.png")
            c1.Close()
            
            c2 = rt.TCanvas()
            htime2.SetAxisRange(-85,85,"X")
            htime2.Draw("E1")
            c2.Print(runNumber+"EtaTimeResponseEB_p2.png")
            hlaser2.SetAxisRange(0., 1.,"X")
            hlaser2.Draw("colz")
            c2.Print(runNumber+"EtaLaserTransparencyEB_p2.png")
            c2.Close()

        else:
            c = rt.TCanvas()
            htime1.SetAxisRange(-85,85,"X")
            htime1.Draw("E1")
            c.Print(runNumber+"EtaTimeResponseEB_c.png")
            hlaser1.SetAxisRange(0., 1.,"X")
            hlaser1.Draw("colz")
            c.Print(runNumber+"EtaLaserTransparencyEB_c.png")
            c.Close()

    if seedmap1 != 0: #print 1 seed map
        s1 = rt.TCanvas()
        if type(htime1) != rt.TH1F: #individual crystal
            seedmap1.Draw("colz")
        else:
            seedmap1.SetAxisRange(-85,85,"X")
            seedmap1.Draw()
        s1.Print(runNumber+"SeedDensityEB.png")
        s1.Close()
        if seedmap2 != 0: #print both seed maps
            s2 = rt.TCanvas()
            if type(htime1) != rt.TH1F: #individual crystal
                seedmap2.Draw("colz")
            else:
                seedmap2.SetAxisRange(-85,85,"X")
                seedmap2.Draw()
            s2.Print(runNumber+"SeedDensityEB_p2.png")
            s2.Close()



#draws the graphs you want to see and saves them as .png in respective folders
def printPrettyPictureEE(runNumber,htimep1,htimep2,htimem1,htimem2,hlaserp1,hlaserp2,hlaserm1,hlaserm2,seedmapp1,seedmapm1,seedmapp2,seedmapm2):
    #Gets rid of legend
    rt.gStyle.SetOptStat(0)
    
    if type(htimep2) == rt.TH2F:
        c1 = rt.TCanvas()
        htimep1.SetAxisRange(-5., 5.,"Z")
        htimep1.Draw("colz")
        c1.Print(runNumber+"IndivTimeResponseEEp_p1.png")
        hlaserp1.SetAxisRange(0., 1.,"Z")
        hlaserp1.Draw("colz")
        c1.Print(runNumber+"IndivLaserTransparencyEEp_p1.png")
        c1.Close()
            
        c2 = rt.TCanvas()
        htimep2.SetAxisRange(-5., 5.,"Z")
        htimep2.Draw("colz")
        c2.Print(runNumber+"IndivTimeResponseEEp_p2.png")
        hlaserp2.SetAxisRange(0., 1.,"Z")
        hlaserp2.Draw("colz")
        c2.Print(runNumber+"IndivLaserTransparencyEEp_p2.png")
        c2.Close()
    
        c3 = rt.TCanvas()
        htimem1.SetAxisRange(-5., 5.,"Z")
        htimem1.Draw("colz")
        c3.Print(runNumber+"IndivTimeResponseEEm_p1.png")
        hlaserm1.SetAxisRange(0., 1.,"Z")
        hlaserm1.Draw("colz")
        c3.Print(runNumber+"IndivLaserTransparencyEEm_p1.png")
        c3.Close()
        
        c4 = rt.TCanvas()
        htimem2.SetAxisRange(-5., 5.,"Z")
        htimem2.Draw("colz")
        c4.Print(runNumber+"IndivTimeResponseEEm_p2.png")
        hlaserm2.SetAxisRange(0., 1.,"Z")
        hlaserm2.Draw("colz")
        c4.Print(runNumber+"IndivLaserTransparencyEEm_p2.png")
        c4.Close()
    else:
        c1 = rt.TCanvas()
        htimep1.SetAxisRange(-5., 5.,"Z")
        htimep1.Draw("colz")
        c1.Print(runNumber+"IndivTimeResponseEEp_c.png")
        hlaserp1.SetAxisRange(0., 1.,"Z")
        hlaserp1.Draw("colz")
        c1.Print(runNumber+"IndivLaserTransparencyEEp_c.png")
        c1.Close()

        c2 = rt.TCanvas()
        htimem1.SetAxisRange(-5., 5.,"Z")
        htimem1.Draw("colz")
        c2.Print(runNumber+"IndivTimeResponseEEm_c.png")
        hlaserm1.SetAxisRange(0., 1.,"Z")
        hlaserm1.Draw("colz")
        c2.Print(runNumber+"IndivLaserTransparencyEEm_c.png")
        c2.Close()

    if seedmapp1 != 0: #print 1 seed map
        s1 = rt.TCanvas()
        seedmapp1.Draw("colz")
        s1.Print(runNumber+"SeedDensityEEp.png")
        s1.Close()

        s3 = rt.TCanvas()
        seedmapm1.Draw("colz")
        s3.Print(runNumber+"SeedDensityEEm.png")
        s3.Close()
        if seedmapp2 != 0: #print both seed maps
            s2 = rt.TCanvas()
            seedmapp2.Draw("colz")
            s2.Print(runNumber+"SeedDensityEEp_p2.png")
            s2.Close()

            s4 = rt.TCanvas()
            seedmapm2.Draw("colz")
            s4.Print(runNumber+"SeedDensityEEm_p2.png")
            s4.Close()

