if 'p_c' in rootfile:
    
    for x in range(0, htcp.GetNbinsX()/2):
        for y in range(0, htcp.GetNbinsY()/2):
            radius =
            
            if hdcp.GetBinContent(x,y) == 0:
                    htcp.Fill(x,y,-999)
                    hlcp.Fill(x,y,-999)
                    hdcp.Fill(x,y,-999)
                    data = [0,"c",x,y,0,-999,0,0,0,-999,0]
                    dataList = np.append(dataList, data)
                    
                    timetitle = "time on plus sc (%i,%i)" %(x,y)
                    transtitle = "transparency on plus sc (%i,%i)" %(x,y)
                    hist = r.Get(timetitle)
                    histList.append(hist.Clone())
                    hist = r.Get(transtitle)
                    histList.append(hist.Clone())
                    continue
                
                ##time response##
                title1 = "time on plus sc (%i,%i)" %(2*x,2*y) #2*x,2*y, +1 each if 0,len-1
                title2 = "time on plus sc (%i,%i)" %(2*x-1,2*y)
                title3 = "time on plus sc (%i,%i)" %(2*x-1,2*y-1)
                title4 = "time on plus sc (%i,%i)" %(2*x,2*y-1)
                ht1 = r.Get(title1)
                ht2 = r.Get(title2)
                ht3 = r.Get(title3)
                    ht4 = r.Get(title4)
                    newname = "time on plus sc (%i,%i)" %(x,y)
                    hist = ht1.Clone(newname)
                    hist.Add(ht2,1)
                    hist.Add(ht3,1)
                    hist.Add(ht4,1)
                    histList.append(hist)
                    
                    #fit baby fit
                    a,b,c,d,e = fit(hist, "time response")
                    data = [0,"c",x,y,a,b,c,d,e]
                    dataList = np.append(dataList, data)
                    htcp.Fill(x,y,data[5])
                    htcp.SetBinError(x+1,y+1,data[6])
                    
                    ##seed density##
                    hdcp.Fill(x,y,data[4])
                    
                    ##laser transparency##
                    title1 = "transparency on plus sc (%i,%i)" %(2*x,2*y) #2*x,2*y, +1 each if 0,len-1
                    title2 = "transparency on plus sc (%i,%i)" %(2*x-1,2*y)
                    title3 = "transparency on plus sc (%i,%i)" %(2*x-1,2*y-1)
                    title4 = "transparency on plus sc (%i,%i)" %(2*x,2*y-1)
                    hl1 = r.Get(title1)
                    hl2 = r.Get(title2)
                    hl3 = r.Get(title3)
                    hl4 = r.Get(title4)
                    newname = "transparency on plus sc (%i,%i)" %(x,y)
                    hist = hl1.Clone(newname)
                    hist.Add(hl2,1)
                    hist.Add(hl3,1)
                    hist.Add(hl4,1)
                    histList.append(hist)
                    
                    #fit baby fit
                    a, b = fit(hist, "transparency")
                    data = [a,b]
                    dataList = np.append(dataList, data)
                    
                    hlcp.Fill(x,y,data[0])
                hlcp.SetBinError(x+1,y+1,data[1])
    
    
        #print out images
        rt.gROOT.LoadMacro('setstyle.c')
            rt.gROOT.Macro('setstyle.c')
            c = rt.TCanvas("c","c",600,500)
            c.cd()
            htcp.SetAxisRange(-5., 5.,"Z")
            htcp.Draw("colz")
            c.Print("clusterTimeResponseEEp_c_" + p.runNumber + ".png")
            hlcp.SetAxisRange(0., 1.,"Z")
            hlcp.Draw("colz")
            c.Print("clusterLaserTransparencyEEp_c_" + p.runNumber + ".png")
            hdcp.SetMinimum(0)
            hdcp.Draw("colz")
            if p.includeClusterSeedMap == True:
                c.Print("clusterPhotonDensityEEp_c_" + p.runNumber + ".png")
        c.Close()
            
            #save files
            f = rt.TFile("ClusterTimeEEp_c_" + p.runNumber + ".root","new")
            htcp.Write()
            hlcp.Write()
            hdcp.Write()
            f.Close()
            
            #formatting and saving all data into a numpy file for analyzing later
            dataList.shape = (51,51,11)
            np.save("clusterdataEEp_c_" + p.runNumber + ".npy", dataList)
