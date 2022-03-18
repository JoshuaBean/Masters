#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 17:18:58 2021

@author: joshuabean
"""

import numpy as np
from scipy.interpolate import interp1d
import os

def calc_mean_deaths(w,i,cwd):
    
        
    file_size = os.stat(cwd + "/gen_" + str(w) + "/Death_" + str(i) + ".txt").st_size
    
    if file_size == 0:
        death_difference = 1000
    else:
        Deaths_file = open(cwd + "/gen_" + str(w) + "/Death_" + str(i) + ".txt", "r")
    
        
        deaths_temp = Deaths_file.read()
        deaths_temp = deaths_temp.split(',')
        Deaths = np.array([int(deaths_temp[i]) for i in range(len(deaths_temp)-1)])
        
        Deaths = Deaths[0:np.int(np.floor(len(Deaths)/30)*30)]
        
        Deaths = Deaths.reshape(int(len(Deaths)/30), 30)
        
        
        mean_deaths = np.mean(Deaths,0)
        
        q_values = np.linspace(0,2,30)
        
        
        f = interp1d(q_values, mean_deaths, kind='cubic')#csaps.CubicSmoothingSpline(q_values, mean_deaths)
        
        
        oracle = np.loadtxt("oracle.txt")
    
        q = np.linspace(0,2,200)
        
        
        pred_deaths = f(q)
        
        
        death_difference = np.sum((pred_deaths-oracle) * 1/2 * np.ones(len(q))) /100
    
    return(death_difference)

plt.plot(q,oracle)
plt.plot(q_values,mean_deaths)