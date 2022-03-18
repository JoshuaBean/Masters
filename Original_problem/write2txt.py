#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 16:15:46 2021

@author: joshuabean
"""

import numpy as np

def write2txt(Designs,cwd):

#    n = np.shape(Designs)[0]
#    f = open(cwd+"/Designs.txt",'w+')
#    
#    for i in range(n-1):
#        [f.write(str(Designs[i,j])+",") for j in range(3)]
#        f.write(str(Designs[i,3])+"\n")
#        
#        
#    [f.write(str(Designs[n-1,j])+",") for j in range(3)]
#    f.write(str(Designs[n-1,3]))
    
#    f.close()
    
    np.savetxt(cwd+"/Designs.txt",Designs)