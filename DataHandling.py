#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 08:34:36 2018

@author: santhosh
"""
import os
import pandas as pd
import numpy as np

def conv(strng):
    sd = ""
    if(type(strng) != 'str'):
        strng = str(strng)
        for d in strng:
            if(',' not in str(d)):
                sd = sd+d
    return float(sd)

files = []
dataframes = []
mobile_list = []

for x in os.listdir('.'):
    if(os.path.isdir(x) and '.' not in x):
        files.append(x)  
        
counts = len(files)

for c in range(counts):
    dataframes.append('df_'+str(c))
    
for df,param in zip(dataframes,files):
    exec('{} = pd.DataFrame'.format(df))
    exec('{} = pd.read_csv("{}/{}.csv")'.format(df, param, param))
    exec('mobile_list.append({})'.format(df))

data = pd.DataFrame

data = pd.concat(mobile_list, ignore_index=True)
data = data.sort_values(by=['device_name'])
data.index = np.arange(1, len(data)+1)

data['price (INR)'] = data['price (INR)'].apply(conv)

data.to_csv('Mobilephones.csv')



