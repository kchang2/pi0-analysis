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
## Updated as of 08/03/2015 (mm/dd/yyyy)
## COND Running as of 08/03/2015
##


#Input Path
runNumber = '2015A_'        #Run sequence from where data is pulled and analyzed
rootFileLocationLocal = '/Users/kaichang/Desktop/output/'      #Location where EcalPro's fit_iter_.py files ROOT files (that are created) are located on local computer
rootFileLocationLXPLUS = '/afs/cern.ch/user/k/kachang/work/public/CMSSW_7_4_2/src/CalibCode/submit/ALL_2015A_RAW_Test1/cfgFile/Fill/output/'        #Location where EcalPro's fit_iter_.py files ROOT files (that are created) are located on LXPLUS cluster

#Analyzing info
numberofFiles = -1          #Number of ROOT files you want to analyze
runRangeStart = 0           #if numberofFiles != -1, specificy which file you want to start with
splitPhotons = True         #True = maps photon 1,2 separately. False = joins photons together
includeHitCounter = True    #True = map of hits per crystal, False = do not include a map of hits
numberofEntries = -1        #Number of Entries per root file you want to analyze
minStat = 10000             #Number of statistic to allow fit to pass. Too small = bad fit for our CORRECTION.

#Output Path
resultPathLocal = '/Users/kaichang/Desktop/'        #Location where you want your .root, .npy, and .png files to be outputted to (local computer)
resultPathLXPLUS = '/afs/cern.ch/user/k/kachang/work/public/CMSSW_7_4_2/src/CalibCode/submit/'           #Location where you want your .root, .npy, and .png files to be outputted to (LXPLUS cluster)
folderName = 'result'       #name of folder your files will go into


#Script Info [fastAnalysis]
runFormat = 'B'             #Batch [B], LXPLUS [X], Locally [L]
runBatchLength = '2nd'      #if isBatch = True, specificy how long program runs normally
displayOutput = False       #False = don't display each fit parameters, True = display on Terminal
runAll = False              #True = run all analysis. False = individual analysis
ifFalsethenWhat = ['fast_clustertimeEE']       #Look at the the python files
isEvenSplit = True          #whether you want the ROOT files to be split evenly in batches
jobIterFiles = 10           #How do you want to break down your batches in terms of files (Ex. 5 jobs per batch), -1 or 0 means directly all in 1
manualSplit = [0,5,10,15,23,28,76,77]        #isEvenSplit = False, then manually split -> Refer to datedList.txt for specific days of runs


## Do NOT modify unless you know what you are doing ##
filesforAll = ['fast_clustertimeEB','fast_clustertimeEE','fast_individualtimeEB']
analFile = 'runAnalysis.sh'
manualHitCounterCut = 0     #(mean-value,mean+value) -> -1 = all values, 0 = fit range, > 0 = own fit value [remember these are bin values, not the values they represent -> bin corresponding to time response instead of value of time response]



includeBackgroundinCount = False        #False = does not include background in minimum stat threshold + entries in seedmap. True = if inStat threshold is too low for reasonable fit. ###Need to fix later###
specCutsIfNTupleTrueIB = [] ###Need to fix later###
