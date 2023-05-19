#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 17:23:43 2023

@author: pablo

Code to generate the DoE for the biosensor
"""

import numpy as np
import pandas as pd
from doebase.OptDes import initGrid, CoordExch, MapDesign2, Deff2

def remap(M, ref=(0,0,0,3)):
    ix = np.where( (M == ref).all(axis=1) )[0]
    if ix.size > 0:
        v = M[ix[0]]
        M[ix[0]] = M[0]
        M[0] = v
    else:
        for i in np.arange(0,M.shape[1]):
            y = ref[i]
            v = M[0,i]
            M[ M[:,i] == v, i ] = -1
            M[ M[:,i] == y, i ] = v
            M[ M[:,i] == -1, i ] = y
    return M

n = 32
factors = [ {'M0','M1','M2','M3'}, 
           {'S0','S1','S2','S3'}, 
           {'P1','P2','P3','P4'}, 
           {'R1','R2','R3','R4','R5'} ]

forbid = set( [('P2','R1'), ('P4','R3'), ('P4','R5'), ('P4','R1')] )
forbid2 = set( [(1,0), (3,2), (3,4), (3,0)] )
allow = []
for i in np.arange(4):
    for j in np.arange(5):
        if (i,j) not in forbid2:
            allow.append( (i,j) )
initGrid(factors)
M , J = CoordExch(factors, n, runs=10, seed=10)
# Remap to Context 0
M = remap(M)
print(Deff2(M, factors))
jj = set()
for i in np.arange(M.shape[0]):
    if (M[i,2],M[i,3]) in forbid2:
        j = np.random.choice(np.arange(len(allow)))
        M[i,2] = allow[j][0]
        M[i,3] = allow[j][1]        
        del allow[j]
print(Deff2(M, factors))

D = MapDesign2( factors, M )
#print(D)
found = set()
for row in D:
    pair = row[2:4]
    found.add(tuple(pair))


for row in D:
    for pair in forbid:
        if row[2] == pair[0] and row[3] == pair[1]:
            print(row)
df = pd.DataFrame(D, columns = ['Media','Substrate','Promoter','RBS'])
df.to_csv('design.csv', index=False)
