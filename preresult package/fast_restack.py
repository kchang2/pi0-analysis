##
## This program clusters all the crystals together in 2x2 cluster and then outputs them.
## Currently it only runs with endcap, will be modified to run with EB soon.
##
##
## Running as of 08/19/2015
##
import ROOT as rt
import sys, random, math
import time, datetime
import os, shutil
import numpy as np

sys.path.insert(1, '/Users/kaichang/Desktop/analysis/')
import parameters as p
import stackNfit as snf

def fit(hist, type):
    #get bin position of maximum value
    binmax = hist.GetMaximumBin()
    max = hist.GetXaxis().GetBinCenter(binmax)
    
    #get entries for within appropriate range
    entries = snf.pevents(hist,binmax,p.manualHitCounterCut,40)
    
    
    if type == "transparency":
        #check to see if there are enough entries
        if entries < p.minStat:
            return -999, 0
        if entries < p.minNormal:
            return hist.GetMean(), hist.GetMeanError()
    
        m = rt.RooRealVar("Transparency","Transparency Factor",max-0.05,max+0.05)
        dh = rt.RooDataHist("dh","dh",rt.RooArgList(m),rt.RooFit.Import(hist))
        frame = m.frame(rt.RooFit.Title("Transparency"))
        frame.SetYTitle("Counts")
        frame.SetTitleOffset (2.6, "Y")
        dh.plotOn(frame)
        # define gaussian
        mean = rt.RooRealVar("mean","mean",1.,-5.,10)
        sigma = rt.RooRealVar("sigma","sigma",0.1,-5.,10.)
        gauss = rt.RooGaussian("gauss","gauss",m,mean,sigma)
        
        fr = gauss.fitTo(dh,rt.RooFit.Save(),rt.RooFit.PrintLevel(-1), rt.RooFit.Verbose(rt.kFALSE))
        return mean.getVal(), mean.getError()
    else:
        #check to see if there are enough entries
        if entries < p.minStat:
            return entries, -999, 0, 0, 0
        if entries < p.minNormal:
            return entries, hist.GetMean(), hist.GetMeanError(), hist.GetStdDev(), hist.GetStdDevError()

        m = rt.RooRealVar("t","t (ns)",max-2,max+2)
        dh = rt.RooDataHist("dh","dh",rt.RooArgList(m),rt.RooFit.Import(hist))
        frame = m.frame(rt.RooFit.Title("Time response"))
        frame.SetYTitle("Counts")
        frame.SetTitleOffset (2.6, "Y")
        dh.plotOn(frame)
        # define gaussian
        mean = rt.RooRealVar("mean","mean",0.1,-5,5.)
        sigma = rt.RooRealVar("sigma","sigma",0.1,-5.,5)
        gauss = rt.RooGaussian("gauss","gauss",m,mean,sigma)
        
        fr = gauss.fitTo(dh,rt.RooFit.Save(),rt.RooFit.PrintLevel(-1), rt.RooFit.Verbose(rt.kFALSE))
        return entries, mean.getVal(), mean.getError(), sigma.getVal(), sigma.getError()






if __name__ == "__main__":

    os.chdir('..')
    rootList = [] #list of root files from result, should at max 2
    fileList = os.listdir('.') #list of files in the result folder
    
    #finds all the .root files
    for file in fileList:
        if ".root" in file and 'IndivTime' in file:
            rootList.append(file)

    if len(rootList) == 0:
        print "sorry, no .root files in folder"
        exit()

    #clustered histograms
    htcp = rt.TH2F("Cluster TR in EE+", "Cluster TR in EE+; iX;iY;ns",51,0,51,51,0,51) #first column or row is 0
    htcm = rt.TH2F("Cluster TR in EE-", "Cluster TR in EE-; iX;iY;ns",51,0,51,51,0,51)
    hlcp = rt.TH2F("Cluster Transparency in EE+", "Cluster Transparency in EE+; iX;iY;Relative Transparency",51,0,51,51,0,51)
    hlcm = rt.TH2F("Cluster Transparency in EE-", "Cluster Transparency in EE-; iX;iY;Relative Transparency",51,0,51,51,0,51)
    hdcp = rt.TH2F("Cluster SPD in EE+", "Cluster SPD in EE+; iX;iY;Photon Counts",51,0,51,51,0,51)
    hdcm = rt.TH2F("Cluster SPD in EE-", "Cluster SPD in EE-; iX;iY;Photon Counts",51,0,51,51,0,51)

