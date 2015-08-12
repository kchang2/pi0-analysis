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

#return True = pass, False = not pass
def applyCuts (event, rec, eta, isOne):
    if p.manualCuts is False:
        return True
    if abs(eta) < 1.0: ## inner barrel
        if p.noCorr is True: #no corrections data
            if event.STr2_ptPi0_nocor[rec] < p.Pi0PtCutEB_low:
                return False
            if isOne is True: #photon 1
                if event.STr2_ptG1_nocor[rec] < p.gPtCutEB_low:
                    return False
                if event.STr2_S4S9_1[rec] < p.S4S9_EB_low:
                    return False
            else: #photon 2
                if event.STr2_ptG2_nocor[rec] < p.gPtCutEB_low:
                    return False
                if event.STr2_S4S9_2[rec] < p.S4S9_EB_low:
                    return False
                
        else: #with corrections
            if event.STr2_ptPi0_rec[rec] < p.Pi0PtCutEB_low:
                return False
            if isOne is True: #photon 1
                if event.STr2_ptG1_rec[rec] < p.gPtCutEB_low:
                    return False
                if event.STr2_S4S9_1[rec] < p.S4S9_EB_low:
                    return False
            else: #photon 2
                if event.STr2_ptG2_rec[rec] < p.gPtCutEB_low:
                    return False
                if event.STr2_S4S9_2[rec] < p.S4S9_EB_low:
                    return False

        if event.STr2_IsoPi0_rec[rec] > p.Pi0IsoCutEB_low:
            return False
        if event.STr2_n1CrisPi0_rec[rec] < p.nXtal_1_EB_low:
            return False
        if event.STr2_n2CrisPi0_rec[rec] < p.nXtal_2_EB_low:
            return False
                
    elif 1.0 <= abs(eta) <= 1.4: ## outer barrel
        if p.noCorr is True: #no corrections data
            if event.STr2_ptPi0_nocor[rec] < p.Pi0PtCutEB_high:
                return False
            if isOne is True: #photon 1
                if event.STr2_ptG1_nocor[rec] < p.gPtCutEB_high:
                    return False
                if event.STr2_S4S9_1[rec] < p.S4S9_EB_high:
                    return False
            else: #photon 2
                if event.STr2_ptG2_nocor[rec] < p.gPtCutEB_high:
                    return False
                if event.STr2_S4S9_2[rec] < p.S4S9_EB_high:
                    return False
    
        else: #with corrections
            if event.STr2_ptPi0_rec[rec] < p.Pi0PtCutEB_high:
                return False
            if isOne is True: #photon 1
                if event.STr2_ptG1_rec[rec] < p.gPtCutEB_high:
                    return False
                if event.STr2_S4S9_1[rec] < p.S4S9_EB_high:
                    return False
            else: #photon 2
                if event.STr2_ptG2_rec[rec] < p.gPtCutEB_high:
                    return False
                if event.STr2_S4S9_2[rec] < p.S4S9_EB_high:
                    return False

        if event.STr2_IsoPi0_rec[rec] > p.Pi0IsoCutEB_high:
            return False
        if event.STr2_n1CrisPi0_rec[rec] < p.nXtal_1_EB_high:
            return False
        if event.STr2_n2CrisPi0_rec[rec] < p.nXtal_2_EB_high:
            return False
                
    elif 1.4 < abs(eta) < 1.8: ## low eta endcap
        if p.noCorr == True: #no corrections data
            if event.STr2_ptPi0_nocor[rec] < p.Pi0PtCutEE_low:
                return False
            if isOne is True: #photon 1
                if event.STr2_ptG1_nocor[rec] < p.gPtCutEE_low:
                    return False
                if event.STr2_S4S9_1[rec] < p.S4S9_EE_low:
                    return False
            else: #photon 2
                if event.STr2_ptG2_nocor[rec] < p.gPtCutEE_low:
                    return False
                if event.STr2_S4S9_2[rec] < p.S4S9_EE_low:
                    return False
    
        else: #with corrections
            if event.STr2_ptPi0_rec[rec] < p.Pi0PtCutEE_low:
                return False
            if isOne is True: #photon 1
                if event.STr2_ptG1_rec[rec] < p.gPtCutEE_low:
                    return False
                if event.STr2_S4S9_1[rec] < p.S4S9_EE_low:
                    return False
            else: #photon 2
                if event.STr2_ptG2_rec[rec] < p.gPtCutEE_low:
                    return False
                if event.STr2_S4S9_2[rec] < p.S4S9_EE_low:
                    return False

        if event.STr2_IsoPi0_rec[rec] > p.Pi0IsoCutEE_low:
            return False
        if event.STr2_n1CrisPi0_rec[rec] < p.nXtal_1_EE_low:
            return False
        if event.STr2_n2CrisPi0_rec[rec] < p.nXtal_2_EE_low:
            return False
                
    else: ## high eta endcap
        if p.noCorr == True: #no corrections data
            if event.STr2_ptPi0_nocor[rec] < p.Pi0PtCutEE_high:
                return False
            if isOne is True: #photon 1
                if event.STr2_ptG1_nocor[rec] < p.gPtCutEE_high:
                    return False
                if event.STr2_S4S9_1[rec] < p.S4S9_EE_high:
                    return False
            else: #photon 2
                if event.STr2_ptG2_nocor[rec] < p.gPtCutEE_high:
                    return False
                if event.STr2_S4S9_2[rec] < p.S4S9_EE_high:
                    return False
    
        else: #with corrections
            if event.STr2_ptPi0_rec[rec] < p.Pi0PtCutEE_high:
                return False
            if isOne is True: #photon 1
                if event.STr2_ptG1_rec[rec] < p.gPtCutEE_high:
                    return False
                if event.STr2_S4S9_1[rec] < p.S4S9_EE_high:
                    return False
            else: #photon 2
                if event.STr2_ptG2_rec[rec] < p.gPtCutEE_high:
                    return False
                if event.STr2_S4S9_2[rec] < p.S4S9_EE_high:
                    return False

        if event.STr2_IsoPi0_rec[rec] > p.Pi0IsoCutEE_high:
            return False
        if event.STr2_n1CrisPi0_rec[rec] < p.nXtal_1_EE_high:
            return False
        if event.STr2_n2CrisPi0_rec[rec] < p.nXtal_2_EE_high:
            return False
    return True



