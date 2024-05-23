def calculate_values(master_df):
     import pandas as pd
     import importlib
     

     [
          'commitment_rate_never_in_community',
          'commitment_rate_not_in_comm_in_comm_as_dep',
          'commitment_rate_in_comm_in_comm_prior_to_dep',
          'commitment_rate_in_comm_as_inquired',
          'commitment_rate_in_comm_as_applied',
          'commitment_rate_in_comm_as_comp_app',
          'commitment_rate_in_comm_as_accept'
          ]

     
     #__________________________________
     
     function_dataframe = pd.DataFrame()
     in_comm_master_df = master_df[master_df['ZM.Community'] == 'Community'].reset_index(drop = True)
     not_in_comm_master_df = master_df[master_df['ZM.Community'] == 'Not in Community'].reset_index(drop = True)
     
     
     #___________________________________ 1
     #1.1
     #commitment_rate_never_in_community
     numerator = len(not_in_comm_master_df[not_in_comm_master_df['ZM.Committed']== 1])
     denominator = len(not_in_comm_master_df[not_in_comm_master_df['ZM.Accepted']== 1])
    
     if denominator>0:
          commitment_rate_never_in_community = round(numerator/denominator,3)
     else: commitment_rate_never_in_community = ''
    
     #1.2
     #commitment_rate_not_in_comm_and_in_comm_as_committed
     temp_df_1_numerator = not_in_comm_master_df[(not_in_comm_master_df['ZM.Committed']== 1)]
     temp_df_2_numerator = master_df[(master_df['ZM.Committed'] == 1)]
     temp_df_2_numerator = temp_df_2_numerator[
         (temp_df_2_numerator['ZM.Joined.Stage'] == '06 COMMITTED')]
     numerator = len(pd.concat([temp_df_1_numerator,temp_df_2_numerator]))
     
     temp_df_1_denominator = not_in_comm_master_df[(not_in_comm_master_df['ZM.Accepted'] == 1)]
     temp_df_2_denominator = master_df[(master_df['ZM.Accepted'] == 1)]
     temp_df_2_denominator = temp_df_2_denominator[
         (temp_df_2_denominator['ZM.Joined.Stage'] == '06 COMMITTED')]
     denominator = len(pd.concat([temp_df_1_denominator, temp_df_2_denominator]))
     
     if denominator>0:
         commitment_rate_not_in_comm_and_in_comm_as_committed = round(numerator/denominator,3)
     else: commitment_rate_not_in_comm_and_in_comm_as_committed = ''
     
     #1.3
     #commitment_rate_in_comm_in_comm_prior_to_committed
     temp_df_1_numerator = in_comm_master_df[(in_comm_master_df['ZM.Committed']== 1)]
     temp_df_2_numerator = temp_df_1_numerator[
          (temp_df_1_numerator['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
          (temp_df_1_numerator['ZM.Joined.Stage'] == '02 INQUIRED') |
          (temp_df_1_numerator['ZM.Joined.Stage'] == '03 APPLIED') |
          (temp_df_1_numerator['ZM.Joined.Stage'] == '04 APP COMPLETE') |
          (temp_df_1_numerator['ZM.Joined.Stage'] == '05 ACCEPTED') ]
     numerator = len(temp_df_2_numerator)
     
     temp_df_1_denominator = in_comm_master_df[(in_comm_master_df['ZM.Accepted'] == 1)]
     temp_df_2_denominator = temp_df_1_denominator[
          (temp_df_1_denominator['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
          (temp_df_1_denominator['ZM.Joined.Stage'] == '02 INQUIRED') |
          (temp_df_1_denominator['ZM.Joined.Stage'] == '03 APPLIED') |
          (temp_df_1_denominator['ZM.Joined.Stage'] == '04 APP COMPLETE') |
          (temp_df_1_denominator['ZM.Joined.Stage'] == '05 ACCEPTED') ]
     denominator = len(temp_df_2_denominator)
     
     if denominator>0:
         commitment_rate_in_comm_in_comm_prior_to_committed = round(numerator/denominator,3)
     else: commitment_rate_in_comm_in_comm_prior_to_committed = ''
     
     #1.4
     #commitment_rate_in_comm_as_inquired
     temp_df_1_numerator = in_comm_master_df[(in_comm_master_df['ZM.Committed']== 1)]
     temp_df_2_numerator = temp_df_1_numerator[
          (temp_df_1_numerator['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
          (temp_df_1_numerator['ZM.Joined.Stage'] == '02 INQUIRED')]
     numerator = len(temp_df_2_numerator)
     
     temp_df_1_denominator = in_comm_master_df[(in_comm_master_df['ZM.Accepted'] == 1)]
     temp_df_2_denominator = temp_df_1_denominator[
          (temp_df_1_denominator['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
          (temp_df_1_denominator['ZM.Joined.Stage'] == '02 INQUIRED') ]
     denominator = len(temp_df_2_denominator)
     
     if denominator>0:
         commitment_rate_in_comm_as_inquired = round(numerator/denominator,3)
     else: commitment_rate_in_comm_as_inquired = ''
     
     #1.5
     #commitment_rate_in_comm_as_applied
     temp_df_1_numerator = in_comm_master_df[(in_comm_master_df['ZM.Committed']== 1)]
     temp_df_2_numerator = temp_df_1_numerator[
          (temp_df_1_numerator['ZM.Joined.Stage'] == '03 APPLIED')]
     numerator = len(temp_df_2_numerator)
     
     temp_df_1_denominator = in_comm_master_df[(in_comm_master_df['ZM.Accepted'] == 1)]
     temp_df_2_denominator = temp_df_1_denominator[
          (temp_df_1_denominator['ZM.Joined.Stage'] == '03 APPLIED')]
     denominator = len(temp_df_2_denominator)
     
     if denominator>0:
         commitment_rate_in_comm_as_applied = round(numerator/denominator,3)
     else: commitment_rate_in_comm_as_applied = ''
     
     #1.6
     #commitment_rate_in_comm_as_comp_app
     temp_df_1_numerator = in_comm_master_df[(in_comm_master_df['ZM.Committed']== 1)]
     temp_df_2_numerator = temp_df_1_numerator[
          (temp_df_1_numerator['ZM.Joined.Stage'] == '04 APP COMPLETE')]
     numerator = len(temp_df_2_numerator)
     
     temp_df_1_denominator = in_comm_master_df[(in_comm_master_df['ZM.Accepted'] == 1)]
     temp_df_2_denominator = temp_df_1_denominator[
          (temp_df_1_denominator['ZM.Joined.Stage'] == '04 APP COMPLETE')]
     denominator = len(temp_df_2_denominator)
     
     if denominator>0:
         commitment_rate_in_comm_as_comp_app = round(numerator/denominator,3)
     else: commitment_rate_in_comm_as_comp_app = ''
     
     #1.7
     #commitment_rate_in_comm_as_accepted
     temp_df_1_numerator = in_comm_master_df[(in_comm_master_df['ZM.Committed']== 1)]
     temp_df_2_numerator = temp_df_1_numerator[
          (temp_df_1_numerator['ZM.Joined.Stage'] == '05 ACCEPTED')]
     numerator = len(temp_df_2_numerator)
     
     temp_df_1_denominator = in_comm_master_df[(in_comm_master_df['ZM.Accepted'] == 1)]
     temp_df_2_denominator = temp_df_1_denominator[
          (temp_df_1_denominator['ZM.Joined.Stage'] == '05 ACCEPTED')]
     denominator = len(temp_df_2_denominator)
     
     if denominator>0:
         commitment_rate_in_comm_as_accepted = round(numerator/denominator,3)
     else: commitment_rate_in_comm_as_accepted = ''
     
     function_dataframe['commitment_rate_never_in_community'] = [commitment_rate_never_in_community]
     function_dataframe['commitment_rate_not_in_comm_in_comm_as_dep'] = [commitment_rate_not_in_comm_and_in_comm_as_committed]
     function_dataframe['commitment_rate_in_comm_in_comm_prior_to_dep'] = [commitment_rate_in_comm_in_comm_prior_to_committed]
     function_dataframe['commitment_rate_in_comm_as_inquired'] = [commitment_rate_in_comm_as_inquired]
     function_dataframe['commitment_rate_in_comm_as_applied'] = [commitment_rate_in_comm_as_applied]
     function_dataframe['commitment_rate_in_comm_as_comp_app'] = [commitment_rate_in_comm_as_comp_app]
     function_dataframe['commitment_rate_in_comm_as_accept'] = [commitment_rate_in_comm_as_accepted]
     #___________________________________ 
     
     
     
     return function_dataframe
