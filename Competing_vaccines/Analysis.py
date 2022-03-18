#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 10:04:59 2021

@author: joshuabean
"""

import numpy as np
import os
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.stats import multivariate_normal

cwd = os.getcwd()


#MAP_v1 = dict()
#MAP_v2 = dict()

num_hosp_c = dict()
num_hosp_v1 = dict()
num_hosp_v2 = dict()

num_vacc_v1 = dict()
num_vacc_v2 = dict()


for i in range(7):
    
    
    curr_dir = cwd+ "/Data" + "/Design_"+ str(i)
    
    d,f,r = next(os.walk(curr_dir))
    n_runs = len(f)
    
    
#    temp_MAP_v1 = np.zeros([20,20])
#    temp_MAP_v2 = np.zeros([20,20])
    
    temp_num_hosp_c = np.zeros([20,20])
    temp_num_hosp_v1 = np.zeros([20,20])
    temp_num_hosp_v2 = np.zeros([20,20])
    
    temp_num_vacc_v1 = np.zeros([20,20])
    temp_num_vacc_v2 = np.zeros([20,20])
    count = 0
    for j in range(n_runs):
        print([i,j])
        temp_dir = curr_dir + "/" + f[j]
        dt,ft,rt = next(os.walk(temp_dir))
        
        if len(rt) > 0:
            count = count+1
        
#            temp_MAP_v1 = + temp_MAP_v1 + np.loadtxt(temp_dir+"/MAP_v1.txt")
#            temp_MAP_v2 = + temp_MAP_v2 + np.loadtxt(temp_dir+"/MAP_v2.txt")
            
            temp_num_hosp_c = + temp_num_hosp_c + np.loadtxt(temp_dir+"/num_hosp_c.txt")
            temp_num_hosp_v1 = + temp_num_hosp_v1 + np.loadtxt(temp_dir+"/num_hosp_v1.txt")
            temp_num_hosp_v2 = + temp_num_hosp_v2 + np.loadtxt(temp_dir+"/num_hosp_v2.txt")
            
            temp_num_vacc_v1 = + temp_num_vacc_v1 + np.loadtxt(temp_dir+"/num_vacc_v1.txt")
            temp_num_vacc_v2 = + temp_num_vacc_v2 + np.loadtxt(temp_dir+"/num_vacc_v2.txt")
        
        
        
#    temp_MAP_v1 = temp_MAP_v1/count
#    temp_MAP_v2 = temp_MAP_v2/count
    
    temp_num_hosp_c = temp_num_hosp_c/count
    temp_num_hosp_v1 = temp_num_hosp_v1/count
    temp_num_hosp_v2 = temp_num_hosp_v2/count
    
    temp_num_vacc_v1 = temp_num_vacc_v1/count
    temp_num_vacc_v2 = temp_num_vacc_v2/count
    
#    MAP_v1[i] = temp_MAP_v1
#    MAP_v2[i] = temp_MAP_v2
    
    num_hosp_c[i] = temp_num_hosp_c
    num_hosp_v1[i] = temp_num_hosp_v1
    num_hosp_v2[i] = temp_num_hosp_v2
    
    num_vacc_v1[i] = temp_num_vacc_v1
    num_vacc_v2[i] = temp_num_vacc_v2
    
    
    
    
    
    
    
    
    
    
    
designs = [
            [100,800],
            [100,100],
            [200,50],
            [200,200],
            [200,300],
            [200,600],
            [300,200]
          ]
    
    

qs = np.linspace(0.05,1,20)
q1,q2 = np.meshgrid(qs,qs)
 
colourbar_lim = 0
for i in range(np.shape(designs)[0]):
    colourbar_lim_temp = np.max(num_hosp_c[i]+num_hosp_v1[i]+num_hosp_v2[i])
    if colourbar_lim_temp > colourbar_lim:
        colourbar_lim = colourbar_lim_temp


p = np.zeros([20,20])
mu = [0.3,0.6]
sigma = [[0.1,0],[0,0.1]]


####### This is for the number Hospitalised      
for i in range(np.shape(designs)[0]):
    
    
    #Calculate utility
    total = num_hosp_c[i]+num_hosp_v1[i]+num_hosp_v2[i]

    least_worst = np.zeros(20)
    
    for k in range(20):
        least_worst[k] = total[19-k,k]
        
    utility = np.min(least_worst)#np.trapz(np.trapz(total,qs),qs)
    
        
    which_ute = np.argmax(np.diag(total))

    
    
    
    f, axs = plt.subplots(2, 2)
    temp = axs[0,0].contourf(q1,q2,num_hosp_c[i],np.linspace(0,np.ceil(colourbar_lim),10))
    axs[0,0].set_title("Control")
    axs[0,0].set_xlabel("q1")
    axs[0,0].set_ylabel("q2")
    axs[0,1].contourf(q1,q2,num_hosp_v1[i],np.linspace(0,np.ceil(colourbar_lim),10))
    axs[0,1].set_title("Vaccine 1")
    axs[0,1].set_xlabel("q1")
    axs[0,1].set_ylabel("q2")
    axs[1,0].contourf(q1,q2,num_hosp_v2[i],np.linspace(0,np.ceil(colourbar_lim),10))
    axs[1,0].set_title("Vaccine 2")
    axs[1,0].set_xlabel("q1")
    axs[1,0].set_ylabel("q2")
    axs[1,1].contourf(q1,q2,num_hosp_c[i]+num_hosp_v1[i]+num_hosp_v2[i],np.linspace(0,np.ceil(colourbar_lim),10))
    axs[1,1].set_title("Total")
    axs[1,1].set_xlabel("q1")
    axs[1,1].set_ylabel("q2")
    f.suptitle("Design = " + str(designs[i]) +", AUC = " + str(np.round(np.trapz(np.trapz(total,qs),qs),3)) + ", Ute = " + str(np.round(utility,3)) + ", [q1,q2] = [" + str(diagonal[0,which_ute]) +", " + str(diagonal[1,which_ute]) + "]",y=1.05,x=0.45)
    f.tight_layout()
    f.colorbar(temp,ax=axs)
    f.savefig(cwd + "/Plots" + "/Num_Hosp_Design_" + str(i) + ".png", dpi = 800, bbox_inches='tight')
    
    
    
    
    
####### MAPs    
    colourbar_lim = 1
    
    f, axs = plt.subplots(1, 2)
    temp = axs[0].contourf(q1,q2,MAP_v1[i],np.linspace(0,np.ceil(colourbar_lim),10))
    axs[0].set_title("Vaccine 1")
    axs[0].set_xlabel("q1")
    axs[0].set_ylabel("q2")
    axs[1].contourf(q1,q2,MAP_v2[i],np.linspace(0,np.ceil(colourbar_lim),10))
    axs[1].set_title("Vaccine 2")
    axs[1].set_xlabel("q1")
    axs[1].set_ylabel("q2")
    f.tight_layout()
    f.colorbar(temp,ax=axs)
    f.suptitle("Design = " + str(designs[i]),y=1.05,x=0.45)
    f.savefig(cwd + "/Plots" + "/MAP_Design_" + str(i) + ".png", dpi = 800, bbox_inches='tight')
    
    
    
    
####### num_vacc   
    colourbar_lim = np.max([np.max(num_vacc_v1[i]),np.max(num_vacc_v2[i])])
    
    f, axs = plt.subplots(1, 2)
    temp = axs[0].contourf(q1,q2,num_vacc_v1[i],np.linspace(0,np.ceil(colourbar_lim),10))
    axs[0].set_title("Vaccine 1")
    axs[0].set_xlabel("q1")
    axs[0].set_ylabel("q2")
    axs[1].contourf(q1,q2,num_vacc_v2[i],np.linspace(0,np.ceil(colourbar_lim),10))
    axs[1].set_title("Vaccine 2")
    axs[1].set_xlabel("q1")
    axs[1].set_ylabel("q2")
    f.tight_layout()
    f.colorbar(temp,ax=axs)
    f.suptitle("Design = " + str(designs[i]),y=1.05,x=0.45)
    f.savefig(cwd + "/Plots" + "/num_vacc_Design_" + str(i) + ".png", dpi = 800, bbox_inches='tight')
    
    
    
#    i=3
#    f = plt.contourf(q1,q2,num_hosp_c[i]+num_hosp_v1[i]+num_hosp_v2[i])
#    plt.colorbar(f)
    
    
    
