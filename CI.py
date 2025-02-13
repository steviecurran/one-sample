#!/usr/bin/python3
import numpy as np
import os 
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
from scipy import stats

print("********************************************************************************")
print("For independent samples - if using dependent samples (the difference)\n e.g. before/after, husband/wife, SAT/course accepetance, use CI.py")
print("*******************************************************************************")
form1 = str(input("\nInputing full data or summary [f/s]? "))
if form1 == "s" or form1 == "S": 
    print("This will test the two data sets from the summarised data - for input data use CI-t-2_means.py")
    print("Sample 1...")
    n1 = int(input("Size of sample? ")); m1 = float(input("Mean of sample? ")); s1 = float(input("SD of sample? "))
    print("Sample 2...")
    n2 = int(input("Size of sample? ")); m2 = float(input("Mean of sample? ")); s2 = float(input("SD of sample? "))
else:
    form = str(input("Data format, csv or  dat [c/d]? "))

    if form != "d":
        os.system("ls *.csv")
    else:
        os.system("ls *.dat")

    infile = str(input("Data wtih the two samples to compare? "))
    os.system("head %s" %(infile))
    
    '''
    if form != "d":
        df = pd.read_csv(infile,comment='#')
    else:
        df = pd.read_csv(infile,delim_whitespace=True,comment='#')
    '''
    hq = str(input("\nIs there a header [y/n]? " ))

    if form != "d":
        if hq == "n":
            df = pd.read_csv(infile,header=None,comment='#')
        else:
            df = pd.read_csv(infile,comment='#')
    else:
        if hq == "n":
            df = pd.read_csv(infile,delim_whitespace=True,header=None,comment='#')
        else:
            df = pd.read_csv(infile,delim_whitespace=True,comment='#')
        
    tran = str(input("Need to tranpose [y/n]? " ))
    if tran == "y" or tran == "Y":
        df = df.T
        df.columns = df.iloc[0]
        df= df[1:]
        
    df = df.replace('NaN', np.nan) # AS STRING
    zeroes = str(input("Replace 0s with Nans [y/n]? " ))
    if zeroes == "y" or zeroes == "Y":
        df = df.replace(0, np.nan)

    print(df)
    col1 = df.columns[0]; col2 = df.columns[1];  #print(col1,col2)
    nans1 = df[df[col1] != df[col1]]
    nans2 = df[df[col2] != df[col2]] 
    #import statistics as stats
    m1 = np.mean(df[col1]); n1 = len(df[col1]) - len(nans1);
    s1 = np.std(df[col1]) * (float(n1)/(n1-1))**0.5; 
    SE1 = s1/(float(n1)**0.5) # SAMPLE SD

    m2 = np.mean(df[col2]); n2 = len(df[col2])-len(nans2); #-nans
    s2 = np.std(df[col2]) * (float(n2)/(n2-1))**0.5
    SE2 = s2/(float(n2)**0.5)

    print("For %s -  n = %d, mean = %1.3f, SD = %1.3f [sample]" %(col1,n1,m1,s1)) 
    print("For %s -  n = %d, mean = %1.3f, SD = %1.3f [sample]" %(col2,n2,m2,s2))

    x = df[col1]; y = df[col2]; print(x,y)
    #t,p_t = stats.ttest_ind(x,y);#The bug is in line 3885, in file scipy/scipy/stats/stats.py 
    #t,p_t = stats.ttest_ind(df.dropna()[col1], df.dropna()[col2],equal_var=True)
    t,p_t = stats.ttest_ind(df.dropna()[col1], df.dropna()[col2],equal_var=False)
    ks = stats.kstest(x,y); p_ks = ks[1]
    print("t-test (BUGGY WITH NaN) gives p = %1.3f and KS gives p = %1.3e of being drawn from same population"%(p_t,p_ks))
       
m = m1 - m2
pi = np.pi

con = float(input("\nLevel of confidence [e.g. 95, 99, 99.9% - z = 3 sigma is 99.75]? "))

from scipy.stats import norm

