##
## This is the meaty part of the code.
## Not too much to say about it.
##
## Updated as of 07/27/2015
## NOT Running as of 07/27/2015
##
from __future__ import division
import ROOT as rt
import sys, random, math
from FastProgressBar import progressbar

# This will stack time response based upon each individual crystal (both eta,phi and x,y)
# This is for endcap and barrel
def stackTime(rTree, entries, histlist, histlist2, histlist3, histlist4):

    if entries != -1:
        nentries = entries
    else:
        #gets number of entries (collision bunches)
        nentries = rTree.GetEntries()

    #creates a progress bar
    pbar = progressbar("Stacking", nentries).start()

    #check if want to make 2 separate plots for p1 and p2 or conjoined
    if histlist3 !=0:
        pass

    #makes 1 plot for both photon 1 and 2, double stacking all the way
    else:
        if len(histlist) != 101: #not endcap
            for i in range(0, nentries):
                rTree.GetEntry(i)
                for rec in range(0,rTree.STr2_NPi0_rec):
                    if rTree.STr2_iEta_1[rec]+85 < 0 or rTree.STr2_iPhi_1[rec] < 0:
                        pass
                    else:
                        histlist[rTree.STr2_iEta_1[rec]+85][rTree.STr2_iPhi_1[rec]].Fill(rTree.STr2_Time_1[rec])
                    if rTree.STr2_iEta_2[rec]+85 < 0 or rTree.STr2_iPhi_2[rec] < 0:
                        pass
                    else:
                        histlist[rTree.STr2_iEta_2[rec]+85][rTree.STr2_iPhi_2[rec]].Fill(rTree.STr2_Time_2[rec])
                pbar.update(i+1)
            pbar.finish()
            return histlist

        else: #is endcap
            for i in range(0, nentries):
                rTree.GetEntry(i)
                for rec in range(0,rTree.STr2_NPi0_rec):
                    if rTree.STr2_Eta_1[rec] > 1.4:
                        if rTree.STr2_iX_1[rec] < 0 or rTree.STr2_iY_1[rec] < 0:
                            pass
                        else:
                            histlist[rTree.STr2_iX_1[rec]][rTree.STr2_iY_1[rec]].Fill(rTree.STr2_Time_1[rec])
                    elif rTree.STr2_Eta_1[rec] < 1.4:
                        if rTree.STr2_iX_1[rec] < 0 or rTree.STr2_iY_1[rec] < 0:
                            pass
                        else:
                            histlist2[rTree.STr2_iX_1[rec]][rTree.STr2_iY_1[rec]].Fill(rTree.STr2_Time_1[rec])
                    if rTree.STr2_Eta_2[rec] > 1.4:
                        if rTree.STr2_iX_2[rec] < 0 or rTree.STr2_iY_2[rec] < 0:
                            pass
                        else:
                            histlist[rTree.STr2_iX_2[rec]][rTree.STr2_iY_2[rec]].Fill(rTree.STr2_Time_2[rec])
                    elif rTree.STr2_Eta_2[rec] < 1.4:
                        if rTree.STr2_iX_2[rec] < 0 or rTree.STr2_iY_2[rec] < 0:
                            pass
                        else:
                            histlist2[rTree.STr2_iX_2[rec]][rTree.STr2_iY_2[rec]].Fill(rTree.STr2_Time_2[rec])
                pbar.update(i+1)
            pbar.finish()
            return histlist, histlist2
    
    #stack 2 separate plots for 2 photons of interest
    if len(histlist) != 101: #not endcap
        for i in range(0, nentries):
            rTree.GetEntry(i)
            for rec in range(0,rTree.STr2_NPi0_rec):
                if rTree.STr2_iEta_1[rec]+85 < 0 or rTree.STr2_iPhi_1[rec] < 0:
                    pass
                else:
                    histlist[rTree.STr2_iEta_1[rec]+85][rTree.STr2_iPhi_1[rec]].Fill(rTree.STr2_Time_1[rec])
                if rTree.STr2_iEta_2[rec]+85 < 0 or rTree.STr2_iPhi_2[rec] < 0:
                    pass
                else:
                    histlist2[rTree.STr2_iEta_2[rec]+85][rTree.STr2_iPhi_2[rec]].Fill(rTree.STr2_Time_2[rec])
            pbar.update(i+1)
        pbar.finish()
        return histlist, histlist2
    else: #is endcap
        for i in range(0, nentries): ####CHANGED####
            rTree.GetEntry(i)
            for rec in range(0,rTree.STr2_NPi0_rec):
                if rTree.STr2_Eta_1[rec] > 1.4:
                    if rTree.STr2_iX_1[rec] < 0 or rTree.STr2_iY_1[rec] < 0:
                        pass
                    else:
                            histlist[rTree.STr2_iX_1[rec]][rTree.STr2_iY_1[rec]].Fill(rTree.STr2_Time_1[rec])
                elif rTree.STr2_Eta_1[rec] < 1.4:
                    if rTree.STr2_iX_1[rec] < 0 or rTree.STr2_iY_1[rec] < 0:
                        pass
                    else:
                            histlist2[rTree.STr2_iX_1[rec]][rTree.STr2_iY_1[rec]].Fill(rTree.STr2_Time_1[rec])
                if rTree.STr2_Eta_2[rec] > 1.4:
                    if rTree.STr2_iX_2[rec] < 0 or rTree.STr2_iY_2[rec] < 0:
                        pass
                    else:
                            histlist3[rTree.STr2_iX_2[rec]][rTree.STr2_iY_2[rec]].Fill(rTree.STr2_Time_2[rec])
                elif rTree.STr2_Eta_2[rec] < 1.4:
                    if rTree.STr2_iX_2[rec] < 0 or rTree.STr2_iY_2[rec] < 0:
                        pass
                    else:
                            histlist4[rTree.STr2_iX_2[rec]][rTree.STr2_iY_2[rec]].Fill(rTree.STr2_Time_2[rec])
            pbar.update(i+1)
        pbar.finish()
        return histlist, histlist2, histlist3, histlist4


