#!/bin/bash


cd /afs/cern.ch/user/k/kachang/work/public/CMSSW_7_4_2/src/CalibCode/submit/analysis/
eval `scramv1 runtime -sh`
#python runFills.py
python individualtimeEB.py
python individualtimeEE.py
python clustertimeEB.py





##
## This will run all the analysis of our programs. It will extract,
## fit, and plot all the information you need to make a significant
## contribution. It also runs on batch.
##
## Updated as of 07/23/2015
## Working as of 07/23/2015
##