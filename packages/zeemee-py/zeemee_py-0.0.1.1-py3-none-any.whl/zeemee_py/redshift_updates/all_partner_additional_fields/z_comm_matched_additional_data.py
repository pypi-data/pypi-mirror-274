def get_URM_race_related_df(master_df, master_df_filtered, not_in_community_df):
    import pandas as pd
    import numpy as np
    
    comm_matched_list = list()
    list_15_values = list()

    in_comm_URM_race_ethnicity = master_df_filtered[(master_df_filtered['ZM.Race.Ethnicity'] == 'Asian') |
                                          (master_df_filtered['ZM.Race.Ethnicity'] == 'American Indian or Alaska Native') |
                                          (master_df_filtered['ZM.Race.Ethnicity'] == 'American Indian or Alaskan Native') |
                                          (master_df_filtered['ZM.Race.Ethnicity'] == 'Black or African American') |
                                          (master_df_filtered['ZM.Race.Ethnicity'] == 'Hispanic of any race') |
                                          (master_df_filtered['ZM.Race.Ethnicity'] == 'Native Hawaiian or Other Pacific') |
                                          (master_df_filtered['ZM.Race.Ethnicity'] == 'Two or more races')] #in community already filtered

    not_in_comm_URM_race_ethnicity = not_in_community_df[(not_in_community_df['ZM.Race.Ethnicity'] == 'Asian') |
                                          (not_in_community_df['ZM.Race.Ethnicity'] == 'American Indian or Alaska Native') |
                                          (not_in_community_df['ZM.Race.Ethnicity'] == 'American Indian or Alaskan Native') |
                                          (not_in_community_df['ZM.Race.Ethnicity'] == 'Black or African American') |
                                          (not_in_community_df['ZM.Race.Ethnicity'] == 'Hispanic of any race') |
                                          (not_in_community_df['ZM.Race.Ethnicity'] == 'Native Hawaiian or Other Pacific') |
                                          (not_in_community_df['ZM.Race.Ethnicity'] == 'Two or more races')]

    list_12_values.append(str(int(len(in_comm_URM_race_ethnicity[in_comm_URM_race_ethnicity['ZM.Inquired'] == 1])) ))
    list_12_values.append(str(int(len(in_comm_URM_race_ethnicity[in_comm_URM_race_ethnicity['ZM.Applied'] == 1])) ))
    list_12_values.append(str(int(len(in_comm_URM_race_ethnicity[in_comm_URM_race_ethnicity['ZM.AppComplete'] == 1])) ))
    list_12_values.append(str(int(len(in_comm_URM_race_ethnicity[in_comm_URM_race_ethnicity['ZM.Accepted'] == 1])) ))
    list_12_values.append(str(int(len(in_comm_URM_race_ethnicity[in_comm_URM_race_ethnicity['ZM.Committed'] == 1])) ))
    list_12_values.append(str(int(len(in_comm_URM_race_ethnicity[in_comm_URM_race_ethnicity['ZM.Enrolled'] == 1])) ))

    list_12_values.append(str(int(len(not_in_comm_URM_race_ethnicity[not_in_comm_URM_race_ethnicity['ZM.Inquired'] == 1])) ))
    list_12_values.append(str(int(len(not_in_comm_URM_race_ethnicity[not_in_comm_URM_race_ethnicity['ZM.Applied'] == 1])) ))
    list_12_values.append(str(int(len(not_in_comm_URM_race_ethnicity[not_in_comm_URM_race_ethnicity['ZM.AppComplete'] == 1])) ))
    list_12_values.append(str(int(len(not_in_comm_URM_race_ethnicity[not_in_comm_URM_race_ethnicity['ZM.Accepted'] == 1])) ))
    list_12_values.append(str(int(len(not_in_comm_URM_race_ethnicity[not_in_comm_URM_race_ethnicity['ZM.Committed'] == 1])) ))
    list_12_values.append(str(int(len(not_in_comm_URM_race_ethnicity[not_in_comm_URM_race_ethnicity['ZM.Enrolled'] == 1])) ))

    #'commitment_rate_comm_before_deposit_URM_race_ethnicity',
    x12 = in_comm_URM_race_ethnicity[(in_comm_URM_race_ethnicity['ZM.Committed'] == 1)]
    x13 = x12[
        (x12['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
            (x12['ZM.Joined.Stage'] == '02 INQUIRED') |
            (x12['ZM.Joined.Stage'] == '03 APPLIED') |
            (x12['ZM.Joined.Stage'] == '04 APP COMPLETE') |
            (x12['ZM.Joined.Stage'] == '05 ACCEPTED') ]
    x1 = len(x13)

    x22 = in_comm_URM_race_ethnicity[(in_comm_URM_race_ethnicity['ZM.Accepted'] == 1)]
    x23 = x22[
        (x22['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
            (x22['ZM.Joined.Stage'] == '02 INQUIRED') |
            (x22['ZM.Joined.Stage'] == '03 APPLIED') |
            (x22['ZM.Joined.Stage'] == '04 APP COMPLETE') |
            (x22['ZM.Joined.Stage'] == '05 ACCEPTED') ]
    x2 = len(x23)
    if x2>0:
        list_12_values.append(round(x1/x2,2))
    else:
        list_12_values.append(np.NaN)


    #'commitment_rate_not_in_comm_in_comm_as_dep_URM_race_ethnicity'
    x11 = not_in_comm_URM_race_ethnicity[(not_in_comm_URM_race_ethnicity['ZM.Committed'] == 1)]
    x12 = in_comm_URM_race_ethnicity[(in_comm_URM_race_ethnicity['ZM.Committed'] == 1)]
    x13 = x12[
        (x12['ZM.Joined.Stage'] == '06 COMMITTED')]
    x1 = len(pd.concat([x13,x11]))

    x21 = not_in_comm_URM_race_ethnicity[(not_in_comm_URM_race_ethnicity['ZM.Accepted'] == 1)]
    x22 = in_comm_URM_race_ethnicity[(in_comm_URM_race_ethnicity['ZM.Accepted'] == 1)]
    x23 = x22[
        (x22['ZM.Joined.Stage'] == '06 COMMITTED')]
    x2 = len(pd.concat([x23,x21]))
    if x2>0:
        list_12_values.append(round(x1/x2,2))
    else:
        list_12_values.append(np.NaN)

    #commitment_rate_never_in_community_URM_race_ethnicity
    if len(not_in_comm_URM_race_ethnicity[not_in_comm_URM_race_ethnicity['ZM.Accepted'] == 1]) >0:
        list_12_values.append(round(len(not_in_comm_URM_race_ethnicity[not_in_comm_URM_race_ethnicity['ZM.Committed'] == 1])/ len(not_in_comm_URM_race_ethnicity[not_in_comm_URM_race_ethnicity['ZM.Accepted'] == 1]),2))
    else:
        list_12_values.append(np.NaN)
        

    #melt rate calculation
    if len(not_in_comm_URM_race_ethnicity[not_in_comm_URM_race_ethnicity['ZM.Committed'] == 1]) >0:
        list_12_values.append(round(1-len(not_in_comm_URM_race_ethnicity[not_in_comm_URM_race_ethnicity['ZM.Enrolled'] == 1])/ len(not_in_comm_URM_race_ethnicity[not_in_comm_URM_race_ethnicity['ZM.Committed'] == 1]),2))
    else:
        list_12_values.append(np.NaN)
        
    if len(in_comm_URM_race_ethnicity[in_comm_URM_race_ethnicity['ZM.Committed'] == 1]) >0:
        list_12_values.append(round(1-len(in_comm_URM_race_ethnicity[in_comm_URM_race_ethnicity['ZM.Enrolled'] == 1])/ len(in_comm_URM_race_ethnicity[in_comm_URM_race_ethnicity['ZM.Committed'] == 1]),2))
    else:
        list_12_values.append(np.NaN)
        

    #yield rate
    #yield_rate_comm_before_deposit_URM_race_ethnicity',
    x12 = in_comm_URM_race_ethnicity[(in_comm_URM_race_ethnicity['ZM.Enrolled'] == 1)]
    x13 = x12[
        (x12['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
            (x12['ZM.Joined.Stage'] == '02 INQUIRED') |
            (x12['ZM.Joined.Stage'] == '03 APPLIED') |
            (x12['ZM.Joined.Stage'] == '04 APP COMPLETE') |
            (x12['ZM.Joined.Stage'] == '05 ACCEPTED') ]
    x1 = len(x13)

    x22 = in_comm_URM_race_ethnicity[(in_comm_URM_race_ethnicity['ZM.Accepted'] == 1)]
    x23 = x22[
        (x22['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
            (x22['ZM.Joined.Stage'] == '02 INQUIRED') |
            (x22['ZM.Joined.Stage'] == '03 APPLIED') |
            (x22['ZM.Joined.Stage'] == '04 APP COMPLETE') |
            (x22['ZM.Joined.Stage'] == '05 ACCEPTED') ]
    x2 = len(x23)
    if x2>0:
        list_12_values.append(round(x1/x2,2))
    else:
        list_12_values.append(np.NaN)


    #'yield_rate_not_in_comm_in_comm_as_dep_URM_race_ethnicity'
    x11 = not_in_comm_URM_race_ethnicity[(not_in_comm_URM_race_ethnicity['ZM.Enrolled'] == 1)]
    x12 = in_comm_URM_race_ethnicity[(in_comm_URM_race_ethnicity['ZM.Enrolled'] == 1)]
    x13 = x12[
        (x12['ZM.Joined.Stage'] == '06 COMMITTED')]
    x1 = len(pd.concat([x13,x11]))

    x21 = not_in_comm_URM_race_ethnicity[(not_in_comm_URM_race_ethnicity['ZM.Accepted'] == 1)]
    x22 = in_comm_URM_race_ethnicity[(in_comm_URM_race_ethnicity['ZM.Accepted'] == 1)]
    x23 = x22[
        (x22['ZM.Joined.Stage'] == '06 COMMITTED')]
    x2 = len(pd.concat([x23,x21]))
    if x2>0:
        list_12_values.append(round(x1/x2,2))
    else:
        list_12_values.append(np.NaN)

    #yield_rate_never_in_community_URM_race_ethnicity
    if len(not_in_comm_URM_race_ethnicity[not_in_comm_URM_race_ethnicity['ZM.Accepted'] == 1])>0:
        list_12_values.append(round(len(not_in_comm_URM_race_ethnicity[not_in_comm_URM_race_ethnicity['ZM.Enrolled'] == 1])/ len(not_in_comm_URM_race_ethnicity[not_in_comm_URM_race_ethnicity['ZM.Accepted'] == 1]),2))
    else:
        list_12_values.append(np.NaN)


    #app rate
    #app_rate_comm_before_app_URM_race_ethnicity',
    x12 = in_comm_URM_race_ethnicity[(in_comm_URM_race_ethnicity['ZM.Applied'] == 1)]
    x13 = x12[
        (x12['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
            (x12['ZM.Joined.Stage'] == '02 INQUIRED')
            ]
    x1 = len(x13)

    x22 = in_comm_URM_race_ethnicity[(in_comm_URM_race_ethnicity['ZM.Inquired'] == 1)]
    x23 = x22[
        (x22['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
            (x22['ZM.Joined.Stage'] == '02 INQUIRED') 
            ]
    x2 = len(x23)
    if x2>0:
        list_12_values.append(round(x1/x2,2))
    else:
        list_12_values.append(np.NaN)
        


    #'yield_rate_not_in_comm_in_comm_as_dep_URM_race_ethnicity'
    x11 = not_in_comm_URM_race_ethnicity[(not_in_comm_URM_race_ethnicity['ZM.Applied'] == 1)]
    x12 = in_comm_URM_race_ethnicity[(in_comm_URM_race_ethnicity['ZM.Applied'] == 1)]
    x13 = x12[
        (x12['ZM.Joined.Stage'] == '03 APPLIED') |
            (x12['ZM.Joined.Stage'] == '04 APP COMPLETE') |
            (x12['ZM.Joined.Stage'] == '05 ACCEPTED') |
        (x12['ZM.Joined.Stage'] == '06 COMMITTED')]
    x1 = len(pd.concat([x13,x11]))

    x21 = not_in_comm_URM_race_ethnicity[(not_in_comm_URM_race_ethnicity['ZM.Inquired'] == 1)]
    x22 = in_comm_URM_race_ethnicity[(in_comm_URM_race_ethnicity['ZM.Inquired'] == 1)]
    x23 = x22[
        (x22['ZM.Joined.Stage'] == '03 APPLIED') |
            (x22['ZM.Joined.Stage'] == '04 APP COMPLETE') |
            (x22['ZM.Joined.Stage'] == '05 ACCEPTED') |
        (x22['ZM.Joined.Stage'] == '06 COMMITTED')]
    x2 = len(pd.concat([x23,x21]))
    if x2>0:
        list_12_values.append(round(x1/x2,2))
    else:
        list_12_values.append(np.NaN)

    #app_rate_never_in_community_URM_race_ethnicity
    if len(not_in_comm_URM_race_ethnicity[not_in_comm_URM_race_ethnicity['ZM.Inquired'] == 1]):
        list_12_values.append(round(len(not_in_comm_URM_race_ethnicity[not_in_comm_URM_race_ethnicity['ZM.Applied'] == 1])/ len(not_in_comm_URM_race_ethnicity[not_in_comm_URM_race_ethnicity['ZM.Inquired'] == 1]),2))
    else:
        list_12_values.append(np.NaN)
    
    function_df = pd.DataFrame()
    for i in range(len(known_race_ethnicity_list)):
         function_df[known_race_ethnicity_list[i]] = [list_12_values[i]]
 
    return function_df



