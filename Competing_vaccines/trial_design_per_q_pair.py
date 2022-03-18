#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 12:27:44 2020

@author: joshuabean
"""


from Simulate_SEIIRH import Simulate_SEIIRH
import numpy as np

def trial_design_per_q_pair(k,model_parameters, x0, design, q, cwd):

    obs_data,ts,data,vaccinations = Simulate_SEIIRH(model_parameters, q, x0, design)
        
    #plt.plot(q_values, post1)
    #plt.plot(q_values, post2)
    #plt.legend(["q1","q2"])
    #plt.savefig(cwd + "Post_" + str(k) + ".png", dpi = 500)
    #plt.close()    
       
        
    num_hosp_c = data[-1,5]
    num_hosp_v1 = data[-1,11]
    num_hosp_v2 = data[-1,17]
    
    num_vacc_v1 = sum(data[-1,6:12])
    num_vacc_v2 = sum(data[-1,12:18])
    
#    MAP_v1 = q_values[np.argmax(post1)]
#    MAP_v2 = q_values[np.argmax(post2)]
    
    return([num_hosp_c,num_hosp_v1,num_hosp_v2, num_vacc_v1, num_vacc_v2]) #, MAP_v1, MAP_v2])
    
