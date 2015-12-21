##
## File is done before the fastAnalysis.py file is run.
## What this program does is goes inside a list of fill_.py files
## and makes appropriate ranges for the run numbers from a list
## of runs. The master key in which this is adjusted is through
## a text file which is _manually_ modified. This is only valid with
## paramters of run numbers.
##
## NOT Running as of 12/14/2015
##

import ROOT as rt
import sys, random, math
import fileinput
import time
import os
import shutil
import copy

import parameters as p


### ACQUIRING ALL THE RUN DATA BINNING ###
# Check current working directory.
retdir = os.getcwd()
print "Current working directory %s" % retdir

## Ripping text file from runs_bin.txt ##
os.chdir(retdir + "/necessary documents/")
print "Grabbing data from %s" % os.getcwd()

lsrun_total = []
lsrun = []
startfound = False
endfound = False

print 'Begin reading appropriate ROOT binnings'

with open('run_bins.txt') as file: #open txt file
    for num, line in enumerate(file, 1): #iterate through each line
        if endfound == False: #if END has not been found
            if "END" in line:
                endfound = True
            else:
                if startfound == False: #if START has not been found
                    if "START" in line:
                        startfound = True
                else: #begin gathering data
                    if line != "\n":
                        lsrun.append(line[0:line.index(',')])
                    else:
                        lsrun_total.append(copy.deepcopy(lsrun))
                        lsrun[:] = []
    lsrun_total.append(copy.deepcopy(lsrun)) #see if you can fix

print 'End appropriate ROOT binnings'

run_total = []
#organizes the runlists to notation similar to that of the .list format
for runs in lsrun_total:
    run = []
    for indiv_run in runs:
        run.append(indiv_run[:3] + "/" + indiv_run[3:])
    run_total.append(copy.deepcopy(run))

print 'Sucessfully structured to fit .list specifications'

#gets the run number list
for f in os.listdir('.'):
    if p.runNumber in f:
        runlist = f

#extract the appropriate spacing in the ROOT list
lsrun_total_loc = []

print 'Begin extracting from .list'
for rootbin in run_total:
    lsrun_loc = []
    with open(runlist) as file:
        for line in enumerate(file, 1):
            if any(number in line[1] for number in rootbin):
                newline = line[1].replace("\n","")
                lsrun_loc.append(copy.deepcopy(newline))
    lsrun_total_loc.append(copy.deepcopy(lsrun_loc))
print 'Successfully extract from .list'

### PLACING THE BINNING INTO ACTUAL FILL_.PY FILES ###
# if files accessing are local or LXPLUS #
if p.runFormat == 'L':
    if "output" in p.rootFileLocationLocal:
        fileLocation = p.rootFileLocationLocal[:-7]
    else:
        fileLocation = p.rootFileLocationLocal
else:
    if "output" in p.rootFileLocationLXPLUS:
        fileLocation = p.rootFileLocationLXPLUS[:-7]
    else:
        fileLocation = p.rootFileLocationLXPLUS

# since this is originally for where the ROOT files are,
# we want to do 1 step prior, so this gets us the python files
os.chdir(fileLocation)
fillLocation = os.getcwd() #python file location

# Check current working directory.
retdir = os.getcwd()
print "Directory changed successfully %s" % retdir

print 'Begin filling .py files'
#reading each fill_.py within the fill folder

listofFillspy = os.listdir('.')
listofFillspy.sort()

#with open(listofFillspy[0]) as file: #open txt file
#    for num, line in reversed(enumerate(file, 1)): #iterate through each line
#        if 'root://eoscms//eos/cms/store/data/' in line:
#            removeLine(file, num)
#            root_line = copy.deepcopy(num)
#        if 'EcalNtp' in line:
#            file.replace('EcalNtp_0.root','EcalNtp_')
#
#for line in reversed(open(listofFillspy[0]).readlines()):
#    if 'root://eoscms//eos/cms/store/data/' in line:
#        removeLine(file, num)
#        root_line = copy.deepcopy(num)
#    if 'EcalNtp' in line:
#        file.replace('EcalNtp_0.root','EcalNtp_')

with open(listofFillspy[0], 'r') as infile:
    with open("fillEpsilonPlot_template.py", 'w') as outfile:
        for line in infile:
            if 'fileNames' in line:
                line = line.replace("fileNames = cms.untracked.vstring(", "fileNames")
            if 'root://eoscms//eos/cms/store/data/' in line:
                infile.next()
                continue
            if 'EcalNtp' in line:
                line = line.replace('EcalNtp_0.root','EcalNtp_')
            outfile.write(line)

print "removed all pre-exisiting root sources and specific EcalNtp_0.roots"

for file in listofFillspy:
    if "fillEpsilon" in file and file != 'fillEpsilonPlot_template.py':
        os.remove(file)
print "removed all files such that only the template is left"

for bin in lsrun_total_loc:
    f = open("fillEpsilonPlot_template.py", 'r')
    filedata = f.read()
    f.close()

    insert = "fileNames = cms.untracked.vstring(\n"
    for run in bin:
        insert = insert + "'" + run + "'"
        if bin[-1] != run:
            insert = insert + ',\n'

    EcalNtp_index = 'EcalNtp_' + str(lsrun_total_loc.index(bin)) + '.root'
    fileName = 'fillEpsilonPlot_iter_0_job_' + str(lsrun_total_loc.index(bin)) + '.py'

    newfill = filedata.replace('EcalNtp_',EcalNtp_index)
    newfill = newfill.replace('fileNames',insert)

    f = open(fileName, 'w')
    f.write(newfill)
    f.close()

print "created new fill files"
os.remove("fillEpsilonPlot_template.py")
print os.listdir('.')
print "deleted template file"

