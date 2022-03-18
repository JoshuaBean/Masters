#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 10:15:10 2021

@author: joshuabean
"""

import numpy as np
import multiprocessing as mp


import os
import sys



from trial_design_per_q import trial_design_per_q 




cwd = os.getcwd()

np.random.seed()

pool = mp.Pool(int(os.getenv('SLURM_NTASKS')))



d = sys.argv[1]
d = np.int(d)-1

w = sys.argv[2]
w = np.int(w)





pool = mp.Pool(os.cpu_count())





model_parameters = dict([('pd' , 0.3), ('N',1000), ('gamma',0.2), ('beta',0.3), ('sigma', 0.05), ('Nbins',10000)])


Designs = np.array(np.loadtxt(cwd+"/gen_"+str(w)+"/Designs.txt"))

design = [Designs[d][i] for i in range(4)]

design[0] = np.int(design[0])
design[1] = np.int(design[1])

v = min([model_parameters['N'],design[0]])

x0 = np.array([996-v,4,0,0,v,0,0,0])

dist = "uniform"

#N = 10**6
N=2

Q = np.linspace(0,2,30)



q_allocation = np.mod(range(30),6)
data_allocation = np.floor(np.arange(30)/6)
file_death = open(cwd+"/gen_"+str(w)+"/Death_"+str(d)+".txt",'a')



for i in range(N):
    
    result_over_grid = []
    
    for k in range(30):
        result = pool.apply_async(trial_design_per_q, (model_parameters, x0, design,Q,k,q_allocation,dist))
        result_over_grid.append(result)
        
        
        
    
    results = [result.get() for result in result_over_grid]
        
    
    




    death = np.zeros(30)
    
    for l in range(5):
        temp = np.where(data_allocation==l)[0]
        
        for h in range(6):
            death[q_allocation==np.mod(h,6)] = results[temp[h]]

        
        [file_death.write('%i,' % death[i]) for i in range(30)]
#            file_death.write('%i\n' % death[-1])


file_death.close()


pool.close()
pool.join()

 