# This will fit gaussians to all the individual crystal time response histograms and converge them into a 2d histogram with the mean value.
def fitTime(histlist, htime):
    #rt.RooMsgService.instance().setSilentMode(True)
    #rt.RooFit.PrintEvalErrors(-1)

    if len(histlist) != 101:
        yaxis = "phi"
        adjust = -85
    else:
        yaxis = "Y"
        adjust = 0

    for x in range(0,len(histlist)):
        #print "completed " + str(x) + " out of " + str(len(histlist)) + " columns."
        for y in range(0,len(histlist[0])):
            hist = histlist[x][y]
            binmax = hist.GetMaximumBin()
            max = hist.GetXaxis().GetBinCenter(binmax)
            
            m = rt.RooRealVar("t","t (ns)",max-2,max+2)
            dh = rt.RooDataHist("dh","dh",rt.RooArgList(m),rt.RooFit.Import(hist))
                                        
            frame = m.frame(rt.RooFit.Title("Time response"))
                                            
            frame.SetYTitle("Counts")
            frame.SetTitleOffset (1.4, "Y")
            
            dh.plotOn(frame)
                                                        
            # define gaussian
            mean = rt.RooRealVar("mean","mean",0.,-2,2.)
            sigma = rt.RooRealVar("sigma","sigma",0.,-2,2)
            gauss = rt.RooGaussian("gauss","gauss",m,mean,sigma)
                                                                    
            #Construct the composite model
            #nsig = rt.RooRealVar("nsig","number of signal events", 100000., 0., 10000000)
            #nbkg = rt.RooRealVar("nbkg", "number of background events", 10000, 0., 10000000)

            fr = gauss.fitTo(dh,rt.RooFit.Save())

            if x == 0 and y == 0:
                gauss.plotOn(frame)
                c1 = rt.TCanvas()
                #c1.SetLogy()
                frame.Draw()
                c1.Print("timeresponse"+str(x)+str(yaxis)+str(y)+".png")
            
            htime.Fill(x+adjust,y,mean.getVal())
    return htime


# This will stack time response based upon each eta ring
# This is for barrel
def stackTimeEta(rTree,entries,histlist,histlist2):

    if entries != -1:
        nentries = entries
    else:
        #gets number of entries (collision bunches)
        nentries = rTree.GetEntries()
    
    #creates a progress bar
    pbar = progressbar("Stacking", nentries).start()

    if histlist2 != 0:
        pass
    else:
        for i in range(0, nentries):
            rTree.GetEntry(i)
            for rec in range(0,rTree.STr2_NPi0_rec):
                if rTree.STr2_iEta_1[rec]+85 < 0:
                    pass
                else:
                    histlist[rTree.STr2_iEta_1[rec]+85].Fill(rTree.STr2_Time_1[rec])
                if rTree.STr2_iEta_2[rec]+85 < 0:
                    pass
                else:
                    histlist[rTree.STr2_iEta_2[rec]+85].Fill(rTree.STr2_Time_2[rec])
            pbar.update(i+1)
        pbar.finish()
        return histlist

    for i in range(0, nentries):
        rTree.GetEntry(i)
        for rec in range(0,rTree.STr2_NPi0_rec):
            if rTree.STr2_iEta_1[rec]+85 < 0:
                pass
            else:
                histlist[rTree.STr2_iEta_1[rec]+85].Fill(rTree.STr2_Time_1[rec])
            if rTree.STr2_iEta_2[rec]+85 < 0:
                pass
            else:
                histlist2[rTree.STr2_iEta_2[rec]+85].Fill(rTree.STr2_Time_2[rec])
        pbar.update(i+1)
    pbar.finish()
    return histlist, histlist2

