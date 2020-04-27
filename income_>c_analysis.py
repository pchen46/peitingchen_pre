#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 00:20:37 2020

@author: chenpeiting
"""


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

merge1 = pd.read_csv('results.csv')

mm=[]
mm.append(merge1[abs(merge1['H/T_GO'])<5])
mm.append(merge1[abs(merge1['H/T_GS'])<5])
mm.append(merge1[abs(merge1['H/T_PO'])<5])
mm.append(merge1[abs(merge1['H/T_PS'])<5])

plt.figure()
jg = sns.jointplot('H/T_GO','income',data=mm[0],kind="hex" )
jg = sns.jointplot('H/T_GO','>c',data=mm[0],kind="reg" )

jg = sns.jointplot('H/T_GS','income',data=mm[1],kind="kde" )
jg = sns.jointplot('H/T_GS','>c',data=mm[1],kind="kde" )

jg = sns.jointplot('H/T_PO','income',data=mm[2],kind="hex" )
jg = sns.jointplot('H/T_PO','>c',data=mm[2],kind="reg" )

jg = sns.jointplot('H/T_PS','income',data=mm[3],kind="hex" )
jg = sns.jointplot('H/T_PS','>c',data=mm[3],kind="reg" )

mm2=[]
mm2.append(merge1[abs(merge1['H/T_G'])<10])
mm2.append(merge1[abs(merge1['H/T_P'])<10])

jg = sns.jointplot('H/T_G','income',data=mm2[0],kind="kde" )
jg = sns.jointplot('H/T_G','>c',data=mm2[0],kind="kde" )

jg = sns.jointplot('H/T_P','income',data=mm2[1],kind="reg" )
jg = sns.jointplot('H/T_P','>c',data=mm2[1],kind="reg" )





mm3=[]
mm3.append(merge1[abs(merge1['H'])<10])
mm3.append(merge1[abs(merge1['T'])<10])

jg = sns.jointplot('H','income',data=mm3[0],kind="reg" )
jg = sns.jointplot('H','>c',data=mm3[0],kind="reg" )

jg = sns.jointplot('T','income',data=mm3[1],kind="reg" )
jg = sns.jointplot('T','>c',data=mm3[1],kind="reg" )

jg = sns.jointplot('H/T','income',data=merge1,kind="reg" )
jg = sns.jointplot('H/T','>c',data=merge1,kind="reg" )
