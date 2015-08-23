##
## This is the meaty part of the code.
## Not too much to say about it.
##
## Running as of 08/19/2015
##
from __future__ import division
import ROOT as rt
import sys, random, math
from FastProgressBar import progressbar
import fast_cut as fc

# This will stack time response based upon each individual crystal (both eta,phi and x,y)
# This is for endcap and barrel
def stackTime(rTree, entries, histlist, histlist2, histlist3, histlist4, translist, translist2, translist3, translist4):

    if entries != -1:
        nentries = entries
    else:
        #gets number of entries (collision bunches)
        nentries = rTree.GetEntries()

    #creates a progress bar
    pbar = progressbar("Stacking", nentries).start()

    #check if want to make 2 separate plots for p1 and p2 or conjoined
    if histlist3 !=0: #(p1,p2,m1,m2)
        pass

    #makes 1 plot for both photon 1 and 2, double stacking all the way
    else: #(p,m,0,0)
        if len(histlist) != 101: #not endcap
            for i in range(0, nentries):
                rTree.GetEntry(i)
                for rec in range(0,rTree.STr2_NPi0_rec):
                    if rTree.STr2_Pi0recIsEB[rec] != True:
                        continue
                    if rTree.STr2_iEta_1[rec]+85 < 0 or rTree.STr2_iPhi_1[rec] < 0:
                        pass
                    else:
                        if fc.applyCuts(rTree,rec,rTree.STr2_Eta_1[rec], True) is False: #photon 1
                            continue
                        if rTree.STr2_iEta_1[rec] >= 0: #accounting for crystal 0 being 1
                            histlist[rTree.STr2_iEta_1[rec]+86][rTree.STr2_iPhi_1[rec]].Fill(rTree.STr2_Time_1[rec])
                            translist[rTree.STr2_iEta_1[rec]+86][rTree.STr2_iPhi_1[rec]].Fill(float(1)/rTree.STr2_Laser_rec_1[rec])
                        else:
                            histlist[rTree.STr2_iEta_1[rec]+85][rTree.STr2_iPhi_1[rec]].Fill(rTree.STr2_Time_1[rec])
                            translist[rTree.STr2_iEta_1[rec]+85][rTree.STr2_iPhi_1[rec]].Fill(float(1)/rTree.STr2_Laser_rec_1[rec])
                    if rTree.STr2_iEta_2[rec]+85 < 0 or rTree.STr2_iPhi_2[rec] < 0:
                        pass
                    else:
                        if fc.applyCuts(rTree,rec,rTree.STr2_Eta_2[rec], False) is False: #photon 2
                            continue
                        if rTree.STr2_iEta_2[rec] >= 0: #accounting for crystal 0 being 1
                            histlist[rTree.STr2_iEta_2[rec]+86][rTree.STr2_iPhi_2[rec]].Fill(rTree.STr2_Time_2[rec])
                            translist[rTree.STr2_iEta_2[rec]+86][rTree.STr2_iPhi_2[rec]].Fill(float(1)/rTree.STr2_Laser_rec_2[rec])
                        else:
                            histlist[rTree.STr2_iEta_2[rec]+85][rTree.STr2_iPhi_2[rec]].Fill(rTree.STr2_Time_2[rec])
                            translist[rTree.STr2_iEta_2[rec]+85][rTree.STr2_iPhi_2[rec]].Fill(float(1)/rTree.STr2_Laser_rec_2[rec])
                pbar.update(i+1)
            pbar.finish()
            return histlist, translist

        else: #is endcap
            for i in range(0, nentries):
                rTree.GetEntry(i)
                for rec in range(0,rTree.STr2_NPi0_rec):
                    if rTree.STr2_Pi0recIsEB[rec] == True:
                        continue
                    if rTree.STr2_Eta_1[rec] > 1.479:
                        if rTree.STr2_iX_1[rec] < 0 or rTree.STr2_iY_1[rec] < 0:
                            pass
                        else:
                            if fc.applyCuts(rTree,rec,rTree.STr2_Eta_1[rec], True) is False: #photon 1 in EE+
                                continue
                            histlist[rTree.STr2_iX_1[rec]][rTree.STr2_iY_1[rec]].Fill(rTree.STr2_Time_1[rec])
                            translist[rTree.STr2_iX_1[rec]][rTree.STr2_iY_1[rec]].Fill(float(1)/rTree.STr2_Laser_rec_1[rec])
                    elif rTree.STr2_Eta_1[rec] < -1.479:
                        if rTree.STr2_iX_1[rec] < 0 or rTree.STr2_iY_1[rec] < 0:
                            pass
                        else:
                            if fc.applyCuts(rTree,rec,rTree.STr2_Eta_1[rec], True) is False: #photon 1 in EE-
                                continue
                            histlist2[rTree.STr2_iX_1[rec]][rTree.STr2_iY_1[rec]].Fill(rTree.STr2_Time_1[rec])
                            translist2[rTree.STr2_iX_1[rec]][rTree.STr2_iY_1[rec]].Fill(float(1)/rTree.STr2_Laser_rec_1[rec])
                    if rTree.STr2_Eta_2[rec] > 1.479:
                        if rTree.STr2_iX_2[rec] < 0 or rTree.STr2_iY_2[rec] < 0:
                            pass
                        else:
                            if fc.applyCuts(rTree,rec,rTree.STr2_Eta_2[rec], False) is False: #photon 2 in EE+
                                continue
                            histlist[rTree.STr2_iX_2[rec]][rTree.STr2_iY_2[rec]].Fill(rTree.STr2_Time_2[rec])
                            translist[rTree.STr2_iX_2[rec]][rTree.STr2_iY_2[rec]].Fill(float(1)/rTree.STr2_Laser_rec_2[rec])
                    elif rTree.STr2_Eta_2[rec] < -1.479:
                        if rTree.STr2_iX_2[rec] < 0 or rTree.STr2_iY_2[rec] < 0:
                            pass
                        else:
                            if fc.applyCuts(rTree,rec,rTree.STr2_Eta_2[rec], False) is False: #photon 2 in EE-
                                continue
                            histlist2[rTree.STr2_iX_2[rec]][rTree.STr2_iY_2[rec]].Fill(rTree.STr2_Time_2[rec])
                            translist2[rTree.STr2_iX_2[rec]][rTree.STr2_iY_2[rec]].Fill(float(1)/rTree.STr2_Laser_rec_2[rec])
                pbar.update(i+1)
            pbar.finish()
            return histlist, histlist2, translist, translist2
    
    #stack 2 separate plots for 2 photons of interest
    if len(histlist) != 101: #not endcap
        for i in range(0, nentries):
            rTree.GetEntry(i)
            for rec in range(0,rTree.STr2_NPi0_rec):
                if rTree.STr2_Pi0recIsEB[rec] != True:
                    continue
                if rTree.STr2_iEta_1[rec]+85 < 0 or rTree.STr2_iPhi_1[rec] < 0:
                    pass
                else:
                    if fc.applyCuts(rTree,rec,rTree.STr2_Eta_1[rec], True) is False: #photon 1
                        continue
                    if rTree.STr2_iEta_1[rec] >= 0: #accounting for crystal 0 being 1
                        histlist[rTree.STr2_iEta_1[rec]+86][rTree.STr2_iPhi_1[rec]].Fill(rTree.STr2_Time_1[rec])
                        translist[rTree.STr2_iEta_1[rec]+86][rTree.STr2_iPhi_1[rec]].Fill(float(1)/rTree.STr2_Laser_rec_1[rec])
                    else:
                        histlist[rTree.STr2_iEta_1[rec]+85][rTree.STr2_iPhi_1[rec]].Fill(rTree.STr2_Time_1[rec])
                        translist[rTree.STr2_iEta_1[rec]+85][rTree.STr2_iPhi_1[rec]].Fill(float(1)/rTree.STr2_Laser_rec_1[rec])
                if rTree.STr2_iEta_2[rec]+85 < 0 or rTree.STr2_iPhi_2[rec] < 0:
                    pass
                else:
                    if fc.applyCuts(rTree,rec,rTree.STr2_Eta_2[rec], False) is False: #photon 2
                        continue
                    if rTree.STr2_iEta_2[rec] >= 0: #accounting for crystal 0 being 1
                        histlist2[rTree.STr2_iEta_2[rec]+86][rTree.STr2_iPhi_2[rec]].Fill(rTree.STr2_Time_2[rec])
                        translist2[rTree.STr2_iEta_2[rec]+86][rTree.STr2_iPhi_2[rec]].Fill(float(1)/rTree.STr2_Laser_rec_2[rec])
                    else:
                        histlist2[rTree.STr2_iEta_2[rec]+85][rTree.STr2_iPhi_2[rec]].Fill(rTree.STr2_Time_2[rec])
                        translist2[rTree.STr2_iEta_2[rec]+85][rTree.STr2_iPhi_2[rec]].Fill(float(1)/rTree.STr2_Laser_rec_2[rec])
            pbar.update(i+1)
        pbar.finish()
        return histlist, histlist2, translist, translist2
    else: #is endcap
        for i in range(0, nentries):
            rTree.GetEntry(i)
            for rec in range(0,rTree.STr2_NPi0_rec):
                if rTree.STr2_Pi0recIsEB[rec] == True:
                    continue
                if rTree.STr2_Eta_1[rec] > 1.479:
                    if rTree.STr2_iX_1[rec] < 0 or rTree.STr2_iY_1[rec] < 0:
                        pass
                    else:
                        if fc.applyCuts(rTree,rec,rTree.STr2_Eta_1[rec], True) is False: #photon 1 in EE+
                            continue
                        histlist[rTree.STr2_iX_1[rec]][rTree.STr2_iY_1[rec]].Fill(rTree.STr2_Time_1[rec])
                        translist[rTree.STr2_iX_1[rec]][rTree.STr2_iY_1[rec]].Fill(float(1)/rTree.STr2_Laser_rec_1[rec])
                elif rTree.STr2_Eta_1[rec] < 1.479:
                    if rTree.STr2_iX_1[rec] < 0 or rTree.STr2_iY_1[rec] < 0:
                        pass
                    else:
                        if fc.applyCuts(rTree,rec,rTree.STr2_Eta_1[rec], True) is False: #photon 1 in EE-
                            continue
                        histlist2[rTree.STr2_iX_1[rec]][rTree.STr2_iY_1[rec]].Fill(rTree.STr2_Time_1[rec])
                        translist2[rTree.STr2_iX_1[rec]][rTree.STr2_iY_1[rec]].Fill(float(1)/rTree.STr2_Laser_rec_1[rec])
                if rTree.STr2_Eta_2[rec] > 1.479:
                    if rTree.STr2_iX_2[rec] < 0 or rTree.STr2_iY_2[rec] < 0:
                        pass
                    else:
                        if fc.applyCuts(rTree,rec,rTree.STr2_Eta_2[rec], False) is False: #photon 2 in EE+
                            continue
                        histlist3[rTree.STr2_iX_2[rec]][rTree.STr2_iY_2[rec]].Fill(rTree.STr2_Time_2[rec])
                        translist3[rTree.STr2_iX_2[rec]][rTree.STr2_iY_2[rec]].Fill(float(1)/rTree.STr2_Laser_rec_2[rec])
                elif rTree.STr2_Eta_2[rec] < 1.479:
                    if rTree.STr2_iX_2[rec] < 0 or rTree.STr2_iY_2[rec] < 0:
                        pass
                    else:
                        if fc.applyCuts(rTree,rec,rTree.STr2_Eta_2[rec], False) is False: #photon 2 in EE-
                            continue
                        histlist4[rTree.STr2_iX_2[rec]][rTree.STr2_iY_2[rec]].Fill(rTree.STr2_Time_2[rec])
                        translist4[rTree.STr2_iX_2[rec]][rTree.STr2_iY_2[rec]].Fill(float(1)/rTree.STr2_Laser_rec_2[rec])
            pbar.update(i+1)
        pbar.finish()
        return histlist, histlist2, histlist3, histlist4, translist, translist2, translist3, translist4


