##
## ASSUME the files outputted are purely _c files (combining photon 1 and photon 2)
## currently only for endcaps, will be soon modified for barrel
##
##
## NOT Running as of 08/19/2015
##
import ROOT as rt
import sys, random, math
import time, datetime
import os, shutil
import numpy as np

import stackNfit as snf
import parameters as p
import fast_assemble as a

from FastProgressBar import progressbar

#assumes all data is correct (no modifications)
#assumes canvas already made
## just fits transparency to time response
def fit(npyList):
    grphlist, fitdata T, t = []
    #maybe need to draw canvas
    for x in len(npyList[0]):
        for y in len(npyList[0][0]):
            for file in npyList:
                T.append(file[x][y][9])
                t.append(file[x][y][5])
                eT.append(file[x][y]10) # <- not sure if need
                et.append(file[x][y][6])#transparency, time response, time response error
                hprof.SetBinError()
            
            name = "transparency vs. time response (%i,%i)" %(x,y)
            title = "transparency vs. time response (%i,%i)" %(x,y)
            gr = rt.TGraphErrors(name,title,len(T),T,t,eT,et)

            #apply fit
            
            
            #append to grphlist
            #save fit to fitdata

    return grphlist, fitdata

if __name__ == "__main__":

    #add in parameters.py the location of the npy files

    npyList_EEp = []
    npyList_EEm = []
    npyList_EB = []
    fileList = os.listdir('.')

    for file in fileList:
        if '.npy' in file and 'data' and "EEp" in file:
            npyList_EEp.append(file)
        if '.npy' in file and 'data' and "EEm" in file:
            npyList_EEm.append(file)
        if '.npy' in file and 'data' and "EB" in file:
            npyList_EB.append(file)

    if len(npyList_EB) == 0 and len(npyList_EEp) == 0 and len(npyList_EEm) == 0:
        print "sorry, no .npy files in folder. Check parameters.py for search location"
        exit()

        npyList_EEp.sort()
        npyList_EEm.sort()
        npyList_EB.sort()

    #creates permanent canvas, only need to do ONCE.
#    rt.gROOT.LoadMacro('setstyle.c')
#    rt.gROOT.Macro('setstyle.c')
#    c = rt.TCanvas("c","c",600,500)
#    c.cd()

    #maybe need to normalize the data

    grphlistEEp, fitdataEEp = fit(npyList_EEp)
    grphlistEEm, fitdataEEm = fit(npyList_EEm)
    grphlistEB, fitdataEB = fit(npyList_EB)

    #save graph list to .root
    #save fitdata to .npy

