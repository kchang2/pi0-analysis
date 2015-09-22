# Neutral Pion Analysis

##Setup
This should come straight out of the box. Everything is set, all you need to do is run the appropriate scripts on
batch for LXPLUS or for any T2 server.
Made to use with ECALpro: https://github.com/lpernie/ECALpro. Current edition compatibility is CMSSW is 7.4.2 and 7.4.6_patch6.

##What you should change
I have since modified from the pre-Alpha version. All you need to do to change for integrated use is to edit the parameters.py file. It has most of the options you would want for things like selection cuts, filepaths, which files to run. If you want more advanced analysis or data scrubbing, feel free to edit the section at the end, which will eventually be called 'Developer's Section'. Word of caution is some of these parameters affect the output, and some don't. If you mess up, it could make the entire analysis framework unusable --> so modify cautiously. 

If you would like to edit the code more, feel free to edit any necessary python files to your liking. Some things range from making the appropriate fit range, to how many individual histograms get outputted, to which types of fit to incorporate (all will be added on for modification in the future).

##How to Run
In LXPLUS, you should have these files within your CMSSW folder. Within your CMSSW folder, 
```
  cmsenv
```
should start a new CMS framework software (like a virtual machine). 

Then locate where your pi0-analysis folder is and type in the following command :
```
  python runAnalysis.py
```
Now, based on the packages CMSSW has for python, it should run smoothly. *Edit your parameters before hand, or else it will be set to the standard settings*

##Things that may seem confusing
There are ALOT of things that may seem confusing. This is because this is a work in progress. At the end of the 
summer, everything should be tuned up and running smoothly and efficiently. As of 09/03/2015 (MM/DD/YYYY), I have optimized for efficiency in stacking the data points. If you are using batch, you should do 8nh for etaEB, 1nd for EE, and 1nw for EB. I will be editing this before the academic year begins so that it becomes even more efficient.

##FAQs
####How do I edit parameters?

Well, there are two easy way to do this (that I use). 1) downloading it to your local machine to edit by hand. You can use editing programs such as Notepad++, XCode, WinPython. You get the point, there's a lot of these environments (or interfaces) out there. 2) You can directly edit it in terminal. For BASH, you can use vim or emacs. I only know how to use vim, so to do that, simply type in:
```
  vim FILE_U_WANT_2_EDIT
```
  or in this specific case
```
  vim parameters.py
```
####This is great/terrible and all, but I need to set up my CMSSW, ECALpro, and pull the root files out before I can use this. What should I do?

Well, I have a manual just for that. Email me, kchang2@caltech.edu, to get the manual.

####I want to print out all the pictures and graphs. How do I do that?

Currently, this version does not allow it, so just wait patiently until I make a new version with this feature. If you need it urgently, I suggest you go into the stackNfit.py file and manually load the command. Or, another probably smart thing to do is load up the .root file and then select the ones or print the ones you want straight from terminal. Saves you're computer from heating up from printing so many images.

####Hey, where's the Eta and Phi? It's great that you iX and iY as well as iEta and iPhi, but I want to do some fits by region and analyze effects on each.

This is also in the works. I have included this in our pre-selection cuts for the i-positioning. Now it's a matter of yielding the eta and phi results so we can work with it. Barrel is very simple, and is done in the pre-lim code I've included in fastFindEtaPhi.py, but endcap is much more difficult because of the weighted position of the cluster, NOT the eta of the seed crystal. Only time will tell. Cool? Cool.

####Hey, your method of determining mean and gaussian fits doesn't seem too good of a method. What's up with that?

I agree the method is somewhat less than optimal. I am in the works of making a method that will call for the collection of sigmas and then provide appropriate cutoffs for acceptable sigmas. This should be a better call for what to determine an appropriate gaussian fit than just minimum data threshold.

####The files keep crashing; it just isn't running on my dataset.

There are 3 reasons for it. 1) You modified the code incorrectly OR didn't add the appropriate files (ex. FillEpsilonPlot.cc/.h). 2) Your data files are corrupt and you are running on Batch. This is an unfortunately case in CMSSW framework. The way it digitizes or sorts things can cause issues in the ROOT file from ECALpro. To check if your files are bad, do
```
  root -l GENERIC_ROOT_FILE_NAME*
```
or in a specific case
```
  root -l 2015A_EcalNtp*
```
In the case that a ROOT file is bad, the program will output to 'file [2015A_EcalNtp_12.root] probably not closed, trying to recover'. The FAST analysis programs will still work on these files, just not through batch. It'll have to be locally or through LXPLUS.
3) It could possibly be my fault. Most of the time, it'll be with the program having some bugs. Contact my email and I'll try to help/fix it in anyway.

####Corrupt datafiles?

Yes, there will be times when this happens. The only thing I can offer to you is writing an exception (throwing an exception) in the CMSSW src (source code). I am currently working on that so you do not have to. Will keep you updated soon (as of 09/03/2015).

####Yo, what exactly classifies a corrupt datafile, and can you still run it on for Pi0-Analysis?

A corrupt datafile is any file, when you load in ROOT through the terminal, that doesn't load with the following line: 'Attaching file 2015A_EcalNtp_10.root as _file0...'. These files are created from a mixture of exceptions and formatting between ECALpro and CMSSW.

Yes, you can still run it on Pi0-Analysis (it's a tough cookie), but not using Batch (not that tough though).

##Want to make this better?
Email me @ kchang2@caltech.edu if interested in commiting to this repository. I am relatively new with Github, and relatively new with programming tasks involving big data, so I have a much smaller idea of what I am doing. Basic coder.
