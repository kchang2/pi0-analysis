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

sys.path.insert(1, '/Users/kaichang/Desktop/analysis/') #this will get changed in fastAnalysis to appropriate location.
import stackNfit as snf
import parameters as p
import fast_assemble as a

from FastProgressBar import progressbar

#assumes all data is correct (no modifications)
#assumes canvas already made
## just fits transparency to time response
def fit(npyList):
    grphlist = []
    fitdata = []
    T = []
    t = []
    print len(npyList)
    print npyList
    #maybe need to draw canvas
    for x in range(len(npyList[0])):
        for y in range(len(npyList[0][0])):
            for file in npyList:
#                print file
#                print file[x][y]
                t.append(file[x][y][5])
                T.append(file[x][y][9])
                et.append(file[x][y][6])
                eT.append(file[x][y][10]) # <- not sure if need #transparency, time response, time response error
            
            name = "transparency vs. time response (%i,%i)" %(x,y)
            title = "transparency vs. time response (%i,%i)" %(x,y)
            gr = rt.TGraphErrors(name,title,len(T),T,t,eT,et)

            #apply fit
            gr.Fit("pol1")
            linplot = gr.GetFunction("pol1")
            p0 = linplot.GetParameter(0)
            p1 = linplot.GetParameter(1)

            #append to grphlist
            grphlist.append(linplot)

            #save fit to fitdata
            fitdata.append(p0,p1)

    fitdata.flatten()
    if len(npyList[0]) == 101:
        fitdata.shape = (101,101,2)
    elif len(npyList[0]) == 51:
        fitdata.shape = (51, 51, 2)
    else:
        fitdata.shape = (171,361,2)
    return grphlist, fitdata

if __name__ == "__main__":

    #add in parameters.py the location of the npy files

    npyList_EEp = []
    npyList_EEm = []
    npyList_EB = []
    fileList = os.listdir('.')

    for file in fileList:
        if '.npy' in file and 'data' in file and "EEp" in file:
            npyList_EEp.append(file)
        if '.npy' in file and 'data' in file and "EEm" in file:
            npyList_EEm.append(file)
        if '.npy' in file and 'data' in file and "EB" in file:
            npyList_EB.append(file)

    if len(npyList_EB) == 0 and len(npyList_EEp) == 0 and len(npyList_EEm) == 0:
        print "sorry, no .npy files in folder. Check parameters.py for search location"
        exit()

    if len(npyList_EB) != 0:
        npyList_EB.sort()
        grphlistEB, fitdataEB = fit(npyList_EB)
        #save graph list to .root
        f.rt.TFile("fit_EEp.root","new")
        for x in range(0,len(grphlistEEp)):
            grphlistEEp.Write()
        f.Close()
        #saves data to npy file
        np.save("fit_parameters_EEp.npy",fitdataEEp)

    if len(npyList_EEp) != 0:
        npyList_EEp.sort()
        grphlistEEp, fitdataEEp = fit(npyList_EEp)
        #save graph list to .root
        f.rt.TFile("fit_EEp.root","new")
        for x in range(0,len(grphlistEEp)):
            grphlistEEp.Write()
        f.Close()
        np.save("fit_parameters_EEp.npy",fitdataEEp)

    if len(npyList_EB) != 0:
        npyList_EEm.sort()
        grphlistEEm, fitdataEEm = fit(npyList_EEm)
        #save graph list to .root
        f.rt.TFile("fit_EEp.root","new")
        for x in range(0,len(grphlistEEp)):
            grphlistEEp.Write()
        f.Close()
        #saves data to npy file
        np.save("fit_parameters_EEp.npy",fitdataEEp)

    #creates permanent canvas, only need to do ONCE.
#    rt.gROOT.LoadMacro('setstyle.c')
#    rt.gROOT.Macro('setstyle.c')
#    c = rt.TCanvas("c","c",600,500)
#    c.cd()


