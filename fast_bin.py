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

import parameters as p


### ACQUIRING ALL THE RUN DATA BINNING ###
# Check current working directory.
retdir = os.getcwd()
print "Current working directory %s" % retdir

## Ripping text file from runs_bin.txt ##
os.chdir(".\necessary_documents\ ")
print "Grabbing data from %s" % os.getcwd()

lsrun_total = []
lsrun = []
startfound = False
endfound = False

print 'Begin reading appropriate ROOT binnings'

with open('run_bins.txt') as file: #open txt file
    for num, line in enumerate(file, 1): #iterate through each line
        if endfound == False: #if END has not been found
            if startfound == False: #if START has not been found
                if "START" in line:
                    startfound = True
            else: #begin gathering data
                if line != " ":
                    lsrun.append(line[0:line.index(',')])
                else:
                    lsrun_total.append(lsrun)
                    lsrun[:]
            if "STOP" in line:
                endfound = True

print 'End appropriate ROOT binnings'

#organizes the runlists to notation similar to that of the .list format
for runs in lsrun_total:
    for indiv_run in runs:
        indiv_run = indiv_run(:3) + "/" + indiv_run(3:)
print 'Sucessfully structured to fit .list specifications'

#gets the run number list
for f in os.listdir():
    if p.runNumber in f:
        runlist = f

#extract the appropriate spacing in the ROOT list
lsrun_total_loc = []

print 'Begin extracting from .list'
for rootbin in lsrun_total:
    lsrun_loc = []
    with open(runlist) as file:
        for line in enumerate(file, 1):
            if any(number in line for number in rootbin):
                lsrun_loc.append(line)
    lsrun_total_loc.append(lsrun_loc)
print 'Successfully extract from .list'

### PLACING THE BINNING INTO ACTUAL FILL_.PY FILES ###
# if files accessing are local or LXPLUS #
if p.runFormat == 'L':
    fileLocation = p.rootFileLocationLocal
else:
    fileLocation = p.rootFileLocationLXPLUS

# since this is originally for where the ROOT files are,
# we want to do 1 step prior, so this gets us the python files
os.chdir("..")
fillLocation = os.getcwd() #python file location

# Check current working directory.
retdir = os.getcwd()
print "Directory changed successfully %s" % retdir

print 'Begin filling .py files'
#reading each fill_.py within the fill folder

listofFillspy = os.listdir()
listofFillspy.sort()

with open(listofFillspy[0]) as file: #open txt file
    for num, line in reversed(enumerate(file, 1)): #iterate through each line
        if 'root://eoscms//eos/cms/store/data/' in line:
            removeLine(file, num)
            root_line = copy.deepcopy(num)
        if 'EcalNtp' in line:
            file.replace('EcalNtp_0.root','EcalNtp_')

for k in range(1,len(listofFillspy)):
    os.remove(listofFillspy[k])

os.rename(listofFillspy[0],"fillEpsilonPlot_template.py")

for bin in lsrun_total_loc:
    insert = ""
    for run in bin:
        insert = insert + run +',\n' # will \n converts into actual new lines???
    
    f = open("fillEpsilonPlot_template.py", 'r')
    filedata = f.read()
    f.close()

    EcalNtp_index = 'EcalNtp_' + String(lsrun_total_loc.index(bin)) + '.root'
    fileName = 'fillEpsilonPlot_iter_0_job_' + String(lsrun_total_loc.index(bin)) + '.py'

    newfill = filedata.insert(root_line, insert)
    newfill = filedata.insert('EcalNtp_',EcalNtp_index)

    f = open(fileName, 'w')
    f.write(newfill)
    f.close()


