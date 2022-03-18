#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 14:11:29 2021

@author: joshuabean
"""

import numpy as np

def prob_good(post,q_values,cutoff):
    
    i = np.where(q_values>cutoff)[0][0]
    
    
    if np.size(np.where(q_values>cutoff)[0][0]) == 0:
        p_good=1
    else:
        p_good = np.trapz(post[0:i],q_values[0:i])
        
        
    return(p_good)