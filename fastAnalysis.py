##
## This is the file that runs all the fast python files
## and can run everything based off your parameters. It is
## primarily used for script (.sh), but can be used for
## any local or LXPLUS runs. It is noticeably slower versus
## running any of the standalone non-FAST files when not on
## distributing jobs in BATCH.
##
## Running as of 08/19/2015
##


import ROOT as rt
import sys, random, math
import fileinput
import time
import os
import numpy as np

import parameters as p

## if files accessing are local or LXPLUS ##
if p.runFormat == 'L':
    fileLocation = p.rootFileLocationLocal
    resultLocation = p.resultPathLocal
else:
    fileLocation = p.rootFileLocationLXPLUS
    resultLocation = p.resultPathLXPLUS
analysisLocation = os.getcwd()

## Division Group marks for files ##
iterFiles = []

## Get list of files ##
rootList = os.listdir(fileLocation)
fileList = os.listdir(os.getcwd())

## if you want to analyze all the ROOT files ##
if p.numberofFiles == -1:
    if p.jobIterFiles == -1 or p.jobIterFiles == 0:
        iterFiles = [0,len(rootList)]
    else:
        #if you want to split evenly#
        if p.isEvenSplit == True:
            splitValue = int(len(rootList)/p.jobIterFiles)
            #bins files within ranges#
            for i in range(0,len(rootList)+1):
                if i % splitValue == 0:
                    iterFiles.append(i)
            #checks to see if last file is at end#
            if len(rootList) % splitValue != 0:
                del iterFiles[-1]
                iterFiles.append(len(rootList))
        else:
            print "applying manual split"
            iterFiles = p.manualSplit
            #check to see if 0 and last file are smallest and largest in your split
            if 0 not in iterFiles:
                iterFiles.insert(0,0)
            if len(rootList) not in iterFiles:
                iterFiles.append(len(rootList))
# only want to analyze a certain range of ROOT files #
else:
    if p.jobIterFiles == -1 or p.jobIterFiles == 0:
        iterFiles = [p.runRangeStart,p.runRangeStart + p.numberofFiles]
    else:
        if p.isEvenSplit == True:
            splitValue = int(p.numberofFiles/p.jobIterFiles)
            #bins files within ranges#
            for i in range(p.runRangeStart,p.runRangeStart + p.numberofFiles + 1):
                if i % splitValue == 0:
                    iterFiles.append(i)
            #checks to see if your boundary conditions are in file
            if p.runRangeStart not in iterFiles:
                iterFiles.insert(0,p.runRangeStart)
            if p.runRangeStart + p.numberofFiles not in iterFiles:
                    del iterFiles[-1]
                    iterFiles.append(p.runRangeStart + p.numberofFiles)
        else:
            print "applying manual split"
            iterFiles = p.manualSplit
            if p.runRangeStart not in iterFiles:
                iterFiles.insert(0,p.runRangeStart)
            if p.runRangeStart + p.numberofFiles not in iterFiles:
                del iterFiles[-1]
                iterFiles.append(p.runRangeStart + p.numberofFiles)

#print iterFiles    #check to see if the files are appropriately outputting
#exit()

## checks which format you want to run from ##
if p.runFormat == 'B':
    prefix = 'bsub -q %s < ' %(p.runBatchLength)
    if p.runAllScript == True:
        for k in range(0,len(iterFiles)-1):
            f = open(p.analFile, 'r')
            filedata = f.read()
            f.close()
            
            newscript = filedata.replace(".py",".py " + fileLocation + " " + resultLocation + " " + str(iterFiles[k]) + " " + str(iterFiles[k+1]))
            
            f = open(p.analFile,'w')
            f.write(newscript)
            f.close()
            
            os.system(prefix + p.analFile)
            
            #return to original
            f = open(p.analFile, 'r')
            filedata = f.read()
            f.close()
            newscript = filedata.replace(".py " + fileLocation + " " + resultLocation + " " + str(iterFiles[k]) + " " + str(iterFiles[k+1]), ".py")
            f = open(p.analFile,'w')
            f.write(newscript)
            f.close()
    else:
        for name in p.ifFalsethenWhat:
            for k in range(0,len(iterFiles)-1):
                filein = 'run' + name + '.sh'
                f = open(filein,'r')
                filedata = f.read()
                f.close()
            
                newscript = filedata.replace(".py",".py " + fileLocation + " " + resultLocation + " " + str(iterFiles[k]) + " " + str(iterFiles[k+1]))
                f = open(filein,'w')
                f.write(newscript)
                f.close()
                
                os.system(prefix + filein)

                #return to original
                f = open(filein, 'r')
                filedata = f.read()
                f.close()
                newscript = filedata.replace(".py " + fileLocation + " " + resultLocation + " " + str(iterFiles[k]) + " " + str(iterFiles[k+1]), ".py")
                f = open(filein,'w')
                f.write(newscript)
                f.close()

# running on LXPLUS or local#
else:
    if p.displayOutput == True or p.runFormat == 'L':
        if p.runAllScript == True:
            for pyfiles in p.filesforAll:
                for k in range(0,len(iterFiles)-1):
                    os.system('python ' + pyfiles + ".py " + fileLocation + " " + resultLocation +  " " + str(iterFiles[k]) + " " + str(iterFiles[k+1]))
        else:
            for pyfiles in p.ifFalsethenWhat:
                for k in range(0,len(iterFiles)-1):
                    os.system('python ' + pyfiles + ".py " + fileLocation + " " + resultLocation +  " " + str(iterFiles[k]) + " " + str(iterFiles[k+1]))
    else:
        if p.runAllScript == True:
            for pyfiles in p.filesforAll:
                for k in range(0,len(iterFiles)-1):
                    os.system('nohup python ' + pyfiles + ".py " + fileLocation + " " + resultLocation +  " " + str(iterFiles[k]) + " " + str(iterFiles[k+1]))
        else:
            for pyfiles in p.ifFalsethenWhat:
                for k in range(0,len(iterFiles)-1):
                    os.system('nohup python ' + pyfiles + ".py " + fileLocation + " " + resultLocation +  " " + str(iterFiles[k]) + " " + str(iterFiles[k+1]))

