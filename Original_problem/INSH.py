#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 16:23:39 2021

@author: joshuabean
"""

import numpy as np
import os
import sys

from Perturbation import Perturbation
from calc_mean_deaths import calc_mean_deaths
from write2txt import write2txt


cwd = os.getcwd()

w = sys.argv[1]
w = np.int(w)

model_parameters = dict([('pd' , 0.3), ('N',1000), ('gamma',0.2), ('beta',0.3), ('sigma', 0.05), ('Nbins',10000)])


r = 19
m = 5

Designs = np.array(np.loadtxt(cwd+"/gen_"+str(w)+"/Designs.txt"))


best_des = open(cwd+"/best_design.txt",'r')
best_design = best_des.read()
best_des.close()

best_des = best_design.split(',')
best_design = np.array([float(best_des[i]) for i in range(4)])


best_md = open(cwd+"/best_mean_deaths.txt",'r')
best_mean_deaths = float(best_md.read())
best_md.close()





mean_deaths = np.zeros(np.shape(Designs)[0])

for i in range(np.shape(Designs)[0]):
    print(i)
    mean_deaths[i] = calc_mean_deaths(w,i,cwd)

mean_deaths[np.isnan(mean_deaths)] = 1000


ma = np.min(mean_deaths)
ind = np.argmin(mean_deaths)



if ma <= best_mean_deaths:
    best_design = Designs[ind]
    
    f = open(cwd+"/best_design.txt",'w+')
    f.write(str(best_design[0])+",")
    f.write(str(best_design[1])+",")
    f.write(str(best_design[2])+",")
    f.write(str(best_design[3]))
    f.close()


    
    f = open(cwd+"/best_mean_deaths.txt",'w+')
    f.write("%i" % mean_deaths[ind])
    f.close()



ind = np.argsort(mean_deaths)

best_designs = Designs[ind[0:r],:]

new_designs = np.vstack([best_designs ,best_design])

new_designs = Perturbation(new_designs,m,model_parameters["N"])




if os.path.exists(cwd+"/gen_" +str(w+1)) == False:
    os.mkdir(cwd+"/gen_" +str(w+1))
     
    
write2txt(new_designs,cwd+"/gen_" +str(w+1))



