#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 13:46:51 2021

@author: joshuabean
"""

import numpy as np


def Likelihood(model_parameters,data,ts,q):
   
    difference = np.diff(data,axis=0)
    time_difference = np.diff(ts,axis=0)
    
    rates = np.vstack([
         model_parameters["beta"]*(data[:,1]+data[:,5])*data[:,0]/(model_parameters["N"]-1),
         (1-model_parameters["pd"])*model_parameters["gamma"]*data[:,1],
         model_parameters["pd"]*model_parameters["gamma"]*data[:,1],
         q*model_parameters["beta"]*(data[:,1]+data[:,5])*data[:,4]/(model_parameters["N"]-1),
         (1-model_parameters["pd"])*model_parameters["gamma"]*data[:,5],
         model_parameters["pd"]*model_parameters["gamma"]*data[:,5]
         ])
    
    total_rate = np.sum(rates,0)

    l = 0
    transition = 0
    
    for i in range(np.shape(difference)[0]):
        
        if all(difference[i] == [-1,1,0,0,0,0,0,0]):
            transition = 0
        elif all(difference[i] == [0,-1,1,0,0,0,0,0]):
            transition = 1
        elif all(difference[i] == [0,-1,0,1,0,0,0,0]):
            transition = 2
        elif all(difference[i] == [0,0,0,0,-1,1,0,0]):
            transition = 3
        elif all(difference[i] == [0,0,0,0,0,-1,1,0]):
            transition = 4
        elif all(difference[i] == [0,0,0,0,0,-1,0,1]):
            transition = 5
        else:
            transition = 6
            
            
        
        if transition == 6:
            l =  l - total_rate[i]*time_difference[i]
        else:
            if rates[transition,i] == 0:
                raise Exception(transition,i,q,data,difference,rates)

            l =  l + np.log(rates[transition,i]) - total_rate[i]*time_difference[i]

        
        
            
    return(l)
    