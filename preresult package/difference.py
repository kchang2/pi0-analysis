##
## This program plots the difference plots between runs.
## ASSUMES that fastFindResult.py has been run, and results can easily be found.
## As of now, it's is frankensteined for a very specific set of files, but can be
## modified later for a series of files. The only difference is that this would take
## an extreme amount of coding. Not hard coding, just coding.
##
## ASSUMES all .npy files are of same size (all cluster or all individual)
##
##
## NOT Running as of 09/12/2015
##

import ROOT as rt
import sys, random, math
import time, datetime
import os, shutil
import numpy as np

sys.path.insert(1, '/Users/kaichang/Desktop/analysis/') #this will get changed in fastAnalysis to appropriate location.
import parameters as p
import stackNfit as snf

def stack(clustorindiv, f1_p, f1_m, f2_p, f2_m, addorsubtract):
    dataList_m = np.array([]) #[eta, photon, ix, iy, counts, t mean, t mean error, t sigma, t sigma error, T mean, T mean error]
    dataList_p = np.array([]) # ["  ,  "]
    
    for x in range(len(f1_p)):
        for y in range(len(f1_p[0])):
        ## plus ##
            #time response
            #print "x, y, time response 1: " + str(x) + ", " + str(y) + ", " + f1_p[x][y][5]
            if float(f1_p[x][y][4]) == 0 or float(f2_p[x][y][4]) == 0:
                time = -999
                time_sigma = 0
                transp = -999
                transp_sigma = 0
                dens = 0
            else:
                if addorsubtract == "subtract":
                    f2_p[x][y][5] = -float(f2_p[x][y][5])
                time = float(f1_p[x][y][5]) + float(f2_p[x][y][5])
                time_sigma = math.sqrt( math.pow(float(f1_p[x][y][5]),2) + math.pow(float(f2_p[x][y][5]),2) )
                #percent deviation is: time_sigma = time * math.sqrt( math.pow(float(f1_p[x][y][6])/f1_p[x][y][5],2) + math.pow(float(f2_p[x][y][6])/f2_p[x][y][5],2))
                
                #laser transparency
                if addorsubtract == "subtract":
                    f2_p[x][y][9] = -float(f2_p[x][y][9])
                transp = float(f1_p[x][y][9]) + float(f2_p[x][y][9])
                transp_sigma = math.sqrt( math.pow(float(f1_p[x][y][10]),2) + math.pow(float(f2_p[x][y][10]),2) )
            
                #seed density
                dens = float(f1_p[x][y][4]) + float(f2_p[x][y][4]) #problem w/ reading file, so is float instead of int
            
            #appending
            dataList_p = np.append(dataList_p,[f1_p[x][y][0],f1_p[x][y][1],f1_p[x][y][2],f1_p[x][y][3],dens,time,time_sigma,0,0,transp,transp_sigma])
        
        ## minus ##
            #time response
            if float(f1_m[x][y][4]) == 0 or float(f2_m[x][y][4]) == 0:
                time = -999
                time_sigma = 0
                transp = -999
                transp_sigma = 0
                dens = 0
            else:
                if addorsubtract == "subtract":
                    f2_m[x][y][5] = -float(f2_m[x][y][5])
                time = float(f1_m[x][y][5]) + float(f2_m[x][y][5])
                time_sigma = math.sqrt( math.pow(float(f1_m[x][y][6]),2) + math.pow(float(f2_m[x][y][6]),2) )

                #laser transparency
                if addorsubtract == "subtract":
                    f2_m[x][y][9] = -float(f2_m[x][y][9])
                transp = float(f1_m[x][y][9]) + float(f2_m[x][y][9])
                transp_sigma = math.sqrt( math.pow(float(f1_m[x][y][10]),2) + math.pow(float(f2_m[x][y][10]),2) )

                #seed density
                dens = float(f1_m[x][y][4]) + float(f2_m[x][y][4])

            #appending
            dataList_m = np.append(dataList_m,[f1_m[x][y][0],f1_m[x][y][1],f1_m[x][y][2],f1_m[x][y][3],dens,time,time_sigma,0,0,transp,transp_sigma])
        print "Finished Row: " + str(x)
    
    dataList_p.flatten()
    dataList_m.flatten()
    if clustorindiv == "cluster":
        dataList_p.shape = (51,51,11)
        dataList_m.shape = (51,51,11)
    else:
        dataList_p.shape = (101,101,11)
        dataList_m.shape = (101,101,11)

    return dataList_p, dataList_m


def fill(dataList, hist_t, hist_l, hist_d):
    #[eta, photon, ix, iy, counts, t mean, t mean error, t sigma, t sigma error, T mean, T mean error]
    for x in range(len(dataList_p)):
        for y in range(len(dataList_p[0])):
            #time response
            hist_t.Fill(x,y,float(dataList[x][y][5])) #response mean
            hist_t.SetBinError(x+1,y+1,float(dataList[x][y][6])) #response uncertainty
            #laser transparency
            hist_l.Fill(x,y,float(dataList[x][y][9])) #transparency mean
            hist_l.SetBinError(x+1,y+1,float(dataList[x][y][10])) #transparency uncertainty
            #seed density plot
            hist_d.Fill(x,y,float(dataList[x][y][4])) #seed count
    return hist_t, hist_l, hist_d


