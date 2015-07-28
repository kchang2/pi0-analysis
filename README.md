# Neutral Pion Analysis

##Setup
This should come straight out of the box. Everything is set, all you need to do is run the appropriate scripts on
batch for LXPLUS or for any T2 server.
Made to use with ECALpro: https://github.com/lpernie/ECALpro. Current edition of CMSSW is 7.4.2.

##How to Run
In LXPLUS, type in the following:
```
  bsub -q 1nd < SCRIPTNAME.SH
```
where 1nd can be 1nh, 1nd, 2nd, 1nw, etc. These represent # of normal (hours, days, weeks) it takes for your program
to normally run on your local machine.
