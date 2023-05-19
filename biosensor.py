#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 17:23:43 2023

@author: pablo
"""

import numpy as np
import pandas as pd
from doebase.OptDes import initGrid, CoordExch, MapDesign2

def remap(M):
    ix = np.where( (M == (0,0,0,0)).all(axis=1) )[0]
    if ix.size > 0:
        v = M[ix[0]]
        M[ix[0]] = M[0]
        M[0] = v
    else:
        for i in np.arange(0,M.shape[1]):
            v = M[0,i]
            M[ M[:,i] == v, i ] = -1
            M[ M[:,i] == 0, i ] = v
            M[ M[:,i] == -1, i ] = 0
    return M

n = 32
factors = [ {'M0','M1','M2','M3'}, 
           {'S0','S1','S2','S3'}, 
           {'P0','P1','P2','P3','P4'}, 
           {'R0','R1','R2','R3','R4'} ]
initGrid(factors)
M , J = CoordExch(factors, n, runs=1000, seed=10)
# Remap to Context 0
M = remap(M)
D = MapDesign2( factors, M )
print(D)
df = pd.DataFrame(D, columns = ['Media','Substrate','Promoter','RBS'])
df.to_csv('design.csv', index=False)
