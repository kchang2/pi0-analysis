##
## This program will run all the fillEpsilonPlot_iter files that are created
## when you run the ./submitCalibration.py file in the ECALpro. It only runs
## the first iteration (iter_0) because this is the one without any corrections
## applied. All the other iterations use the same RAW file.
##
## Working as of 07/23/2015
##

import sys
import os
import shutil



if __name__ == "__main__":

    # Check current working directory.
    os.chdir('..')
    retdir = os.getcwd()
    print "Current working directory %s" % retdir
    
    # Makes new folder for all resulting .png
    os.system('mkdir result')

    # Now change the directory
    os.chdir( retdir + '/ALL_2015B_RAW_Test1/cfgFile/Fill/' )

    # Check current working directory.
    retdir = os.getcwd()
    print "Directory changed successfully %s" % retdir

    # Makes new folder to store all files
    os.system('mkdir output')
    
    for k in range (0,1): #iterations
        for j in range (0,10): #jobs
            file = "fillEpsilonPlot_iter_" + str(k) + "_job_" + str(j) + ".py"
            print "Running", file
            os.system('cmsRun ' + file)


    for j in range (0,10):
        shutil.move(retdir + "/2015B_EcalNtp_" + str(j) + ".root", retdir + "/output" + "/2015B_EcalNtp_" + str(j) + ".root")



    #os.system("exit")
    #os.system("cd ~/Documents/")
    #os.system("mkdir fillEpsilonOut")
    #os.system("cd fillEpsilonOut")
    #os.system("scp kachang@lxplus.cern.ch:/afs/cern.ch/user/k/kachang/work/public/CMSSW_7_4_2/src/CalibCode/submit/ALL_2015A_RAW_Test1/cfgFile/Fill/2015A_* ." )