if __name__ == "__main__":

    #maybe add in parameters.py
    numpyList = [] #list of root files from result, should at max 2
    fileList = os.listdir('.') #list of files in the result folder
    
    #finds all the .npy files
    for file in fileList:
        if '.npy' in file and 'data' in file:
            numpyList.append(file)

    if len(numpyList) == 0:
        print "sorry, no .npy files in folder"
        exit()

    if "cluster" in numpyList[0]:
        clustorindiv = "cluster"
        
        #difference histograms (htdp = *h*istgram of *t*ime response *d*ifference, plus)
        htdp = rt.TH2F("Cluster TR difference in EE+", "Cluster TR difference in EE+; iX;iY;ns",51,0,51,51,0,51) #first column or row is 0
        htdm = rt.TH2F("Cluster TR difference in EE-", "Cluster TR difference in EE-; iX;iY;ns",51,0,51,51,0,51)
        hldp = rt.TH2F("Cluster Transparency Difference in EE+", "Cluster Transparency Difference in EE+; iX;iY;Relative Transparency",51,0,51,51,0,51)
        hldm = rt.TH2F("Cluster Transparency Difference in EE-", "Cluster Transparency Difference in EE-; iX;iY;Relative Transparency",51,0,51,51,0,51)
        hddp = rt.TH2F("Cluster SPD in EE+", "Cluster SPD in EE+; iX;iY;Photon Counts",51,0,51,51,0,51)
        hddm = rt.TH2F("Cluster SPD in EE-", "Cluster SPD in EE-; iX;iY;Photon Counts",51,0,51,51,0,51)
    else:
        clustorindiv = "indiv"

        #difference histograms (htdp = *h*istgram of *t*ime response *d*ifference, plus)
        htdp = rt.TH2F("TR difference in EE+", "TR difference in EE+; iX;iY;ns",101,0,101,101,0,101) #first column or row is 0
        htdm = rt.TH2F("TR difference in EE-", "TR difference in EE-; iX;iY;ns",101,0,101,101,0,101)
        hldp = rt.TH2F("Transparency Difference in EE+", "Transparency Difference in EE+; iX;iY;Relative Transparency",101,0,101,101,0,101)
        hldm = rt.TH2F("Transparency Difference in EE-", "Transparency Difference in EE-; iX;iY;Relative Transparency",101,0,101,101,0,101)
        hddp = rt.TH2F("SPD in EE+", "SPD in EE+; iX;iY;Photon Counts",101,0,101,101,0,101)
        hddm = rt.TH2F("SPD in EE-", "SPD in EE-; iX;iY;Photon Counts",101,0,101,101,0,101)


    #2015A - 2015B
    for numpyfile in numpyList:
        if "2015A" and "EEp" in numpyfile:
            fA_p = np.load(numpyfile)
        if "2015A" and "EEm" in numpyfile:
            fA_m = np.load(numpyfile)
        if "2015B" and "EEp" in numpyfile:
            fB_p = np.load(numpyfile)
        if "2015B" and "EEm" in numpyfile:
            fB_m = np.load(numpyfile)

    #stack data and place into arrays
    dataList_p, dataList_m = stack(clustorindiv,fA_p,fA_m,fB_p,fB_m,"subtract")

    #Fill the histograms
    htdp, hldp, hddp = fill(dataList_p, htdp, hldp, hddp)
    htdm, hldm, hddm = fill(dataList_m, htdm, hldm, hddm)

    #creates permanent canvas, only need to do ONCE.
    rt.gROOT.LoadMacro('setstyle.c')
    rt.gROOT.Macro('setstyle.c')
    c = rt.TCanvas("c","c",600,500)
    c.cd()

    #Print out results and saves them#
    #plus
    htdp.SetAxisRange(-2., 2.,"Z")
    htdp.Draw("colz")
    htdp.GetYaxis().SetTitleOffset(1.1)
    htdp.GetZaxis().SetTitleOffset(0.8)
    c.Print("AB_TR_D_EEp.png")
    hldp.SetAxisRange(-0.2, 0.2,"Z")
    hldp.Draw("colz")
    hldp.GetYaxis().SetTitleOffset(1.1)
    hldp.GetZaxis().SetTitleOffset(1.1)
    c.Print("AB_LS_D_EEp.png")
    hddp.SetMinimum(0.)
    hddp.Draw("colz")
    hddp.GetYaxis().SetTitleOffset(1.1)
    c.Print("AB_SD_D_EEp.png")
    #minus
    htdm.SetAxisRange(-5., 5.,"Z")
    htdm.Draw("colz")
    htdm.GetYaxis().SetTitleOffset(1.1)
    htdm.GetZaxis().SetTitleOffset(0.8)
    c.Print("AB_TR_D_EEm.png")
    hldm.SetAxisRange(-1., 1.,"Z")
    hldm.Draw("colz")
    hldm.GetYaxis().SetTitleOffset(1.1)
    hldm.GetZaxis().SetTitleOffset(1.1)
    c.Print("AB_LS_D_EEm.png")
    hddm.SetMinimum(0.)
    hddm.Draw("colz")
    hddm.GetYaxis().SetTitleOffset(1.1)
    c.Print("AB_SD_D_EEm.png")


    #2015A - 2015C
    for numpyfile in numpyList:
        if "2015C" and "EEp" in numpyfile:
            fC_p = np.load(numpyfile)
        if "2015C" and "EEm" in numpyfile:
            fC_m = np.load(numpyfile)
    #stack
    dataList_p, dataList_m = stack(clustorindiv,fA_p,fA_m,fC_p,fC_m,"subtract")

    #Fill the histograms
    htdp, hldp, hddp = fill(dataList_p, htdp, hldp, hddp)
    htdm, hldm, hddm = fill(dataList_m, htdm, hldm, hddm)

    #Print out results and saves them#
    #plus
    htdp.SetAxisRange(-5., 5.,"Z")
    htdp.Draw("colz")
    htdp.GetYaxis().SetTitleOffset(1.1)
    htdp.GetZaxis().SetTitleOffset(0.8)
    c.Print("AC_TR_D_EEp.png")
    hldp.SetAxisRange(-1., 1.,"Z")
    hldp.Draw("colz")
    hldp.GetYaxis().SetTitleOffset(1.1)
    hldp.GetZaxis().SetTitleOffset(1.1)
    c.Print("AC_LS_D_EEp.png")
    hddp.SetMinimum(0.)
    hddp.Draw("colz")
    hddp.GetYaxis().SetTitleOffset(1.1)
    c.Print("AC_SD_D_EEp.png")
    #minus
    htdm.SetAxisRange(-5., 5.,"Z")
    htdm.Draw("colz")
    htdm.GetYaxis().SetTitleOffset(1.1)
    htdm.GetZaxis().SetTitleOffset(0.8)
    c.Print("AC_TR_D_EEm.png")
    hldm.SetAxisRange(-1, 1.,"Z")
    hldm.Draw("colz")
    hldm.GetYaxis().SetTitleOffset(1.1)
    hldm.GetZaxis().SetTitleOffset(1.1)
    c.Print("AC_LS_D_EEm.png")
    hddm.SetMinimum(0.)
    hddm.Draw("colz")
    hddm.GetYaxis().SetTitleOffset(1.1)
    c.Print("AC_SD_D_EEm.png")


    #(2015A + 2015B) - 2015C
    #stack data and place into arrays
    dataList_p, dataList_m = stack(clustorindiv,fA_p,fA_m,fB_p,fB_m,"add")
    dataList_p, dataList_m = stack(clustorindiv,dataList_p, dataList_p,fC_p,fC_m,"subtract")

    #Fill the histograms
    htdp, hldp, hddp = fill(dataList_p, htdp, hldp, hddp)
    htdm, hldm, hddm = fill(dataList_m, htdm, hldm, hddm)

    #Print out results and saves them#
    #plus
    htdp.SetAxisRange(-5., 5.,"Z")
    htdp.Draw("colz")
    htdp.GetYaxis().SetTitleOffset(1.1)
    htdp.GetZaxis().SetTitleOffset(0.8)
    c.Print("A+B-C_TR_D_EEp.png")
    hldp.SetAxisRange(-1., 1.,"Z")
    hldp.Draw("colz")
    hldp.GetYaxis().SetTitleOffset(1.1)
    hldp.GetZaxis().SetTitleOffset(1.1)
    c.Print("A+B-C_LS_D_EEp.png")
    hddp.SetMinimum(0.)
    hddp.Draw("colz")
    hddp.GetYaxis().SetTitleOffset(1.1)
    c.Print("A+B-C_SD_D_EEp.png")
    #minus
    htdm.SetAxisRange(-5., 5.,"Z")
    htdm.Draw("colz")
    htdm.GetYaxis().SetTitleOffset(1.1)
    htdm.GetZaxis().SetTitleOffset(0.8)
    c.Print("A+B-C_TR_D_EEm.png")
    hldm.SetAxisRange(-1., 1.,"Z")
    hldm.Draw("colz")
    hldm.GetYaxis().SetTitleOffset(1.1)
    hldm.GetZaxis().SetTitleOffset(1.1)
    c.Print("A+B-C_LS_D_EEm.png")
    hddm.SetMinimum(0.)
    hddm.Draw("colz")
    hddm.GetYaxis().SetTitleOffset(1.1)
    c.Print("A+B-C_SD_D_EEm.png")