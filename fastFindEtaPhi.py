##
## Helps establish the values of phi and eta for each crystal
## in the barrel and endcap. The crystal in the barrel
## uses the actual eta length per crystal. The crystal
## in the endcap uses a mean weight distribution since
## the eta from the data takes in the weighted location
## of the hit, and there is not real defined range for these
## crystals and their eta lengths.
##
## NOT Running as of 08/19/2015
##


import ROOT as rt
import sys, random, math
import time, datetime
import os, shutil
import numpy as np

import parameters as p

if __name__ == "__main__":

    
#Barrel
    barreleta = [['iEta','eta']]
    barreleta.append([-85, -1.4703]) #-1.4703 comes from 85 crystals * 0.0174 eta width - 0.0174/2 for the center of -85 iEta crystal.
    
    for i in range(1,170): #key is that we start at 1, so we can end at 170
        nexteta = barreleta[i][1] + 0.0174
        nextpos = -85+i
        if i >= 85:
            nextpos+=1
        barreleta.append([nextpos, nexteta])
#    np.save("barrelEtaValues.npy",barreleta)
#    print barreleta[86] #this is the 1st positive

#Endcap

    endcapetaplus = [[['x','y','eta']]] #[x[y[eta]]]
    endcapetaminus = [[['x','y','eta']]]

    #Fill array with necessary data
    for x in range(101):
        endcapetaplus.append([])
        endcapetaminus.append([])
        for y in range(101):
            endcapetaplus[x+1].append([x,y,-999])
            endcapetaminus[x+1].append([x,y,-999])
#    print endcapetaplus

    #Check and change current working directory.
    stardir = os.getcwd()
    print "Current working directory %s" % stardir
    os.chdir(p.rootFileLocationLocal)
    retdir = os.getcwd()
    print "Directory changed successfully %s" % retdir

    ## Root file path and file name you analyze ##
    fileList = os.listdir(p.rootFileLocationLocal)
    fileList.sort()
    filename = p.runNumber + "EcalNtp_"

    ##Get data ready to search
    rTree = rt.TChain("Tree_Optim")
    for k in range(len(fileList)):
        if filename in fileList[k]:
            rTree.Add(fileList[k])
            print "successfully cut branch from " + fileList[k]

    ##Find eta and fill
    nentries = rTree.GetEntries()

    for i in range(0, nentries):
        rTree.GetEntry(i)
        for rec in range(0, rTree.STr2_NPi0_rec):
#            print "Phi: " + str(rTree.STr2_iPhi_1[rec]) + ", iEta: " + str(rTree.STr2_iEta_1[rec]) + ", iY: " + str(rTree.STr2_iY_1[rec]) + ", iX: " + str(rTree.STr2_iX_1[rec]) + ", Eta: " + str(rTree.STr2_Eta_1[rec]) + ", is in EB: " + str(rTree.STr2_Pi0recIsEB[rec])
            if rTree.STr2_Pi0recIsEB[rec] == True: #If not endcap, kick out
                continue
            if rTree.STr2_iX_1[rec] < 0 or rTree.STr2_iY_1[rec] < 0:
                pass
            else:
                print "Phi: " + str(rTree.STr2_iPhi_1[rec]) + ", iEta: " + str(rTree.STr2_iEta_1[rec]) + ", iY: " + str(rTree.STr2_iY_1[rec]) + ", iX: " + str(rTree.STr2_iX_1[rec]) + ", Eta: " + str(rTree.STr2_Eta_1[rec]) + ", is in EB: " + str(rTree.STr2_Pi0recIsEB[rec])
#                if rTree.STr2_Eta_1[rec] > 1.479: #Is it EE+?
#                    endcapetaplus[rTree.STr2_iX_1[rec]+1].append([rTree.STr2_iX_1[rec], rTree.STr2_iY_1[rec], rTree.STr2_Eta_1[rec]])
#                elif rTree.STr2_Eta_1[rec] < -1.479: #Is it EE-?
#                    endcapetaminus[rTree.STr2_iX_1[rec]+1].append([rTree.STr2_iX_1[rec], rTree.STr2_iY_1[rec], rTree.STr2_Eta_1[rec]])
#
#            if rTree.STr2_iX_2[rec] < 0 or rTree.STr2_iY_2[rec] < 0:
#                pass
#            else:
#                #Now we work on the second photon hit
#                if rTree.STr2_Eta_2[rec] > 1.479: #Is it EE+?
#                    endcapetaplus[rTree.STr2_iX_2[rec]+1].append([rTree.STr2_iX_2[rec], rTree.STr2_iY_2[rec], rTree.STr2_Eta_2[rec]])
#                elif rTree.STr2_Eta_2[rec] < -1.479:
#                    endcapetaminus[rTree.STr2_iX_2[rec]+1].append([rTree.STr2_iX_2[rec], rTree.STr2_iY_2[rec], rTree.STr2_Eta_2[rec]])
