#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 15:59:29 2021

@author: joshuabean
"""

import os
import lhsmdu
import numpy as np



from write2txt import write2txt


cwd = os.getcwd()



if os.path.exists(cwd+"/Slurms") == False:
    os.mkdir(cwd+"/Slurms")



if os.path.exists(cwd+"/gen_1") == False:
    os.mkdir(cwd+"/gen_1")
        


Designs = lhsmdu.sample(100,4)
Designs[:,0] = np.floor(Designs[:,0]*1000)
Designs[:,1] = np.floor(Designs[:,1]*1000)
Designs[:,2] = Designs[:,2]*2


write2txt(Designs,cwd+"/gen_1")


f = open(cwd+"/best_design.txt",'w+')
[f.write(str(0)+",") for i in range(3)]
f.write(str(0))
f.close()


f = open(cwd+"/best_mean_deaths.txt",'w+')
f.write("%i"%1000)
f.close()


