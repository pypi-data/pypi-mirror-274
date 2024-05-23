def get_campus_related_related_df(master_df, master_df_filtered, not_in_community_df):
    import pandas as pd
    import numpy as np
    
    list_campus_visit = [
         'inquired_comm_campus_visit',
            'applied_comm_campus_visit',
            'app_complete_comm_campus_visit',
            'accepted_comm_campus_visit',
            'committed_comm_campus_visit',
            'enrolled_comm_campus_visit',
          
            'inquired_not_in_comm_campus_visit',
            'applied_not_in_comm_campus_visit',
            'app_complete_not_in_comm_campus_visit',
            'accepted_not_in_comm_campus_visit',
            'committed_not_in_comm_campus_visit',
            'enrolled_not_in_comm_campus_visit',
          
            'commitment_rate_in_comm_in_comm_prior_to_deposit_campus_visit',
            'commitment_rate_not_in_comm_in_comm_as_dep_campus_visit',
            'commitment_rate_never_in_community_campus_visit',
          
            'melt_rate_never_in_community_campus_visit',
            'melt_rate_in_comm_all_campus_visit',
          
            'yield_rate_in_comm_in_comm_prior_to_deposit_campus_visit',
            'yield_rate_not_in_comm_in_comm_as_deposit_campus_visit',
            'yield_rate_never_in_community_campus_visit',
          
            'app_rate_in_comm_in_comm_prior_to_app_campus_visit',
            'app_rate_not_in_comm_in_comm_as_app_or_after_campus_visit',
            'app_rate_never_in_community_campus_visit'
              ]
    
    list_12_values = list()

    in_comm_camp_visit = master_df_filtered[(master_df_filtered['ZM.CV.Flag'] == 'Campus Visit')] #in community already filtered
    not_in_comm_camp_visit = not_in_community_df[not_in_community_df['ZM.CV.Flag'] == 'Campus Visit']

    list_12_values.append(str(int(len(in_comm_camp_visit[in_comm_camp_visit['ZM.Inquired'] == 1])) ))
    list_12_values.append(str(int(len(in_comm_camp_visit[in_comm_camp_visit['ZM.Applied'] == 1])) ))
    list_12_values.append(str(int(len(in_comm_camp_visit[in_comm_camp_visit['ZM.AppComplete'] == 1])) ))
    list_12_values.append(str(int(len(in_comm_camp_visit[in_comm_camp_visit['ZM.Accepted'] == 1])) ))
    list_12_values.append(str(int(len(in_comm_camp_visit[in_comm_camp_visit['ZM.Committed'] == 1])) ))
    list_12_values.append(str(int(len(in_comm_camp_visit[in_comm_camp_visit['ZM.Enrolled'] == 1])) ))

    list_12_values.append(str(int(len(not_in_comm_camp_visit[not_in_comm_camp_visit['ZM.Inquired'] == 1])) ))
    list_12_values.append(str(int(len(not_in_comm_camp_visit[not_in_comm_camp_visit['ZM.Applied'] == 1])) ))
    list_12_values.append(str(int(len(not_in_comm_camp_visit[not_in_comm_camp_visit['ZM.AppComplete'] == 1])) ))
    list_12_values.append(str(int(len(not_in_comm_camp_visit[not_in_comm_camp_visit['ZM.Accepted'] == 1])) ))
    list_12_values.append(str(int(len(not_in_comm_camp_visit[not_in_comm_camp_visit['ZM.Committed'] == 1])) ))
    list_12_values.append(str(int(len(not_in_comm_camp_visit[not_in_comm_camp_visit['ZM.Enrolled'] == 1])) ))

    #'commitment_rate_comm_before_deposit_camp_visit',
    x12 = in_comm_camp_visit[(in_comm_camp_visit['ZM.Committed'] == 1)]
    x13 = x12[
        (x12['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
            (x12['ZM.Joined.Stage'] == '02 INQUIRED') |
            (x12['ZM.Joined.Stage'] == '03 APPLIED') |
            (x12['ZM.Joined.Stage'] == '04 APP COMPLETE') |
            (x12['ZM.Joined.Stage'] == '05 ACCEPTED') ]
    x1 = len(x13)

    x22 = in_comm_camp_visit[(in_comm_camp_visit['ZM.Accepted'] == 1)]
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


    #'commitment_rate_not_in_comm_in_comm_as_dep_camp_visit'
    x11 = not_in_comm_camp_visit[(not_in_comm_camp_visit['ZM.Committed'] == 1)]
    x12 = in_comm_camp_visit[(in_comm_camp_visit['ZM.Committed'] == 1)]
    x13 = x12[x12['ZM.Joined.Stage'] == '06 COMMITTED']
    x1 = len(pd.concat([x13,x11]))

    x21 = not_in_comm_camp_visit[(not_in_comm_camp_visit['ZM.Accepted'] == 1)]
    x22 = in_comm_camp_visit[(in_comm_camp_visit['ZM.Accepted'] == 1)]
    x23 = x22[
        (x22['ZM.Joined.Stage'] == '06 COMMITTED')]
    x2 = len(pd.concat([x23,x21]))
    if x2>0:
        list_12_values.append(round(x1/x2,2))
    else:
        list_12_values.append(np.NaN)

    #commitment_rate_never_in_community_camp_visit
    if len(not_in_comm_camp_visit[not_in_comm_camp_visit['ZM.Accepted'] == 1]) >0: 
        list_12_values.append(round(len(not_in_comm_camp_visit[not_in_comm_camp_visit['ZM.Committed'] == 1])/ len(not_in_comm_camp_visit[not_in_comm_camp_visit['ZM.Accepted'] == 1]),2))
    else:
        list_12_values.append(np.NaN)

    #melt rate calculation
    if len(not_in_comm_camp_visit[not_in_comm_camp_visit['ZM.Committed'] == 1]) >0:
        list_12_values.append(round(1-len(not_in_comm_camp_visit[not_in_comm_camp_visit['ZM.Enrolled'] == 1])/ len(not_in_comm_camp_visit[not_in_comm_camp_visit['ZM.Committed'] == 1]),2))
    else:
        list_12_values.append(np.NaN)
        
    if len(in_comm_camp_visit[in_comm_camp_visit['ZM.Committed'] == 1]) >0:
        list_12_values.append(round(1-len(in_comm_camp_visit[in_comm_camp_visit['ZM.Enrolled'] == 1])/ len(in_comm_camp_visit[in_comm_camp_visit['ZM.Committed'] == 1]),2))
    else:
        list_12_values.append(np.NaN)
        
        
    #yield rate
    #yield_rate_comm_before_deposit_camp_visit',
    x12 = in_comm_camp_visit[(in_comm_camp_visit['ZM.Enrolled'] == 1)]
    x13 = x12[
        (x12['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
            (x12['ZM.Joined.Stage'] == '02 INQUIRED') |
            (x12['ZM.Joined.Stage'] == '03 APPLIED') |
            (x12['ZM.Joined.Stage'] == '04 APP COMPLETE') |
            (x12['ZM.Joined.Stage'] == '05 ACCEPTED') ]
    x1 = len(x13)

    x22 = in_comm_camp_visit[(in_comm_camp_visit['ZM.Accepted'] == 1)]
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


    #'yield_rate_not_in_comm_in_comm_as_dep_camp_visit'
    x11 = not_in_comm_camp_visit[(not_in_comm_camp_visit['ZM.Enrolled'] == 1)]
    x12 = in_comm_camp_visit[(in_comm_camp_visit['ZM.Enrolled'] == 1)]
    x13 = x12[x12['ZM.Joined.Stage'] == '06 COMMITTED']
    x1 = len(pd.concat([x13,x11]))

    x21 = not_in_comm_camp_visit[(not_in_comm_camp_visit['ZM.Accepted'] == 1)]
    x22 = in_comm_camp_visit[(in_comm_camp_visit['ZM.Accepted'] == 1)]
    x23 = x22[
        (x22['ZM.Joined.Stage'] == '06 COMMITTED')]
    x2 = len(pd.concat([x23,x21]))
    if x2>0:
        list_12_values.append(round(x1/x2,2))
    else:
        list_12_values.append(np.NaN)

    #yield_rate_never_in_community_camp_visit
    if len(not_in_comm_camp_visit[not_in_comm_camp_visit['ZM.Accepted'] == 1]) >0:
        list_12_values.append(round(len(not_in_comm_camp_visit[not_in_comm_camp_visit['ZM.Enrolled'] == 1])/ len(not_in_comm_camp_visit[not_in_comm_camp_visit['ZM.Accepted'] == 1]),2))
    else:
        list_12_values.append(np.NaN)


    #app rate
    #app_rate_comm_before_app_camp_visit',
    x12 = in_comm_camp_visit[(in_comm_camp_visit['ZM.Applied'] == 1)]
    x13 = x12[
        (x12['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
            (x12['ZM.Joined.Stage'] == '02 INQUIRED')
            ]
    x1 = len(x13)

    x22 = in_comm_camp_visit[(in_comm_camp_visit['ZM.Inquired'] == 1)]
    x23 = x22[
        (x22['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
            (x22['ZM.Joined.Stage'] == '02 INQUIRED') 
            ]
    x2 = len(x23)
    if x2>0:
        list_12_values.append(round(x1/x2,2))
    else:
        list_12_values.append(np.NaN)


    #'yield_rate_not_in_comm_in_comm_as_dep_camp_visit'
    x11 = not_in_comm_camp_visit[(not_in_comm_camp_visit['ZM.Applied'] == 1)]
    x12 = in_comm_camp_visit[(in_comm_camp_visit['ZM.Applied'] == 1)]
    x13 = x12[
        (x12['ZM.Joined.Stage'] == '03 APPLIED') |
            (x12['ZM.Joined.Stage'] == '04 APP COMPLETE') |
            (x12['ZM.Joined.Stage'] == '05 ACCEPTED') |
        (x12['ZM.Joined.Stage'] == '06 COMMITTED')]
    x1 = len(pd.concat([x13,x11]))

    x21 = not_in_comm_camp_visit[(not_in_comm_camp_visit['ZM.Inquired'] == 1)]
    x22 = in_comm_camp_visit[(in_comm_camp_visit['ZM.Inquired'] == 1)]
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

    #app_rate_never_in_community_camp_visit
    if len(not_in_comm_camp_visit[not_in_comm_camp_visit['ZM.Inquired'] == 1]) >0:
        list_12_values.append(round(len(not_in_comm_camp_visit[not_in_comm_camp_visit['ZM.Applied'] == 1])/ len(not_in_comm_camp_visit[not_in_comm_camp_visit['ZM.Inquired'] == 1]),2))
    else:
        list_12_values.append(np.NaN)

    function_df = pd.DataFrame()
    for i in range(len(list_campus_visit)):
         function_df[list_campus_visit[i]] = [list_12_values[i]]
    
    return function_df
