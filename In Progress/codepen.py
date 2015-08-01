##
## Temporary storage for code.
##
##
    
    
    # Check current working directory.
    retdir = os.getcwd()
    print "Current working directory %s" % retdir
    
    # Now change the directory
    os.chdir( retdir + "/ALL_2015A_RAW_Test1/cfgFile/Fill/fillEpsilonOut/" )
    
    # Check current working directory.
    retdir = os.getcwd()
    print "Directory changed successfully %s" % retdir
    
    # Get list of root files in directory
    for k in range(0,len(os.listdir()):
                   fileName = os.listdir[k]
                   rootFile = rt.TFile.Open(fileName)
                   rTree = rootFile.Get("Tree_Optim")
                   #rootFile.Print("v")
                   
                   
                   #NEED TO FIGURE OUT HOW TO ADD THE DATA TOGETHER <-- to do this, just keep Htime up and add through loops of ROOT files.
                   #TO GET + or - endcap, you do eta >1.4 or < -1.4
    
    #creation of numpy array to store values for faster analysis(courtesy of Ben Bartlett)
    datalist = np.array([])
                   
    dataList = np.append([(eta, time) for time in timelist])
    np.save("stuff.npy", datalist)
    
    #load:
    tuplelist = np.load("stuff.npy")

                   

/ALL_2015A_RAW_Test1/cfgFile/Fill
                   ALL_2015A_RAW_Test1/cfgFile/Fill/
                   
                   #hevent = rt.TH2F("Events in Barrel", "iPhi vs. iEta",170,-85,85,360,0,360)


"/ALL_2015A_RAW_Test1/cfgFile/Fill/output/"


                   #creates a progress bar
                   pbar = progressbar.ProgressBar(maxval=nentries, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()]).start()







