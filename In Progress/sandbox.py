##
## Safety for small tests of code before implementation
## on larger scale.
##

if __name__ == "__main__":


def stackTimeEta(rTree,entries,histlist,histlist2,translist,translist2):
    
    if entries != -1:
        nentries = entries
    else:
        #gets number of entries (collision bunches)
        nentries = rTree.GetEntries()
    
    #creates a progress bar
    pbar = progressbar("Stacking", nentries).start()

if histlist2 != 0:
    pass
    else: #merged 1 plot
        for i in range(0, nentries):
            rTree.GetEntry(i)
            for rec in range(0,rTree.STr2_NPi0_rec):
                if rTree.STr2_Pi0recIsEB[rec] != True:
                    continue
                if rTree.STr2_iEta_1[rec]+85 < 0:
                    pass
                else:
                    if fc.applyCutsEta(rTree,rec,rTree.STr2_Eta_1[rec], True) is False: #photon 1 merged
                        continue
                    if rTree.STr2_iEta_1[rec] >= 0: #accounting for crystal 0 being 1
                        histlist[rTree.STr2_iEta_1[rec]+86].Fill(rTree.STr2_Time_1[rec])
                        translist[rTree.STr2_iEta_1[rec]+86].Fill(rTree.STr2_Laser_rec_1[rec])
                    else:
                        histlist[rTree.STr2_iEta_1[rec]+85].Fill(rTree.STr2_Time_1[rec])
                        translist[rTree.STr2_iEta_1[rec]+85].Fill(rTree.STr2_Laser_rec_1[rec])
                if rTree.STr2_iEta_2[rec]+85 < 0:
                    pass
                else:
                    if fc.applyCutsEta(rTree,rec,rTree.STr2_Eta_2[rec], False) is False: #photon 2 merged
                        continue
                    if rTree.STr2_iEta_2[rec] >= 0: #accounting for crystal 0 being 1
                        histlist[rTree.STr2_iEta_2[rec]+86].Fill(rTree.STr2_Time_2[rec])
                        translist[rTree.STr2_iEta_2[rec]+86].Fill(rTree.STr2_Laser_rec_2[rec])
                    else:
                        histlist[rTree.STr2_iEta_2[rec]+85].Fill(rTree.STr2_Time_2[rec])
                        translist[rTree.STr2_iEta_2[rec]+85].Fill(rTree.STr2_Laser_rec_2[rec])
            pbar.update(i+1)
        pbar.finish()
        return histlist,translist
