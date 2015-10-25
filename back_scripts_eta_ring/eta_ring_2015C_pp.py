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

##run Nuber
runNumber_this = '2015C'
##specific region in EE
iX_min = 50
iX_max = 101
iY_min = 50
iY_max = 101
## the input file lists
input_root_files = glob.glob('/afs/cern.ch/user/z/zhicaiz/private/ECALpro/local/CMSSW_7_4_2/src/result/ctEE_'+runNumber_this+'*/*.root')
input_root_files.sort()

##some basic constats of EE
eta_max = 3.0
eta_min = 1.479
phi_max = 25.672 ## in degree
phi_min = 5.7 ## in degree
###########################
## time and transparency fit range (if you want to change this)
time_fit_min = -10.0
time_fit_max = -10.0
trans_fit_min = 0.5
trans_fit_max = 1.5
##########################
## the minimum number of events that trigger you to fit the histogram
min_gaus = 10

##plot settings
XTitleSize =  0.06
YTitleSize =  0.05
XLabelSize = 0.06
YLabelSize = 0.05
XTitleOffset = 0.8
YTitleOffset = 0.8
THLineWidth = 3
##gStyle
#rt.gROOT.SetStyle("Plain")
rt.gStyle.SetOptStat(0)
#rt.gStyle.SetTextFont(132)
#rt.gStyle.SetLegendFont(132)
#rt.gStyle.SetLabelFont(132,"xyz")
#rt.gStyle.SetLegendFillColor( 10 )
#rt.gStyle.SetCanvasColor(0)
#rt.gStyle.cd()
#rt.gROOT.ForceStyle()

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
	print "now extracting the time response and transparency histogram in different eta rings from the iX iY data...."
	eta_time_p = range(0,32)
	eta_time_m = range(0,32)
	eta_trans_p = range(0,32)
	eta_trans_m = range(0,32)

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
					

	for x in range(iX_min,iX_max):
		print "iX = %i" % x
		for y in range(iY_min,iY_max):
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
	## fit the histograms
	time_mean_p = range(0,32)
	time_sigma_p = range(0,32)
	trans_mean_p = range(0,32)
	trans_sigma_p = range(0,32)
	
	time_mean_m = range(0,32)
	time_sigma_m = range(0,32)
	trans_mean_m = range(0,32)
	trans_sigma_m = range(0,32)
	
	print "Now fitting the time response and transparency histogram in different eta rings..."
	for index in range(0,32):
		print "iEta = %i" % index
		TF1_timenamep = "time p %i" % index 	
		TF1_timenamem = "time m %i" % index 	
		TF1_transnamep = "trans p %i" % index 	
		TF1_transnamem = "trans m %i" % index 	
		fit_time_p = rt.TF1(TF1_timenamep,"gaus",time_fit_min,time_fit_max);
		fit_time_m = rt.TF1(TF1_timenamem,"gaus",time_fit_min,time_fit_max);
		fit_trans_p = rt.TF1(TF1_transnamep,"gaus",trans_fit_min,trans_fit_max);
		fit_trans_m = rt.TF1(TF1_transnamem,"gaus",trans_fit_min,trans_fit_max);
		
		if eta_time_p[index].GetEntries() > min_gaus: 
			eta_time_p[index].Fit(fit_time_p, 'q')
			time_mean_p[index] = fit_time_p.GetParameter(1)
			time_sigma_p[index] = fit_time_p.GetParameter(2)
		else:
			time_mean_p[index] = eta_time_p[index].GetMean()
			time_sigma_p[index] = eta_time_p[index].GetStdDev()
		if eta_time_m[index].GetEntries() > min_gaus: 
			eta_time_m[index].Fit(fit_time_m, 'q')
			time_mean_m[index] = fit_time_m.GetParameter(1)
			time_sigma_m[index] = fit_time_m.GetParameter(2)
		else:
			time_mean_m[index] = eta_time_m[index].GetMean()
			time_sigma_m[index] = eta_time_m[index].GetStdDev()
		
		if eta_trans_p[index].GetEntries() > min_gaus: 
			eta_trans_p[index].Fit(fit_trans_p, 'q')
			trans_mean_p[index] = fit_trans_p.GetParameter(1)
			trans_sigma_p[index] = fit_trans_p.GetParameter(2)
		else:
			trans_mean_p[index] = eta_trans_p[index].GetMean()
			trans_sigma_p[index] = eta_trans_p[index].GetStdDev()
		if eta_trans_m[index].GetEntries() > min_gaus: 
			eta_trans_m[index].Fit(fit_trans_m, 'q')
			trans_mean_m[index] = fit_trans_m.GetParameter(1)
			trans_sigma_m[index] = fit_trans_m.GetParameter(2)
		else:
			trans_mean_m[index] = eta_trans_m[index].GetMean()
			trans_sigma_m[index] = eta_trans_m[index].GetStdDev()
		
	## get the time response and transparency vs. eta plot..
	print "now getting the time response and transparency vs. eta plot..."

	h_eta_time_p = rt.TH1F("Time Response in Endcap plus for all photons","Time Response in EE+; eta; ns", 32, 1.40,3.00)
	h_eta_time_m = rt.TH1F("Time Response in Endcap minus for all photons","Time Response in EE-; eta; ns", 32, 1.40,3.00)
        h_eta_trans_p = rt.TH1F("Transparency in Endcap plus for all photons", "Transparency in EE+; eta; Transparency", 32, 1.40, 3.00)
        h_eta_trans_m = rt.TH1F("Transparency in Endcap minus for all photons", "Transparency in EE-; eta; Transparency", 32, 1.40, 3.00)

	for index in range(0,32):
		print "iEta = %i" % index
		h_eta_time_p.SetBinContent(index+1,time_mean_p[index])
		h_eta_time_p.SetBinError(index+1,time_sigma_p[index])
		
		h_eta_time_m.SetBinContent(index+1,time_mean_m[index])
		h_eta_time_m.SetBinError(index+1,time_sigma_m[index])
		
		h_eta_trans_p.SetBinContent(index+1,trans_mean_p[index])
		h_eta_trans_p.SetBinError(index+1,trans_sigma_p[index])
		
		h_eta_trans_m.SetBinContent(index+1,trans_mean_m[index])
		h_eta_trans_m.SetBinError(index+1,trans_sigma_m[index])
	
	c_time_p = rt.TCanvas('time response EE plus','time response EE plus', 200,10,800,600)					
	c_time_p.cd()
	h_eta_time_p.SetTitle("time response vs. #eta in EE+")
	h_eta_time_p.SetLineWidth(THLineWidth)
	h_eta_time_p.GetXaxis().SetTitleSize(XTitleSize)	
	h_eta_time_p.GetXaxis().SetLabelSize(XLabelSize)	
	h_eta_time_p.GetXaxis().SetTitleOffset(XTitleOffset)
	h_eta_time_p.GetYaxis().SetTitleSize(YTitleSize)	
	h_eta_time_p.GetYaxis().SetLabelSize(YLabelSize)	
	h_eta_time_p.GetYaxis().SetTitleOffset(YTitleOffset)
	h_eta_time_p.GetXaxis().SetTitle("#eta")
	h_eta_time_p.GetYaxis().SetTitle("time response (ns)")
	h_eta_time_p.GetYaxis().SetNdivisions(510)
	h_eta_time_p.Draw()
	c_time_p.Print('result_eta_ring/TimeResponseVsEta_EE_p_'+runNumber_this+'.pdf')	
	c_time_p.Print('result_eta_ring/TimeResponseVsEta_EE_p_'+runNumber_this+'.png')	
	c_time_p.Print('result_eta_ring/TimeResponseVsEta_EE_p_'+runNumber_this+'.eps')	

	c_time_m = rt.TCanvas('time response EE minus','time response EE minus', 200,10,800,600)					
	c_time_m.cd()
	h_eta_time_m.SetTitle("time response vs. #eta in EE-")
	h_eta_time_m.SetLineWidth(THLineWidth)
	h_eta_time_m.GetXaxis().SetTitleSize(XTitleSize)	
	h_eta_time_m.GetXaxis().SetLabelSize(XLabelSize)	
	h_eta_time_m.GetXaxis().SetTitleOffset(XTitleOffset)
	h_eta_time_m.GetYaxis().SetTitleSize(YTitleSize)	
	h_eta_time_m.GetYaxis().SetLabelSize(YLabelSize)	
	h_eta_time_m.GetYaxis().SetTitleOffset(YTitleOffset)
	h_eta_time_m.GetXaxis().SetTitle("#eta")
	h_eta_time_m.GetYaxis().SetTitle("time response (ns)")
	h_eta_time_m.GetYaxis().SetNdivisions(510)
	h_eta_time_m.Draw()
	c_time_m.Print('result_eta_ring/TimeResponseVsEta_EE_m_'+runNumber_this+'.pdf')	
	c_time_m.Print('result_eta_ring/TimeResponseVsEta_EE_m_'+runNumber_this+'.png')	
	c_time_m.Print('result_eta_ring/TimeResponseVsEta_EE_m_'+runNumber_this+'.eps')	
	
	c_trans_p = rt.TCanvas('transparency EE plus','transparency EE plus', 200,10,800,600)					
	c_trans_p.cd()
	h_eta_trans_p.SetTitle("transparency vs. #eta in EE+")
	h_eta_trans_p.SetLineWidth(THLineWidth)
	h_eta_trans_p.GetXaxis().SetTitleSize(XTitleSize)	
	h_eta_trans_p.GetXaxis().SetLabelSize(XLabelSize)	
	h_eta_trans_p.GetXaxis().SetTitleOffset(XTitleOffset)
	h_eta_trans_p.GetYaxis().SetTitleSize(YTitleSize)	
	h_eta_trans_p.GetYaxis().SetLabelSize(YLabelSize)	
	h_eta_trans_p.GetYaxis().SetTitleOffset(YTitleOffset)
	h_eta_trans_p.GetXaxis().SetTitle("#eta")
	h_eta_trans_p.GetYaxis().SetTitle("transparency")
	h_eta_trans_p.GetYaxis().SetNdivisions(510)
	h_eta_trans_p.Draw()
	c_trans_p.Print('result_eta_ring/TransparencyVsEta_EE_p_'+runNumber_this+'.pdf')	
	c_trans_p.Print('result_eta_ring/TransparencyVsEta_EE_p_'+runNumber_this+'.png')	
	c_trans_p.Print('result_eta_ring/TransparencyVsEta_EE_p_'+runNumber_this+'.eps')	

	c_trans_m = rt.TCanvas('transparency EE minus','transparency EE minus', 200,10,800,600)					
	c_trans_m.cd()
	h_eta_trans_m.SetTitle("transparency vs. #eta in EE-")
	h_eta_trans_m.SetLineWidth(THLineWidth)
	h_eta_trans_m.GetXaxis().SetTitleSize(XTitleSize)	
	h_eta_trans_m.GetXaxis().SetLabelSize(XLabelSize)	
	h_eta_trans_m.GetXaxis().SetTitleOffset(XTitleOffset)
	h_eta_trans_m.GetYaxis().SetTitleSize(YTitleSize)	
	h_eta_trans_m.GetYaxis().SetLabelSize(YLabelSize)	
	h_eta_trans_m.GetYaxis().SetTitleOffset(YTitleOffset)
	h_eta_trans_m.GetXaxis().SetTitle("#eta")
	h_eta_trans_m.GetYaxis().SetTitle("transparency")
	h_eta_trans_p.GetYaxis().SetNdivisions(510)
	h_eta_trans_m.Draw()
	c_trans_m.Print('result_eta_ring/TransparencyVsEta_EE_m_'+runNumber_this+'.pdf')	
	c_trans_m.Print('result_eta_ring/TransparencyVsEta_EE_m_'+runNumber_this+'.png')	
	c_trans_m.Print('result_eta_ring/TransparencyVsEta_EE_m_'+runNumber_this+'.eps')	
	## time response vs. transparency plot
	print "now getting the time response vs. transparency plot..."
	t_p = np.array([])
	et_p = np.array([])
	T_p = np.array([])
	eT_p = np.array([])
	
	t_m = np.array([])
	et_m = np.array([])
	T_m = np.array([])
	eT_m = np.array([])
	
	for index in range(0,32):
		t_p = np.append(t_p, time_mean_p[index])
		et_p = np.append(et_p, time_sigma_p[index])
		T_p = np.append(T_p, trans_mean_p[index])
		eT_p = np.append(eT_p, trans_sigma_p[index])
		t_m = np.append(t_m, time_mean_m[index])
		et_m = np.append(et_m, time_sigma_m[index])
		T_m = np.append(T_m, trans_mean_m[index])
		eT_m = np.append(eT_m, trans_sigma_m[index])
	

	c_gr_plus = rt.TCanvas('time response vs. transparency plus','time response vs. transparency for plus', 200,10,800,600)
	gr_plus = rt.TGraphErrors(32, T_p, t_p, eT_p, et_p)
	gr_plus.SetTitle("time response vs. transparency in EE+")	
	gr_plus.GetYaxis().SetTitle("time response (ns)")	
	gr_plus.GetXaxis().SetTitle("transparency")	
	gr_plus.GetXaxis().SetRangeUser(0.6,1.0)
	gr_plus.GetYaxis().SetRangeUser(-4.0,2.0)


	gr_plus.GetXaxis().SetTitleSize(XTitleSize)	
	gr_plus.GetXaxis().SetLabelSize(XLabelSize)	
	gr_plus.GetXaxis().SetTitleOffset(XTitleOffset)
	gr_plus.GetYaxis().SetTitleSize(YTitleSize)	
	gr_plus.GetYaxis().SetLabelSize(YLabelSize)	
	gr_plus.GetYaxis().SetTitleOffset(YTitleOffset)
	
	gr_plus.SetMarkerStyle(22)	
	gr_plus.SetMarkerColor(2)	
	gr_plus.SetLineColor(1)	
	gr_plus.SetLineWidth(1)	
	gr_plus.SetMarkerSize(1.5)
	gr_plus.Draw("APZ")
	c_gr_plus.Print('result_eta_ring/TimeVsTransparency_EE_p_'+runNumber_this+'.pdf')	
	c_gr_plus.Print('result_eta_ring/TimeVsTransparency_EE_p_'+runNumber_this+'.png')	
	c_gr_plus.Print('result_eta_ring/TimeVsTransparency_EE_p_'+runNumber_this+'.eps')	
	
	c_gr_minus = rt.TCanvas('time response vs. transparency minus','time response vs. transparency for minus', 200,10,800,600)
	gr_minus = rt.TGraphErrors(32, T_m, t_m, eT_m, et_m)
	gr_minus.SetTitle("time response vs. transparency in EE-")	
	gr_minus.GetYaxis().SetTitle("time response (ns)")	
	gr_minus.GetXaxis().SetTitle("transparency")	
	gr_minus.GetXaxis().SetRangeUser(0.6,1.0)
	gr_minus.GetYaxis().SetRangeUser(-4.0,2.0)

	
	gr_minus.GetXaxis().SetTitleSize(XTitleSize)	
	gr_minus.GetXaxis().SetLabelSize(XLabelSize)	
	gr_minus.GetXaxis().SetTitleOffset(XTitleOffset)
	gr_minus.GetYaxis().SetTitleSize(YTitleSize)	
	gr_minus.GetYaxis().SetLabelSize(YLabelSize)	
	gr_minus.GetYaxis().SetTitleOffset(YTitleOffset)
	
	gr_minus.SetMarkerStyle(22)	
	gr_minus.SetMarkerColor(2)	
	gr_minus.SetLineColor(1)	
	gr_minus.SetLineWidth(1)	
	gr_minus.SetMarkerSize(1.5)
	gr_minus.Draw("APZ")
	c_gr_minus.Print('result_eta_ring/TimeVsTransparency_EE_m_'+runNumber_this+'.pdf')	
	c_gr_minus.Print('result_eta_ring/TimeVsTransparency_EE_m_'+runNumber_this+'.png')	
	c_gr_minus.Print('result_eta_ring/TimeVsTransparency_EE_m_'+runNumber_this+'.eps')	
		
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
	
	f_out_vs_eta = rt.TFile('result_eta_ring/Time_Trans_VsEta_EE_'+runNumber_this+'.root','RECREATE')
 	h_eta_time_p.Write()
	h_eta_time_m.Write()
	h_eta_trans_p.Write()
	h_eta_trans_m.Write()
	f_out_vs_eta.Close()
	
	f_out_time_vs_trans = rt.TFile('result_eta_ring/Time_Vs_Trans_EE_'+runNumber_this+'.root','RECREATE')
 	gr_plus.Write()
 	gr_minus.Write()
	f_out_time_vs_trans.Close()
