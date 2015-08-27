##
## Safety for small tests of code before implementation
## on larger scale.
##

import ROOT as rt
if __name__ == "__main__":
    c = rt.TCanvas("c","c",600,500)
    c.cd()