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

                   
                   #creates histogram for event count
                   #hevent = rt.TH2F("Events in Barrel", "X vs Y",100,0,100,100,0,100)
                   




                   
                   #
                   #    #fit graph
                   #    histname = "calibration for ((%i),(%i));ns;Transparency" %(crystalx,crystaly)
                   #    histtitle = "calibration for ((%i),(%i));ns;Transparency" %(crystalx,crystaly)
                   #    hist = rt.TH1F(histname,histtitle) ##CHECK THIS##
                   #
                   #    for db in dList:
                   #        data = np.load(db)
                   #
                   #        #location of important data
                   #        time_mean_pos = len(data[0][0])-1-6
                   #        time_uncertainty_pos = mean_pos+1
                   #        transparency_mean_pos = len(data[0][0])-1-1
                   ##        transparency_uncertainty_pos = transparency_mean_pos+1 ##Assumption that transparency is 100% correct
                   #        "do something weird with transparency factor"
                   #
                   #        hist.fill("TRANSPARENCY", data[crystalx][crystaly][time_mean_pos], "time error", "transparency error")
                   
                   
                   #take crystal ID, take time response + transparency and just time response
                   #fit to make 2 plots


                   
                   
                   
                   
                   
                   #### WEIGHTED AVERAGE ###
                   #    #opens the endcap region and then stacks in clusters
                   #    for rootfile in rootList:
                   #        r = rt.TFile.Open(rootfile)
                   #        if 'dataEEp_c' in rootfile:
                   #            ht = r.Get("Time Response in Endcap plus for all photons")
                   #            hl = r.Get("Transparency in Endcap plus for all photons")
                   #            hd = r.Get("spdpc_")
                   #        elif 'dataEEm_c' in rootfile:
                   #            h = r.Get("Time Response in Endcap minus for all photons")
                   #            hl = r.Get("Transparency in Endcap minus for all photons")
                   #            hd = r.Get("spdmc_")
                   #        else:
                   #            return "sorry, no .root files with appropriate name found"
                   #
                   #        #clustered histograms
                   #        htc = rt.TH2F("Cluster TR in EE+", "Cluster TR in EE+; iX;iY;ns",51,0,51,51,0,51)
                   #        hlc = rt.TH2F("Cluster Transparency in EE+", "Cluster Transparency in EE+; iX;iY;Relative Transparency",51,0,51,51,0,51)
                   #        hdc = rt.TH2F("Cluster SPD in EE+", "Cluster SPD in EE+; iX;iY;Photon Counts",51,0,51,51,0,51)
                   #
                   #        #fitting clustered histograms
                   #        for x in range(htc.GetNbinsX()):


