#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 11:10:40 2020

@author: joshuabean
"""


from scipy import optimize
import numpy as np
import matplotlib.pyplot as plt
# the MAP of the worst vaccine will initially have a sqrt function for the maximum number vaccinated
x = np.linspace(0,1,100)
#lin = 90*(1-x)+10
lin = (1-x)
f = 1/(10*np.sqrt(x))

t = 0.5
plt.plot(x,f)
plt.plot(x,lin)
plt.plot(x,x)
#plt.plot(x,90*x+11)
plt.plot(x,t*f + (1-t)*lin)






x = np.linspace(0,1,100)
lin = 90*(1-x)+10
f = 10/np.sqrt(x)

t = 0.8
plt.plot(x,f)
plt.plot(x,lin)
#plt.plot(x,90*x+10)


values = np.zeros([200,2])
curve = np.zeros([200,2])
lin = np.zeros([200,2])
k=0
for i in range(-100,100):

    # plt.plot(x,90*x+i,alpha=0.4)
    
    
    curve[k,0] = optimize.root(lambda x: 10/np.sqrt(x) - 90*x+i, 0.01).x
    lin[k,0] = optimize.root(lambda x: 90*(1-x)+10 - 90*x+i, 0.01).x
    
    curve[k,1] = 10/np.sqrt(curve[k,0])
    lin[k,1] = 90*(1-lin[k,0])+10
    
    values[k,:] =  [t*curve[k,0] + (1-t)*lin[k,0], t*curve[k,1]+(1-t)*lin[k,1] ]
    k=k+1
    

plt.plot(values[:,0],values[:,1])
np.savetxt("number_vacc_curve.txt", curve, fmt="%s")
np.savetxt("number_vacc_linear.txt", lin, fmt="%s")






t = 0.5
curve = np.loadtxt("number_vacc_curve.txt")
linear = np.loadtxt("number_vacc_linear.txt")

values =  np.transpose(np.vstack([t*curve[:,0] + (1-t)*linear[:,0], t*curve[:,1]+(1-t)*linear[:,1]]))

values = values[values[:,0]<=1,:]
    


x = np.linspace(0,1,100)
lin = 90*(1-x)+10
f = 10/np.sqrt(x)
plt.plot(x,f)
plt.plot(x,lin)
plt.plot(values[:,0],values[:,1])






#######
# This section is now looking at the curve for the proportion vaccinated based on the difference in MAP

# the MAP of the worst vaccine will initially have a sqrt function for the maximum number vaccinated
x = np.linspace(0,1,100)
#lin = 90*(1-x)+10
lin = 1/2*x+1/2
curve = -1 + np.exp(x*np.log(2))
perp = -2*x+1

plt.plot(x,lin)
plt.plot(x,curve)
#plt.plot(x,perp)




curve = np.zeros([200,2])
lin = np.zeros([200,2])
k=0

r = np.linspace(-4,-1,200)
for i in range(200):

    plt.plot(x,-2*x+1+r[i],alpha=0.4)
    
    
    curve[k,0] = optimize.root(lambda x: -1 + np.exp(x*np.log(2)) - -2*x+1+r[i], 0.01).x
    lin[k,0] = optimize.root(lambda x: 1/2*x+1/2 - -2*x+1+r[i], 0.01).x
    
    curve[k,1] = -1 + np.exp(curve[k,0]*np.log(2))   
    lin[k,1] = 1/2*lin[k,0]+1/2
    
    k=k+1

plt.plot(curve[:,0],curve[:,1],'.')
plt.plot(lin[:,0],lin[:,1],'.')





np.savetxt("prop_vacc_curve.txt", curve, fmt="%s")
np.savetxt("prop_vacc_linear.txt", lin, fmt="%s")








######
t = 0.7
curve = np.loadtxt("prop_vacc_curve.txt")
linear = np.loadtxt("prop_vacc_linear.txt")

values =  np.transpose(np.vstack([t*curve[:,0] + (1-t)*linear[:,0], t*curve[:,1] + (1-t)*linear[:,1]]))

values = values[values[:,0]>=0,:]
    

x = np.linspace(0,1,100)
lin = 1/2*x+1/2
curve = -1 + np.exp(x*np.log(2))
plt.plot(x,curve)
plt.plot(x,lin)
plt.plot(values[:,0],values[:,1])



###
t = 0.7
curve = np.loadtxt("number_vacc_curve.txt")
linear = np.loadtxt("number_vacc_linear.txt")

values =  np.transpose(np.vstack([t*curve[:,0] + (1-t)*linear[:,0], t*curve[:,1] + (1-t)*linear[:,1]]))

values = values[values[:,0]<1,:]
    

x = np.linspace(0,1,100)
lin = 90*(1-x)+10
curve = 10/(np.sqrt(x))
plt.plot(x,curve)
plt.plot(x,lin)
plt.plot(values[:,0],values[:,1])






