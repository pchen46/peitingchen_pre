#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 23:27:00 2020

@author: chenpeiting
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#2 Read 'individual_contribution.csv'
contrib=pd.read_csv('individual_contribution.csv',dtype=str)
dropvars=['memo_cd','memo_text','image_num','other_id','amndt_ind','rpt_tp','name','other_id','tran_id','file_num']
contrib.drop(dropvars,axis=1,inplace=True)


#4. Read 'by_candidate_committe.csv':
com = pd.read_csv('by_candidate_committe.csv',dtype=str)
clinton = com['cand_id']=='P00003392'
trump = com['cand_id']=='P80001571'
com=com[trump | clinton]
com['candidate_name']=com['candidate_name'].str.replace('CLINTON, HILLARY RODHAM / TIMOTHY MICHAEL KAINE','Hillary')
com['candidate_name']=com['candidate_name'].str.replace('TRUMP, DONALD J. / MICHAEL R. PENCE ','Trump')

#7. remove the duplicated rows and aggregate its values
obj = com['support_oppose_indicator']=='O'
sup = com['support_oppose_indicator']=='S'
com['total']=com['total'].astype(float)

com_O = com[obj]
com_O1=com_O.groupby('cmte_id').agg({'total':sum,'count':sum})
com_O = com_O.merge(com_O1,on='cmte_id',how='left',validate='m:1',indicator=True)
com_O = com_O[~com_O['cmte_id'].duplicated()]
com_O.drop(['total_x','_merge','count_x'],axis = 1, inplace=True)

com_S = com[sup]
com_S1=com_S.groupby('cmte_id').agg({'total':sum,'count':sum})
com_S = com_S.merge(com_S1,on='cmte_id',how='left',validate='m:1',indicator=True)
com_S = com_S[~com_S['cmte_id'].duplicated()]
com_S.drop(['total_x','_merge','count_x'],axis = 1, inplace=True)

com=pd.concat([com_O,com_S])
com.reset_index(drop=True, inplace=True)

#8. save dataset:
contrib.to_pickle('contrib_all.pkl')
com.to_csv('com.csv')


