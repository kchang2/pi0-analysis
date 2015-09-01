##
## This file plots the luminosity data for CMS runs.
## collisions and cosmic rays
##
## Running as of 08/03/2015
##
import ROOT as rt
import sys, random, math
import time, datetime
import os, shutil
import numpy as np

import stackNfit as snf

if __name__ == "__main__":


#    hcosmic = rt.TH1F("Cosmic - Luminosity vs Run Number", "Luminosity vs Run Number; Run #;Luminosity",171,-85,86)

    ## Collisions
    datan = [254459, 455, 254500, 49, 254511, 15, 254512, 51, 254513, 18, 254530, 55]
    ## Cosmic
    datac = [254460, 17, 254461, 86, 254472, 230, 254480, 62, 254488, 293, 254497, 150, 254499, 247, 254507, 54, 254509, 102, 254517, 195, 254519, 101, 254524, 73, 254526, 94, 254528, 182]
        
    hcollision = rt.TH1F("a","a",10000,254400,254600)
    hcosmic = rt.TH1F("b","b",10000,254400,254600)

    for i in xrange(0,len(datan)-1,2):
        hcollision.Fill(datan[i],datan[i+1])



    for i in xrange(0,len(datac)-1,2):
        hcosmic.Fill(datac[i],datac[i+1])

    c = rt.TCanvas()
    hcollision.Draw()
    c.SetLogy()
    c.Print("luminosityRunCollision.png")
    c.Close()

    c2 = rt.TCanvas()
    c2.SetLogy()
    hcosmic.Draw()
    c2.Print("luminosityRunCosmic.png")
    c2.Close()





### Time Response
#max = hist.GetXaxis().GetBinCenter(binmax)
#    m = rt.RooRealVar("t","t (ns)",max-2,max+2)
#        dh = rt.RooDataHist("dh","dh",rt.RooArgList(m),rt.RooFit.Import(hist))
#            
#            frame = m.frame(rt.RooFit.Title("Time response"))
#            frame.SetYTitle("Counts")
#            frame.SetTitleOffset (2.6, "Y")
#            
#            dh.plotOn(frame)
#            
#            # define gaussian
#            mean = rt.RooRealVar("mean","mean",0.,-2,2.)
#            sigma = rt.RooRealVar("sigma","sigma",0.,-2,2)
#            gauss = rt.RooGaussian("gauss","gauss",m,mean,sigma)
#            
#            fr = gauss.fitTo(dh,rt.RooFit.Save(), rt.RooFit.PrintLevel(-1), rt.RooFit.Verbose(rt.kFALSE))
#
