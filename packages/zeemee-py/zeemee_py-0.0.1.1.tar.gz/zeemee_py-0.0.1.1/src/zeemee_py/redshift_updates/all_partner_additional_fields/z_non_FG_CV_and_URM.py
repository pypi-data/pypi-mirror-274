def non_FG_CV_URM_function(master_df, master_df_filtered, not_in_community_df):
    import pandas as pd
    import numpy as np
    
    description = list()
    values = list()

    #-------- commitment_rate_in_comm_in_comm_prior_to_deposit_non_first_gen
    
    master_df_not_FG = master_df[master_df["ZM.First.Gen"] != "First Generation"].reset_index(drop = True)
    
    x12 = master_df_not_FG[(master_df_not_FG['ZM.Committed'] == 1)
                       & (master_df_not_FG['ZM.Community'] == 'Community') ]
    x13 = x12[
        (x12['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
        (x12['ZM.Joined.Stage'] == '02 INQUIRED') |
        (x12['ZM.Joined.Stage'] == '03 APPLIED') |
        (x12['ZM.Joined.Stage'] == '04 APP COMPLETE') |
        (x12['ZM.Joined.Stage'] == '05 ACCEPTED') ]
    
    x1 = len(x13)
    
    x22 = master_df_not_FG[(master_df_not_FG['ZM.Accepted'] == 1)
                   & (master_df_not_FG['ZM.Community'] == 'Community') ]
    x23 = x22[
        (x22['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
        (x22['ZM.Joined.Stage'] == '02 INQUIRED') |
        (x22['ZM.Joined.Stage'] == '03 APPLIED') |
        (x22['ZM.Joined.Stage'] == '04 APP COMPLETE') |
        (x22['ZM.Joined.Stage'] == '05 ACCEPTED') ]
    
    x2 = len(x23)
    
    if x2>0:
      description.append("commitment_rate_in_comm_in_comm_prior_to_deposit_non_first_gen")
      values.append(x1/x2)
    else: 
      description.append("commitment_rate_in_comm_in_comm_prior_to_deposit_non_first_gen")
      values.append("")
    
    #-----------------------
    
    #-----------------------
  
  
    master_df_not_FG_non_comm = master_df[(master_df["ZM.First.Gen"] != "First Generation") & (master_df_not_FG['ZM.Community'] != 'Community') ].reset_index(drop = True)
    
    if len(master_df_not_FG_non_comm[master_df_not_FG_non_comm['ZM.Accepted']== 1]) > 0:
            
        description.append("commitment_rate_never_in_community_non_first_gen")
        values.append(len(master_df_not_FG_non_comm[master_df_not_FG_non_comm['ZM.Committed']== 1])/
                 len(master_df_not_FG_non_comm[master_df_not_FG_non_comm['ZM.Accepted']== 1]))
                             
    else:
        description.append("commitment_rate_never_in_community_non_first_gen")
        values.append("")
    
    #-----------------------
    
    #-----------------------
    
  
    master_df_not_FG_comm = master_df[(master_df["ZM.First.Gen"] != "First Generation") & (master_df_not_FG['ZM.Community'] == 'Community') ].reset_index(drop = True)

    if len(master_df_not_FG_non_comm[master_df_not_FG_non_comm['ZM.Accepted']== 1]) > 0:
        
        description.append("yield_rate_in_community_regardless_of_join_stage_non_first_gen")
        values.append(len(master_df_not_FG_non_comm[master_df_not_FG_non_comm['ZM.Enrolled']== 1])/
                 len(master_df_not_FG_non_comm[master_df_not_FG_non_comm['ZM.Accepted']== 1]))
                 
    else:
        description.append("yield_rate_in_community_regardless_of_join_stage_non_first_gen")
        values.append("")
    
    #-----------------------
    
    #-----------------------
    
  
    master_df_not_FG_comm = master_df[(master_df["ZM.First.Gen"] != "First Generation") & (master_df_not_FG['ZM.Community'] == 'Community') ].reset_index(drop = True)
    
    x12 = master_df_not_FG[(master_df_not_FG['ZM.Enrolled'] == 1)
                       & (master_df_not_FG['ZM.Community'] == 'Community') ]
    x13 = x12[
        (x12['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
        (x12['ZM.Joined.Stage'] == '02 INQUIRED') |
        (x12['ZM.Joined.Stage'] == '03 APPLIED') |
        (x12['ZM.Joined.Stage'] == '04 APP COMPLETE') |
        (x12['ZM.Joined.Stage'] == '05 ACCEPTED') ]
    
    x1 = len(x13)
    
    x22 = master_df_not_FG[(master_df_not_FG['ZM.Accepted'] == 1)
                   & (master_df_not_FG['ZM.Community'] == 'Community') ]
    x23 = x22[
        (x22['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
        (x22['ZM.Joined.Stage'] == '02 INQUIRED') |
        (x22['ZM.Joined.Stage'] == '03 APPLIED') |
        (x22['ZM.Joined.Stage'] == '04 APP COMPLETE') |
        (x22['ZM.Joined.Stage'] == '05 ACCEPTED') ]
    
    x2 = len(x23)
    
    if x2>0:
      description.append("yield_rate_in_comm_in_comm_prior_to_deposit_non_first_gen")
      values.append((x1/x2))
    else: 
      description.append("yield_rate_in_comm_in_comm_prior_to_deposit_non_first_gen")
      values.append("")
    
    
    #-----------------------
    
    #-----------------------
    
  
    master_df_not_FG_comm = master_df[(master_df["ZM.First.Gen"] != "First Generation") & (master_df_not_FG['ZM.Community'] == 'Community') ].reset_index(drop = True)

    if len(master_df_not_FG_non_comm[master_df_not_FG_non_comm['ZM.Committed']== 1]) > 0:
        
        description.append("melt_rate_in_community_non_first_gen")
        values.append(1 - (len(master_df_not_FG_non_comm[master_df_not_FG_non_comm['ZM.Enrolled']== 1])/
                 len(master_df_not_FG_non_comm[master_df_not_FG_non_comm['ZM.Committed']== 1])))
                 
    else:
        description.append("melt_rate_in_community_non_first_gen")
        values.append("")
    
    #----------------------------------
    
    
    #----------------------------------
    #----------------------------------
    #----------------------------------
    #----------------------------------
    
    
    master_df_not_CV = master_df[master_df["ZM.CV.Flag"] != "Campus Visit"].reset_index(drop = True)
    
    x12 = master_df_not_CV[(master_df_not_CV['ZM.Committed'] == 1)
                       & (master_df_not_CV['ZM.Community'] == 'Community') ]
    x13 = x12[
        (x12['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
        (x12['ZM.Joined.Stage'] == '02 INQUIRED') |
        (x12['ZM.Joined.Stage'] == '03 APPLIED') |
        (x12['ZM.Joined.Stage'] == '04 APP COMPLETE') |
        (x12['ZM.Joined.Stage'] == '05 ACCEPTED') ]
    
    x1 = len(x13)
    
    x22 = master_df_not_CV[(master_df_not_CV['ZM.Accepted'] == 1)
                   & (master_df_not_CV['ZM.Community'] == 'Community') ]
    x23 = x22[
        (x22['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
        (x22['ZM.Joined.Stage'] == '02 INQUIRED') |
        (x22['ZM.Joined.Stage'] == '03 APPLIED') |
        (x22['ZM.Joined.Stage'] == '04 APP COMPLETE') |
        (x22['ZM.Joined.Stage'] == '05 ACCEPTED') ]
    
    x2 = len(x23)
    
    if x2>0:
      description.append("commitment_rate_in_comm_in_comm_prior_to_deposit_non_CV")
      values.append(x1/x2)
    else: 
      description.append("commitment_rate_in_comm_in_comm_prior_to_deposit_non_CV")
      values.append("")
    
    #-----------------------
    
    #-----------------------
    
  
    master_df_not_CV_non_comm = master_df[(master_df["ZM.CV.Flag"] != "Campus Visit") & (master_df_not_CV['ZM.Community'] != 'Community') ].reset_index(drop = True)
    
    if len(master_df_not_CV_non_comm[master_df_not_CV_non_comm['ZM.Accepted']== 1]) > 0:
            
        description.append("commitment_rate_never_in_community_non_CV")
        values.append(len(master_df_not_CV_non_comm[master_df_not_CV_non_comm['ZM.Committed']== 1])/
                 len(master_df_not_CV_non_comm[master_df_not_CV_non_comm['ZM.Accepted']== 1]))
                             
    else:
        description.append("commitment_rate_never_in_community_non_CV")
        values.append("")
    
    #-----------------------
    
    #-----------------------
    
  
    master_df_not_CV_comm = master_df[(master_df["ZM.CV.Flag"] != "Campus Visit") & (master_df_not_CV['ZM.Community'] == 'Community') ].reset_index(drop = True)

    if len(master_df_not_CV_non_comm[master_df_not_CV_non_comm['ZM.Accepted']== 1]) > 0:
        
        description.append("yield_rate_in_community_regardless_of_join_stage_non_CV")
        values.append(len(master_df_not_CV_non_comm[master_df_not_CV_non_comm['ZM.Enrolled']== 1])/
                 len(master_df_not_CV_non_comm[master_df_not_CV_non_comm['ZM.Accepted']== 1]))
                 
    else:
        description.append("yield_rate_in_community_regardless_of_join_stage_non_CV")
        values.append("")
    
    #-----------------------
    
    #-----------------------
    
  
    master_df_not_CV_comm = master_df[(master_df["ZM.CV.Flag"] != "Campus Visit") & (master_df_not_CV['ZM.Community'] == 'Community') ].reset_index(drop = True)
    
    x12 = master_df_not_CV[(master_df_not_CV['ZM.Enrolled'] == 1)
                       & (master_df_not_CV['ZM.Community'] == 'Community') ]
    x13 = x12[
        (x12['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
        (x12['ZM.Joined.Stage'] == '02 INQUIRED') |
        (x12['ZM.Joined.Stage'] == '03 APPLIED') |
        (x12['ZM.Joined.Stage'] == '04 APP COMPLETE') |
        (x12['ZM.Joined.Stage'] == '05 ACCEPTED') ]
    
    x1 = len(x13)
    
    x22 = master_df_not_CV[(master_df_not_CV['ZM.Accepted'] == 1)
                   & (master_df_not_CV['ZM.Community'] == 'Community') ]
    x23 = x22[
        (x22['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
        (x22['ZM.Joined.Stage'] == '02 INQUIRED') |
        (x22['ZM.Joined.Stage'] == '03 APPLIED') |
        (x22['ZM.Joined.Stage'] == '04 APP COMPLETE') |
        (x22['ZM.Joined.Stage'] == '05 ACCEPTED') ]
    
    x2 = len(x23)
    
    if x2>0:
      description.append("yield_rate_in_comm_in_comm_prior_to_deposit_non_CV")
      values.append((x1/x2))
    else: 
      description.append("yield_rate_in_comm_in_comm_prior_to_deposit_non_CV")
      values.append("")
    
    
    #-----------------------
    
    #-----------------------
    
  
    master_df_not_CV_comm = master_df[(master_df["ZM.CV.Flag"] != "Campus Visit") & (master_df_not_CV['ZM.Community'] == 'Community') ].reset_index(drop = True)

    if len(master_df_not_CV_non_comm[master_df_not_CV_non_comm['ZM.Committed']== 1]) > 0:
        
        description.append("melt_rate_in_community_non_CV")
        values.append(1 - (len(master_df_not_CV_non_comm[master_df_not_CV_non_comm['ZM.Enrolled']== 1])/
                 len(master_df_not_CV_non_comm[master_df_not_CV_non_comm['ZM.Committed']== 1])))
                 
    else:
        description.append("melt_rate_in_community_non_CV")
        values.append("")
    
    #----------------------------------
    #----------------------------------
    #----------------------------------
    #----------------------------------
    #----------------------------------
    
    
    master_df_not_URM = master_df[(master_df['ZM.Race.Ethnicity'] != 'Asian') &
                                          (master_df['ZM.Race.Ethnicity'] != 'American Indian or Alaska Native') &
                                          (master_df['ZM.Race.Ethnicity'] != 'American Indian or Alaskan Native') &
                                          (master_df['ZM.Race.Ethnicity'] != 'Black or African American') &
                                          (master_df['ZM.Race.Ethnicity'] != 'Hispanic of any race') &
                                          (master_df['ZM.Race.Ethnicity'] != 'Native Hawaiian or Other Pacific') &
                                          (master_df['ZM.Race.Ethnicity'] != 'Two or more races')].reset_index(drop = True)
    
    x12 = master_df_not_URM[(master_df_not_URM['ZM.Committed'] == 1)& (master_df_not_URM['ZM.Community'] == 'Community') ]
    x13 = x12[
        (x12['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
        (x12['ZM.Joined.Stage'] == '02 INQUIRED') |
        (x12['ZM.Joined.Stage'] == '03 APPLIED') |
        (x12['ZM.Joined.Stage'] == '04 APP COMPLETE') |
        (x12['ZM.Joined.Stage'] == '05 ACCEPTED') ]
    
    x1 = len(x13)
    
    x22 = master_df_not_URM[(master_df_not_URM['ZM.Accepted'] == 1)
                   & (master_df_not_URM['ZM.Community'] == 'Community') ]
    x23 = x22[
        (x22['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
        (x22['ZM.Joined.Stage'] == '02 INQUIRED') |
        (x22['ZM.Joined.Stage'] == '03 APPLIED') |
        (x22['ZM.Joined.Stage'] == '04 APP COMPLETE') |
        (x22['ZM.Joined.Stage'] == '05 ACCEPTED') ]
    
    x2 = len(x23)
    
    if x2>0:
      description.append("commitment_rate_in_comm_in_comm_prior_to_deposit_non_URM")
      values.append(x1/x2)
    else: 
      description.append("commitment_rate_in_comm_in_comm_prior_to_deposit_non_URM")
      values.append("")
    
    #-----------------------
    
    #-----------------------
    
  
    master_df_not_URM_non_comm = master_df[(master_df['ZM.Race.Ethnicity'] != 'Asian') &
                                          (master_df['ZM.Race.Ethnicity'] != 'American Indian or Alaska Native') &
                                          (master_df['ZM.Race.Ethnicity'] != 'American Indian or Alaskan Native') &
                                          (master_df['ZM.Race.Ethnicity'] != 'Black or African American') &
                                          (master_df['ZM.Race.Ethnicity'] != 'Hispanic of any race') &
                                          (master_df['ZM.Race.Ethnicity'] != 'Native Hawaiian or Other Pacific') &
                                          (master_df['ZM.Race.Ethnicity'] != 'Two or more races') & 
                                          (master_df['ZM.Community'] != 'Community') ].reset_index(drop = True)
    
    if len(master_df_not_URM_non_comm[master_df_not_URM_non_comm['ZM.Accepted']== 1]) > 0:
            
        description.append("commitment_rate_never_in_community_non_URM")
        values.append(len(master_df_not_URM_non_comm[master_df_not_URM_non_comm['ZM.Committed']== 1])/
                 len(master_df_not_URM_non_comm[master_df_not_URM_non_comm['ZM.Accepted']== 1]))
                             
    else:
        description.append("commitment_rate_never_in_community_non_URM")
        values.append("")
    
    #-----------------------
    
    #-----------------------
    
  
    master_df_not_URM_comm = master_df[(master_df['ZM.Race.Ethnicity'] != 'Asian') &
                                          (master_df['ZM.Race.Ethnicity'] != 'American Indian or Alaska Native') &
                                          (master_df['ZM.Race.Ethnicity'] != 'American Indian or Alaskan Native') &
                                          (master_df['ZM.Race.Ethnicity'] != 'Black or African American') &
                                          (master_df['ZM.Race.Ethnicity'] != 'Hispanic of any race') &
                                          (master_df['ZM.Race.Ethnicity'] != 'Native Hawaiian or Other Pacific') &
                                          (master_df['ZM.Race.Ethnicity'] != 'Two or more races') & 
                                          (master_df['ZM.Community'] == 'Community') ].reset_index(drop = True)

    if len(master_df_not_URM_non_comm[master_df_not_URM_non_comm['ZM.Accepted']== 1]) > 0:
        
        description.append("yield_rate_in_community_regardless_of_join_stage_non_URM")
        values.append(len(master_df_not_URM_non_comm[master_df_not_URM_non_comm['ZM.Enrolled']== 1])/
                 len(master_df_not_URM_non_comm[master_df_not_URM_non_comm['ZM.Accepted']== 1]))
                 
    else:
        description.append("yield_rate_in_community_regardless_of_join_stage_non_URM")
        values.append("")
    
    #-----------------------
    
    #-----------------------
    
  
    master_df_not_URM_comm = master_df[(master_df['ZM.Race.Ethnicity'] != 'Asian') &
                                          (master_df['ZM.Race.Ethnicity'] != 'American Indian or Alaska Native') &
                                          (master_df['ZM.Race.Ethnicity'] != 'American Indian or Alaskan Native') &
                                          (master_df['ZM.Race.Ethnicity'] != 'Black or African American') &
                                          (master_df['ZM.Race.Ethnicity'] != 'Hispanic of any race') &
                                          (master_df['ZM.Race.Ethnicity'] != 'Native Hawaiian or Other Pacific') &
                                          (master_df['ZM.Race.Ethnicity'] != 'Two or more races') & 
                                          (master_df['ZM.Community'] == 'Community') ].reset_index(drop = True)
    
    x12 = master_df_not_URM[(master_df_not_URM['ZM.Enrolled'] == 1)
                       & (master_df_not_URM['ZM.Community'] == 'Community') ]
    x13 = x12[
        (x12['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
        (x12['ZM.Joined.Stage'] == '02 INQUIRED') |
        (x12['ZM.Joined.Stage'] == '03 APPLIED') |
        (x12['ZM.Joined.Stage'] == '04 APP COMPLETE') |
        (x12['ZM.Joined.Stage'] == '05 ACCEPTED') ]
    
    x1 = len(x13)
    
    x22 = master_df_not_URM[(master_df_not_URM['ZM.Accepted'] == 1)
                   & (master_df_not_URM['ZM.Community'] == 'Community') ]
    x23 = x22[
        (x22['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
        (x22['ZM.Joined.Stage'] == '02 INQUIRED') |
        (x22['ZM.Joined.Stage'] == '03 APPLIED') |
        (x22['ZM.Joined.Stage'] == '04 APP COMPLETE') |
        (x22['ZM.Joined.Stage'] == '05 ACCEPTED') ]
    
    x2 = len(x23)
    
    if x2>0:
      description.append("yield_rate_in_comm_in_comm_prior_to_deposit_non_URM")
      values.append((x1/x2))
    else: 
      description.append("yield_rate_in_comm_in_comm_prior_to_deposit_non_URM")
      values.append("")
    
    
    #-----------------------
    
    #-----------------------
    
  
    master_df_not_CV_comm = master_df[(master_df['ZM.Race.Ethnicity'] != 'Asian') &
                                          (master_df['ZM.Race.Ethnicity'] != 'American Indian or Alaska Native') &
                                          (master_df['ZM.Race.Ethnicity'] != 'American Indian or Alaskan Native') &
                                          (master_df['ZM.Race.Ethnicity'] != 'Black or African American') &
                                          (master_df['ZM.Race.Ethnicity'] != 'Hispanic of any race') &
                                          (master_df['ZM.Race.Ethnicity'] != 'Native Hawaiian or Other Pacific') &
                                          (master_df['ZM.Race.Ethnicity'] != 'Two or more races') & 
                                          (master_df['ZM.Community'] == 'Community') ].reset_index(drop = True)

    if len(master_df_not_CV_non_comm[master_df_not_CV_non_comm['ZM.Committed']== 1]) > 0:
        
        description.append("melt_rate_in_community_non_URM")
        values.append(1 - (len(master_df_not_CV_non_comm[master_df_not_CV_non_comm['ZM.Enrolled']== 1])/
                 len(master_df_not_CV_non_comm[master_df_not_CV_non_comm['ZM.Committed']== 1])))
                 
    else:
        description.append("melt_rate_in_community_non_URM")
        values.append("")
        
    function_df = pd.DataFrame()
    for i in range(len(description)):
         function_df[description[i]] = [values[i]]
  
    return function_df