#return True = pass, False = not pass
def applyCutsEta (event, rec, eta, isOne):
    if p.manualCuts is False:
        return True
    if abs(eta) < 1.0: ## inner barrel
        if p.noCorr is True: #no corrections data
            if event.STr2_ptPi0_nocor[rec] < p.Pi0PtCutEB_low:
#                print "we out ptPi0_nocor, value is " + str(event.STr2_ptPi0_nocor[rec])
                return False
            if isOne is True: #photon 1
                if event.STr2_ptG1_nocor[rec] < p.gPtCutEB_low:
                    return False
                if event.STr2_S4S9_1[rec] < p.S4S9_EB_low:
                    return False
            else: #photon 2
                if event.STr2_ptG2_nocor[rec] < p.gPtCutEB_low:
                    return False
                if event.STr2_S4S9_2[rec] < p.S4S9_EB_low:
                    return False
    
        else: #with corrections
            if event.STr2_ptPi0_rec[rec] < p.Pi0PtCutEB_low:
                return False
            if isOne is True: #photon 1
                if event.STr2_ptG1_rec[rec] < p.gPtCutEB_low:
                    return False
                if event.STr2_S4S9_1[rec] < p.S4S9_EB_low:
                    return False
            else: #photon 2
                if event.STr2_ptG2_rec[rec] < p.gPtCutEB_low:
                    return False
                if event.STr2_S4S9_2[rec] < p.S4S9_EB_low:
                    return False

        if event.STr2_IsoPi0_rec[rec] > p.Pi0IsoCutEB_low:
            return False
        if event.STr2_n1CrisPi0_rec[rec] < p.nXtal_1_EB_low:
            return False
        if event.STr2_n2CrisPi0_rec[rec] < p.nXtal_2_EB_low:
            return False

    else: ## outer barrel
        if p.noCorr is True: #no corrections data
            if event.STr2_ptPi0_nocor[rec] < p.Pi0PtCutEB_high:
                return False
            if isOne is True: #photon 1
                if event.STr2_ptG1_nocor[rec] < p.gPtCutEB_high:
                    return False
                if event.STr2_S4S9_1[rec] < p.S4S9_EB_high:
                    return False
            else: #photon 2
                if event.STr2_ptG2_nocor[rec] < p.gPtCutEB_high:
                    return False
                if event.STr2_S4S9_2[rec] < p.S4S9_EB_high:
                    return False

        else: #with corrections
            if event.STr2_ptPi0_rec[rec] < p.Pi0PtCutEB_high:
                return False
            if isOne is True: #photon 1
                if event.STr2_ptG1_rec[rec] < p.gPtCutEB_high:
                    return False
                if event.STr2_S4S9_1[rec] < p.S4S9_EB_high:
                    return False
            else: #photon 2
                if event.STr2_ptG2_rec[rec] < p.gPtCutEB_high:
                    return False
                if event.STr2_S4S9_2[rec] < p.S4S9_EB_high:
                    return False

        if event.STr2_IsoPi0_rec[rec] > p.Pi0IsoCutEB_high:
            return False
        if event.STr2_n1CrisPi0_rec[rec] < p.nXtal_1_EB_high:
            return False
        if event.STr2_n2CrisPi0_rec[rec] < p.nXtal_2_EB_high:
            return False
                
    return True




#Pi0PtCutEB_low = '1.8'     << STr2_ptPi0_rec / STr2_ptPi0_nocor
#Pi0IsoCutEB_low = '0.2'    << STr2_IsoPi0_rec <------LESS THAN
#gPtCutEB_low = '0.6'       << STr2_ptG1_rec, STr2_ptG2_rec / STr2_ptG1_nocor, STr2_ptG2_nocor
#nXtal_1_EB_low = '4'       << STr2_n1CrisPi0_rec
#nXtal_2_EB_low = '5'       << STr2_n2CrisPi0_rec
#S4S9_EB_low = '0.6'   <<   STr2_S4S9_1, STr2_S4S9_2
