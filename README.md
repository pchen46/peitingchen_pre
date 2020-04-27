#Presentation: The condition of individual contribution of 2016 US Presidential Election

### Summary:
  This Presentation focuses on how much 2 candidates of 2016 Election get from individual contributions,Hillary and Trum, and how the condition change from Primary election to General election.

### Input Data:
  1. **individual_contribution.csv** : downloaded from Federal Election Commission-https://www.fec.gov/data/browse-data/?tab=bulk-data-'contribution by individuals'-'2015-2016'.
  2. **by_candidate_committe.csv** : download **weball16**, and **ccl.txt** from Federal Election Commission website.**weball16** is the candidate lists of 2016 Election, where Hillary's and Trump's CMTE_ID are gotten.**ccl.txt** is a file of the cnadidate-committe linkage which includes opposing and supporting indicator.
  3. 2016 ACS data by state: obtained via its API.
  4. **tl_2016_us_state.zip** : downloaded from Tiger shapfile website.

### Files:
  1. **data_clean.py**
  2. **counts_cm_ic.py**
  3. **period_cand_ACS_dataset.py**
  4. **D. period_cand_ACS_dataset.py**
  5. **ic_state.qgz**
  6. **income_>c_analysis.py**

###Instructions:
  **A. data_clean.py**
  1. Import packages:
          pandas
  2. Read 'individual_contribution.csv':
          set 'contrib' to the result of calling `pd.read_csv()`
          3. drop some colomns:
            set 'dropvars' to a list.
            apply the `drop()` to 'contrib' with 2 arguments.
  4. Read 'by_candidate_committe.csv':
          set 'com' to the result of calling 'pd.read_csv()'
          make 'total' numeric by applying `.astype(float)` to it.
          5. Filter committe with 2 candidates:
              set 'com' to its subset where 'com['cand_id']=='P00003392' or 'com['cand_id']=='P80001571'
          6. simplify the contents in fields:
                  apply the `str.replace()` to 'com['candidate_name']' with 'Hillary' and 'Trump'.
  7. remove the duplicated rows on ('CMTE_ID','support_oppose_indicator') and aggregate its values on ('total' and 'count'):
          1)set 'obj' to 'com['support_oppose_indicator']=='O'' ,
            set 'sup' to 'com['support_oppose_indicator']=='S''
            set 'com_O' to 'com[obj]' and set com_S to 'com[sup]'
          2)set `groupby()` with 'cmte_id' and apply `agg()` with argument of '{'total':sum,'count':sum}' to get new dataframe 'com_O1' and 'com_S1'.
          3)set 'com_O' to `com_O.merge()`with arguments of 'com_O1' and'on='cmte_id',how='left'', as well as 'com_S'.
          4)remove the duplicated rows
            set 'com_O' to '~com_O['cmte_id'].duplicated()]' as well as 'com_S'.
          5) get new 'com' variable:
            set 'com' by calling `pd.concat()` to joint 'com_O' and 'com_S'.
            apply `reset_index()`.
          6)modify the columns:
            apply `drop()` to drop the column of 'total_x' and '-merge'.
            apply `rename()` to rename the column of 'total_y' with 'total'
  8. save dataset:
          1) call `.to_pickle()` method to save 'contrib.pkl'
          2) call `.to_csv()` method to save 'com.csv'

   **B. counts_cm.py**     
  1. Import packages:
          pands, numpy, seaborn, matplotlib.pyplot
  2. Read 'com.csv':set 'com' to the result of calling `pd.read_csv()`
  3. Count the number of committees supporting or opposing Trump and Clinton:
          1)set 'obj' to 'com['support_oppose_indicator']=='O''
            set 'sup' to 'com['support_oppose_indicator']=='S''
            set 'clinton' to 'clinton = 'com['cand_id']=='P00003392''
            set 'trump' to 'com['cand_id']=='P80001571''
          2)count the number:
          Create a for-loop over `[obj,sup]` using `v` as the running variabl:
              apply `value_counts()` to 'com[v]['candidate_name']' and apply `print()` to them.
          3)plot the results to barplot:
          apply  `plt.figure(dpi=300,figsize=(10,8))` and  `sns.catplot()` with arguments of `x='candidate_name',kind='count',data=com,hue='support_oppose_indicator'`
  4. Count the total investment values of committees to support or oppose Trump and Clinton:
          1)count the number:
          Create a for-loop over `[obj,sup]` using `v` as the running variabl:
              apply `sum()` to 'com[v&clinton]' and call `print()` method to print it.
              apply `sum()` to 'com[v&trump]' and call `print()` method to print it.
          2)plot the results to barplot:
          apply  `plt.figure(dpi=300,figsize=(10,8))` and  `sns.barplot()` with arguments of `hue='candidate_name',y='total',data=com,x='support_oppose_indicator',estimator=sum`.

  **C. counts_ic.py**     
  1. Import packages:
          pands, numpy, seaborn, matplotlib.pyplot
  2. Read 'contrib.pkl':set 'contrib' to the result of calling `pd.read_pickle()`
     Read 'com.csv': set 'com' to the result of calling `pd.read_csv()`, and get com_O and com_S as above.
  3. Count individual contributions in the primary/General period\n
            1)set 'Pri' to 'contrib['transaction_pgi']=='P''
              set 'Gen' to 'contrib['transaction_pgi']=='G''\n
            2)set 'cPG' to 'contrib[Pri|Gen]'\n
            3)merge the 'cPG' and com_O/com_S
              set 'cPG' to `cPG.merge()`with arguments of 'com_O' and'on='cmte_id',how='left''.
              apply the `drop()` to 'cPG' with arguments:'['candidate_id', 'committee_id','candidate_name', 'committee_name']'.
              set 'cPG' to `cPG.merge()`with arguments of 'com_S' and'on='cmte_id',how='left''.\n
            4)filter data where individual contributes to the Hillary and Trump related committees:
                set 'merO' to 'cPG['-merge']=='both'' ,
                set 'merS' to 'cPG['mergeS']=='both''
                set 'cPG' to 'cPG[merO|merS]'\n
            5) set more conditions:
                set 's1' to 'merO'
                set 's2' to 'merS'
                set 's3' to 'cPG['candidate_name']=='Trump''
                set 's4' to 'cPG['candidate_name']=='Hillary''
                set s5 to 'cPG['transaction_pgi']=='P''
                set s6 to 'cPG['transaction_pgi']=='G''\n
            6) set a colomn named 'side' and know where the contributions goes, the values are 'T'-'support Trump', 'H'-'oppose Hillary','B_T'-'support and oppose Trump','B_H'-'support and oppose Hillary':
              Set 'cPG['side']' to'N'.
              In the sequence, apply`loc()` with argument conditions and the colomn name 'side'\n
            7) remove the rows where the values of 'side' is 'N'\n
            8) apply `value_counts()` to 'cPG['side']'\n
            9)count the sum values of individual conributions by Primary/General period:
                apply`astype(float)` on 'transaction_amt' column and  `groupby()` by '['side','transaction_pgi']' , getting dataframe gg.
                apply `sum()` with argument of 'transaction_amt' and get dataframe gg2.
                apply  `unstack()` to get new dataframe gg3.\n
            10)print the results.\n
    4. create 4 new dataframe on different period and different conditions on 'support or oppose'
            1) set `conP` to 'contrib[Pri]'
               set `conG` to 'contrib[Gen]'
            2) merge `conP`(and `conG`) with `com_S` and `com_O` to get 4 new dataframe `conG_S`,`conP_S`,`conG_O`,`conP_O`.
    5. anlaysis
            1) create 3 lists for the following for-loops:
                set 'v2' to '[conG_S,conP_S,conG_O,conP_O]'
                set 'v3' to '['P00003392','P80001571']'
                set 'v4' to '['conG_S','conP_S','conG_O','conP_O']'\n
            2) create a 'v41' list for the names of pictures:
               Create a for-loop over `range(0,4)` using `i` as the running variabl:
               Create a for-loop over `range(0,2)` using `s` as the running variabl:
                apply `append()` with argument of 'v4[i]+v3[s]+'.png'' to 'v41'.\n
            3)anlaysis and plot:
                set 'l' to 0,
                Create a for-loop over `v2` using `v` as the running variabl:
                Create a for-loop over `v3` using `t` as the running variabl:
                set `p` to `plt.figure()`
                print the name of `v41[l]`\n
                a)count the 15 committees with the largest number of individual contributions:
                apply `value_counts()` to 'v[v['cand_id']==t]['committee_name']' , set it to `m` and apply `print()` it.\n
                b)plot the barplot of the results and save it
                apply `sns.barplot()` with arguments of `y = m.index,x=m`, `get.figure()` and `savefig` with argument of 'v41[l]'.
                c)get the total amount of individual donations\n
                apply `sum()` to 'v[v['cand_id']==t]['transaction_amt']' and call `print()` method to print it.\n
    6.  get grouped dataset by stages and conditions(support or oppose)
            input: 'v2'
            method: `for-loop`: `groupby()`, `sum()`, `unstack()`
            output: 'ttempt2', a 4-size list with 2 colomns of contributions to Hillary and Trump, the index is state.
    7.   get summary dataset by stages and conditions(support or oppose)
            input: 'ttempt2','po'(gotten by read 'pocodes.csv')
            method: `merge()`,`copy()`,`drop()`
            output: 'po'
    8. save the 'po' dataset by call `.to_csv()` with argument 'by_state_cand.csv'.

    **D. period_cand_ACS_dataset.py**
    1. import packages:
            requests and pandas
    2. set 'var_name' to the variables to analyze, '['NAME']+['B10010_001E',"B02001_001E","B02001_002E","B02001_003E",'B06009_005E','B06009_006E']' and call `','.join()` to 'var_name', getting 'var_string'
    3. get 'api' from the ACS website, notice the for should be changed to 'state:* '
    4. get 'key_value' and 'payload' which is a dictionary,' {'get':var_string, 'key':key_value}'
    5. get the data
          input: 'api', 'payload'
          method: `requests.get()`
          output:'response',
    6. save it to a dataframe
          Input:'response'
          method1:`.json()`
          output:'row_list','colnames'(row_list[0]),'datarows'(row_list[1:])
          method2:`pd.DataFrame()`with arguments 'columns = colnames, data=datarows'
          output: 'results'
    7. rename the colomns and save the 'results' to 'census_by_state.csv'.
    8. read 'by_state_cand.csv' and set it to 'y1'.
    9. merge 'y1' and 'results' and get the final 'merge1'
    10. calculate columns in 'merge':
        'income' : 'income';
        '>c' :('Bachelor Degree'+'Graduate Degree')/'total_pop'
        'H/T_GO'='Hillary_conG_O'/'Trump_conG_O'
        'H/T_GS'='Hillary_conG_S'/'Trump_conG_S'
        'H/T_PO'='Hillary_conP_O'/'Trump_conP_O'
        'H/T_PS'='Hillary_conG_S'/'Trump_conG_S'
        'H/T_G'='H/T_GO'/'H/T_GS'
        'H/T_P'='H/T_PO'/'H/T_PS'
        'H'=('Hillary_conG_O'/'Hillary_conG_S')/('Hillary_conP_O'/'Hillary_conP_S])
        'T'=('Trump_conG_O'/'Trump_conG_S')/('Trump_conP_O'/'Trump_conP_S])
        'H/T'='H'/'T'
    11. save it to the 'results.csv'


    **E. ic_state.qgz**
    1. add the layor of 'tl_2016_us_state.zip' and choose the 'shp' one.
    2. add the deliminated text layor of 'results.csv'
    3. join them on state 'Name' and 'NAME'.
    4. select 'Graduated' in layor styling of ['H/T_GO', 'H/T_GS', 'H/T_PO', 'H/T_PS', 'H/T_G', 'H/T_P', 'H', 'T','H/T'] values.
    5. export pictures.

    **F. income_>c_analysis.py**
    1. import packages:
      pandas, numpy, seaborn, matplotlib.pyplot
    2. read 'results.csv' to 'merge1'
    3. call `np.log()` to ['H/T_GO', 'H/T_GS', 'H/T_PO', 'H/T_PS', 'H/T_G', 'H/T_P', 'H', 'T','H/T']
    4. call `sns.jointplot()`
        argument:
        1) x=['H/T_GO', 'H/T_GS', 'H/T_PO', 'H/T_PS', 'H/T_G', 'H/T_P', 'H', 'T','H/T'] (in sequnce, not a list)
        2) y=['income','>c'] (in sequnce, not a list)
        3) data =merge (filter the abs of values < 5)
        4) kind = 'reg','hex'or'kde'
         save pictures
