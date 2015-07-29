##
## This program is in charge of changing the directory path of our
## fill_iter_epsilon_.py files, which have currently been set to
## /tmp/. We replace them with more suitable paths to work in.
##
## Working as of 07/23/2015
##

import fileinput, sys
import os

# Check current working directory.
retdir = os.getcwd()
print "Current working directory %s" % retdir

# Now change the directory
os.chdir("..")
os.chdir( os.getcwd() + "/ALL_2015B_RAW_Test1/cfgFile/Fill/" )

# Check current working directory.
retdir = os.getcwd()
print "Directory changed successfully %s" % retdir

for i in range(0,30):
    filein = "fillEpsilonPlot_iter_0_job_%i.py" %i
    f = open(filein,'r')
    filedata = f.read()
    f.close()

    newdata = filedata.replace("process.analyzerFillEpsilon.OutputDir = cms.untracked.string('/tmp/')","process.analyzerFillEpsilon.OutputDir = cms.untracked.string('./')")

    f = open(filein,'w')
    f.write(newdata)
    f.close()

print "Files sucessfully modified, Mr. Chang."