# This will fit gaussians to all the individual crystal time response histograms and converge them into a 2d histogram with the mean value.
def fitTime(histlist, translist, htime, hlaser, minstat, minnorm, includehitcounter, manualcut, name, graphs2print):
    fitdata = [[[0 for values in range(7)] for phi in range(361)] for eta in range(171)]
        #(mean,error,sigma,error) for [eta or x ,phi or y]
    
    #selection of random control fit response coordinates
    prntableGraphsX = random.sample(xrange(len(histlist)), graphs2print)
    prntableGraphsY = random.sample(xrange(len(histlist[0])), graphs2print)
    prntable = []
    for i in range (0,len(prntableGraphsX)):
        prntable.append((prntableGraphsX[i],prntableGraphsY[i]))
    
    #differentiate between barrel and endcap
    if len(histlist) != 101:
        xaxis = "iEta_"
        yaxis = "iPhi_"
        adjust = -85
        labelnTitle = "Seed photon density for EB (min stats = %i);iEta;iPhi;counts" %(minstat)
        seedmap = rt.TH2F("Spd"+name, labelnTitle,171,-85,86,361,0,361)
    
        #time evolution fixed crystal selection
        lowerx = 100
        upperx = 20
        lowery = 150
        uppery = 250
    else:
        xaxis = "iX_"
        yaxis = "iY_"
        adjust = 0
        labelnTitle = "Seed photon density for EE (min stats = %i);iX;iY;counts" %(minstat)
        seedmap = rt.TH2F("Spd"+name, labelnTitle,101,0,101,101,0,101)

        #time evolution fixed crystal selection
        lowerx = 50
        upperx = 50
        lowery = 25
        uppery = 90

    for x in range(0,len(histlist)):
        #print "completed " + str(x) + " out of " + str(len(histlist)) + " columns."
        for y in range(0,len(histlist[0])):
            hist = histlist[x][y] #this is before the time response section b.c. we need to see if we have enough statistic
            binmax = hist.GetMaximumBin()
            
            entries = pevents(hist,binmax,manualcut,40)
            seedmap.Fill(x+adjust,y,entries)
            fitdata[x][y][0] = entries

            if entries < minstat:
                htime.Fill(x+adjust,y,-999)
                continue
            if entries < minnorm: #mean fit, NOT gaussian fit
                fitdata[x][y][1] = hist.GetMean()
                fitdata[x][y][2] = hist.GetMeanError()
                fitdata[x][y][3] = hist.GetStdDev()
                fitdata[x][y][4] = hist.GetStdDevError()
                htime.Fill(x+adjust,y,hist.GetMean())
                htime.SetBinError(x+1,y+1,hist.GetMeanError()) #this value is the bin number
                
                hist = translist[x][y]
                fitdata[x][y][5] = hist.GetMean()
                fitdata[x][y][6] = hist.GetMeanError()
                #fitdata[x][y][2] = sigma.getVal()
                #fitdata[x][y][3] = sigma.getError()
                hlaser.Fill(x+adjust,y,hist.GetMean())
                hlaser.SetBinError(x+1,y+1,hist.GetMeanError()) #this value is the bin number
                continue
        
        #### Gaussian Fit ####
        ## Time Response
            max = hist.GetXaxis().GetBinCenter(binmax)
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

            fr = gauss.fitTo(dh,rt.RooFit.Save(),rt.RooFit.PrintLevel(-1),rt.RooFit.Verbose(rt.kFALSE))

            if (x,y) in prntable or (x,y) is (lowerx,lowery) or (x,y) is (upperx,uppery):
                gauss.plotOn(frame)
                c1 = rt.TCanvas()
                #c1.SetLogy()
                frame.Draw()
                c1.Print("timeresponse_"+name+xaxis+str(x)+"_"+yaxis+str(y)+".png")

            if len(histlist) != 101 and x == 85: #barrel, 0 ieta
                fitdata[x][y][1] = 0
                fitdata[x][y][2] = 0
                fitdata[x][y][3] = 0
                fitdata[x][y][4] = 0
                htime.Fill(x+adjust,y,-999)
                htime.SetBinError(x+1,y+1,0) #this value is the bin number
            else: #endcap
                fitdata[x][y][1] = mean.getVal()
                fitdata[x][y][2] = mean.getError()
                fitdata[x][y][3] = sigma.getVal()
                fitdata[x][y][4] = sigma.getError()
                htime.Fill(x+adjust,y,mean.getVal())
                htime.SetBinError(x+1,y+1,mean.getError()) #this value is the bin number


        ## Laser Transparency
            hist = translist[x][y]
            binmax = hist.GetMaximumBin()
            max = hist.GetXaxis().GetBinCenter(binmax)
            
            m = rt.RooRealVar("Transparency","Transparency Factor",max-0.05,max+0.05)
            dh = rt.RooDataHist("dh","dh",rt.RooArgList(m),rt.RooFit.Import(hist))
            
            frame = m.frame(rt.RooFit.Title("Transparency"))
            frame.SetYTitle("Counts")
            frame.SetTitleOffset (2.6, "Y")
            
            dh.plotOn(frame)
            
            # define gaussian
            mean = rt.RooRealVar("mean","mean",1.,-10.,10)
            sigma = rt.RooRealVar("sigma","sigma",0.1,-10.,10.)
            gauss = rt.RooGaussian("gauss","gauss",m,mean,sigma)
            
            fr = gauss.fitTo(dh,rt.RooFit.Save(),rt.RooFit.PrintLevel(-1), rt.RooFit.Verbose(rt.kFALSE))
            
            if (x,y) in prntable or (x,y) is (lowerx,lowery) or (x,y) is (upperx,uppery):
                gauss.plotOn(frame)
                c1 = rt.TCanvas()
                #c1.SetLogy()
                frame.Draw()
                c1.Print("lasertransparency_"+name+xaxis+str(x)+"_"+yaxis+str(y)+".png")
            
            if len(histlist) != 101 and x == 85: #barrel, 0 ieta
                fitdata[x][y][5] = 0
                fitdata[x][y][6] = 0
                hlaser.Fill(x+adjust,y,-999)
                hlaser.SetBinError(x+1,y+1,0) #this value is the bin number
            else:
                fitdata[x][y][5] = mean.getVal()
                fitdata[x][y][6] = mean.getError()
                #fitdata[x][y][2] = sigma.getVal()
                #fitdata[x][y][3] = sigma.getError()
                hlaser.Fill(x+adjust,y,mean.getVal())
                hlaser.SetBinError(x+1,y+1,mean.getError()) #this value is the bin number

    if includehitcounter == True:
        return htime, hlaser, fitdata, seedmap
    else:
        return htime, hlaser, fitdata, 0

