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
            if float(f1_p[x][y][4]) == 0 or float(f1_p[x][y][5]) == 0 or float(f2_p[x][y][4]) == 0 or float(f2_p[x][y][5]) == 0:
                time = -999
                time_sigma = 0
                transp = -999
                transp_sigma = 0
                dens = 0
            else:
                if addorsubtract == "subtract":
                    val = -float(f2_p[x][y][5])
                else:
                    val = float(f2_p[x][y][5])
                time = float(f1_p[x][y][5]) + val
                try:
                    time_sigma = math.sqrt( math.pow(float(f1_p[x][y][6]),2) + math.pow(float(f2_p[x][y][6]),2) )
                except:
                    pass
                #print f2_p[x][y][5] + ", " + f1_p[x][y][5]
                #percent deviation is: time_sigma = time * math.sqrt( math.pow(float(f1_p[x][y][6])/f1_p[x][y][5],2) + math.pow(float(f2_p[x][y][6])/f2_p[x][y][5],2))
                
                #laser transparency
                if addorsubtract == "subtract":
                    val = -float(f2_p[x][y][9])
                else:
                    val = float(f2_p[x][y][9])
                transp = float(f1_p[x][y][9]) + val
                try:
                    transp_sigma = math.sqrt( math.pow(float(f1_p[x][y][10]),2) + math.pow(float(f2_p[x][y][10]),2) )
                except:
                    pass
            
                #seed density
                dens = float(f1_p[x][y][4]) + float(f2_p[x][y][4]) #problem w/ reading file, so is float instead of int
            
            #appending
            dataList_p = np.append(dataList_p,[f1_p[x][y][0],f1_p[x][y][1],f1_p[x][y][2],f1_p[x][y][3],dens,time,time_sigma,0,0,transp,transp_sigma])
        
        ## minus ##
            #time response
            if float(f1_m[x][y][4]) == 0 or float(f1_m[x][y][5]) == 0 or float(f2_m[x][y][4]) == 0 or float(f2_m[x][y][5]) == 0:
                time = -999
                time_sigma = 0
                transp = -999
                transp_sigma = 0
                dens = 0
            else:
                if addorsubtract == "subtract":
                    val = -float(f2_m[x][y][5])
                else:
                    val = float(f2_m[x][y][5])
                time = float(f1_m[x][y][5]) + val
                try:
                    time_sigma = math.sqrt( math.pow(float(f1_m[x][y][6]),2) + math.pow(float(f2_m[x][y][6]),2) )
                except:
                    pass

                #laser transparency
                if addorsubtract == "subtract":
                    val = -float(f2_m[x][y][9])
                else:
                    val = float(f2_m[x][y][9])
                transp = float(f1_m[x][y][9]) + val
                try:
                    transp_sigma = math.sqrt( math.pow(float(f1_m[x][y][10]),2) + math.pow(float(f2_m[x][y][10]),2) )
                except:
                    pass
                #seed density
                dens = float(f1_m[x][y][4]) + float(f2_m[x][y][4])

            #appending
            dataList_m = np.append(dataList_m,[f1_m[x][y][0],f1_m[x][y][1],f1_m[x][y][2],f1_m[x][y][3],dens,time,time_sigma,0,0,transp,transp_sigma])
        
        if x % 11 == 0:
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