def z_bit(con):
    p = 1-con/100; alpha = 0.5-(p/2) # actually alpha/2 -doing one sided

    pooled_var = s1**2/n1 + s2**2/n2
    pooled_SD = pooled_var**0.5
    pooled_SE = pooled_SD*(1/n1 + 1/n2)**0.5
    
    Z = norm.ppf(1-p/2,loc=0,scale=1) # AGREES WITH ~/C/stats/Z-value TO ~ 1e-15 (8 sigma)
        
    CI = Z*pooled_SD
    print("\nFor %1.5f %% confidence, z-value is %1.3f, \n  giving  mean diff of %1.2f +/- %1.2f (%1.2f to %1.2f)" %(con,Z,m,CI,m-CI,m+CI))

def t_bit(con):
    p = 1-con/100;alpha = 0.5-(p/2) 
    npts = 100000
    xi = 0.0; yi = 0;xf = 100; # SHOULD BE INFINITY
    def gamma_f(value):
        x = [xi]; y = [yi]; gamma =0
        for i in range(1,npts):
            dx = (xf-xi)/npts           
            x = i*dx
            y = x**(value-1)*np.exp(-x)
            area =y*dx
            gamma = gamma + area
        return gamma

    var_ratio = s1**2/s2**2
    print("Variance ratio is %1.2f," %(var_ratio))
    equ = str(input("Assume equal sample variances (for ratio between 0.5 and 2 can assume equal) [y/n]? "))

    if equ == "y" or equ == "Y":
    #if var_ratio >= 0.5 and var_ratio >= 0.5:
        #print(" which is between 0.5 and 2 so can assume same population variances")
        dof = n1 + n2 -2
        pooled_var = ((n1 - 1)*s1**2 + (n2 - 1)*s2**2)/(n1 + n2 -2)
        pooled_SD = pooled_var**0.5
        pooled_SE = pooled_SD*(1/n1 + 1/n2)**0.5; #print(pooled_SD,pooled_SE) #OKAY SO FAR

    else:
        A = s1**2/n1; B =  s2**2/n2
        dof = (A+B)**2/(A**2/(n1-1) + B**2/(n2-1))
        
        pooled_SE = (s1**2/n1 + s2**2/n2)**0.5;
        
    n = dof+1
    gamma_num = gamma_f(float(n)/2)
    gamma_den = gamma_f(float(dof)/2)
    stand =  gamma_num/(((np.pi*dof)**0.5)*gamma_den)
    #print("For %d dof, gamma_num = %1.5f, gamma_den = %1.5f (xf = %1.0f ratio = %1.3f stand = %1.3f)" %(dof,gamma_num,gamma_den, xf,gamma_num/gamma_den,norm))
         
    npts = 100000; 
    xf = 5;x = [xi];yy = [yi]; total =0;y_total = 0; total = 0; area = 0; j =0
    dx = (xf-xi)/npts
    for i in range(npts):
        x = i*dx
        y = stand*(1+ x**2/dof)**float(-n/2)
        while(total < alpha):
            y_total = stand*(1+ (j*dx)**2/dof)**float(-n/2)
            area = y_total*dx
            total = total + area; 
            j = j+1
    T = dx*j; 
    CI = T*pooled_SE
    print("For %1.2f%% confidence (%1.0f DoFs), t-value is %1.3f, giving mean diff of %1.2f +/- %1.2f (%1.2f to %1.2f)" %(con,dof,T,m,CI,m-CI,m+CI))

cut = 30
    
if n1 > cut and n2 > cut:
    print("Both sample sizes > %d so using z-value" %(cut))
    z_bit(con)
    again = str(input("Try another confidence level [y/n]? "))
    while again != "n":
        con = float(input("\nHow much [e.g. 95, 99, 99.9% - z = 3 sigma is 99.75]? "))
        z_bit(con)
        again = str(input("Try another confidence level [y/n]? "))        
else:
    print("At least one sample size < %d so using t-value" %(cut))
    t_bit(con)
    again = str(input("Try another confidence level [y/n]? "))
    while again != "n":
        con = float(input("\nHow much [e.g. 95, 99, 99.9% - z = 3 sigma is 99.75]? "))
        t_bit(con)
        again = str(input("Try another confidence level [y/n]? "))
    
 
