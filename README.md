# Neutral Pion Analysis

##Setup
This should come straight out of the box. Everything is set, all you need to do is run the appropriate scripts on
batch for LXPLUS or for any T2 server.
Made to use with ECALpro: https://github.com/lpernie/ECALpro. Current edition of CMSSW is 7.4.2.

##What you should change
You definitely need to change the filepath of where the python programs get the .root files. Note that I have
made appropriate folders for these programs in respective programs (most of it should be called in runFills.py).
Otherwise, everything else should be okay. The only TRUE difference between my code and your code would be 
where we get the information needed to analyze (where the data is stored and where we output our results). This could be file paths, which run you are getting your data from, where you ouput your files.

##How to Run
In LXPLUS, you should have these files within your CMSSW folder. Within your CMSSW folder, 
```
  cmsenv
```
should start a new CMS framework software (like a virtual machine). 

Then locate where your script files (.sh) are and type in the following command :
```
  bsub -q 1nd < SCRIPTNAME.SH
```
where 1nd can be 1nh, 1nd, 2nd, 1nw, etc. These represent # of normal (hours, days, weeks) it takes for your program
to normally run on your local machine.

##Things that may seem confusing
There are ALOT of things that may seem confusing. This is because this is a work in progress. At the end of the 
summer, everything should be tuned up and running smoothly and efficiently. As of 07/28/2015, there is a lack of
efficiency in the code (more of a lack of POWER in memory I can use before getting booted off batch). I will be
editing this in the course of the summer so that you can run it (albeit slower) in any busy server.

##Want to make upgrades?
Email me @ kchang2@caltech.edu if interested in commiting to this repository. I am relatively new with Github, so 
I have absolutely no idea what I am doing. Basic coder.
