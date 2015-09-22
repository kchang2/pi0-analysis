##
## Tutorial for fitting for a composite function (multiple functions into 1)
## https://root.cern.ch/root/html/tutorials/roofit/rf202_extendedmlfit.C.html
## Know that in their case, they fit 2 gaussian + chebychev
## In our case we fit gaussian + chebychev
##
import ROOT as rt
import sys

if __name__ == "__main__":
    
    if len(sys.argv)<2 or ('.root' not in sys.argv[1]):
        print "give a root file as input"
        sys.exit()

    fileName = sys.argv[1]
    rootFile = rt.TFile.Open(fileName)
    rootFile.Print("v")

    hist = rootFile.Get("allEpsilon_EE")
    
    m = rt.RooRealVar("m","m (GeV)",0.07,0.2);
    
    dh = rt.RooDataHist("dh","dh",rt.RooArgList(m),rt.RooFit.Import(hist))
    
    frame = m.frame(rt.RooFit.Title("Invariant Mass of PI0 with Poisson Error bars (EE)"))#"Import TH1 with Poisson error bars"
    
    frame.SetYTitle("Counts")
    frame.SetTitleOffset (1.4, "Y")
    
    dh.plotOn(frame)
    
    # define gaussian
    mean = rt.RooRealVar("mean","mean",0.14,0,1.)
    sigma = rt.RooRealVar("sigma","sigma",0.1,0.,1)
    gauss = rt.RooGaussian("gauss","gauss",m,mean,sigma)
    
    # define chebychev polynomial
    a0 = rt.RooRealVar("a0", "a0", 0.3, -10., 10)
    a1 = rt.RooRealVar("a1", "a1", -0.7, -10., 10)
    bkg = rt.RooChebychev("bkg", "Background", m, rt.RooArgList(a0,a1))
    
    #Construct the composite model
    nsig = rt.RooRealVar("nsig","number of signal events", 100000., 0., 10000000)
    nbkg = rt.RooRealVar("nbkg", "number of background events", 10000, 0., 10000000)
    model = rt.RooAddPdf("model", "gauss + chebychev", rt.RooArgList(bkg,gauss), rt.RooArgList(nbkg,nsig))
    
    
    fr = model.fitTo(dh,rt.RooFit.Save())
    print ""
    print "THIS IS THE FIT RESULT:"
    fr.Print("v")
    print ""
    model.plotOn(frame)
#model.plotOn(frame,rt.RooFit.Components("gauss"),rt.RooFit.LineStyle(rt.kDashed),rt.RooFit.LineColor(rt.kRed))
#model.plotOn(frame,rt.RooFit.Components("bkg"),rt.RooFit.LineStyle(rt.kDashed),rt.RooFit.LineColor(rt.kGreen))
    
    c = rt.TCanvas()
    #c.SetLogy()
    frame.Draw()
    c.Print("1DmassfitEE.png")