#This will fit gaussians to all the eta rings
def fitTimeEta(histlist, htime):
    fitdata = [[0 for values in range(4)] for eta in range(171)] #(mean,error,sigma,error)
    for eta in range(0,len(histlist)):
        hist = histlist[eta]
        binmax = hist.GetMaximumBin()
        max = hist.GetXaxis().GetBinCenter(binmax)
        m = rt.RooRealVar("t","t (ns)",max-1.5,max+1.5)
        dh = rt.RooDataHist("dh","dh",rt.RooArgList(m),rt.RooFit.Import(hist))
        
        frame = m.frame(rt.RooFit.Title("Time response"))
        
        
        frame.SetYTitle("Counts")
        frame.SetTitleOffset(1.4, "Y")
        
        dh.plotOn(frame)
        
        # define gaussian
        mean = rt.RooRealVar("mean","mean",0.1,-2,2.)
        sigma = rt.RooRealVar("sigma","sigma",0.1,-2.,2)
        gauss = rt.RooGaussian("gauss","gauss",m,mean,sigma)
            
        fr = gauss.fitTo(dh,rt.RooFit.Save(),rt.RooFit.PrintLevel(-1), rt.RooFit.Verbose(rt.kFALSE))

        if eta <10:
            gauss.plotOn(frame)
            c1 = rt.TCanvas()
            #c1.SetLogy()
            frame.Draw()
            c1.Print("timeresponseEta"+str(eta)+".png")

        fitdata[eta][0]=mean.getVal()
        fitdata[eta][1]=mean.getError()
        fitdata[eta][2]=sigma.getVal()
        fitdata[eta][3]=sigma.getError()
        htime.Fill(eta-85,mean.getVal())
    return htime, fitdata


# This will stack mass based on the ROOT file
def stackMass(rTree,histmass):
    
    #gets number of entries (collision bunches)
    nentries = rTree.GetEntries()
    
    #creates a progress bar
    pbar = progressbar("Stacking", nentries).start()
    
    for i in range(0, nentries):
        rTree.GetEntry(i)
        for rec in range(0,rTree.STr2_NPi0_rec):
            if rTree.STr2_Pi0recIsEB[rec]:
                histmass.Fill(rTree.STr2_mPi0_rec[rec])
        pbar.update(i+1)
    pbar.finish()
    return histmass


#This will fit the appropriate fit by ROOT files
def fitMassROOT(histlist):
    hmassvalues = [0]*len(histlist)
    for j in range(0,len(histlist)):
        hist = histlist[j]
        binmax = hist.GetMaximumBin()
        max = hist.GetXaxis().GetBinCenter(binmax)
        #print "binmax: " + str(binmax) + " and max: " + str(max)
        m = rt.RooRealVar("mass","mass (MeV)",max-0.02,max+0.02)
        dh = rt.RooDataHist("dh","dh",rt.RooArgList(m),rt.RooFit.Import(hist))
        
        frame = m.frame(rt.RooFit.Title("Pi0 Mass"))
        frame.SetYTitle("Counts")
        frame.SetTitleOffset(1.4, "Y")
        
        dh.plotOn(frame)
        
        # define gaussian
        mean = rt.RooRealVar("mean","mean",0.,-2,2.)
        sigma = rt.RooRealVar("sigma","sigma",0.,-2,2)
        gauss = rt.RooGaussian("gauss","gauss",m,mean,sigma)
        
        #Construct the composite model
        #nsig = rt.RooRealVar("nsig","number of signal events", 100000., 0., 10000000)
        #nbkg = rt.RooRealVar("nbkg", "number of background events", 10000, 0., 10000000)
        
        fr = gauss.fitTo(dh,rt.RooFit.Save())
        
        gauss.plotOn(frame)
        c1 = rt.TCanvas()
        c1.SetLogy()
        frame.Draw()
        c1.Print("Pi0mass"+str(hist)+".png")
        hmassvalues[j] = mean.getVal()
    return hmassvalues


#This will fit the appropriate fit by the Run
def fitMass(hist):
    binmax = hist.GetMaximumBin()
    max = hist.GetXaxis().GetBinCenter(binmax)
    #print "binmax: " + str(binmax) + " and max: " + str(max)
    m = rt.RooRealVar("mass","mass (MeV)",max-0.02,max+0.02)
    dh = rt.RooDataHist("dh","dh",rt.RooArgList(m),rt.RooFit.Import(hist))
        
    frame = m.frame(rt.RooFit.Title("Pi0 Mass"))
    frame.SetYTitle("Counts")
    frame.SetTitleOffset(1.4, "Y")
    
    dh.plotOn(frame)
    
    # define gaussian
    mean = rt.RooRealVar("mean","mean",0.,-2,2.)
    sigma = rt.RooRealVar("sigma","sigma",0.,-2,2)
    gauss = rt.RooGaussian("gauss","gauss",m,mean,sigma)
        
    #Construct the composite model
    #nsig = rt.RooRealVar("nsig","number of signal events", 100000., 0., 10000000)
    #nbkg = rt.RooRealVar("nbkg", "number of background events", 10000, 0., 10000000)
        
    fr = gauss.fitTo(dh,rt.RooFit.Save())
    gauss.plotOn(frame)
    c1 = rt.TCanvas()
    c1.SetLogy()
    frame.Draw()
    c1.Print("Pi0massRun2015A.png")
    return mean.getVal()







