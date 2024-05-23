

def get_ap_values_missing_dates(master_df):
     import pandas as pd
     import sys
     import importlib
     
     sys.dont_write_bytecode = True
     
     [
          'percent_missing_inquired_date_in_comm',
          'percent_missing_applied_date_in_comm',
          'percent_missing_comp_app_date_in_comm',
          'percent_missing_accepted_date_in_comm',
          'percent_missing_committed_date_in_comm'
          ]

     
     #__________________________________
     
     function_dataframe = pd.DataFrame()
     in_comm_master_df = master_df[master_df['ZM.Community'] == 'Community'].reset_index(drop = True)
     not_in_comm_master_df = master_df[master_df['ZM.Community'] == 'Not in Community'].reset_index(drop = True)
        
     #___________________________________ 1
     #1.1
     #percent_missing_inquired_date_in_comm
     in_comm_master_df['Date.of.Initial.Contact'] = in_comm_master_df['Date.of.Initial.Contact'].fillna('not available')
     
     numerator = len(in_comm_master_df[(in_comm_master_df['ZM.Inquired']== 1) & (in_comm_master_df['Date.of.Initial.Contact'] == 'not available')])
     denominator = len(in_comm_master_df[in_comm_master_df['ZM.Inquired']== 1]) 
    
     if denominator>0:
          percent_missing_inquired_date_in_comm = round(numerator/denominator,3)
     else: percent_missing_inquired_date_in_comm = ''
     
     
     #1.2
     #percent_missing_applied_date_in_comm
     in_comm_master_df['Application.Date'] = in_comm_master_df['Application.Date'].fillna('not available')
        
     numerator = len(in_comm_master_df[(in_comm_master_df['ZM.Applied']== 1) & (in_comm_master_df['Application.Date'] == 'not available')])
     denominator = len(in_comm_master_df[in_comm_master_df['ZM.Applied']== 1]) 
    
     if denominator>0:
          percent_missing_applied_date_in_comm = round(numerator/denominator,3)
     else: percent_missing_applied_date_in_comm = ''
     
     #1.3
     #percent_missing_comp_app_date_in_comm
     in_comm_master_df['Application.Completed.Date'] = in_comm_master_df['Application.Completed.Date'].fillna('not available')
        
     numerator = len(in_comm_master_df[(in_comm_master_df['ZM.AppComplete']== 1) & (in_comm_master_df['Application.Completed.Date'] == 'not available')])
     denominator = len(in_comm_master_df[in_comm_master_df['ZM.AppComplete']== 1]) 
    
     if denominator>0:
          percent_missing_comp_app_date_in_comm = round(numerator/denominator,3)
     else: percent_missing_comp_app_date_in_comm = ''
     
     #1.4
     #percent_missing_accepted_date_in_comm
     in_comm_master_df['Accepted.Date'] = in_comm_master_df['Accepted.Date'].fillna('not available')
        
     numerator = len(in_comm_master_df[(in_comm_master_df['ZM.Accepted']== 1) & (in_comm_master_df['Accepted.Date'] == 'not available')])
     denominator = len(in_comm_master_df[in_comm_master_df['ZM.Accepted']== 1]) 
    
     if denominator>0:
          percent_missing_accepted_date_in_comm = round(numerator/denominator,3)
     else: percent_missing_accepted_date_in_comm = ''
     
     #1.5
     #percent_missing_committed_date_in_comm
     in_comm_master_df['Committed.Date'] = in_comm_master_df['Committed.Date'].fillna('not available')
        
     numerator = len(in_comm_master_df[(in_comm_master_df['ZM.Committed']== 1) & (in_comm_master_df['Committed.Date'] == 'not available')])
     denominator = len(in_comm_master_df[in_comm_master_df['ZM.Committed']== 1]) 
    
     if denominator>0:
          percent_missing_committed_date_in_comm = round(numerator/denominator,3)
     else: percent_missing_committed_date_in_comm = ''
     
     
     function_dataframe['percent_missing_inquired_date_in_comm'] = [percent_missing_inquired_date_in_comm]
     function_dataframe['percent_missing_applied_date_in_comm'] = [percent_missing_applied_date_in_comm]
     function_dataframe['percent_missing_comp_app_date_in_comm'] = [percent_missing_comp_app_date_in_comm]
     function_dataframe['percent_missing_accepted_date_in_comm'] = [percent_missing_accepted_date_in_comm]
     function_dataframe['percent_missing_committed_date_in_comm'] = [percent_missing_committed_date_in_comm]
     #___________________________________ 
     
     
     
     return function_dataframe
