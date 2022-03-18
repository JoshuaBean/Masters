#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 11:37:13 2020

@author: joshuabean
"""

import numpy as np
from scipy.integrate import odeint
import math




def SEIIRH_ODE(y,t,model_parameters,q):
    
    return(np.array([-model_parameters['beta']*y[0]*sum(y[[2,3,8,9,14,15]]), 
              model_parameters['beta']*y[0]*sum(y[[2,3,8,9,14,15]]) - model_parameters['sigma']*y[1], 
              model_parameters['sigma']*y[1] - model_parameters['gamma1']*y[2], 
              model_parameters['gamma1']*y[2] - model_parameters['gamma2']*y[3], 
              (1-model_parameters['prob_hospitalisation'])*model_parameters['gamma2']*y[3], 
              model_parameters['prob_hospitalisation']*model_parameters['gamma2']*y[3], 
              
              -q[0]*model_parameters['beta']*y[6]*sum(y[[2,3,8,9,14,15]]), 
              q[0]*model_parameters['beta']*y[6]*sum(y[[2,3,8,9,14,15]]) - model_parameters['sigma']*y[7], 
              model_parameters['sigma']*y[7] - model_parameters['gamma1']*y[8], 
              model_parameters['gamma1']*y[8] - model_parameters['gamma2']*y[9], 
              (1-model_parameters['prob_hospitalisation'])*model_parameters['gamma2']*y[9], 
              model_parameters['prob_hospitalisation']*model_parameters['gamma2']*y[9],
              
              -q[1]*model_parameters['beta']*y[12]*sum(y[[2,3,8,9,14,15]]), 
              q[1]*model_parameters['beta']*y[12]*sum(y[[2,3,8,9,14,15]]) - model_parameters['sigma']*y[13], 
              model_parameters['sigma']*y[13] - model_parameters['gamma1']*y[14], 
              model_parameters['gamma1']*y[14] - model_parameters['gamma2']*y[15], 
              (1-model_parameters['prob_hospitalisation'])*model_parameters['gamma2']*y[15], 
              model_parameters['prob_hospitalisation']*model_parameters['gamma2']*y[15],
              
              model_parameters['gamma1']*y[2],
              model_parameters['gamma1']*y[8],
              model_parameters['gamma1']*y[14]]) )
    
   
    
    
    
def Likelihood(data, q, model_parameters, x0, vaccinations):
    n_days = np.shape(data)[0]

    vacc_dist = x0[[0,1,2]]/np.sum(x0[[0,1,2]])
    
    
    if np.sum(vaccinations) < np.sum(x0[[0,1,2]]):
        x0[[0,1,2]] = x0[[0,1,2]] - vacc_dist*np.sum(vaccinations)
        x0[[6,7,8]] = x0[[6,7,8]] + vacc_dist*vaccinations[0]
        x0[[12,13,14]] = x0[[12,13,14]] + vacc_dist*vaccinations[1]
    elif sum(x0[[0,1,2]]) > 0:
        vacc_new = np.array([vaccinations[0],vaccinations[1]])/np.sum(vaccinations)*np.sum(x0[[0,1,2]])
        x0[[0,1,2]] = x0[[0,1,2]] - np.sum(vacc_new)
        x0[[6,7,8]] = x0[[6,7,8]] + vacc_new[0]
        x0[[12,13,14]] = x0[[12,13,14]] + vacc_new[1]
        
        
    y = SEIIRH_ODE_solve(q, model_parameters, x0, n_days)
    
    
    if np.size(y) <= 21:
        raise Exception(y,vaccinations,data,n_days,q)

    
    ode_data = y[1:,[18,19,20]]
    
    end_of_week_state = y[-1,0:18]
    
    likelihood = np.zeros([n_days,2])
    
    for i in range(n_days):
        temp_data = data[i,]
        
        lam = ode_data[i,]
        
        likelihood[i,] = [  -lam[1] + temp_data[1]*np.log(lam[1]) - np.log(np.double(math.factorial(temp_data[1]))), 
                           -lam[2] + temp_data[2]*np.log(lam[2]) - np.log(np.double(math.factorial(temp_data[2])))]
        #-lam[0] + temp_data[0]*np.log(lam[0]) - np.log(np.double(math.factorial(temp_data[0]))),
        
#        likelihood[i,] = np.log(prob)
    
    l = np.sum(likelihood)
    
    return(l,end_of_week_state)
    
    
    

def SEIIRH_ODE_solve(q, model_parameters, x0, n_days):

    initial_state = np.append(x0,[0,0,0])/model_parameters["N"]
    
    last_day = initial_state
    
    y = initial_state
    
    for i in range(n_days):
        last_day[[18,19,20]] = 0
        
        last_day = odeint(SEIIRH_ODE,last_day,[0,1],args=(model_parameters,q))
        last_day = last_day[-1,:]
        
        y = np.vstack([y,last_day])


    y=y*model_parameters["N"]

    return(y)

