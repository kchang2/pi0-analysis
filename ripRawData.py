##
## This takes all needed data from any runs
## and compiles them into a list so that you can access and
## use.
##
## Updated as of 07/23/2015
## Working as of 07/23/2015
##
import sys, random, math
import time
import os

from FastProgressBar import progressbar

if __name__ == "__main__":
    
    #creates .list file
    dlname = '2015B_ALL_RAW.list'
    file = open(dirname, 'a')
    print("created " + dlname)
    
    retdir = os.getcwd()
    masterdir = '/eos/cms/store/data/Run2015B/AlCaP0/RAW/v1/000/'
    masterList = os.lsdir(datadir)
    
    #Just checking to see if we are in right path
    os.system('eos ls ' + masterdir)

    for k in range(0,len(masterList)):
        currentdir = masterdir + dataList[k]
        while currentdir != masterdir:
            currentList = os.lsdir(currentdir)
            if currentList[1]