## input:  the .root files from fastAnalysis.py, IndivTimeEE/EBp/m_c_2015A/B/C/D_.root,
##        which contains the time response and transparency histogram for each crytal in EE/EB
## 
## output: group the crystal into different eta rings, and generate transparency, time response vs. eta plots;
##
## Zhicai Zhang (zzhang2@caltech.edu)
## Latest update: 10/23/2015

import ROOT as rt
import sys, random, math
import time
import os
import numpy as np
import glob
import parameters as p

runNumber_this = '2015A'
## the input file lists
input_root_files = glob.glob('/afs/cern.ch/user/z/zhicaiz/private/ECALpro/local/CMSSW_7_4_2/src/result/ctEE_'+runNumber_this+'*/*.root')
input_root_files.sort()

##some basic constats of EE
eta_max = 3.0
eta_min = 1.479
phi_max = 25.672 ## in degree
phi_min = 5.7 ## in degree
###########################

## find all the .root files
if len(input_root_files) == 0:
	print "sorry, no .root files in folder"
	exit(0)

input_root_files.sort()
print "Find root files:"
for input_file in input_root_files:
	print input_file	

print input_root_files[0]
