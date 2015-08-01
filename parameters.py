##
##
## This is to help you run all the files appropriately, and easily. Note
## that this is meant to be run from ECALpro that L. Pernie made, so if
## you change any location of the files, you should add in the FULL length
## of your path where the data is.
##
## Note that this does NOT include runFills.py. <-- that you will need to
## run on your own.
##
## Updated as of 07/31/2015 (mm/dd/yyyy)
## NOT Running as of 07/31/2015
##


#Data File info
runNumber = '2015B_'        #Run sequence from where data is pulled and analyzed
rootFileLocation = '/Users/kaichang/Desktop/output/'#'/afs/cern.ch/user/k/kachang/work/public/CMSSW_7_4_2/src/CalibCode/submit/ALL_2015A_RAW_Test1/cfgFile/Fill/output/'      #Location where EcalPro's fit_iter_.py files ROOT files (that are created) are located

#Analyzing info
numberofFiles = -1          #Number of ROOT files you want to analyze
splitPhotons = True         #True = maps photon 1,2 separately. False = joins photons together
numberofEntries = -1        #Number of Entries per root file you want to analyze

#Output Path
resultPath = '/Users/kaichang/Desktop/'#'/afs/cern.ch/user/k/kachang/work/public/CMSSW_7_4_2/src/CalibCode/submit/'           #Location where you want your .root, .npy, and .png files to be outputted to
folderName = 'result'       #name of folder your files will go into
