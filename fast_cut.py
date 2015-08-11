##
## Strict file for making the manual cuts needed to tighten
## on the data we use.
##
## Updated as of 08/08/2015
## NOT Running as of 08/08/2015
##

import ROOT as rt
import sys, random, math
import time, datetime
import os, shutil
import numpy as np

import stackNfit as snf
import parameters as p
import fast_assemble as a

from FastProgressBar import progressbar

##implement beore
#return True = pass, False = not pass
def cutsEB (event, rec, isOne):
    if isOne is True: #photon 1
        if event.STr2_iEta_1[rec] < 0: #inner barrel
            if Pi0PtCutEB_low
        else: #outer barrel
    
    else: #photon 2

Pi0PtCutEB_low = '1.8'     << STr2_ptPi0_rec
gPtCutEB_low = '0.6'       << STr2_ptG1_rec, STr2_ptG2_rec
Pi0IsoCutEB_low = '0.2'    << STr2_IsoPi0_rec
nXtal_1_EB_low = '4'
nXtal_2_EB_low = '5'
S4S9_EB_low = '0.6'   <<   STr2_S4S9_1, STr2_S4S9_2

cor vs nocor???

#outer barrel
Pi0PtCutEB_high = '2.6'
gPtCutEB_high = '0.6'
Pi0IsoCutEB_high = '0.05'
nXtal_1_EB_high = '4'
nXtal_2_EB_high = '5'
S4S9_EB_high = '0.75'



def cutsEE (event, rec, mORp, isOne):
    if mORp == "m":
    
    else: