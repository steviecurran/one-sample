#!/usr/bin/python3
import numpy as np
from scipy import stats
import os 
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd

print("**************************************************************************************")
print("Gives the mean and confidence interval, based on both Z (n > 30) and T-statistics (n < 30)")
print("**************************************************************************************")
form = str(input("Data format, csv or  dat [c/d]? "))
if form != "d":
    os.system("ls *.csv")
else:
    os.system("ls *.dat")

infile = str(input("Data to get confidence interval for? "))
# ~/teaching/VUW/245_Experimental_Physics/data/salaries.dat
os.system("head %s" %(infile))

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

ot = str(input("One [o] or two-sided [any other]: "))
    
df = df.replace('NaN', np.nan) # AS STRING

blankIndex=[''] * len(df); df.index=blankIndex # TO LOSE INDEX
print(df)

no = int(input("Which column do you want to test [1,2,..]? "))
col = df.columns[no-1]; print("Column selected is", col)

def strip(ch):
    df[col] = df[col].str.replace(ch,'', regex=True)

st = str(input("Strip column of weird characters, e.g. $ [y/n]? " ))
if st == "y" or st == "Y":
    ch1 = str(input("Enter character, e.g. $ " )); #print(ch1)
    strip(ch1)
    df[col] = df[col].astype(float)
    
mean = np.mean(df[col]); n = len(df[col]); 
std = np.std(df[col])
stds = std*(float(n)/(n-1))**0.5# TO GET POPULATION, AS OPPOSED TO SAMPLE, VALUE
SE = stds/(float(n)**0.5)

##### WEE HISTO TO VISUALISE ######
data = df[col]

print("%d data points ranging from %1.f to %1.1f, mean = %1.2f, SD = %1.2f (pop) %1.2f (samp)" %(n,min(df[col]), max(df[col]),mean,std,stds))

def histo(dbs):
    min_val = np.min(data); max_val = np.max(data);  #print(min_val,max_val)
    min_boundary = -1.0 * (min_val % dbs - min_val)
    max_boundary = max_val - max_val % dbs + dbs
    n_bins = int((max_boundary - min_boundary) / dbs) + 1
    bins = np.linspace(min_boundary, max_boundary, n_bins)

    size = 14
    plt.rcParams.update({'font.size': size})
    plt.figure(figsize = (6, 4))
    ax = plt.gca();
    plt.setp(ax.spines.values(), linewidth=2)
    ax.tick_params(direction='in', length=6, width=1.5, which='major')
    ax.tick_params(direction='in', length=3, width=1.5, which='minor')
    ax.tick_params(axis='both', which='major', pad=7)

    ax.hist(data, bins=bins-dbs/2, color="w", edgecolor="darkblue",linewidth=3);
    plt.xlabel(col); plt.ylabel("Number")
    
    #xmin = round(min_val-dbs,0); xmax = round(max_val+dbs,0)
    xmin, xmax = plt.xlim();ax.set_xlim(xmin,xmax)
    ymin, ymax = plt.ylim(); #print(xmin,xmax,bins, len(bins))
    xpos = xmin+(xmax-xmin)/16; ypos = ymax-(ymax-ymin)/12; yskip = (ymax-ymin)/12;

    mean = np.mean(data); std =  np.std(data); 
    plt.text(xpos,ypos,"\u03BC = %1.2f, \u03C3 = %1.2f" %(mean,std),
             fontsize = int(0.8*size), c = 'k')
    plt.tight_layout()
    outfile = '%s-histo.png' %(infile) # HAS TO BE HERE, REMOVED dbs SO OVERWRITTEN
    #plt.savefig(outfile); #print('Written to %s' %(outfile))
    plt.show()

ph = str(input("Plot histogram [y/n]? "))
if ph == "y" or ph == "Y" :
    dbs = float(input("Desired bin width? "))
    histo(dbs)    
    again = str(input("Another bin width [y/n]? "))
    while again == "y" or again == "Y" :
        dbs = float(input("Desired bin width? "))
        histo(dbs)
        again = str(input("Another bin width [y/n]? "))

    #os.system("mv %s-histo.eps %s-histo_dbs=%1.2f.eps" %(infile,infile,dbs));
    #print('Written to %s-histo_dbs=%1.2f.eps' %(infile,dbs))
#####################################
con = float(input("\nLevel of confidence [e.g. 95, 99, 99.9% - 3 sigma is 99.75]? "))

from scipy.stats import norm

def z_bit(con):
    p = 1-con/100
    if ot == "o":
        alpha = 0.5-p
        ot_text = "one-sided"
    else:
        alpha = 0.5-(p/2)
        ot_text = "two-sided"
    pi = 3.141592654;
    stand = 1/((2*pi)**0.5)
    
    Z = norm.ppf(1-p/2,loc=0,scale=1) # AGREES WITH ~/C/stats/Z-value TO ~ 1e-15 (8 sigma)

    ########################################################################
    
    CI = Z*SE
    print("\nFor %1.2f%% confidence, z = %1.3f,\n  giving mean of %1.2f +/- %1.2f (range of %1.2f to %1.2f)"
          %(con,Z,mean,CI,mean-CI,mean+CI))
    
def t_bit(con):
    p = 1-con/100;
    if ot == "o":
        alpha = 0.5-p
        ot_text = "one-sided"
    else:
        alpha = 0.5-(p/2)
        ot_text = "two-sided"

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

    dof = n-1
    gamma_num = gamma_f(float(n)/2)
    gamma_den = gamma_f(float(dof)/2)
    stand =  gamma_num/(((np.pi*dof)**0.5)*gamma_den)

    npts = 100000; 
    xf = 5;x = [xi]; y = [yi]; total =0;y_total = 0; total = 0; area = 0; j =0
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
    CI = T*SE
    print("For %1.2f%% confidence (%1.0f DoFs), t= %1.3f [%s],\n giving mean diff of %1.2f +/- %1.2f (%1.2f to %1.2f)"
          %(con,dof,T,ot_text,mean,CI,mean-CI,mean+CI))

if n >= 30:
    print("Sample size >= 30 so using z-value")
    z_bit(con)
    again = str(input("Try another confidence level [y/n]? "))
    while again != "n":
        con = float(input("\nHow much [e.g. 95, 99, 99.9% - z = 3 sigma is 99.75]? "))
        z_bit(con)
        again = str(input("Try another confidence level [y/n]? "))        
else:
    print("Sample size < 30 so using t-value")
    t_bit(con)
    again = str(input("Try another confidence level [y/n]? "))
    while again != "n":
        con = float(input("\nHow much [e.g. 95, 99, 99.9% - z = 3 sigma is 99.75]? "))
        t_bit(con)
        again = str(input("Try another confidence level [y/n]? "))
