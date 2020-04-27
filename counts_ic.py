#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 23:40:47 2020

@author: chenpeiting
"""


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#2. Read 'contrib.pkl' and 'com.csv'
com = pd.read_csv('com.csv')
contrib=pd.read_pickle('contrib_all.pkl')

obj = com['support_oppose_indicator']=='O'
sup = com['support_oppose_indicator']=='S'
com_O = com[obj]
com_S = com[sup]


#3. Count individual contributions in the primary/General period
Pri = contrib['transaction_pgi']=='P'
Gen = contrib['transaction_pgi']=='G'
cPG=contrib[Pri|Gen]

cPG=cPG.merge(com_O,on='cmte_id',how='left',validate='m:1',indicator=True)
cPG.drop(['candidate_id', 'committee_id','candidate_name', 'committee_name'],axis = 1, inplace=True)
cPG=cPG.merge(com_S,on='cmte_id',how='left',validate='m:1',indicator='mergeS')

merO=cPG['_merge']=='both'
merS=cPG['mergeS']=='both'
cPG = cPG[merO|merS]

s1=(cPG['_merge']=='both')
s2=(cPG['mergeS']=='both') 
s3=(cPG['candidate_name']=='Trump')
s4=(cPG['candidate_name']=='Hillary')
s5=(cPG['transaction_pgi']=='P')
s6=(cPG['transaction_pgi']=='G')

cPG['side']='N'

cPG.loc[s1&s4,'side']='T'
cPG.loc[s2&s3,'side']='T'
cPG.loc[s2&s4,'side']='H'
cPG.loc[s1&s3,'side']='H'
cPG.loc[s1&s2&s3,'side']='B_T'
cPG.loc[s6&s1&s2&s3,'side']='BG_T'
cPG.loc[s1&s2&s4,'side']='B_H'
cPG.loc[s6&s1&s2&s4,'side']='BG_H'

cPG['side'].value_counts()
cPG=cPG[cPG['side']!='N']

gg = cPG.groupby(['side','transaction_pgi'])
cPG['transaction_amt'] = cPG['transaction_amt'].astype(float)
gg2 = gg['transaction_amt'].sum()
gg3 = gg2.unstack()
print(gg3)

#4. create 4 new dataframe on different period and different conditions on 'support or oppose'

conP = contrib[Pri]
conG = contrib[Gen]

contrib_PS = conP.merge(com_S,on='cmte_id',how='left',validate='m:1',indicator=True)
contrib_GS = conG.merge(com_S,on='cmte_id',how='left',validate='m:1',indicator=True)
conP_S = contrib_PS[contrib_PS['_merge']=='both']
conG_S = contrib_GS[contrib_GS['_merge']=='both']
conP_S.drop('_merge',axis = 1, inplace=True)
conG_S.drop('_merge',axis = 1, inplace=True)

contrib_GO = conP.merge(com_O,on='cmte_id',how='left',validate='m:1',indicator=True)
contrib_SO = conG.merge(com_O,on='cmte_id',how='left',validate='m:1',indicator=True)
conP_O = contrib_GO[contrib_GO['_merge']=='both']
conG_O = contrib_SO[contrib_SO['_merge']=='both']
conP_O.drop('_merge',axis = 1, inplace=True)
conG_O.drop('_merge',axis = 1, inplace=True)


#5. anlaysis

#1) create 3 lists for the following for-loops:
v2=[conG_S,conP_S,conG_O,conP_O]
v3=['P00003392','P80001571']
v4=['conG_S','conP_S','conG_O','conP_O']

#2) create a 'v41' list for the names of pictures:
v41=[]
l=0
for i in range(0,4):
    for s in range(0,2):
        v41.append(v4[i]+v3[s]+'.png')
        
#3)anlaysis and plot:
l=0        
for v in v2:
    for t in v3:
        p = plt.figure()
        print(v41[l])
        m = v[v['cand_id']==t]['committee_name'].value_counts()[:15]
        print(m)
       # sns.barplot(y = m.index,x=m).get_figure().savefig(v41[l])
        print(v[v['cand_id']==t]['transaction_amt'].astype(float).sum())
        l = l+1
l=0

#6.  get grouped dataset by stages and conditions(support or oppose)
ttemp2=[]

for i in range(0,4):
    v2[i]['transaction_amt']=v2[i]['transaction_amt'].astype(float)
    #v2[i]['zip_code']=v2[i]['zip_code'].str[0:5]
    #st = v4[i]+'group_by_zip'
    st2 = v4[i]+'group_by_state'
    #temp2.append(v2[i].groupby(['state','zip_code','candidate_name'])['transaction_amt'].sum().unstack())
    ttemp2.append(v2[i].groupby(['state','candidate_name'])['transaction_amt'].sum().unstack())

#7. get summary dataset by stages and conditions(support or oppose)

po = pd.read_csv('pocodes.csv')
l=0
for t in ttemp2:
    st ='_'+ v4[l]    
    po=po.merge(t,left_on='PO',right_on='state',how='outer',validate='m:1',indicator=False,suffixes=['',st2])
    l = l+1
l=0  

#8 save
po.to_csv('by_state_cand.csv')












