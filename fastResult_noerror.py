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
import copy
import numpy as np

sys.path.insert(1, '/Users/kaichang/Desktop/analysis/') #this will get changed in fastAnalysis to appropriate location.
import stackNfit as snf
import parameters as p
import fast_assemble as a

from FastProgressBar import progressbar

#assumes all data is correct (no modifications)
#assumes canvas already made
## just fits transparency to time response
def fit(npyList, length, depth, type):
    grphlist = [[rt.TGraphErrors() for i in range(depth)] for j in range(length)]
    fitdata = np.array([])
    n = len(npyList)
    if type == "EB":
        time_loc = 3
        trans_loc = 7
    else:
        time_loc = 5
        trans_loc = 9
    #maybe need to draw canvas
    for x in range(length):
        for y in range(depth):
            T = np.array([])
            t = np.array([])
            eT = np.array([])
            et = np.array([])
            for file in npyList:
                f = np.load(file)
                t = np.append(t, float(f[x][y][time_loc]))
                T = np.append(T, float(f[x][y][trans_loc]))
                try:
                    et = np.append(eT, 0)
#                    et = np.append(et, float(f[x][y][6]))
                except:
                    et = np.append(et, 0)
                try:
                    eT = np.append(eT, 0)
#                    eT = np.append(eT, float(f[x][y][10])) # <- not sure if need #transparency, time response, time response error
                except:
                    eT = np.append(eT, 0)
        
#            print t, T
            gr = rt.TGraphErrors(4,T,t,eT,et)

            #apply fit
            fit1 = rt.TF1("fit1","pol1", -100, 100)
            gr.Fit(fit1)
            
            p0 = fit1.GetParameter(0)
            p1 = fit1.GetParameter(1)
            e0 = fit1.GetParError(0)
            e1 = fit1.GetParError(1)

#            gr.Fit("pol1")
#            linplot = gr.GetFunction("pol1")
#            p0 = linplot.GetParameter(0)
#            p1 = linplot.GetParameter(1)
#            
#            name = "transparency vs. time response (%i,%i)" %(x,y)
#            title = "transparency vs. time response (%i,%i)" %(x,y)
#            linplot.SetTitle(name)
#            linplot.GetXaxis().SetTitle("Transparency")
#            linplot.GetYaxis().SetTitle("Time Response")
#            linplot.GetXaxis().CenterTitle()
#            linplot.GetYaxis().CenterTitle()

            print x,y
            if x == 20 and y == 30:
#                print t, T
#                print p0, p1
                c = rt.TCanvas()
                gr.SetTitle(name)
                gr.GetXaxis().SetTitle("Transparency")
                gr.GetYaxis().SetTitle("ns")
                gr.Draw("A*")
                #linplot.Draw()
                c.Print("tvT_20-30_noerr" + type + ".png")
                    
            if x == 40 and y == 20:
#                print t, T
#                print p0, p1
                c = rt.TCanvas()
                gr.SetTitle(name)
                gr.GetXaxis().SetTitle("Transparency")
                gr.GetYaxis().SetTitle("ns")
                gr.Draw("A*")
                #linplot.Draw()
                c.Print("tvT_40-20_noerr" + type + ".png")

            #append to grphlist
            grphlist[x][y] = copy.deepcopy(gr)
#            grphlist[x][y] = copy.deepcopy(linplot)
#            grphlist.append(linplot)

            #save fit to fitdata
            fitdata = np.append(fitdata,[p0,p1,e0,e1])
    
    fitdata.flatten()
    if len(f[0]) == 101:
        fitdata.shape = (101,101,2)
    elif len(f[0]) == 51:
        fitdata.shape = (51,51,2)
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
        grphlistEB, fitdataEB = fit(npyList_EB, 171, 361, "EB")
        #save graph list to .root
        f = rt.TFile("fit_EB_noerr.root","new")
        for x in range(0,len(grphlistEB)):
            for y in range(0,len(grphlistEB[0])):
                grphlistEB[x][y].Write()
        f.Close()
        #saves data to npy file
        np.save("fit_parameters_EB_noerr.npy",fitdataEB)

    if len(npyList_EEp) != 0:
        npyList_EEp.sort()
        grphlistEEp, fitdataEEp = fit(npyList_EEp, 51, 51, "EEp")
        #save graph list to .root
        f = rt.TFile("fit_EEp_noerr.root","new")
#        print type(grphlistEEp[1][0])
#        print type(grphlistEEp[1][1])
#        exit()
        for x in range(0,len(grphlistEEp)):
            for y in range(0,len(grphlistEEp[0])):
                grphlistEEp[x][y].Write()
        f.Close()
        np.save("fit_parameters_EEp_noerr.npy",fitdataEEp)

    if len(npyList_EEm) != 0:
        npyList_EEm.sort()
        grphlistEEm, fitdataEEm = fit(npyList_EEm, 51, 51, "EEm")
        #save graph list to .root
        f = rt.TFile("fit_EEm_noerr.root","new")
        for x in range(0,len(grphlistEEm)):
            for y in range(0,len(grphlistEEm[0])):
                grphlistEEm[x][y].Write()
        f.Close()
        #saves data to npy file
        np.save("fit_parameters_EEm_noerr.npy",fitdataEEm)

    print "Finished fitting the crystals, Mr. Chang."
    #creates permanent canvas, only need to do ONCE.
#    rt.gROOT.LoadMacro('setstyle.c')
#    rt.gROOT.Macro('setstyle.c')
#    c = rt.TCanvas("c","c",600,500)
#    c.cd()


