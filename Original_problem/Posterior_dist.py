#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 11:07:02 2021

@author: joshuabean
"""

from Prior import Prior
from Likelihood import Likelihood


def Posterior_dist(model_parameters,data,ts,q,dist,l):
    
    likelihood = Likelihood(model_parameters,data,ts,q)

    likelihood = likelihood + l

    post = Prior(q,"prob",dist) + likelihood
    
    
    return(post,likelihood)