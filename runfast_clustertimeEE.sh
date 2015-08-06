#!/bin/bash


cd /afs/cern.ch/user/k/kachang/work/public/CMSSW_7_4_2/src/CalibCode/submit/pi0-analysis/
eval `scramv1 runtime -sh`
python clustertimeEE.py





##
## This will run all the analysis of our programs. It will extract,
## fit, and plot all the information you need to make a significant
## contribution. It also runs on batch.
##
## Updated as of 07/27/2015
## Working as of 07/27/2015
##