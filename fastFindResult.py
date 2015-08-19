##
## CURRENTLY ONLY DOING COMBINED P1 AND P2.
##
## NOT Running as of 08/19/2015
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


def fitNormalized (Crystal, dList):

def fit (crystal, dList):
    for db in dList:
        data = np.load(db)
    for
    #take crystal ID, take time response + transparency and just time response
    #fit to make 2 plots

def extract
    ##ASSUMPTION THAT WE ARE ALREADY IN THE FOLDER OF CHOICE
    fList = os.listdir('.')
    dList = []
    for file in fList:
        if 'data' in file:
            dList.append(file)

    dList.sort()
    return dList




def relocate:
    #Check and change current working directory.
    stardir = os.getcwd()
    print "Current working directory %s" % stardir
    if p.runFormat == 'L':
        os.chdir(p.resultPathLocal + p.folderName + '/')
    else:
        os.chdir(p.resultPathLXPLUS + p.folderName + '/')
    retdir = os.getcwd()
    print "Directory changed successfully %s" % retdir

    #List of folders in the result path
    fList = os.listdir(retdir)
    fList.sort()

    if isEE == True: #endcap analysis
        #EE+, EE-
        #rip images into 1 folder (time response + transparency)
        #fit all crystals photon 1 and 2 TOGETHER in 1 plot (response vs time, transparency vs time, response vs. transparency)
        ######fit all crystals photons 1 and 2 SEPARATRELY in 1 plot
        #rip all images in 1 folder

    elif isEta == True: #Eta analysis
#        folder = p.runNumber + 'RESULT_ctEB_' datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        folder = p.runNumber + 'RESULT_ctEB'
        os.system('mkdir ' + folder)
        shutil.copyfile(startdir + '/' 'fastFindResult.py', retdir + '/' + folder + 'fastFindResult.py')
        fname = "ctEB_c_"
        etaFiles = []

        for file in fList:
            if fname in file:
                etaFiles.append(file)
        for f in range(len(etaFiles)):
            shutil.copyfile(retdir + '/' + etaFiles[f] + '/2015A_EtaRunInfoEB.npy', retdir + '/' + folder + '/Info_' + f + '.npy')
            shutil.copyfile(retdir + '/' + etaFiles[f] + '/2015A_EtadataEB_c.npy', retdir + '/' + folder + '/data_' + f + '.npy')
            shutil.copyfile(retdir + '/' + etaFiles[f] + '/2015A_EtaLaserTransparencyEB_c.png', retdir + '/' + folder + '/transparency_' + f + '.png')
            shutil.copyfile(retdir + '/' + etaFiles[f] + '/2015A_EtaTimeResponseEB_c.png', retdir + '/' + folder + '/response_' + f + '.png')
            shutil.copyfile(retdir + '/' + etaFiles[f] + '/2015A_SeedDensityEB.png', retdir + '/' + folder + '/density_' + f + '.png')
            shutil.copyfile(retdir + '/' + etaFiles[f] + '/lasertransparency_c_Eta_-65.png', retdir + '/' + folder + '/transparency-65_' + f + '.png')
            shutil.copyfile(retdir + '/' + etaFiles[f] + '/lasertransparency_c_Eta_15.png', retdir + '/' + folder + '/transparency15_' + f + '.png')
            shutil.copyfile(retdir + '/' + etaFiles[f] + '/timeresponse_c_Eta_-65.png', retdir + '/' + folder + '/response-65_' + f + '.png')
            shutil.copyfile(retdir + '/' + etaFiles[f] + '/timeresponse_c_Eta_15.png', retdir + '/' + folder + '/response15_' + f + '.png')


    else: #individual EB crystal analysis