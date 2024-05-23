

def get_ap_values_not_campus_visit(master_df):
     import pandas as pd
     import sys
     import importlib
     
     sys.dont_write_bytecode = True
     
     [
          'inquired_comm_not_campus_visit',
          'applied_comm_not_campus_visit',
          'app_complete_comm_not_campus_visit',
          'accepted_comm_not_campus_visit',
          'committed_comm_not_campus_visit',
          'enrolled_comm_not_campus_visit',
          
          'inquired_not_in_comm_not_campus_visit',
          'applied_not_in_comm_not_campus_visit',
          'app_complete_not_in_comm_not_campus_visit',
          'accepted_not_in_comm_not_campus_visit',
          'committed_not_in_comm_not_campus_visit',
          'enrolled_not_in_comm_not_campus_visit',
          
          'commitment_rate_in_comm_in_comm_prior_to_deposit_not_campus_visit',
          'commitment_rate_not_in_comm_in_comm_as_dep_not_campus_visit',
          'commitment_rate_never_in_community_not_campus_visit',
          
          'melt_rate_never_in_community_not_campus_visit',
          'melt_rate_in_comm_all_not_campus_visit',
          
          'yield_rate_in_comm_in_comm_prior_to_deposit_not_campus_visit',
          'yield_rate_not_in_comm_in_comm_as_deposit_not_campus_visit',
          'yield_rate_never_in_community_not_campus_visit',
          
          'app_rate_in_comm_in_comm_prior_to_app_not_campus_visit',
          'app_rate_not_in_comm_in_comm_as_app_or_after_not_campus_visit',
          'app_rate_never_in_community_not_campus_visit'
          ]

     
     #__________________________________
     
     function_dataframe = pd.DataFrame()
     
     not_campus_visit_master_df =  master_df[(master_df['ZM.CV.Flag'] != 'Campus Visit')].reset_index(drop = True)
     in_comm_not_campus_visit_master_df = not_campus_visit_master_df[not_campus_visit_master_df['ZM.Community'] == 'Community'].reset_index(drop = True)
     not_in_comm_not_campus_visit_master_df = not_campus_visit_master_df[not_campus_visit_master_df['ZM.Community'] == 'Not in Community'].reset_index(drop = True)
     

     #___________________________________ 1
     inquired_comm_not_campus_visit = len(in_comm_not_campus_visit_master_df[in_comm_not_campus_visit_master_df['ZM.Inquired'] == 1])
     applied_comm_not_campus_visit = len(in_comm_not_campus_visit_master_df[in_comm_not_campus_visit_master_df['ZM.Applied'] == 1])
     app_complete_comm_not_campus_visit = len(in_comm_not_campus_visit_master_df[in_comm_not_campus_visit_master_df['ZM.AppComplete'] == 1])
     accepted_comm_not_campus_visit = len(in_comm_not_campus_visit_master_df[in_comm_not_campus_visit_master_df['ZM.Accepted'] == 1])
     committed_comm_not_campus_visit = len(in_comm_not_campus_visit_master_df[in_comm_not_campus_visit_master_df['ZM.Committed'] == 1])
     enrolled_comm_not_campus_visit = len(in_comm_not_campus_visit_master_df[in_comm_not_campus_visit_master_df['ZM.Enrolled'] == 1])
     
     function_dataframe['inquired_comm_not_campus_visit'] = [inquired_comm_not_campus_visit]
     function_dataframe['applied_comm_not_campus_visit'] = [applied_comm_not_campus_visit]
     function_dataframe['app_complete_comm_not_campus_visit'] = [app_complete_comm_not_campus_visit]
     function_dataframe['accepted_comm_not_campus_visit'] = [accepted_comm_not_campus_visit]
     function_dataframe['committed_comm_not_campus_visit'] = [committed_comm_not_campus_visit]
     function_dataframe['enrolled_comm_not_campus_visit'] = [enrolled_comm_not_campus_visit]
     #___________________________________
     
     
     #___________________________________ 2
     inquired_not_in_comm_not_campus_visit = len(not_in_comm_not_campus_visit_master_df[not_in_comm_not_campus_visit_master_df['ZM.Inquired'] == 1])
     applied_not_in_comm_not_campus_visit = len(not_in_comm_not_campus_visit_master_df[not_in_comm_not_campus_visit_master_df['ZM.Applied'] == 1])
     app_complete_not_in_comm_not_campus_visit = len(not_in_comm_not_campus_visit_master_df[not_in_comm_not_campus_visit_master_df['ZM.AppComplete'] == 1])
     accepted_not_in_comm_not_campus_visit = len(not_in_comm_not_campus_visit_master_df[not_in_comm_not_campus_visit_master_df['ZM.Accepted'] == 1])
     committed_not_in_comm_not_campus_visit = len(not_in_comm_not_campus_visit_master_df[not_in_comm_not_campus_visit_master_df['ZM.Committed'] == 1])
     enrolled_not_in_comm_not_campus_visit = len(not_in_comm_not_campus_visit_master_df[not_in_comm_not_campus_visit_master_df['ZM.Enrolled'] == 1])
     
     function_dataframe['inquired_not_in_comm_not_campus_visit'] = [inquired_not_in_comm_not_campus_visit]
     function_dataframe['applied_not_in_comm_not_campus_visit'] = [applied_not_in_comm_not_campus_visit]
     function_dataframe['app_complete_not_in_comm_not_campus_visit'] = [app_complete_not_in_comm_not_campus_visit]
     function_dataframe['accepted_not_in_comm_not_campus_visit'] = [accepted_not_in_comm_not_campus_visit]
     function_dataframe['committed_not_in_comm_not_campus_visit'] = [committed_not_in_comm_not_campus_visit]
     function_dataframe['enrolled_not_in_comm_not_campus_visit'] = [enrolled_not_in_comm_not_campus_visit]
     #___________________________________
     
     
     
     #___________________________________ 
     #3.1
     #commitment_rate_in_comm_in_comm_prior_to_deposit_not_campus_visit
     temp_df_1_numerator = in_comm_not_campus_visit_master_df[(in_comm_not_campus_visit_master_df['ZM.Committed'] == 1)]
     temp_df_2_numerator = temp_df_1_numerator[
          (temp_df_1_numerator['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
          (temp_df_1_numerator['ZM.Joined.Stage'] == '02 INQUIRED') |
          (temp_df_1_numerator['ZM.Joined.Stage'] == '03 APPLIED') |
          (temp_df_1_numerator['ZM.Joined.Stage'] == '04 APP COMPLETE') |
          (temp_df_1_numerator['ZM.Joined.Stage'] == '05 ACCEPTED') 
          ]
     numerator= len(temp_df_2_numerator)

     temp_df_1_denominator = in_comm_not_campus_visit_master_df[(in_comm_not_campus_visit_master_df['ZM.Accepted'] == 1)]
     temp_df_2_demoninator = temp_df_1_denominator[
          (temp_df_1_denominator['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
          (temp_df_1_denominator['ZM.Joined.Stage'] == '02 INQUIRED') |
          (temp_df_1_denominator['ZM.Joined.Stage'] == '03 APPLIED') |
          (temp_df_1_denominator['ZM.Joined.Stage'] == '04 APP COMPLETE') |
          (temp_df_1_denominator['ZM.Joined.Stage'] == '05 ACCEPTED') 
          ]
     denominator = len(temp_df_2_demoninator)
    
     if denominator>0:
          commitment_rate_in_comm_in_comm_prior_to_deposit_not_campus_visit = round(numerator/denominator,3)
     else: commitment_rate_in_comm_in_comm_prior_to_deposit_not_campus_visit = ''
    
    
     #3.2
     #commitment_rate_not_in_comm_in_comm_as_dep_not_campus_visit
     temp_df_1_numerator = not_in_comm_not_campus_visit_master_df[(not_in_comm_not_campus_visit_master_df['ZM.Committed'] == 1)]
     temp_df_2_numerator = in_comm_not_campus_visit_master_df[(in_comm_not_campus_visit_master_df['ZM.Committed'] == 1)]
     temp_df_2_numerator = temp_df_2_numerator[
         (temp_df_2_numerator['ZM.Joined.Stage'] == '06 COMMITTED')]
     numerator = len(pd.concat([temp_df_1_numerator,temp_df_2_numerator]))
     
     temp_df_1_denominator = not_in_comm_not_campus_visit_master_df[(not_in_comm_not_campus_visit_master_df['ZM.Accepted'] == 1)]
     temp_df_2_denominator = in_comm_not_campus_visit_master_df[(in_comm_not_campus_visit_master_df['ZM.Accepted'] == 1)]
     temp_df_2_denominator = temp_df_2_denominator[
         (temp_df_2_denominator['ZM.Joined.Stage'] == '06 COMMITTED')]
     denominator = len(pd.concat([temp_df_1_denominator,temp_df_2_denominator]))
     
     if denominator>0:
         commitment_rate_not_in_comm_in_comm_as_dep_not_campus_visit = round(numerator/denominator,3)
     else: commitment_rate_not_in_comm_in_comm_as_dep_not_campus_visit = ''
     
     
     #3.3
     #commitment_rate_never_in_community_not_campus_visit
     denominator = len(not_in_comm_not_campus_visit_master_df[not_in_comm_not_campus_visit_master_df['ZM.Accepted'] == 1])
     if denominator>0:
          numerator = len(not_in_comm_not_campus_visit_master_df[not_in_comm_not_campus_visit_master_df['ZM.Committed'] == 1])
          commitment_rate_never_in_community_not_campus_visit = round(numerator/denominator,3)
     else: commitment_rate_never_in_community_not_campus_visit = ''
     
     function_dataframe['commitment_rate_in_comm_in_comm_prior_to_deposit_not_campus_visit'] = [commitment_rate_in_comm_in_comm_prior_to_deposit_not_campus_visit]
     function_dataframe['commitment_rate_not_in_comm_in_comm_as_dep_not_campus_visit'] = [commitment_rate_not_in_comm_in_comm_as_dep_not_campus_visit]
     function_dataframe['commitment_rate_never_in_community_not_campus_visit'] = [commitment_rate_never_in_community_not_campus_visit]
     #___________________________________ 
     
     
     
     #___________________________________ 
     #4.1
     #melt_rate_never_in_community_not_campus_visit
     denominator = len(not_in_comm_not_campus_visit_master_df[not_in_comm_not_campus_visit_master_df['ZM.Committed'] == 1])
     if denominator >0:
          numerator = len(not_in_comm_not_campus_visit_master_df[not_in_comm_not_campus_visit_master_df['ZM.Enrolled'] == 1])
          melt_rate_never_in_community_not_campus_visit = round(1 - (numerator/denominator),3)
     else: melt_rate_never_in_community_not_campus_visit = ''
     
     
     #4.2
     #melt_rate_in_comm_all_not_campus_visit
     denominator = len(in_comm_not_campus_visit_master_df[in_comm_not_campus_visit_master_df['ZM.Committed'] == 1])
     if denominator >0:
          numerator = len(in_comm_not_campus_visit_master_df[in_comm_not_campus_visit_master_df['ZM.Enrolled'] == 1])
          melt_rate_in_comm_all_not_campus_visit = round(1 - (numerator/denominator),3)
     else: melt_rate_never_in_community_not_campus_visit = ''
     
     function_dataframe['melt_rate_never_in_community_not_campus_visit'] = [melt_rate_never_in_community_not_campus_visit]
     function_dataframe['melt_rate_never_in_community_not_campus_visit'] = [melt_rate_never_in_community_not_campus_visit]
     #___________________________________     
     
     
     
     #___________________________________
     #5.1
     #yield_rate_in_comm_in_comm_prior_to_deposit_not_campus_visit
     temp_df_1_numerator = in_comm_not_campus_visit_master_df[(in_comm_not_campus_visit_master_df['ZM.Enrolled'] == 1)]
     temp_df_2_numerator = temp_df_1_numerator[
          (temp_df_1_numerator['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
          (temp_df_1_numerator['ZM.Joined.Stage'] == '02 INQUIRED') |
          (temp_df_1_numerator['ZM.Joined.Stage'] == '03 APPLIED') |
          (temp_df_1_numerator['ZM.Joined.Stage'] == '04 APP COMPLETE') |
          (temp_df_1_numerator['ZM.Joined.Stage'] == '05 ACCEPTED') 
          ]
     numerator = len(temp_df_2_numerator)

     temp_df_1_denominator = in_comm_not_campus_visit_master_df[(in_comm_not_campus_visit_master_df['ZM.Accepted'] == 1)]
     temp_df_2_denominator =  temp_df_1_denominator[
          (temp_df_1_denominator['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
          (temp_df_1_denominator['ZM.Joined.Stage'] == '02 INQUIRED') |
          (temp_df_1_denominator['ZM.Joined.Stage'] == '03 APPLIED') |
          (temp_df_1_denominator['ZM.Joined.Stage'] == '04 APP COMPLETE') |
          (temp_df_1_denominator['ZM.Joined.Stage'] == '05 ACCEPTED') 
          ]
     denominator = len(temp_df_2_denominator)
     
     if denominator>0:
         yield_rate_in_comm_in_comm_prior_to_deposit_not_campus_visit = round(numerator/denominator,3)
     else: yield_rate_in_comm_in_comm_prior_to_deposit_not_campus_visit = ''
     
     
     #5.2
     #yield_rate_not_in_comm_in_comm_as_deposit_not_campus_visit
     temp_df_1_numerator = not_in_comm_not_campus_visit_master_df[(not_in_comm_not_campus_visit_master_df['ZM.Enrolled'] == 1)]
     temp_df_2_numerator = in_comm_not_campus_visit_master_df[(in_comm_not_campus_visit_master_df['ZM.Enrolled'] == 1)]
     temp_df_2_numerator = temp_df_2_numerator[
          (temp_df_2_numerator['ZM.Joined.Stage'] == '06 COMMITTED')]
     numerator = len(pd.concat([temp_df_1_numerator,temp_df_2_numerator]))
     
     temp_df_1_denominator = not_in_comm_not_campus_visit_master_df[(not_in_comm_not_campus_visit_master_df['ZM.Accepted'] == 1)]
     temp_df_2_denominator = in_comm_not_campus_visit_master_df[(in_comm_not_campus_visit_master_df['ZM.Accepted'] == 1)]
     temp_df_2_denominator = temp_df_2_denominator[
          (temp_df_2_denominator['ZM.Joined.Stage'] == '06 COMMITTED')]
     denominator = len(pd.concat([temp_df_1_denominator,temp_df_2_denominator]))
     if denominator>0:
          yield_rate_not_in_comm_in_comm_as_deposit_not_campus_visit = round(numerator/denominator,3)
     else: yield_rate_not_in_comm_in_comm_as_deposit_not_campus_visit = ''
     
     
     #5.3
     #yield_rate_never_in_community_not_campus_visit
     denominator = len(not_in_comm_not_campus_visit_master_df[not_in_comm_not_campus_visit_master_df['ZM.Accepted'] == 1])
     if denominator >0:
          numerator = len(not_in_comm_not_campus_visit_master_df[not_in_comm_not_campus_visit_master_df['ZM.Enrolled'] == 1])
          yield_rate_never_in_community_not_campus_visit = round(numerator/denominator,3)
     else: yield_rate_never_in_community_not_campus_visit = ''
     
     function_dataframe['yield_rate_in_comm_in_comm_prior_to_deposit_not_campus_visit'] = [yield_rate_in_comm_in_comm_prior_to_deposit_not_campus_visit]
     function_dataframe['yield_rate_not_in_comm_in_comm_as_deposit_not_campus_visit'] = [yield_rate_not_in_comm_in_comm_as_deposit_not_campus_visit]
     function_dataframe['yield_rate_never_in_community_not_campus_visit'] = [yield_rate_never_in_community_not_campus_visit]
     #___________________________________
     
     
     #___________________________________
     #6.1
     #app_rate_in_comm_in_comm_prior_to_app_not_campus_visit
     temp_df_1_numerator = in_comm_not_campus_visit_master_df[(in_comm_not_campus_visit_master_df['ZM.Applied'] == 1)]
     temp_df_2_numerator = temp_df_1_numerator[
          (temp_df_1_numerator['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
          (temp_df_1_numerator['ZM.Joined.Stage'] == '02 INQUIRED')
          ]
     numerator = len(temp_df_2_numerator)
     
     temp_df_1_denominator = in_comm_not_campus_visit_master_df[(in_comm_not_campus_visit_master_df['ZM.Inquired'] == 1)]
     temp_df_2_denominator = temp_df_1_denominator[
          (temp_df_1_denominator['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
          (temp_df_1_denominator['ZM.Joined.Stage'] == '02 INQUIRED') 
          ]
     denominator = len(temp_df_2_denominator)
     
     if denominator>0:
        app_rate_in_comm_in_comm_prior_to_app_not_campus_visit = round(numerator/denominator,3)
     else: app_rate_in_comm_in_comm_prior_to_app_not_campus_visit = ''
     
     #6.2
     #app_rate_not_in_comm_in_comm_as_app_or_after_not_campus_visit
     temp_df_1_numerator = not_in_comm_not_campus_visit_master_df[(not_in_comm_not_campus_visit_master_df['ZM.Applied'] == 1)]
     temp_df_2_numerator = in_comm_not_campus_visit_master_df[(in_comm_not_campus_visit_master_df['ZM.Applied'] == 1)]
     temp_df_2_numerator = temp_df_2_numerator[
          (temp_df_2_numerator['ZM.Joined.Stage'] == '03 APPLIED') |
          (temp_df_2_numerator['ZM.Joined.Stage'] == '04 APP COMPLETE') |
          (temp_df_2_numerator['ZM.Joined.Stage'] == '05 ACCEPTED') |
          (temp_df_2_numerator['ZM.Joined.Stage'] == '06 COMMITTED')
          ]
     numerator = len(pd.concat([temp_df_1_numerator,temp_df_2_numerator]))
     
     temp_df_1_denominator = not_in_comm_not_campus_visit_master_df[(not_in_comm_not_campus_visit_master_df['ZM.Inquired'] == 1)]
     temp_df_2_denominator = in_comm_not_campus_visit_master_df[(in_comm_not_campus_visit_master_df['ZM.Inquired'] == 1)]
     temp_df_2_denominator = temp_df_2_denominator[
          (temp_df_2_denominator['ZM.Joined.Stage'] == '03 APPLIED') |
          (temp_df_2_denominator['ZM.Joined.Stage'] == '04 APP COMPLETE') |
          (temp_df_2_denominator['ZM.Joined.Stage'] == '05 ACCEPTED') |
          (temp_df_2_denominator['ZM.Joined.Stage'] == '06 COMMITTED')]
     denominator = len(pd.concat([temp_df_1_denominator,temp_df_2_denominator]))
    
     if denominator>0:
        app_rate_not_in_comm_in_comm_as_app_or_after_not_campus_visit = round(numerator/denominator,3)
     else: app_rate_not_in_comm_in_comm_as_app_or_after_not_campus_visit = ''
     
     
     #6.3
     #app_rate_never_in_community_not_campus_visit
     denominator = len(not_in_comm_not_campus_visit_master_df[not_in_comm_not_campus_visit_master_df['ZM.Inquired'] == 1])
     if denominator >0:
          numerator = len(not_in_comm_not_campus_visit_master_df[not_in_comm_not_campus_visit_master_df['ZM.Applied'] == 1])
          app_rate_never_in_community_not_campus_visit = round(numerator/denominator,3)
     else: app_rate_never_in_community_not_campus_visit = ''
     
     function_dataframe['app_rate_in_comm_in_comm_prior_to_app_not_campus_visit'] = [app_rate_in_comm_in_comm_prior_to_app_not_campus_visit]
     function_dataframe['app_rate_not_in_comm_in_comm_as_app_or_after_not_campus_visit'] = [app_rate_not_in_comm_in_comm_as_app_or_after_not_campus_visit]
     function_dataframe['app_rate_never_in_community_not_campus_visit'] = [app_rate_never_in_community_not_campus_visit]
     #___________________________________
     
     return function_dataframe