#####NEED TO SEE IF ANY SEED DENSITY IS TRUE OR FALSE#####
### Individual Rebin ###
    #opens the endcap region and then stacks in clusters
    for rootfile in rootList:
        r = rt.TFile.Open(rootfile)
        histList = [] #list of histograms to save onto the ROOT file
        dataList = np.array([]) #[eta, photon, ix, iy, counts, mean, mean error, sigma, sigma error, t mean, t mean error]
        if 'p_c' in rootfile:
            for x in range(0, htcp.GetNbinsX()):
                for y in range(0, htcp.GetNbinsY()):
                    if x == 0 or y == 0:
                        htcp.Fill(x,y,-999)
                        hlcp.Fill(x,y,-999)
                        hdcp.Fill(x,y,-999)
                        data = [0,"c",x,y,0,-999,0,0,0,-999,0]
                        dataList = np.append(dataList, data)
                        
                        timetitle = "time on plus sc (%i,%i)" %(x,y)
                        transtitle = "transparency on plus sc (%i,%i)" %(x,y)
                        hist = r.Get(timetitle)
                        histList.append(hist.Clone())
                        hist = r.Get(transtitle)
                        histList.append(hist.Clone())
                        continue
                
                ##time response##
                    title1 = "time on plus sc (%i,%i)" %(2*x,2*y) #2*x,2*y, +1 each if 0,len-1
                    title2 = "time on plus sc (%i,%i)" %(2*x-1,2*y)
                    title3 = "time on plus sc (%i,%i)" %(2*x-1,2*y-1)
                    title4 = "time on plus sc (%i,%i)" %(2*x,2*y-1)
                    ht1 = r.Get(title1)
                    ht2 = r.Get(title2)
                    ht3 = r.Get(title3)
                    ht4 = r.Get(title4)
                    newname = "time on plus sc (%i,%i)" %(x,y)
                    hist = ht1.Clone(newname)
                    hist.Add(ht2,1)
                    hist.Add(ht3,1)
                    hist.Add(ht4,1)
                    histList.append(hist)
                    
                    #fit baby fit
                    a,b,c,d,e = fit(hist, "time response")
                    data = [0,"c",x,y,a,b,c,d,e]
                    dataList = np.append(dataList, data)
                    htcp.Fill(x,y,data[5])
                    htcp.SetBinError(x+1,y+1,data[6])
                    
                ##seed density##
                    hdcp.Fill(x,y,data[4])
                    
                ##laser transparency##
                    title1 = "transparency on plus sc (%i,%i)" %(2*x,2*y) #2*x,2*y, +1 each if 0,len-1
                    title2 = "transparency on plus sc (%i,%i)" %(2*x-1,2*y)
                    title3 = "transparency on plus sc (%i,%i)" %(2*x-1,2*y-1)
                    title4 = "transparency on plus sc (%i,%i)" %(2*x,2*y-1)
                    hl1 = r.Get(title1)
                    hl2 = r.Get(title2)
                    hl3 = r.Get(title3)
                    hl4 = r.Get(title4)
                    newname = "transparency on plus sc (%i,%i)" %(x,y)
                    hist = hl1.Clone(newname)
                    hist.Add(hl2,1)
                    hist.Add(hl3,1)
                    hist.Add(hl4,1)
                    histList.append(hist)

                    #fit baby fit
                    a, b = fit(hist, "transparency")
                    data = [a,b]
                    dataList = np.append(dataList, data)
                    
                    hlcp.Fill(x,y,data[0])
                    hlcp.SetBinError(x+1,y+1,data[1])


            #print out images
            c = rt.TCanvas()
            htcp.SetAxisRange(-5., 5.,"Z")
            htcp.Draw("colz")
            c.Print(p.runNumber+"clusterTimeResponseEEp_c.png")
            hlcp.SetAxisRange(0., 1.,"Z")
            hlcp.Draw("colz")
            c.Print(p.runNumber+"clusterLaserTransparencyEEp_c.png")
            hdcp.SetMinimum(0)
            hdcp.Draw("colz")
            if p.includeClusterSeedMap == True:
                c.Print(p.runNumber+"clusterPhotonDensityEEp_c.png")
            c.Close()

            #save files
            f = rt.TFile(p.runNumber+"ClusterTimeEEp_c.root","new")
            htcp.Write()
            hlcp.Write()
            hdcp.Write()
            f.Close()
            
            #formatting and saving all data into a numpy file for analyzing later
            dataList.shape = (51,51,11)
            np.save(p.runNumber+"cluserdataEEp_c.npy", dataList)

        elif 'm_c' in rootfile:
            for x in range(0, htcm.GetNbinsX()):
                for y in range(0, htcm.GetNbinsY()):
                    if x == 0 or y == 0:
                        htcm.Fill(x,y,-999)
                        hlcm.Fill(x,y,-999)
                        hdcm.Fill(x,y,-999)
                        data = [0,"c",x,y,0,-999,0,0,0,-999,0]
                        dataList = np.append(dataList, data)
                        
                        timetitle = "time on minus sc (%i,%i)" %(x,y)
                        transtitle = "transparency on minus sc (%i,%i)" %(x,y)
                        hist = r.Get(timetitle)
                        histList.append(hist.Clone())
                        hist = r.Get(transtitle)
                        histList.append(hist.Clone())
                        continue
                
                    ##time response##
                    title1 = "time on minus sc (%i,%i)" %(2*x,2*y) #2*x,2*y, +1 each if 0,len-1
                    title2 = "time on minus sc (%i,%i)" %(2*x-1,2*y)
                    title3 = "time on minus sc (%i,%i)" %(2*x-1,2*y-1)
                    title4 = "time on minus sc (%i,%i)" %(2*x,2*y-1)
                    ht1 = r.Get(title1)
                    ht2 = r.Get(title2)
                    ht3 = r.Get(title3)
                    ht4 = r.Get(title4)
