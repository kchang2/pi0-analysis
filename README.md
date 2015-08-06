# Neutral Pion Analysis
#####NEED TO WORK ON#######

##Setup
This should come straight out of the box. Everything is set, all you need to do is run the appropriate scripts on
batch for LXPLUS or for any T2 server.
Made to use with ECALpro: https://github.com/lpernie/ECALpro. Current edition of CMSSW is 7.4.2.

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
summer, everything should be tuned up and running smoothly and efficiently. As of 08/06/2015 (MM/DD/YYYY), there is a lack of true efficiency in the code (more of a lack of POWER in memory I can use before getting booted off batch). I will be editing this in the course of the summer so that you can run it (albeit slower) in any busy server.

##Want to make this better?
Email me @ kchang2@caltech.edu if interested in commiting to this repository. I am relatively new with Github, and relatively new with programming tasks involving big data, so I have a much smaller idea of what I am doing. Basic coder.
