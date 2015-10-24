## input:  the .root files from fastAnalysis.py, IndivTimeEE/EBp/m_c_2015A/B/C/D_.root,
##        which contains the time response and transparency histogram for each crytal in EE/EB
## 
## output: group the crystal into different eta rings, and generate transparency, time response vs. eta plots;
##
## Zhicai Zhang (zzhang2@caltech.edu)
## Latest update: 10/23/2015

import ROOT as rt
import sys, random, math
import time
import os
import numpy as np
import glob
import parameters as p

runNumber_this = '2015A'
## the input file lists
input_root_files = glob.glob('/afs/cern.ch/user/z/zhicaiz/private/ECALpro/local/CMSSW_7_4_2/src/result/ctEE_'+runNumber_this+'*/*.root')
input_root_files.sort()

##some basic constats of EE
eta_max = 3.0
eta_min = 1.479
phi_max = 25.672 ## in degree
phi_min = 5.7 ## in degree
###########################

## find all the .root files
if len(input_root_files) == 0:
	print "sorry, no .root files in folder"
	exit(0)

input_root_files.sort()

print "Find root files:"
for input_file in input_root_files:
	print input_file	

filename_in_m = input_root_files[0]
filename_in_p = input_root_files[1]

f_in_p = rt.TFile(filename_in_p)
f_in_m = rt.TFile(filename_in_m)
	
if p.splitPhotons == True:
		print "to be finished in the future..."
else:
	print "working now...."
	eta_time_p = range(0,32)
	eta_time_m = range(0,32)
	eta_trans_p = range(0,32)
	eta_trans_m = range(0,32)
	h_eta_time_p = rt.TH1F("Time Response in Endcap plus for all photons","Time Response in EE+; eta; ns", 32, 1.40,3.00)
	h_eta_time_m = rt.TH1F("Time Response in Endcap minus for all photons","Time Response in EE-; eta; ns", 32, 1.40,3.00)
        h_eta_trans_p = rt.TH1F("Transparency in Endcap plus for all photons", "Transparency in EE+; eta; Transparency", 32, 1.40, 3.00)
        h_eta_trans_m = rt.TH1F("Transparency in Endcap minus for all photons", "Transparency in EE-; eta; Transparency", 32, 1.40, 3.00)

	histListp = [[0 for x in range(101)] for y in range(101)]
        histListm = [[0 for x in range(101)] for y in range(101)]
       	transListp = [[0 for x in range(101)] for y in range(101)]
        transListm = [[0 for x in range(101)] for y in range(101)]
	
	for index in range(0,32):
		temp_eta = 1.40+index*0.05
		eta_histnamep = "time on plus sc of eta = %5.3f " % temp_eta
		eta_histnamem = "time on minus sc of eta = %5.3f " % temp_eta
		eta_transnamep = "transparency on plus sc of eta = %5.3f " % temp_eta
		eta_transnamem = "transparency on minus sc of eta = %5.3f " % temp_eta
		
		eta_histtitlep = "time response (ns) on plus sc of eta = %5.3f " % temp_eta
		eta_histtitlem = "time response (ns) on minus sc of eta = %5.3f " % temp_eta
		eta_transtitlep = "transparency on plus crystal of eta = %5.3f " % temp_eta
		eta_transtitlem = "transparency on minus crystal of eta = %5.3f " % temp_eta
	
		eta_time_p[index] = rt.TH1F(eta_histnamep,eta_histtitlep,1000,-30,30)
		eta_time_m[index] = rt.TH1F(eta_histnamem,eta_histtitlem,1000,-30,30)
		eta_trans_p[index] = rt.TH1F(eta_transnamep,eta_transtitlep,1000,-5,5)
		eta_trans_m[index] = rt.TH1F(eta_transnamem,eta_transtitlem,1000,-5,5)
					

	for x in range(0,50):
		print x
		for y in range(0,50):
			histnamep = "time on plus sc (%i,%i)" %(x,y)
	                histtitlep = "time response (ns) for plus crystal (%i,%i)" %(x,y)
       		        histnamem = "time on minus sc (%i,%i)" %(x,y)
               		histtitlem = "time response (ns) for minus crystal (%i,%i)" %(x,y)
       	       		histListp[x][y] = f_in_p.Get(histnamep)
               	 	histListm[x][y] = f_in_m.Get(histnamem) 

      	        	transnamep = "transparency on plus sc (%i,%i)" %(x,y)
        	        transtitlep = "transparency for plus crystal (%i,%i)" %(x,y)
       	        	transnamem = "transparency on minus sc (%i,%i)" %(x,y)
	              	transtitlem = "transparency for minus crystal (%i,%i)" %(x,y)
        	       	transListp[x][y] = f_in_p.Get(transnamep) 
      	        	transListm[x][y] = f_in_m.Get(transnamem)
			radius_this = math.sqrt((x*1.0-50.0)*(x*1.0-50.0)+(y*1.0-50.0)*(y*1.0-50.0))
			if radius_this > 1.0:
				eta_this = -1.0*math.log(math.tan(0.5*radius_this*phi_max*3.14159/(50.0*180.0)))
				eta_index = int((eta_this-1.40)/0.05)
				if eta_index < 32:
					eta_time_p[eta_index] = eta_time_p[eta_index] + histListp[x][y] 
					eta_time_m[eta_index] = eta_time_m[eta_index] + histListm[x][y] 
					eta_trans_p[eta_index] = eta_trans_p[eta_index] + transListp[x][y] 
					eta_trans_m[eta_index] = eta_trans_m[eta_index] + transListm[x][y] 

	f_in_p.Close()
	f_in_m.Close()
	## save the time response and transparency histograms to .root file
	f_out_time_hist = rt.TFile('result_eta_ring/TimeResponseHistEta_EE_'+runNumber_this+'.root','RECREATE')
	for index in range(0,32):
		eta_time_p[index].Write()
		eta_time_m[index].Write()
	f_out_time_hist.Close()
	
	f_out_trans_hist = rt.TFile('result_eta_ring/TransparencyHistEta_EE_'+runNumber_this+'.root','RECREATE')
	for index in range(0,32):
		eta_trans_p[index].Write()
		eta_trans_m[index].Write()
	f_out_trans_hist.Close()

