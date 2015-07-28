#!/bin/bash


cd /afs/cern.ch/user/k/kachang/work/public/CMSSW_7_4_2/src/CalibCode/submit/analysis/
eval `scramv1 runtime -sh`
python runFills.py
#python timeEB.py
#python clustertimeEB.py









##
## Self explanatory. You use this to run all the fill_iter_.py files
## This runs on batch, which is much faster than LXPLUS.
##
## Working as of 07/23/2015
##