# This will stack time response based upon each eta ring
# This is for barrel
def stackTimeEta(rTree,entries,histlist,histlist2,translist,translist2):

    if entries != -1:
        nentries = entries
    else:
        #gets number of entries (collision bunches)
        nentries = rTree.GetEntries()
    
    #creates a progress bar
    pbar = progressbar("Stacking", nentries).start()

    if histlist2 != 0:
        pass
    else: #merged 1 plot
        for i in range(0, nentries):
            rTree.GetEntry(i)
            for rec in range(0,rTree.STr2_NPi0_rec):
                if rTree.STr2_Pi0recIsEB[rec] != True:
                    continue
                if rTree.STr2_iEta_1[rec]+85 < 0:
                    pass
                else:
                    if fc.applyCutsEta(rTree,rec,rTree.STr2_Eta_1[rec], True) is False: #photon 1 merged
                        continue
                    if rTree.STr2_iEta_1[rec] >= 0: #accounting for crystal 0 being 1
                        histlist[rTree.STr2_iEta_1[rec]+86].Fill(rTree.STr2_Time_1[rec])
                        translist[rTree.STr2_iEta_1[rec]+86].Fill(float(1)/rTree.STr2_Laser_rec_1[rec])
                    else:
                        histlist[rTree.STr2_iEta_1[rec]+85].Fill(rTree.STr2_Time_1[rec])
                        translist[rTree.STr2_iEta_1[rec]+85].Fill(float(1)/rTree.STr2_Laser_rec_1[rec])
                if rTree.STr2_iEta_2[rec]+85 < 0:
                    pass
                else:
                    if fc.applyCutsEta(rTree,rec,rTree.STr2_Eta_2[rec], False) is False: #photon 2 merged
                        continue
                    if rTree.STr2_iEta_2[rec] >= 0: #accounting for crystal 0 being 1
                        histlist[rTree.STr2_iEta_2[rec]+86].Fill(rTree.STr2_Time_2[rec])
                        translist[rTree.STr2_iEta_2[rec]+86].Fill(float(1)/rTree.STr2_Laser_rec_2[rec])
                    else:
                        histlist[rTree.STr2_iEta_2[rec]+85].Fill(rTree.STr2_Time_2[rec])
                        translist[rTree.STr2_iEta_2[rec]+85].Fill(float(1)/rTree.STr2_Laser_rec_2[rec])
            pbar.update(i+1)
        pbar.finish()
        return histlist,translist

    for i in range(0, nentries): #2 separate plots for p1 and p2
        rTree.GetEntry(i)
        for rec in range(0,rTree.STr2_NPi0_rec):
            if rTree.STr2_Pi0recIsEB[rec] != 1:
                continue
            if rTree.STr2_iEta_1[rec]+85 < 0:
                pass
            else:
                if fc.applyCutsEta(rTree,rec,rTree.STr2_Eta_1[rec], True) is False: #photon 1 separate
                    continue
                if rTree.STr2_iEta_1[rec] >= 0: #accounting for crystal 0 being 1
                    histlist[rTree.STr2_iEta_1[rec]+86].Fill(rTree.STr2_Time_1[rec])
                    translist[rTree.STr2_iEta_1[rec]+86].Fill(float(1)/rTree.STr2_Laser_rec_1[rec])
                else:
                    histlist[rTree.STr2_iEta_1[rec]+85].Fill(rTree.STr2_Time_1[rec])
                    translist[rTree.STr2_iEta_1[rec]+85].Fill(float(1)/rTree.STr2_Laser_rec_1[rec])

            if rTree.STr2_iEta_2[rec]+85 < 0:
                pass
            else:
                if fc.applyCutsEta(rTree,rec,rTree.STr2_Eta_2[rec], False) is False: #photon 2 separate
                    continue
                if rTree.STr2_iEta_2[rec] >= 0: #accounting for crystal 0 being 1
                    histlist2[rTree.STr2_iEta_2[rec]+86].Fill(rTree.STr2_Time_2[rec])
                    translist2[rTree.STr2_iEta_2[rec]+86].Fill(float(1)/rTree.STr2_Laser_rec_2[rec])
                else:
                    histlist2[rTree.STr2_iEta_2[rec]+85].Fill(rTree.STr2_Time_2[rec])
                    translist2[rTree.STr2_iEta_2[rec]+85].Fill(float(1)/rTree.STr2_Laser_rec_2[rec])
        pbar.update(i+1)
    pbar.finish()
    return histlist, histlist2, translist, translist2

