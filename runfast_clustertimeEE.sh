#!/bin/bash


cd /afs/cern.ch/user/k/kachang/work/public/CMSSW_7_4_2/src/CalibCode/submit/pi0-analysis/
eval `scramv1 runtime -sh`
python fast_clustertimeEE.py





##
## This will run all the analysis of our programs. It will extract,
## fit, and plot all the information you need to make a significant
## contribution. It also runs on batch.
##
## Working as of 08/19/2015
##