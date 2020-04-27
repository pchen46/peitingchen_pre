#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 23:34:42 2020

@author: chenpeiting
"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#2.Read 'com.csv'
com = pd.read_csv('com.csv')

#3 Count the number of committees supporting or opposing Trump and Clinton

obj = com['support_oppose_indicator']=='O'
sup = com['support_oppose_indicator']=='S'
clinton = com['cand_id']=='P00003392'
trump = com['cand_id']=='P80001571'

vars=[obj,sup]
for v in vars:
    print(com[v]['candidate_name'].value_counts())

plt.figure(dpi=300,figsize=(10,8))
sns.catplot(x='candidate_name',kind='count',data=com,hue='support_oppose_indicator')

#4. Count the total investment values of committees to support or oppose Trump and Clinton:
for v in vars:
    print('clinton:',round(com[v&clinton]['total_y'].sum(),2))
    print('trump:',round(com[v&trump]['total_y'].sum(),2))
sns.barplot(hue='candidate_name',y='total_y',data=com,x='support_oppose_indicator',estimator=sum)
