#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 19 14:43:02 2023

@author: pablo

Augment DoE using Fisher matrix.
"""

import itertools
import numpy as np
import random
import pandas as pd
from doebase.OptDes import Deff, Deff2

def design(n = 32):
    factors = [ ['M0','M1','M2','M3'], 
               ['S0','S1','S2','S3'], 
               ['P1','P2','P3','P4'], 
               ['R1','R2','R3','R4','R5'] ]
    
    forbid = set( [('P2','R1'), ('P4','R3'), ('P4','R5'), ('P4','R1')] )
    forbid2 = set( [(1,0), (3,2), (3,4), (3,0)] )
    df1 = pd.read_csv('../../data/Biosensors_DoE/design91.csv')
    d1 = set()
    for i in df1.index:
        d1.add(tuple(df1.iloc[i]))
    
    m = itertools.product(*factors)
    A = np.empty((0,4))
    for i in m:
        t = (i[2],i[3])
        if t not in forbid and i not in d1:
            A = np.append(A,np.array([i]), axis=0)
    seq = np.arange(A.shape[0])
    ix = random.sample(list(seq),n)
    D = A[ix,:]
    df = pd.DataFrame(D)
    X = pd.get_dummies(df.append(df1))
    try:
        d = Deff(X)
    except:
        pass
    return (D,d)
    

n = 32
eff = 0
Do = []
for i in np.arange(10000):
    D, d = design(n)
    if d  > eff:
        print(d)
        eff = d
        Do = D
df1 = pd.read_csv('../../data/Biosensors_DoE/design91.csv')
pd.DataFrame(D,columns=df1.columns).to_csv('../../data/Biosensors_DoE/augdesign91.csv')
    


    

