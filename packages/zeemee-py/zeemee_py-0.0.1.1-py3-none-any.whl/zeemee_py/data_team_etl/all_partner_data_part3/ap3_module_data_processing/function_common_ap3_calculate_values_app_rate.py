

def get_ap_values_app_rate(master_df):
     import pandas as pd
     import sys
     import importlib
     
     sys.dont_write_bytecode = True
     
     [
          'app_rate_never_in_community',
          'app_rate_never_in_community_sans_stealth',
          'app_rate_not_in_comm_and_in_comm_as_app_and_after',
          'app_rate_not_in_comm_and_in_comm_as_app_and_after_sans_stealth',
          'app_rate_in_comm_in_comm_prior_to_app'
          ]

     
     #__________________________________
     
     function_dataframe = pd.DataFrame()
     in_comm_master_df = master_df[master_df['ZM.Community'] == 'Community'].reset_index(drop = True)
     not_in_comm_master_df = master_df[master_df['ZM.Community'] == 'Not in Community'].reset_index(drop = True)
     
     in_comm_sans_stealth_df = in_comm_master_df[in_comm_master_df['ZM.Stealth.App'] == 'Not Stealth'].reset_index(drop = True)
     not_in_comm_sans_stealth_df = not_in_comm_master_df[not_in_comm_master_df['ZM.Stealth.App'] == 'Not Stealth'].reset_index(drop = True)
     
     #___________________________________ 1
     #1.1
     #app_rate_never_in_community
     numerator = len(not_in_comm_master_df[not_in_comm_master_df['ZM.Applied']== 1])
     denominator = len(not_in_comm_master_df[not_in_comm_master_df['ZM.Inquired']== 1])
    
     if denominator>0:
          app_rate_never_in_community = round(numerator/denominator,3)
     else: app_rate_never_in_community = ''
     
     
     #1.2
     #app_rate_never_in_community_sans_stealth
     numerator = len(not_in_comm_sans_stealth_df[not_in_comm_sans_stealth_df['ZM.Applied']== 1])
     denominator = len(not_in_comm_sans_stealth_df[not_in_comm_sans_stealth_df['ZM.Inquired']== 1])
     
     if denominator>0:
          app_rate_never_in_community_sans_stealth = round(numerator/denominator,3)
     else: app_rate_never_in_community_sans_stealth = ''
    
    
     #1.3
     #app_rate_not_in_comm_and_in_comm_as_app_and_after
     temp_df_1_numerator = not_in_comm_master_df[(not_in_comm_master_df['ZM.Applied']== 1)]
     temp_df_2_numerator = in_comm_master_df[(in_comm_master_df['ZM.Applied'] == 1)]
     temp_df_2_numerator = temp_df_2_numerator[
          (temp_df_2_numerator['ZM.Joined.Stage'] == '03 APPLIED') |
          (temp_df_2_numerator['ZM.Joined.Stage'] == '04 APP COMPLETE') |
          (temp_df_2_numerator['ZM.Joined.Stage'] == '05 ACCEPTED') |
          (temp_df_2_numerator['ZM.Joined.Stage'] == '06 COMMITTED')]
     numerator = len(pd.concat([temp_df_1_numerator,temp_df_2_numerator]))
     
     temp_df_1_denominator = not_in_comm_master_df[(not_in_comm_master_df['ZM.Inquired'] == 1)]
     temp_df_2_denominator = in_comm_master_df[(in_comm_master_df['ZM.Inquired'] == 1)]
     temp_df_2_denominator = temp_df_2_denominator[
          (temp_df_2_denominator['ZM.Joined.Stage'] == '03 APPLIED') |
          (temp_df_2_denominator['ZM.Joined.Stage'] == '04 APP COMPLETE') |
          (temp_df_2_denominator['ZM.Joined.Stage'] == '05 ACCEPTED') |
          (temp_df_2_denominator['ZM.Joined.Stage'] == '06 COMMITTED')]
     denominator = len(pd.concat([temp_df_1_denominator, temp_df_2_denominator]))
     
     if denominator>0:
         app_rate_not_in_comm_and_in_comm_as_app_and_after = round(numerator/denominator,3)
     else: app_rate_not_in_comm_and_in_comm_as_app_and_after = ''
     
     
     #1.4
     #app_rate_not_in_comm_and_in_comm_as_app_and_after_sans_stealth
     temp_df_1_numerator = not_in_comm_sans_stealth_df[(not_in_comm_sans_stealth_df['ZM.Applied']== 1)]
     temp_df_2_numerator = in_comm_sans_stealth_df[(in_comm_sans_stealth_df['ZM.Applied'] == 1)]
     temp_df_2_numerator = temp_df_2_numerator[
          (temp_df_2_numerator['ZM.Joined.Stage'] == '03 APPLIED') |
          (temp_df_2_numerator['ZM.Joined.Stage'] == '04 APP COMPLETE') |
          (temp_df_2_numerator['ZM.Joined.Stage'] == '05 ACCEPTED') |
          (temp_df_2_numerator['ZM.Joined.Stage'] == '06 COMMITTED')]
     numerator = len(pd.concat([temp_df_1_numerator,temp_df_2_numerator]))
     
     temp_df_1_denominator = not_in_comm_sans_stealth_df[(not_in_comm_sans_stealth_df['ZM.Inquired'] == 1)]
     temp_df_2_denominator = in_comm_sans_stealth_df[(in_comm_sans_stealth_df['ZM.Inquired'] == 1)]
     temp_df_2_denominator = temp_df_2_denominator[
          (temp_df_2_denominator['ZM.Joined.Stage'] == '03 APPLIED') |
          (temp_df_2_denominator['ZM.Joined.Stage'] == '04 APP COMPLETE') |
          (temp_df_2_denominator['ZM.Joined.Stage'] == '05 ACCEPTED') |
          (temp_df_2_denominator['ZM.Joined.Stage'] == '06 COMMITTED')]
     denominator = len(pd.concat([temp_df_1_denominator, temp_df_2_denominator]))
     
     if denominator>0:
         app_rate_not_in_comm_and_in_comm_as_app_and_after_sans_stealth = round(numerator/denominator,3)
     else: app_rate_not_in_comm_and_in_comm_as_app_and_after_sans_stealth = ''
     
     
     #1.5
     #app_rate_in_comm_in_comm_prior_to_app
     temp_df_1_numerator = in_comm_master_df[(in_comm_master_df['ZM.Applied']== 1)]
     temp_df_2_numerator = temp_df_1_numerator[
          (temp_df_1_numerator['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
          (temp_df_1_numerator['ZM.Joined.Stage'] == '02 INQUIRED')]
     numerator = len(temp_df_2_numerator)
     
     temp_df_1_denominator = in_comm_master_df[(in_comm_master_df['ZM.Inquired'] == 1)]
     temp_df_2_denominator = temp_df_1_denominator[
          (temp_df_1_denominator['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
          (temp_df_1_denominator['ZM.Joined.Stage'] == '02 INQUIRED') ]
     denominator = len(temp_df_2_denominator)
     
     if denominator>0:
         app_rate_in_comm_in_comm_prior_to_app = round(numerator/denominator,3)
     else: app_rate_in_comm_in_comm_prior_to_app = ''
     
     
     function_dataframe['app_rate_never_in_community'] = [app_rate_never_in_community]
     function_dataframe['app_rate_never_in_community_sans_stealth'] = [app_rate_never_in_community_sans_stealth]
     function_dataframe['app_rate_not_in_comm_and_in_comm_as_app_and_after'] = [app_rate_not_in_comm_and_in_comm_as_app_and_after]
     function_dataframe['app_rate_not_in_comm_and_in_comm_as_app_and_after_sans_stealth'] = [app_rate_not_in_comm_and_in_comm_as_app_and_after_sans_stealth]
     function_dataframe['app_rate_in_comm_in_comm_prior_to_app'] = [app_rate_in_comm_in_comm_prior_to_app]
     #___________________________________ 
     
     
     
     return function_dataframe
