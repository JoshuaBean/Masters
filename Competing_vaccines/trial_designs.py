#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 11:07:30 2020

@author: joshuabean
"""

import numpy as np
import os
import sys


from Implementing_design import Implementing_design


cwd = os.getcwd()


ind = sys.argv[1]
ind = np.int(ind)-1

designs = [
            [300,200,2,2],
            [300,200,2,0.5],
            [300,200,0.5,2],
            [300,200,0.5,0.5],
            [50,100,2,2],
            [50,100,2,0.5],
            [50,100,0.5,2],
            [50,100,0.5,0.5]
          ]

if os.path.exists(cwd + "/Data") == False:
    os.mkdir(cwd + "/Data")



des_index = ind % np.shape(designs)[0]
design = designs[des_index]
run_index = np.int(np.floor(ind/np.shape(designs)[0]))
    
    

cwd_curr = cwd + "/Data" + "/Design_" + str(des_index) 


if os.path.exists(cwd_curr) == False:
    os.mkdir(cwd_curr)


model_parameters = dict(beta = 0.2, sigma = 1/(5.2-2), gamma1 = 1/2, gamma2 = 1/(9.68-2), prob_hospitalisation = 0.0515, N = 1000)


for i in range(1000):
    Implementing_design(model_parameters,design,run_index,des_index,cwd_curr,i)