def wghtavg(f1, f2, clustorindiv):
    f = np.array([])
    for x in range(len(f1)):
        for y in range(len(f1[0])):
            if float(f1[x][y][4]) == 0 and float(f2[x][y][4]) == 0:
                t_mean = 0
                t_sigma = 0
                t_Sigma = 0
                t_Sigma_sigma = 0
                T_mean = 0
                T_sigma = 0
            else:
                #print f1[x][y][4] + ", " + f2[x][y][4] + ", " + f1[x][y][5] + ", " + f2[x][y][5]
                t_mean = (float(f1[x][y][5]) * float(f1[x][y][4]) + float(f2[x][y][5]) * float(f2[x][y][4]))/(float(f1[x][y][4]) + float(f2[x][y][4]))
                try:
                    t_Sigma = (float(f1[x][y][7]) * float(f1[x][y][4]) + float(f2[x][y][7]) * float(f2[x][y][4]))/(float(f1[x][y][4]) + float(f2[x][y][4]))
                except:
                    pass
                T_mean = (float(f1[x][y][9]) * float(f1[x][y][4]) + float(f2[x][y][9]) * float(f2[x][y][4]))/(float(f1[x][y][4]) + float(f2[x][y][4]))
                
                #print f1[x][y][5] + ", " + str(t_mean)
                
                if float(f1[x][y][5]) == 0 or float(f1[x][y][7]) == 0 or float(f1[x][y][9] == 0) or float(f2[x][y][5]) == 0 or float(f2[x][y][7]) == 0 or float(f2[x][y][9] == 0):
                        t_sigma = 0
                        t_Sigma_sigma = 0
                        T_sigma = 0
                else:
                    t_sigma = t_mean * math.sqrt( math.pow(float(f1[x][y][6])/float(f1[x][y][5]),2) + math.pow(float(f2[x][y][6])/float(f2[x][y][5]),2) )
                    try:
                        t_Sigma_sigma = t_Sigma * math.sqrt( math.pow(float(f1[x][y][8])/float(f1[x][y][7]),2) + math.pow(float(f2[x][y][8])/float(f2[x][y][7]),2) )
                    except:
                        T_sigma = t_mean * math.sqrt( math.pow(float(f1[x][y][10])/float(f1[x][y][9]),2) + math.pow(float(f2[x][y][10])/float(f2[x][y][9]),2) )

            count = float(f1[x][y][4]) + float(f2[x][y][4])
            f = np.append(f, [f1[x][y][0], f1[x][y][1], f1[x][y][2], f1[x][y][3], count, t_mean, t_sigma, t_Sigma, t_Sigma_sigma, T_mean, T_sigma])

    f.flatten()
    if clustorindiv == "cluster":
        f.shape = (51,51,11)
    else:
        f.shape = (101,101,11)
    return f


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
        if "2015A" in numpyfile and "EEp" in numpyfile:
            fA_p = np.load(numpyfile)
        if "2015A" in numpyfile and "EEm" in numpyfile:
            fA_m = np.load(numpyfile)
        if "2015B" in numpyfile and "EEp" in numpyfile:
            fB_p = np.load(numpyfile)
        if "2015B" in numpyfile and "EEm" in numpyfile:
            fB_m = np.load(numpyfile)

    #stack data and place into arrays
    dataList_p, dataList_m = stack(clustorindiv,fB_p,fB_m,fA_p,fA_m,"subtract")

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
    htdp.SetAxisRange(-5, 5,"Z")
    htdp.Draw("colz")
    htdp.GetYaxis().SetTitleOffset(1.1)
    htdp.GetZaxis().SetTitleOffset(1.1)
    c.Print("Clust_BA_TR_D_EEp.png")
    hldp.SetAxisRange(-1, 1,"Z")
    hldp.Draw("colz")
    hldp.GetYaxis().SetTitleOffset(1.1)
    hldp.GetZaxis().SetTitleOffset(1.25)
    c.Print("Clust_BA_LS_D_EEp.png")
    hddp.SetMinimum(0.)
    hddp.Draw("colz")
    hddp.GetYaxis().SetTitleOffset(1.1)
    hddp.GetZaxis().SetTitleOffset(1.1)
    c.Print("Clust_BA_SD_D_EEp.png")
    #minus
    htdm.SetAxisRange(-5, 5,"Z")
    htdm.Draw("colz")
    htdm.GetYaxis().SetTitleOffset(1.1)
    htdm.GetZaxis().SetTitleOffset(1.1)
    c.Print("Clust_BA_TR_D_EEm.png")
    hldm.SetAxisRange(-1, 1,"Z")
    hldm.Draw("colz")
    hldm.GetYaxis().SetTitleOffset(1.1)
    hldm.GetZaxis().SetTitleOffset(1.25)
    c.Print("Clust_BA_LS_D_EEm.png")
    hddm.SetMinimum(0.)
    hddm.Draw("colz")
    hddm.GetYaxis().SetTitleOffset(1.1)
    hddm.GetZaxis().SetTitleOffset(1.1)
    c.Print("Clust_BA_SD_D_EEm.png")


    #2015A - 2015C
    for numpyfile in numpyList:
        if "2015C" in numpyfile and "EEp" in numpyfile:
            fC_p = np.load(numpyfile)
        if "2015C" in numpyfile and "EEm" in numpyfile:
            fC_m = np.load(numpyfile)
    #stack
    dataList_p, dataList_m = stack(clustorindiv, fC_p, fC_m, fA_p, fA_m, "subtract")

    #Fill the histograms
    htdp, hldp, hddp = fill(dataList_p, htdp, hldp, hddp)
    htdm, hldm, hddm = fill(dataList_m, htdm, hldm, hddm)

    #Print out results and saves them#
    #plus
    htdp.SetAxisRange(-5, 5,"Z")
    htdp.Draw("colz")
    htdp.GetYaxis().SetTitleOffset(1.1)
    htdp.GetZaxis().SetTitleOffset(1.1)
    c.Print("Clust_CA_TR_D_EEp.png")
    hldp.SetAxisRange(-1, 1,"Z")
    hldp.Draw("colz")
    hldp.GetYaxis().SetTitleOffset(1.1)
    hldp.GetZaxis().SetTitleOffset(1.25)
    c.Print("Clust_CA_LS_D_EEp.png")
    hddp.SetMinimum(0.)
    hddp.Draw("colz")
    hddp.GetYaxis().SetTitleOffset(1.1)
    hddp.GetZaxis().SetTitleOffset(1.25)
    c.Print("Clust_CA_SD_D_EEp.png")
    #minus
    htdm.SetAxisRange(-5, 5,"Z")
    htdm.Draw("colz")
    htdm.GetYaxis().SetTitleOffset(1.1)
    htdm.GetZaxis().SetTitleOffset(1.1)
    c.Print("Clust_CA_TR_D_EEm.png")
    hldm.SetAxisRange(-1, 1,"Z")
    hldm.Draw("colz")
    hldm.GetYaxis().SetTitleOffset(1.1)
    hldm.GetZaxis().SetTitleOffset(1.25)
    c.Print("Clust_CA_LS_D_EEm.png")
    hddm.SetMinimum(0.)
    hddm.Draw("colz")
    hddm.GetYaxis().SetTitleOffset(1.1)
    hddm.GetZaxis().SetTitleOffset(1.25)
    c.Print("Clust_CA_SD_D_EEm.png")

    #2015A - 2015D
    for numpyfile in numpyList:
        if "2015D" in numpyfile and "EEp" in numpyfile:
            fD_p = np.load(numpyfile)
        if "2015D" in numpyfile and "EEm" in numpyfile:
            fD_m = np.load(numpyfile)
    #stack
    dataList_p, dataList_m = stack(clustorindiv, fD_p, fD_m, fA_p, fA_m, "subtract")
    
    #Fill the histograms
    htdp, hldp, hddp = fill(dataList_p, htdp, hldp, hddp)
    htdm, hldm, hddm = fill(dataList_m, htdm, hldm, hddm)
    
    #Print out results and saves them#
    #plus
    htdp.SetAxisRange(-5, 5,"Z")
    htdp.Draw("colz")
    htdp.GetYaxis().SetTitleOffset(1.1)
    htdp.GetZaxis().SetTitleOffset(1.1)
    c.Print("Clust_DA_TR_D_EEp.png")
    hldp.SetAxisRange(-1, 1,"Z")
    hldp.Draw("colz")
    hldp.GetYaxis().SetTitleOffset(1.1)
    hldp.GetZaxis().SetTitleOffset(1.25)
    c.Print("Clust_DA_LS_D_EEp.png")
    hddp.SetMinimum(0.)
    hddp.Draw("colz")
    hddp.GetYaxis().SetTitleOffset(1.1)
    hddp.GetZaxis().SetTitleOffset(1.25)
    c.Print("Clust_DA_SD_D_EEp.png")
    #minus
    htdm.SetAxisRange(-5, 5,"Z")
    htdm.Draw("colz")
    htdm.GetYaxis().SetTitleOffset(1.1)
    htdm.GetZaxis().SetTitleOffset(1.1)
    c.Print("Clust_DA_TR_D_EEm.png")
    hldm.SetAxisRange(-1, 1,"Z")
    hldm.Draw("colz")
    hldm.GetYaxis().SetTitleOffset(1.1)
    hldm.GetZaxis().SetTitleOffset(1.25)
    c.Print("Clust_DA_LS_D_EEm.png")
    hddm.SetMinimum(0.)
    hddm.Draw("colz")
    hddm.GetYaxis().SetTitleOffset(1.1)
    hddm.GetZaxis().SetTitleOffset(1.25)
    c.Print("Clust_DA_SD_D_EEm.png")


    #(2015A + 2015B) - 2015C
    ## remember that + means adding statistics, not adding the physical value
    #stack data and place into arrays
    AplusBp = wghtavg(fA_p, fB_p, clustorindiv)
    AplusBm = wghtavg(fA_m, fB_m, clustorindiv)
    dataList_p, dataList_m = stack(clustorindiv, fC_p, fC_m, AplusBp, AplusBm, "subtract")

    #Fill the histograms
    htdp, hldp, hddp = fill(dataList_p, htdp, hldp, hddp)
    htdm, hldm, hddm = fill(dataList_m, htdm, hldm, hddm)

    #Print out results and saves them#
    #plus
    htdp.SetAxisRange(-5., 5.,"Z")
    htdp.Draw("colz")
    htdp.GetYaxis().SetTitleOffset(1.1)
    htdp.GetZaxis().SetTitleOffset(0.8)
    c.Print("Clust_C-AB_TR_D_EEp.png")
    hldp.SetAxisRange(-1., 1.,"Z")
    hldp.Draw("colz")
    hldp.GetYaxis().SetTitleOffset(1.1)
    hldp.GetZaxis().SetTitleOffset(1.1)
    c.Print("Clust_C-AB_LS_D_EEp.png")
    hddp.SetMinimum(0.)
    hddp.Draw("colz")
    hddp.GetYaxis().SetTitleOffset(1.1)
    c.Print("Clust_C-AB_SD_D_EEp.png")
    #minus
    htdm.SetAxisRange(-5., 5.,"Z")
    htdm.Draw("colz")
    htdm.GetYaxis().SetTitleOffset(1.1)
    htdm.GetZaxis().SetTitleOffset(0.8)
    c.Print("Clust_C-AB_TR_D_EEm.png")
    hldm.SetAxisRange(-1., 1.,"Z")
    hldm.Draw("colz")
    hldm.GetYaxis().SetTitleOffset(1.1)
    hldm.GetZaxis().SetTitleOffset(1.1)
    c.Print("Clust_C-AB_LS_D_EEm.png")
    hddm.SetMinimum(0.)
    hddm.Draw("colz")
    hddm.GetYaxis().SetTitleOffset(1.1)
    c.Print("Clust_C-AB_SD_D_EEm.png")