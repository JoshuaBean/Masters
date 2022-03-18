#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 09:32:14 2020

@author: joshuabean
"""

import numpy as np
import os
import multiprocessing as mp

#from Simulate_SEIIRH import Simulate_SEIIRH
from trial_design_per_q_pair import trial_design_per_q_pair



def Implementing_design(model_parameters,design,run_index,des_index,cwd_curr,index):
    
    temp_dir = cwd_curr + "/Run_" +str(run_index) + "_" + str(index)
    
    
    if os.path.exists(temp_dir) == False:
        os.mkdir(temp_dir)

    p, d, f = next(os.walk(temp_dir))
    
    if len(f) == 0:
        pool = mp.Pool(int(os.getenv('SLURM_NTASKS')))
#        pool = mp.Pool(mp.cpu_count())
    
        x0 = np.array([model_parameters['N']-4-2*design[0],0,0,4,0,0,design[0],0,0,0,0,0,design[0],0,0,0,0,0])
        
        qs = np.linspace(0.05,1,20)
        q1,q2 = np.meshgrid(qs,qs)
       
            
        result_over_grid = []
        
        n_q_pairs = 400
        
        for k in range(n_q_pairs):
            i = np.int(np.floor(k/20))
            j = k%20
            result = pool.apply_async(trial_design_per_q_pair, (k,model_parameters, x0, design,[q1[i,j],q2[i,j]],temp_dir))
            result_over_grid.append(result)
            
    
        results = [result.get() for result in result_over_grid]
        
        
        
        num_hosp_c = np.zeros([20,20])
        num_hosp_v1 = np.zeros([20,20])
        num_hosp_v2 = np.zeros([20,20])
        
        num_vacc_v1 = np.zeros([20,20])
        num_vacc_v2 = np.zeros([20,20])
        
#        MAP_v1 = np.zeros([20,20])
#        MAP_v2 = np.zeros([20,20])
        
        
        for k in range(n_q_pairs):
            i = np.int(np.floor(k/20))
            j = k%20
            
            num_hosp_c[i,j] = results[k][0]
            num_hosp_v1[i,j] = results[k][1]
            num_hosp_v2[i,j] = results[k][2]
            
            num_vacc_v1[i,j] = results[k][3]
            num_vacc_v2[i,j] = results[k][4]
            
#            MAP_v1[i,j] = results[k][5]
#            MAP_v2[i,j] = results[k][6]
            
        np.savetxt(temp_dir + "/num_hosp_c.txt", num_hosp_c, fmt="%s")
        np.savetxt(temp_dir + "/num_hosp_v1.txt", num_hosp_v1, fmt="%s")
        np.savetxt(temp_dir + "/num_hosp_v2.txt", num_hosp_v2, fmt="%s")
            
        np.savetxt(temp_dir + "/num_vacc_v1.txt", num_vacc_v1, fmt="%s")
        np.savetxt(temp_dir + "/num_vacc_v2.txt", num_vacc_v2, fmt="%s")
            
#        np.savetxt(temp_dir + "/MAP_v1.txt", MAP_v1, fmt="%s")
#        np.savetxt(temp_dir + "/MAP_v2.txt", MAP_v2, fmt="%s")
        
        
        
        
        pool.close()
        pool.join()
        
    else:
        return()
        

