import ROOT as rt
import sys, random, math
import time
import os
import numpy as np

os.chdir('./result_eta_ring_full')
print "current directory is " + os.getcwd()

rootFiles = []
for file in os.listdir(os.getcwd()):
    if '.root' in file:
        rootFiles.append(file)

for rFile in rootFiles:
    r = rt.TFile.Open(rFile)

