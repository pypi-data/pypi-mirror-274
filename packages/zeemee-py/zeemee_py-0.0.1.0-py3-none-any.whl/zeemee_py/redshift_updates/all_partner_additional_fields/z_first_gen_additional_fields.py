def get_first_gen_related_df(master_df, master_df_filtered, not_in_community_df):
    import pandas as pd
    import numpy as np
    
    list_first_gen = ['inquired_comm_first_gen',
                      'applied_comm_first_gen_',
                      'app_complete_comm_first_gen',
                      'accepted_comm_first_gen',
                      'committed_comm_first_gen',
                      'enrolled_comm_first_gen',

                      'inquired_not_in_comm_first_gen',
                      'applied_not_in_comm_first_gen_',
                      'app_complete_not_in_comm_first_gen',
                      'accepted_not_in_comm_first_gen',
                      'committed_not_in_comm_first_gen',
                      'enrolled_not_in_comm_first_gen',

                      'commitment_rate_in_comm_in_comm_prior_to_deposit_first_gen',
                      'commitment_rate_not_in_comm_in_comm_as_dep_first_gen',
                      'commitment_rate_never_in_community_first_gen',

                      'melt_rate_never_in_community_first_gen',
                      'melt_rate_in_comm_all_first_gen',

                      'yield_rate_in_comm_in_comm_prior_to_deposit_first_gen',
                      'yield_rate_not_in_comm_in_comm_as_deposit_first_gen',
                      'yield_rate_never_in_community_first_gen',

                      'app_rate_in_comm_in_comm_prior_to_app_first_gen',
                      'app_rate_not_in_comm_in_comm_as_app_or_after_first_gen',
                      'app_rate_never_in_community_first_gen']
    
    
    list_12_values = list()

    in_comm_first_gen = master_df_filtered[(master_df_filtered['ZM.First.Gen'] == 'First Generation')] #in community already filtered
    not_in_comm_first_gen = not_in_community_df[not_in_community_df['ZM.First.Gen'] == 'First Generation']

    list_12_values.append(str(int(len(in_comm_first_gen[in_comm_first_gen['ZM.Inquired'] == 1]))))
    list_12_values.append(str(int(len(in_comm_first_gen[in_comm_first_gen['ZM.Applied'] == 1])) ))
    list_12_values.append(str(int(len(in_comm_first_gen[in_comm_first_gen['ZM.AppComplete'] == 1])) ))
    list_12_values.append(str(int(len(in_comm_first_gen[in_comm_first_gen['ZM.Accepted'] == 1])) ))
    list_12_values.append(str(int(len(in_comm_first_gen[in_comm_first_gen['ZM.Committed'] == 1])) ))
    list_12_values.append(str(int(len(in_comm_first_gen[in_comm_first_gen['ZM.Enrolled'] == 1])) ))

    list_12_values.append(str(int(len(not_in_comm_first_gen[not_in_comm_first_gen['ZM.Inquired'] == 1])) ))
    list_12_values.append(str(int(len(not_in_comm_first_gen[not_in_comm_first_gen['ZM.Applied'] == 1])) ))
    list_12_values.append(str(int(len(not_in_comm_first_gen[not_in_comm_first_gen['ZM.AppComplete'] == 1])) ))
    list_12_values.append(str(int(len(not_in_comm_first_gen[not_in_comm_first_gen['ZM.Accepted'] == 1])) ))
    list_12_values.append(str(int(len(not_in_comm_first_gen[not_in_comm_first_gen['ZM.Committed'] == 1])) ))
    list_12_values.append(str(int(len(not_in_comm_first_gen[not_in_comm_first_gen['ZM.Enrolled'] == 1])) ))

    #'commitment_rate_comm_before_deposit_first_gen',
    x12 = in_comm_first_gen[(in_comm_first_gen['ZM.Committed'] == 1)]
    x13 = x12[
        (x12['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
            (x12['ZM.Joined.Stage'] == '02 INQUIRED') |
            (x12['ZM.Joined.Stage'] == '03 APPLIED') |
            (x12['ZM.Joined.Stage'] == '04 APP COMPLETE') |
            (x12['ZM.Joined.Stage'] == '05 ACCEPTED') ]
    x1 = len(x13)

    x22 = in_comm_first_gen[(in_comm_first_gen['ZM.Accepted'] == 1)]
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


    #'commitment_rate_not_in_comm_in_comm_as_dep_first_gen'
    x11 = not_in_comm_first_gen[(not_in_comm_first_gen['ZM.Committed'] == 1)]
    x12 = in_comm_first_gen[(in_comm_first_gen['ZM.Committed'] == 1)]
    x13 = x12[
        (x12['ZM.Joined.Stage'] == '06 COMMITTED')]
    x1 = len(pd.concat([x13,x11]))

    x21 = not_in_comm_first_gen[(not_in_comm_first_gen['ZM.Accepted'] == 1)]
    x22 = in_comm_first_gen[(in_comm_first_gen['ZM.Accepted'] == 1)]
    x23 = x22[
        (x22['ZM.Joined.Stage'] == '06 COMMITTED')]
    x2 = len(pd.concat([x23,x21]))
    if x2>0:
        list_12_values.append(round(x1/x2,2))
    else:
        list_12_values.append(np.NaN)

    #commitment_rate_never_in_community_first_gen
    if len(not_in_comm_first_gen[not_in_comm_first_gen['ZM.Accepted'] == 1]) >0:
        list_12_values.append(round(len(not_in_comm_first_gen[not_in_comm_first_gen['ZM.Committed'] == 1])/ len(not_in_comm_first_gen[not_in_comm_first_gen['ZM.Accepted'] == 1]),2))
    else:
        list_12_values.append(np.NaN)

    #melt rate calculation
    if len(not_in_comm_first_gen[not_in_comm_first_gen['ZM.Committed'] == 1]) >0: 
        list_12_values.append(round(1-len(not_in_comm_first_gen[not_in_comm_first_gen['ZM.Enrolled'] == 1])/ len(not_in_comm_first_gen[not_in_comm_first_gen['ZM.Committed'] == 1]),2))
    else:
        list_12_values.append(np.NaN)
        
    if len(in_comm_first_gen[in_comm_first_gen['ZM.Committed'] == 1]) >0:
        list_12_values.append(round(1-len(in_comm_first_gen[in_comm_first_gen['ZM.Enrolled'] == 1])/ len(in_comm_first_gen[in_comm_first_gen['ZM.Committed'] == 1]),2))
    else:
        list_12_values.append(np.NaN)
        
    #yield rate
    #yield_rate_comm_before_deposit_first_gen',
    x12 = in_comm_first_gen[(in_comm_first_gen['ZM.Enrolled'] == 1)]
    x13 = x12[
        (x12['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
            (x12['ZM.Joined.Stage'] == '02 INQUIRED') |
            (x12['ZM.Joined.Stage'] == '03 APPLIED') |
            (x12['ZM.Joined.Stage'] == '04 APP COMPLETE') |
            (x12['ZM.Joined.Stage'] == '05 ACCEPTED') ]
    x1 = len(x13)

    x22 = in_comm_first_gen[(in_comm_first_gen['ZM.Accepted'] == 1)]
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


    #'yield_rate_not_in_comm_in_comm_as_dep_first_gen'
    x11 = not_in_comm_first_gen[(not_in_comm_first_gen['ZM.Enrolled'] == 1)]
    x12 = in_comm_first_gen[(in_comm_first_gen['ZM.Enrolled'] == 1)]
    x13 = x12[
        (x12['ZM.Joined.Stage'] == '06 COMMITTED')]
    x1 = len(pd.concat([x13,x11]))

    x21 = not_in_comm_first_gen[(not_in_comm_first_gen['ZM.Accepted'] == 1)]
    x22 = in_comm_first_gen[(in_comm_first_gen['ZM.Accepted'] == 1)]
    x23 = x22[
        (x22['ZM.Joined.Stage'] == '06 COMMITTED')]
    x2 = len(pd.concat([x23,x21]))
    if x2>0:
        list_12_values.append(round(x1/x2,2))
    else:
        list_12_values.append(np.NaN)

    #yield_rate_never_in_community_first_gen
    if len(not_in_comm_first_gen[not_in_comm_first_gen['ZM.Accepted'] == 1]) >0:
        list_12_values.append(round(len(not_in_comm_first_gen[not_in_comm_first_gen['ZM.Enrolled'] == 1])/ len(not_in_comm_first_gen[not_in_comm_first_gen['ZM.Accepted'] == 1]),2))
    else:
        list_12_values.append(np.NaN)
        

    #app rate
    #app_rate_comm_before_app_first_gen',
    x12 = in_comm_first_gen[(in_comm_first_gen['ZM.Applied'] == 1)]
    x13 = x12[
        (x12['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
            (x12['ZM.Joined.Stage'] == '02 INQUIRED')
            ]
    x1 = len(x13)

    x22 = in_comm_first_gen[(in_comm_first_gen['ZM.Inquired'] == 1)]
    x23 = x22[
        (x22['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
            (x22['ZM.Joined.Stage'] == '02 INQUIRED') 
            ]
    x2 = len(x23)
    if x2>0:
        list_12_values.append(round(x1/x2,2))
    else:
        list_12_values.append(np.NaN)


    #app_rate_not_in_comm_in_comm_as_dep_first_gen'
    x11 = not_in_comm_first_gen[(not_in_comm_first_gen['ZM.Applied'] == 1)]
    x12 = in_comm_first_gen[(in_comm_first_gen['ZM.Applied'] == 1)]
    x13 = x12[
        (x12['ZM.Joined.Stage'] == '03 APPLIED') |
            (x12['ZM.Joined.Stage'] == '04 APP COMPLETE') |
            (x12['ZM.Joined.Stage'] == '05 ACCEPTED') |
        (x12['ZM.Joined.Stage'] == '06 COMMITTED')]
    x1 = len(pd.concat([x13,x11]))

    x21 = not_in_comm_first_gen[(not_in_comm_first_gen['ZM.Inquired'] == 1)]
    x22 = in_comm_first_gen[(in_comm_first_gen['ZM.Inquired'] == 1)]
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

    #app_rate_never_in_community_first_gen
    if len(not_in_comm_first_gen[not_in_comm_first_gen['ZM.Inquired'] == 1]) >0:
        list_12_values.append(round(len(not_in_comm_first_gen[not_in_comm_first_gen['ZM.Applied'] == 1])/ len(not_in_comm_first_gen[not_in_comm_first_gen['ZM.Inquired'] == 1]),2))
    else:
        list_12_values.append(np.NaN)
    
    function_df = pd.DataFrame()
    for i in range(len(list_first_gen)):
         function_df[list_first_gen[i]] = [list_12_values[i]]
    
    return function_df
