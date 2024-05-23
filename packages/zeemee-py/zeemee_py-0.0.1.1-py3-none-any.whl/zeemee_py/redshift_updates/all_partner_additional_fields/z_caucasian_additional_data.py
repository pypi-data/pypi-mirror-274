def get_Caucasian_race_related_df(master_df, master_df_filtered, not_in_community_df):
    import pandas as pd
    import numpy as np
    
    known_race_ethnicity_list = [
        'inquired_comm_Caucasian_race_ethnicity',
        'applied_comm_Caucasian_race_ethnicity',
        'app_complete_Caucasian_race_ethnicity',
        'accepted_comm_Caucasian_race_ethnicity',
        'committed_comm_Caucasian_race_ethnicity',
        'enrolled_comm_Caucasian_race_ethnicity',

        'inquired_not_in_comm_Caucasian_race_ethnicity',
        'applied_not_in_comm_Caucasian_race_ethnicity',
        'app_complete_not_in_comm_Caucasian_race_ethnicity',
        'accepted_not_in_comm_Caucasian_race_ethnicity',
        'committed_not_in_comm_Caucasian_race_ethnicity',
        'enrolled_not_in_comm_Caucasian_race_ethnicity',

        'commitment_rate_in_comm_in_comm_prior_to_deposit_Caucasian_race_ethnicity',
        'commitment_rate_not_in_comm_in_comm_as_dep_Caucasian_race_ethnicity',
        'commitment_rate_never_in_community_Caucasian_race_ethnicity',

        'melt_rate_never_in_community_Caucasian_race_ethnicity',
        'melt_rate_in_comm_all_Caucasian_race_ethnicity',

        'yield_rate_in_comm_in_comm_prior_to_deposit_Caucasian_race_ethnicity',
        'yield_rate_not_in_comm_in_comm_as_deposit_Caucasian_race_ethnicity',
        'yield_rate_never_in_community_Caucasian_race_ethnicity',

        'app_rate_in_comm_in_comm_prior_to_app_Caucasian_race_ethnicity',
        'app_rate_not_in_comm_in_comm_as_app_or_after_Caucasian_race_ethnicity',
        'app_rate_never_in_community_Caucasian_race_ethnicity'

    ]
    
    
    list_12_values = list()

    in_comm_Caucasian_race_ethnicity = master_df_filtered[
                                          (master_df_filtered['ZM.Race.Ethnicity'] == 'White')] #in community already filtered

    not_in_comm_Caucasian_race_ethnicity = not_in_community_df[
                                          (not_in_community_df['ZM.Race.Ethnicity'] == 'White') ]

    list_12_values.append(str(int(len(in_comm_Caucasian_race_ethnicity[in_comm_Caucasian_race_ethnicity['ZM.Inquired'] == 1])) ))
    list_12_values.append(str(int(len(in_comm_Caucasian_race_ethnicity[in_comm_Caucasian_race_ethnicity['ZM.Applied'] == 1])) ))
    list_12_values.append(str(int(len(in_comm_Caucasian_race_ethnicity[in_comm_Caucasian_race_ethnicity['ZM.AppComplete'] == 1])) ))
    list_12_values.append(str(int(len(in_comm_Caucasian_race_ethnicity[in_comm_Caucasian_race_ethnicity['ZM.Accepted'] == 1])) ))
    list_12_values.append(str(int(len(in_comm_Caucasian_race_ethnicity[in_comm_Caucasian_race_ethnicity['ZM.Committed'] == 1])) ))
    list_12_values.append(str(int(len(in_comm_Caucasian_race_ethnicity[in_comm_Caucasian_race_ethnicity['ZM.Enrolled'] == 1])) ))

    list_12_values.append(str(int(len(not_in_comm_Caucasian_race_ethnicity[not_in_comm_Caucasian_race_ethnicity['ZM.Inquired'] == 1])) ))
    list_12_values.append(str(int(len(not_in_comm_Caucasian_race_ethnicity[not_in_comm_Caucasian_race_ethnicity['ZM.Applied'] == 1])) ))
    list_12_values.append(str(int(len(not_in_comm_Caucasian_race_ethnicity[not_in_comm_Caucasian_race_ethnicity['ZM.AppComplete'] == 1])) ))
    list_12_values.append(str(int(len(not_in_comm_Caucasian_race_ethnicity[not_in_comm_Caucasian_race_ethnicity['ZM.Accepted'] == 1])) ))
    list_12_values.append(str(int(len(not_in_comm_Caucasian_race_ethnicity[not_in_comm_Caucasian_race_ethnicity['ZM.Committed'] == 1])) ))
    list_12_values.append(str(int(len(not_in_comm_Caucasian_race_ethnicity[not_in_comm_Caucasian_race_ethnicity['ZM.Enrolled'] == 1])) ))

    #'commitment_rate_comm_before_deposit_Caucasian_race_ethnicity',
    x12 = in_comm_Caucasian_race_ethnicity[(in_comm_Caucasian_race_ethnicity['ZM.Committed'] == 1)]
    x13 = x12[
        (x12['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
            (x12['ZM.Joined.Stage'] == '02 INQUIRED') |
            (x12['ZM.Joined.Stage'] == '03 APPLIED') |
            (x12['ZM.Joined.Stage'] == '04 APP COMPLETE') |
            (x12['ZM.Joined.Stage'] == '05 ACCEPTED') ]
    x1 = len(x13)

    x22 = in_comm_Caucasian_race_ethnicity[(in_comm_Caucasian_race_ethnicity['ZM.Accepted'] == 1)]
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


    #'commitment_rate_not_in_comm_in_comm_as_dep_Caucasian_race_ethnicity'
    x11 = not_in_comm_Caucasian_race_ethnicity[(not_in_comm_Caucasian_race_ethnicity['ZM.Committed'] == 1)]
    x12 = in_comm_Caucasian_race_ethnicity[(in_comm_Caucasian_race_ethnicity['ZM.Committed'] == 1)]
    x13 = x12[
        (x12['ZM.Joined.Stage'] == '06 COMMITTED')]
    x1 = len(pd.concat([x13,x11]))

    x21 = not_in_comm_Caucasian_race_ethnicity[(not_in_comm_Caucasian_race_ethnicity['ZM.Accepted'] == 1)]
    x22 = in_comm_Caucasian_race_ethnicity[(in_comm_Caucasian_race_ethnicity['ZM.Accepted'] == 1)]
    x23 = x22[
        (x22['ZM.Joined.Stage'] == '06 COMMITTED')]
    x2 = len(pd.concat([x23,x21]))
    if x2>0:
        list_12_values.append(round(x1/x2,2))
    else:
        list_12_values.append(np.NaN)

    #commitment_rate_never_in_community_Caucasian_race_ethnicity
    if len(not_in_comm_Caucasian_race_ethnicity[not_in_comm_Caucasian_race_ethnicity['ZM.Accepted'] == 1]) >0:
        list_12_values.append(round(len(not_in_comm_Caucasian_race_ethnicity[not_in_comm_Caucasian_race_ethnicity['ZM.Committed'] == 1])/ len(not_in_comm_Caucasian_race_ethnicity[not_in_comm_Caucasian_race_ethnicity['ZM.Accepted'] == 1]),2))
    else:
        list_12_values.append(np.NaN)

    #melt rate calculation
    if len(not_in_comm_Caucasian_race_ethnicity[not_in_comm_Caucasian_race_ethnicity['ZM.Committed'] == 1]) >0:
        list_12_values.append(round(1-len(not_in_comm_Caucasian_race_ethnicity[not_in_comm_Caucasian_race_ethnicity['ZM.Enrolled'] == 1])/ len(not_in_comm_Caucasian_race_ethnicity[not_in_comm_Caucasian_race_ethnicity['ZM.Committed'] == 1]),2))
    else:
        list_12_values.append(np.NaN)
        
    if len(in_comm_Caucasian_race_ethnicity[in_comm_Caucasian_race_ethnicity['ZM.Committed'] == 1]) >0:
        list_12_values.append(round(1-len(in_comm_Caucasian_race_ethnicity[in_comm_Caucasian_race_ethnicity['ZM.Enrolled'] == 1])/ len(in_comm_Caucasian_race_ethnicity[in_comm_Caucasian_race_ethnicity['ZM.Committed'] == 1]),2))
    else:
        list_12_values.append(np.NaN)
        

    #yield rate
    #yield_rate_comm_before_deposit_Caucasian_race_ethnicity',
    x12 = in_comm_Caucasian_race_ethnicity[(in_comm_Caucasian_race_ethnicity['ZM.Enrolled'] == 1)]
    x13 = x12[
        (x12['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
            (x12['ZM.Joined.Stage'] == '02 INQUIRED') |
            (x12['ZM.Joined.Stage'] == '03 APPLIED') |
            (x12['ZM.Joined.Stage'] == '04 APP COMPLETE') |
            (x12['ZM.Joined.Stage'] == '05 ACCEPTED') ]
    x1 = len(x13)

    x22 = in_comm_Caucasian_race_ethnicity[(in_comm_Caucasian_race_ethnicity['ZM.Accepted'] == 1)]
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


    #'yield_rate_not_in_comm_in_comm_as_dep_Caucasian_race_ethnicity'
    x11 = not_in_comm_Caucasian_race_ethnicity[(not_in_comm_Caucasian_race_ethnicity['ZM.Enrolled'] == 1)]
    x12 = in_comm_Caucasian_race_ethnicity[(in_comm_Caucasian_race_ethnicity['ZM.Enrolled'] == 1)]
    x13 = x12[
        (x12['ZM.Joined.Stage'] == '06 COMMITTED')]
    x1 = len(pd.concat([x13,x11]))

    x21 = not_in_comm_Caucasian_race_ethnicity[(not_in_comm_Caucasian_race_ethnicity['ZM.Accepted'] == 1)]
    x22 = in_comm_Caucasian_race_ethnicity[(in_comm_Caucasian_race_ethnicity['ZM.Accepted'] == 1)]
    x23 = x22[
        (x22['ZM.Joined.Stage'] == '06 COMMITTED')]
    x2 = len(pd.concat([x23,x21]))
    if x2>0:
        list_12_values.append(round(x1/x2,2))
    else:
        list_12_values.append(np.NaN)

    #yield_rate_never_in_community_Caucasian_race_ethnicity
    if len(not_in_comm_Caucasian_race_ethnicity[not_in_comm_Caucasian_race_ethnicity['ZM.Accepted'] == 1]) >0:
        list_12_values.append(round(len(not_in_comm_Caucasian_race_ethnicity[not_in_comm_Caucasian_race_ethnicity['ZM.Enrolled'] == 1])/ len(not_in_comm_Caucasian_race_ethnicity[not_in_comm_Caucasian_race_ethnicity['ZM.Accepted'] == 1]),2))
    else:
        list_12_values.append(np.NaN)


    #app rate
    #app_rate_comm_before_app_Caucasian_race_ethnicity',
    x12 = in_comm_Caucasian_race_ethnicity[(in_comm_Caucasian_race_ethnicity['ZM.Applied'] == 1)]
    x13 = x12[
        (x12['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
            (x12['ZM.Joined.Stage'] == '02 INQUIRED')
            ]
    x1 = len(x13)

    x22 = in_comm_Caucasian_race_ethnicity[(in_comm_Caucasian_race_ethnicity['ZM.Inquired'] == 1)]
    x23 = x22[
        (x22['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
            (x22['ZM.Joined.Stage'] == '02 INQUIRED') 
            ]
    x2 = len(x23)
    if x2>0:
        list_12_values.append(round(x1/x2,2))
    else:
        list_12_values.append(np.NaN)


    #'yield_rate_not_in_comm_in_comm_as_dep_Caucasian_race_ethnicity'
    x11 = not_in_comm_Caucasian_race_ethnicity[(not_in_comm_Caucasian_race_ethnicity['ZM.Applied'] == 1)]
    x12 = in_comm_Caucasian_race_ethnicity[(in_comm_Caucasian_race_ethnicity['ZM.Applied'] == 1)]
    x13 = x12[
        (x12['ZM.Joined.Stage'] == '03 APPLIED') |
            (x12['ZM.Joined.Stage'] == '04 APP COMPLETE') |
            (x12['ZM.Joined.Stage'] == '05 ACCEPTED') |
        (x12['ZM.Joined.Stage'] == '06 COMMITTED')]
    x1 = len(pd.concat([x13,x11]))

    x21 = not_in_comm_Caucasian_race_ethnicity[(not_in_comm_Caucasian_race_ethnicity['ZM.Inquired'] == 1)]
    x22 = in_comm_Caucasian_race_ethnicity[(in_comm_Caucasian_race_ethnicity['ZM.Inquired'] == 1)]
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

    #app_rate_never_in_community_Caucasian_race_ethnicity
    if len(not_in_comm_Caucasian_race_ethnicity[not_in_comm_Caucasian_race_ethnicity['ZM.Inquired'] == 1]) >0:
        list_12_values.append(round(len(not_in_comm_Caucasian_race_ethnicity[not_in_comm_Caucasian_race_ethnicity['ZM.Applied'] == 1])/ len(not_in_comm_Caucasian_race_ethnicity[not_in_comm_Caucasian_race_ethnicity['ZM.Inquired'] == 1]),2))
    else:
        list_12_values.append(np.NaN)
        
    function_df = pd.DataFrame()
    for i in range(len(known_race_ethnicity_list)):
         function_df[known_race_ethnicity_list[i]] = [list_12_values[i]]

    return function_df


