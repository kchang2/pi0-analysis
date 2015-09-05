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
## Updated as of 08/19/2015 (mm/dd/yyyy)
##


###Input Path###
runNumber = '2015A_'        #Run sequence from where data is pulled and analyzed
rootFileLocationLocal = '/Users/kaichang/Desktop/output/'      #Location where EcalPro's fit_iter_.py files ROOT files (that are created) are located on local computer
rootFileLocationLXPLUS = '/afs/cern.ch/user/k/kachang/work/public/CMSSW_7_4_2/src/CalibCode/submit/ALL_LASER_2015A_RAW_Test1/cfgFile/Fill/output/'        #Location where EcalPro's fit_iter_.py files ROOT files (that are created) are located on LXPLUS cluster


###Analyzing info###
numberofFiles = -1          #Number of ROOT files you want to analyze
runRangeStart = 0           #if numberofFiles != -1, specificy which file you want to start with
splitPhotons = False         #True = maps photon 1,2 separately. False = joins photons together
includeSeedMap = True    #True = map of hits per crystal, False = do not include a map of hits
numberofEntries = -1        #Number of Entries per root file you want to analyze
minStat = 10             #Number of statistic to allow a fit or mean to pass. Too small = bad fit for our CORRECTION.
minNormal = 15          #Number of statistic needed to allow a normal fit to pass. Smaller = mean
graphs2printEB = 0        #These are check graphs. We will always print out 1 graph from each eta region, but these are random sampling graphs, so we can see if our fits or derivations are reasonable.
graphs2printEE = 0        #These are the same as above, just for the endcap region. Know that the endcap region is significantly different from the barrel region because in the Endcap we know that there are non Xtal regions.


###Output Path###
resultPathLocal = '/Users/kaichang/Desktop/'        #Location where you want your .root, .npy, and .png files to be outputted to (local computer)
resultPathLXPLUS = '/afs/cern.ch/user/k/kachang/work/public/CMSSW_7_4_2/src/CalibCode/submit/'           #Location where you want your .root, .npy, and .png files to be outputted to (LXPLUS cluster)
folderName = 'result'       #name of folder your files will go into


###Script Info [fastAnalysis]###
runFormat = 'L'             #Batch [B], LXPLUS [X], Locally [L]
runBatchLength = '2nd'      #if isBatch = True, specificy how long program runs normally
displayOutput = False       #False = don't display each fit parameters, True = display on Terminal
runAllScript = False              #True = run all analysis. False = individual analysis
ifFalsethenWhat = ['fast_clustertimeEE']       #Look at the the python files
isEvenSplit = True          #whether you want the ROOT files to be split evenly in batches
jobIterFiles = 2           #How do you want to break down your batches in terms of jobs (Ex. all the files split into 5 jobs), -1 or 0 means directly all in 1
manualSplit = [0,5,10,15,23,28,76,77]        #isEvenSplit = False, then manually split -> Refer to datedList.txt for specific days of runs


###Post Script Tuneup###
needCluster = False #If False, keep individual crystal. If too little statistics, choose True, clusters crystals together to bin more statistic
clusterXtalSide = 2 #Number of crystals per cluster side (ex. 2 = 2x2)
includeClusterSeedMap = True #True = map of hits per crystal, False = do not include a map of hits


###Calibration###
runAllCalib = False          #True = Analyze all the data, False = individual analysis
isEE = True             #True = Analyze the EE data, False = Analyze the EB data
isEta = True            #True = EB Eta clustering data, False = individual crystal
displayFit = False      #False = Print no calibration fit graphs, True = print all graphs of calibration fit/



####### Do NOT modify unless you know what you are doing #######
filesforAll = ['fast_clustertimeEB','fast_clustertimeEE','fast_individualtimeEB', 'fastAnalysis.sh']
analFile = 'runAnalysis.sh'
manualHitCounterCut = 0     #(mean-value,mean+value) -> -1 = all values, 0 = fit range, > 0 = own fit value [remember these are bin values, not the values they represent -> bin corresponding to time response instead of value of time response]

#sigmacutoff = 1.5 #make histogram of sigmas, and anything outside of acceptable sigmas will be converted from normal fit to mean fit.
#includeBackgroundinCount = False        #False = does not include background in minimum stat threshold + entries in seedmap. True = if inStat threshold is too low for reasonable fit.
#specCutsIfNTupleTrueIB = []
#fitBoundaries = 5 #You're fit for the time response and laser transparency come from this. 5 --> [-5,5]
#randChkEB = 1 #Number of random histograms printed out. -1 = ALL of them (BEWARE)
#randChkEE = 7 #Number of random histograms printed out. EE is more hit or miss b/c some positions do not have any fits. This value should be larger.


###Cuts for Pi0###
manualCuts = True          #False = use whatever cuts were intially provided. True = apply personal cuts below.
noCorr = True            #True = use data from nocorr or uncorrected values for containment corrections. False = use corrected values instead.
## inner barrel
Pi0PtCutEB_low = 1.8
gPtCutEB_low = 0.6
Pi0IsoCutEB_low = 0.2
nXtal_1_EB_low = 4
nXtal_2_EB_low = 5
S4S9_EB_low = 0.6
## outer barrel
Pi0PtCutEB_high = 2.6
gPtCutEB_high = 0.6
Pi0IsoCutEB_high = 0.05
nXtal_1_EB_high = 4
nXtal_2_EB_high = 5
S4S9_EB_high = 0.75
## low eta EE
Pi0PtCutEE_low = 3.6
gPtCutEE_low = 1.
Pi0IsoCutEE_low = 0.3
nXtal_1_EE_low = 4
nXtal_2_EE_low = 5
S4S9_EE_low = 0.8
## high eta EE
Pi0PtCutEE_high = 3.6
gPtCutEE_high = 1.
Pi0IsoCutEE_high = 0.3
nXtal_1_EE_high = 4
nXtal_2_EE_high = 5
S4S9_EE_high = 0.8
