

def get_ap_values_melt_rate(master_df):
     import pandas as pd
     import sys
     import importlib
     
     sys.dont_write_bytecode = True
     
     [
          'melt_rate_never_in_community',
          'melt_rate_in_comm_as_inquired',
          'melt_rate_in_comm_as_applied',
          'melt_rate_in_comm_as_comp_app',
          'melt_rate_in_comm_as_accepted',
          'melt_rate_in_comm_as_committed',
          ]

     
     #__________________________________
     
     function_dataframe = pd.DataFrame()
     in_comm_master_df = master_df[master_df['ZM.Community'] == 'Community'].reset_index(drop = True)
     not_in_comm_master_df = master_df[master_df['ZM.Community'] == 'Not in Community'].reset_index(drop = True)
     
     
     #___________________________________ 1
     #1.1
     #melt_rate_never_in_community
     numerator = len(not_in_comm_master_df[not_in_comm_master_df['ZM.Enrolled']== 1])
     denominator = len(not_in_comm_master_df[not_in_comm_master_df['ZM.Committed']== 1])
    
     if denominator>0:
          melt_rate_never_in_community = round((denominator-numerator)/denominator,3)
     else: melt_rate_never_in_community = ''
     
     #1.2
     #melt_rate_in_comm_as_inquired
     temp_df_1_numerator = in_comm_master_df[(in_comm_master_df['ZM.Enrolled']== 1)]
     temp_df_2_numerator = temp_df_1_numerator[
          (temp_df_1_numerator['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
          (temp_df_1_numerator['ZM.Joined.Stage'] == '02 INQUIRED')]
     numerator = len(temp_df_2_numerator)
     
     temp_df_1_denominator = in_comm_master_df[(in_comm_master_df['ZM.Committed'] == 1)]
     temp_df_2_denominator = temp_df_1_denominator[
          (temp_df_1_denominator['ZM.Joined.Stage'] == '01 PRE-INQUIRED') |
          (temp_df_1_denominator['ZM.Joined.Stage'] == '02 INQUIRED') ]
     denominator = len(temp_df_2_denominator)
     
     if denominator>0:
         melt_rate_in_comm_as_inquired = round((denominator-numerator)/denominator,3)
     else: melt_rate_in_comm_as_inquired = ''
     
     #1.3
     #melt_rate_in_comm_as_applied
     temp_df_1_numerator = in_comm_master_df[(in_comm_master_df['ZM.Enrolled']== 1)]
     temp_df_2_numerator = temp_df_1_numerator[
          (temp_df_1_numerator['ZM.Joined.Stage'] == '03 APPLIED')]
     numerator = len(temp_df_2_numerator)
     
     temp_df_1_denominator = in_comm_master_df[(in_comm_master_df['ZM.Committed'] == 1)]
     temp_df_2_denominator = temp_df_1_denominator[
          (temp_df_1_denominator['ZM.Joined.Stage'] == '03 APPLIED')]
     denominator = len(temp_df_2_denominator)
     
     if denominator>0:
         melt_rate_in_comm_as_applied = round((denominator-numerator)/denominator,3)
     else: melt_rate_in_comm_as_applied = ''
     
     #1.4
     #melt_rate_in_comm_as_comp_app
     temp_df_1_numerator = in_comm_master_df[(in_comm_master_df['ZM.Enrolled']== 1)]
     temp_df_2_numerator = temp_df_1_numerator[
          (temp_df_1_numerator['ZM.Joined.Stage'] == '04 APP COMPLETE')]
     numerator = len(temp_df_2_numerator)
     
     temp_df_1_denominator = in_comm_master_df[(in_comm_master_df['ZM.Committed'] == 1)]
     temp_df_2_denominator = temp_df_1_denominator[
          (temp_df_1_denominator['ZM.Joined.Stage'] == '04 APP COMPLETE')]
     denominator = len(temp_df_2_denominator)
     
     if denominator>0:
         melt_rate_in_comm_as_comp_app = round((denominator-numerator)/denominator,3)
     else: melt_rate_in_comm_as_comp_app = ''
     
     #1.5
     #melt_rate_in_comm_as_accepted
     temp_df_1_numerator = in_comm_master_df[(in_comm_master_df['ZM.Enrolled']== 1)]
     temp_df_2_numerator = temp_df_1_numerator[
          (temp_df_1_numerator['ZM.Joined.Stage'] == '05 ACCEPTED')]
     numerator = len(temp_df_2_numerator)
     
     temp_df_1_denominator = in_comm_master_df[(in_comm_master_df['ZM.Committed'] == 1)]
     temp_df_2_denominator = temp_df_1_denominator[
          (temp_df_1_denominator['ZM.Joined.Stage'] == '05 ACCEPTED')]
     denominator = len(temp_df_2_denominator)
     
     if denominator>0:
         melt_rate_in_comm_as_accepted = round((denominator-numerator)/denominator,3)
     else: melt_rate_in_comm_as_accepted = ''
     
     #1.6
     #melt_rate_in_comm_as_committed
     temp_df_1_numerator = in_comm_master_df[(in_comm_master_df['ZM.Enrolled']== 1)]
     temp_df_2_numerator = temp_df_1_numerator[
          (temp_df_1_numerator['ZM.Joined.Stage'] == '06 COMMITTED')]
     numerator = len(temp_df_2_numerator)
     
     temp_df_1_denominator = in_comm_master_df[(in_comm_master_df['ZM.Committed'] == 1)]
     temp_df_2_denominator = temp_df_1_denominator[
          (temp_df_1_denominator['ZM.Joined.Stage'] == '06 COMMITTED')]
     denominator = len(temp_df_2_denominator)
     
     if denominator>0:
         melt_rate_in_comm_as_committed = round((denominator-numerator)/denominator,3)
     else: melt_rate_in_comm_as_committed = ''
     
     function_dataframe['melt_rate_never_in_community'] = [melt_rate_never_in_community]
     function_dataframe['melt_rate_in_comm_as_inquired'] = [melt_rate_in_comm_as_inquired]
     function_dataframe['melt_rate_in_comm_as_applied'] = [melt_rate_in_comm_as_applied]
     function_dataframe['melt_rate_in_comm_as_comp_app'] = [melt_rate_in_comm_as_comp_app]
     function_dataframe['melt_rate_in_comm_as_accepted'] = [melt_rate_in_comm_as_accepted]
     function_dataframe['melt_rate_in_comm_as_committed'] = [melt_rate_in_comm_as_committed]
     #___________________________________ 
     
     
     
     return function_dataframe
