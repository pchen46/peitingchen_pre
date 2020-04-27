#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 00:08:15 2020

@author: chenpeiting
"""


import requests
import pandas as pd
import numpy as np

#get ACS data
var_name=['B10010_001E',"B02001_001E","B02001_002E","B02001_003E",'B06009_005E','B06009_006E']
var_list = ['NAME']+var_name
var_string=','.join(var_list)

api='https://api.census.gov/data/2016/acs/acs5?&for=state:*'
key_value = 'cfe40bdafb447b960f55c11ee93e39c5c7aaa4f7'

payload = {'get':var_string, 'key':key_value}
response = requests.get(api, payload)
if response.status_code == 200:
    print('request succeeded')
else:
    assert False
    
row_list=response.json()
colnames = row_list[0]
datarows = row_list[1:]
results = pd.DataFrame(columns = colnames, data=datarows)

newnames={'B10010_001E':'income',
          "B02001_001E":'total_pop',
          "B02001_002E":'white_pop',
          "B02001_003E":'black_pop',
          'B06009_005E':'Bachelor Degree',
          'B06009_006E':'Graduate Degree',
          'zip code tabulation area':'zip_code'}
results.rename(newnames,axis='columns',inplace=True)
results.to_csv('census_by_state.csv')

#merge with 'by_state_cand.csv'
y1=pd.read_csv('by_state_cand.csv',dtype=str)
results[['income','total_pop','white_pop','black_pop','Bachelor Degree','Graduate Degree']]=results[['income','total_pop','white_pop','black_pop','Bachelor Degree','Graduate Degree']].astype(float)
merge1=y1.merge(results,how='left',validate='m:1',left_on="Name",right_on='NAME')

merge1[['Hillary_conP_S',
       'Trump_conP_S', 'Hillary_conG_S', 'Trump_conG_S', 'Hillary_conP_S.1',
       'Trump_conP_S.1', 'Hillary_conG_O', 'Trump_conG_O', 'Hillary_conP_O',
       'Trump_conP_O','income', 'total_pop',
       'white_pop', 'black_pop', 'Bachelor Degree', 'Graduate Degree']]=merge1[['Hillary_conP_S',
       'Trump_conP_S', 'Hillary_conG_S', 'Trump_conG_S', 'Hillary_conP_S.1',
       'Trump_conP_S.1', 'Hillary_conG_O', 'Trump_conG_O', 'Hillary_conP_O',
       'Trump_conP_O','income', 'total_pop',
       'white_pop', 'black_pop', 'Bachelor Degree', 'Graduate Degree']].astype(float)

merge1['H/T_GO']=np.log(merge1['Hillary_conG_O']/merge1['Trump_conG_O'])
merge1['H/T_GS']=np.log(merge1['Hillary_conG_S']/merge1['Trump_conG_S'])
merge1['H/T_PO']=np.log(merge1['Hillary_conP_O']/merge1['Trump_conP_O'])
merge1['H/T_PS']=np.log(merge1['Hillary_conP_S']/merge1['Trump_conP_S'])

merge1['H/T_G']=np.log(merge1['H/T_GS']/merge1['H/T_GO'])
merge1['H/T_P']=np.log(merge1['H/T_PS']/merge1['H/T_PO'])

merge1['H']=np.log((merge1['Hillary_conG_O']/merge1['Hillary_conG_S'])/(merge1['Hillary_conP_O']/merge1['Hillary_conP_S']))
merge1['T']=np.log((merge1['Trump_conG_O']/merge1['Trump_conG_S'])/(merge1['Trump_conP_O']/merge1['Trump_conP_S']))

merge1['H/T']=np.log(merge1['H']/merge1['T'])

merge1['>c']=(merge1['Bachelor Degree']+ merge1['Graduate Degree'])/merge1['total_pop']

merge1.to_csv('results.csv')



