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

## the input file lists
input_root_files = glob.glob('/afs/cern.ch/user/z/zhicaiz/private/ECALpro/local/CMSSW_7_4_2/src/result/c*/*.root')
input_root_files.sort()

## find all the .root files
if len(input_root_files) == 0:
	print "sorry, no .root files in folder"
	exit(0)

print "Find root files:"
for input_file in input_root_files:
	print input_file	

## process one by one
for input_file in input_root_files:
	f = rt.TFile(input_file)
	#f.ls()
#	if p.splitPhotons == True:
#		print "to be finished"
#	else:
#		print "under working...."
	