#This will fit gaussians to all the eta rings
def fitTimeEta(histlist, translist, htime, hlaser, minstat, minnorm, includehitcounter, manualcut, name, graphs2print):
    fitdata = [[0 for values in range(7)] for eta in range(171)] #(mean,error,sigma,error)
    labelnTitle = "Seed photon density for EB (min stats = %i);iEta;counts" %(minstat)
    seedmap = rt.TH1F("Spd"+name, labelnTitle,171,-85,86)
    prntableGraphs = random.sample(xrange(len(histlist)), 1)
    for eta in range(0,len(histlist)):
        hist = histlist[eta]
        binmax = hist.GetMaximumBin()

        entries = pevents(hist,binmax,manualcut,30)
        seedmap.Fill(eta-85,entries)
        fitdata[eta][0] = entries
        if entries < minstat:
            #htime.Fill(eta-85,0) <-- you don't need for TH1
            continue
        if entries < minnorm:
            fitdata[eta][1]= hist.GetMean()
            fitdata[eta][2]= hist.GetMeanError()
            fitdata[eta][3]= hist.GetStdDev()
            fitdata[eta][4]= hist.GetStdDevError()
            htime.Fill(eta-85,hist.GetMean()) #this value is the physical one (bin value)
            htime.SetBinError(eta+1,hist.GetMeanError()) #this value is the bin number

            hist = translist[eta]
            fitdata[eta][5]= hist.GetMean()
            fitdata[eta][6]= hist.GetMeanError()
            #fitdata[eta][6]=sigmaL.getVal()
            #fitdata[eta][7]=sigmaL.getError()
            hlaser.Fill(eta-85,hist.GetMean()) #this value is the physical one (bin value)
            hlaser.SetBinError(eta+1,hist.GetMeanError()) #this value is the bin number

    ## Time Response
        max = hist.GetXaxis().GetBinCenter(binmax)
        m = rt.RooRealVar("t","t (ns)",max-1.5,max+1.5)
        dh = rt.RooDataHist("dh","dh",rt.RooArgList(m),rt.RooFit.Import(hist))

        frame = m.frame(rt.RooFit.Title("Time response"))

        frame.SetYTitle("Counts")
        frame.SetTitleOffset(2.6, "Y")
        
        dh.plotOn(frame)
        
        # define gaussian
        mean = rt.RooRealVar("mean","mean",0.1,-2,2.)
        sigma = rt.RooRealVar("sigma","sigma",0.1,-2.,2)
        gauss = rt.RooGaussian("gauss","gauss",m,mean,sigma)
            
        fr = gauss.fitTo(dh,rt.RooFit.Save(), rt.RooFit.PrintLevel(-1), rt.RooFit.Verbose(rt.kFALSE))

        if eta in prntableGraphs or eta is 20 or eta is 100:
            gauss.plotOn(frame)
            c1 = rt.TCanvas()
            #c1.SetLogy()
            frame.Draw()
            c1.Print("timeresponse_"+name+"Eta_"+str(eta-85)+".png")
        
        
        if eta != 85:
            fitdata[eta][1]= mean.getVal()
            fitdata[eta][2]= mean.getError()
            fitdata[eta][3]= sigma.getVal()
            fitdata[eta][4]= sigma.getError()
            htime.Fill(eta-85,mean.getVal()) #this value is the physical one (bin value)
            htime.SetBinError(eta+1,mean.getError()) #this value is the bin number
        else:
            fitdata[eta][1]= 0
            fitdata[eta][2]= 0
            fitdata[eta][3]= 0
            fitdata[eta][4]= 0
            htime.Fill(eta-85,0)
            htime.SetBinError(eta+1,0)

    ## Laser Tranparency
        hist = translist[eta]
        binmax = hist.GetMaximumBin()
        max = hist.GetXaxis().GetBinCenter(binmax)
        
        m = rt.RooRealVar("Transparency","Transparency Factor",max-0.05,max+0.05)
        dh = rt.RooDataHist("dh","dh",rt.RooArgList(m),rt.RooFit.Import(hist))
        
        frame = m.frame(rt.RooFit.Title("Transparency"))
        
        frame.SetYTitle("Counts")
        frame.SetTitleOffset(2.6, "Y")
        
        dh.plotOn(frame)
        
        # define gaussian
        mean = rt.RooRealVar("mean","mean",1.,-10.,10)
        sigma = rt.RooRealVar("sigma","sigma",0.1,-10.,10)
        gauss = rt.RooGaussian("gauss","gauss",m,mean,sigma)
        
        fr = gauss.fitTo(dh,rt.RooFit.Save(),rt.RooFit.PrintLevel(-1), rt.RooFit.Verbose(rt.kFALSE))
        
        if eta in prntableGraphs or eta is 20 or eta is 100:
            gauss.plotOn(frame)
            c1 = rt.TCanvas()
            #c1.SetLogy()
            frame.Draw()
            c1.Print("lasertransparency_"+name+"Eta_"+str(eta-85)+".png")

        if eta !=85:
            fitdata[eta][5]= mean.getVal()
            fitdata[eta][6]= mean.getError()
            #fitdata[eta][6]=sigmaL.getVal()
            #fitdata[eta][7]=sigmaL.getError()
            hlaser.Fill(eta-85,mean.getVal()) #this value is the physical one (bin value)
            hlaser.SetBinError(eta+1,mean.getError()) #this value is the bin number
        else:
            fitdata[eta][5]= 0
            fitdata[eta][6]= 0
            hlaser.Fill(eta-85,0)
            hlaser.SetBinError(eta+1,0)

    if includehitcounter == True:
        return htime, hlaser, fitdata, seedmap
    else:
        return htime, hlaser, fitdata, 0

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


def pevents(hist,binmax,manualcut,fitrange):
    if manualcut < 0: #all values
        return hist.GetEntries()
    elif manualcut == 0: #fit range
        return hist.Integral(binmax-fitrange, binmax+fitrange)
    else: #self selection
        return hist.Integral(binmax-manualcut, binmax+manualcut)