#                    print ht1
                    newname = "time on minus sc (%i,%i)" %(x,y)
                    hist = ht1.Clone(newname)
                    hist.Add(ht2,1)
                    hist.Add(ht3,1)
                    hist.Add(ht4,1)
                    histList.append(hist)

                    #fit baby fit
                    a,b,c,d,e = fit(hist, "time response")
                    data = [0,"c", x, y, a, b, c, d, e]
                    dataList = np.append(dataList, data)
                    htcm.Fill(x,y,data[5])
                    htcm.SetBinError(x+1,y+1,data[6])
                    
                    ##seed density##
                    hdcm.Fill(x,y,data[4])
                    
                    ##laser transparency##
                    title1 = "transparency on minus sc (%i,%i)" %(2*x,2*y) #2*x,2*y, +1 each if 0,len-1
                    title2 = "transparency on minus sc (%i,%i)" %(2*x-1,2*y)
                    title3 = "transparency on minus sc (%i,%i)" %(2*x-1,2*y-1)
                    title4 = "transparency on minus sc (%i,%i)" %(2*x,2*y-1)
                    hl1 = r.Get(title1)
                    hl2 = r.Get(title2)
                    hl3 = r.Get(title3)
                    hl4 = r.Get(title4)
                    newname = "transparency on minus sc (%i,%i)" %(x,y)
                    hist = hl1.Clone(newname)
                    hist.Add(hl2,1)
                    hist.Add(hl3,1)
                    hist.Add(hl4,1)
                    histList.append(hist)
                    
                    #fit baby fit
                    a, b = fit(hist, "transparency")
                    data = [a,b]
                    dataList = np.append(dataList, data)

                    hlcm.Fill(x,y,data[0])
                    hlcm.SetBinError(x+1,y+1,data[1])

#                    time.sleep(0.25)

            #print out images
            c = rt.TCanvas()
            htcm.SetAxisRange(-5., 5.,"Z")
            htcm.Draw("colz")
            c.Print(p.runNumber+"clusterTimeResponseEEm_c.png")
            hlcm.SetAxisRange(0., 1.,"Z")
            hlcm.Draw("colz")
            c.Print(p.runNumber+"clusterLaserTransparencyEEm_c.png")
            hdcm.SetMinimum(0)
            hdcm.Draw("colz")
            if p.includeClusterSeedMap == True:
                c.Print(p.runNumber+"clusterPhotonDensityEEm_c.png")
            c.Close()

            #save files
            f = rt.TFile(p.runNumber+"ClusterTimeEEm_c.root","new")
            htcm.Write()
            hlcm.Write()
            hdcm.Write()
            f.Close()
    
            #formatting and saving all data into a numpy file for analyzing later
            dataList.flatten()
            dataList.shape = (51,51,11)
            np.save(p.runNumber+"cluserdataEEm_c.npy", dataList)

        else:
            pass
            #barrel?


#def fit(hist, type):
#    #get bin position of maximum value
#    binmax = hist.GetMaximumBin()
#    max = hist.GetXaxis().GetBinCenter(binmax)
#    
#    #get entries for within appropriate range
#    entries = snf.pevents(hist,binmax,p.manualHitCounterCut,40)
#    
#    
#    if type == "transparency":
#        #check to see if there are enough entries
#        if entries < p.minStat:
#            return -999, 0
#        if entries < p.minNormal:
#            return hist.hist.GetMean(), hist.GetMeanError()
#        
#        m = rt.RooRealVar("Transparency","Transparency Factor",max-0.05,max+0.05)
#        dh = rt.RooDataHist("dh","dh",rt.RooArgList(m),rt.RooFit.Import(hist))
#        frame = m.frame(rt.RooFit.Title("Transparency"))
#        frame.SetYTitle("Counts")
#        frame.SetTitleOffset (2.6, "Y")
#        dh.plotOn(frame)
#        # define gaussian
#        mean = rt.RooRealVar("mean","mean",1.,-5.,10)
#        sigma = rt.RooRealVar("sigma","sigma",0.1,-5.,10.)
#        gauss = rt.RooGaussian("gauss","gauss",m,mean,sigma)
#
#        fr = gauss.fitTo(dh,rt.RooFit.Save(),rt.RooFit.PrintLevel(-1), rt.RooFit.Verbose(rt.kFALSE))
#        return mean.getVal(), mean.getError()
#    else:
#        #check to see if there are enough entries
#        if entries < p.minStat:
#            return entries, -999, 0, 0, 0
#        if entries < p.minNormal:
#            return entries, hist.hist.GetMean(), hist.GetMeanError(), hist.GetStdDev(), hist.GetStdDevError()
#        
#        m = rt.RooRealVar("t","t (ns)",max-2,max+2)
#        dh = rt.RooDataHist("dh","dh",rt.RooArgList(m),rt.RooFit.Import(hist))
#        frame = m.frame(rt.RooFit.Title("Time response"))
#        frame.SetYTitle("Counts")
#        frame.SetTitleOffset (2.6, "Y")
#        dh.plotOn(frame)
#        # define gaussian
#        mean = rt.RooRealVar("mean","mean",0.1,-5,5.)
#        sigma = rt.RooRealVar("sigma","sigma",0.1,-5.,5)
#        gauss = rt.RooGaussian("gauss","gauss",m,mean,sigma)
#
#        fr = gauss.fitTo(dh,rt.RooFit.Save(),rt.RooFit.PrintLevel(-1), rt.RooFit.Verbose(rt.kFALSE))
#        return entries, mean.getVal(), mean.getError(), sigma.getVal(), sigma.getError()
