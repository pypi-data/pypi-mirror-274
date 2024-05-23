def calculate_values(master_df):
     import pandas as pd
     import importlib
     
     in_comm_master_df = master_df[(master_df['ZM.Community'] == 'Community')].reset_index(drop = True)

     [
     'community_entered_term_pre_inquired',
     'community_entered_term_inquired',
     'community_entered_term_applied',
     'community_entered_term_app_completed',
     'community_entered_term_accepted',
     'community_entered_term_committed',
     'community_entered_term_stage_missing',
     'percent_community_entered_term_pre_inquired',
     'percent_community_entered_term_inquired',
     'percent_community_entered_term_applied',
     'percent_community_entered_term_app_completed',
     'percent_community_entered_term_accepted',
     'percent_community_entered_term_committed',
     'percent_community_entered_term_stage_missing'
     ]

     function_dataframe = pd.DataFrame()
     in_comm_master_df = master_df[master_df['ZM.Community'] == 'Community'].reset_index(drop = True)
     not_in_comm_master_df = master_df[master_df['ZM.Community'] == 'Not in Community'].reset_index(drop = True)
     
     in_comm_master_df['ZM.Joined.Stage'] = in_comm_master_df['ZM.Joined.Stage'
                                                          ].fillna('07 DATE OF INITIAL CONTACT MISSING')
     
     community_entered_term_pre_inquired = len(in_comm_master_df[in_comm_master_df['ZM.Joined.Stage'] == '01 PRE-INQUIRED'])
     function_dataframe["community_entered_term_pre_inquired"] = [community_entered_term_pre_inquired]
          
     community_entered_term_inquired = len(in_comm_master_df[in_comm_master_df['ZM.Joined.Stage'] == '02 INQUIRED'])
     function_dataframe["community_entered_term_inquired"] = [community_entered_term_inquired]
          
     community_entered_term_applied = len(in_comm_master_df[in_comm_master_df['ZM.Joined.Stage'] == '03 APPLIED'])
     function_dataframe["community_entered_term_applied"] = [community_entered_term_applied]
          
     community_entered_term_app_completed = len(in_comm_master_df[in_comm_master_df['ZM.Joined.Stage'] == '04 APP COMPLETE'])
     function_dataframe["community_entered_term_app_completed"] = [community_entered_term_app_completed]
          
     community_entered_term_accepted = len(in_comm_master_df[in_comm_master_df['ZM.Joined.Stage'] == '05 ACCEPTED'])
     function_dataframe["community_entered_term_accepted"] = [community_entered_term_accepted]
          
     community_entered_term_committed = len(in_comm_master_df[in_comm_master_df['ZM.Joined.Stage'] == '06 COMMITTED'])
     function_dataframe["community_entered_term_committed"] = [community_entered_term_committed]
        
     community_entered_term_stage_missing = len(in_comm_master_df[in_comm_master_df['ZM.Joined.Stage'] == '07 DATE OF INITIAL CONTACT MISSING'])
     function_dataframe["community_entered_term_stage_missing"] = [community_entered_term_stage_missing]
     
     total_users_in_comm_master_df = len(in_comm_master_df)
     
     if total_users_in_comm_master_df > 0:
          percent_community_entered_term_pre_inquired = round(community_entered_term_pre_inquired / total_users_in_comm_master_df,3)   
          function_dataframe["percent_community_entered_term_pre_inquired"] = [percent_community_entered_term_pre_inquired]
          
          percent_community_entered_term_inquired = round(community_entered_term_inquired / total_users_in_comm_master_df,3)   
          function_dataframe["percent_community_entered_term_inquired"] = [percent_community_entered_term_inquired]
          
          percent_community_entered_term_applied = round(community_entered_term_applied / total_users_in_comm_master_df,3)   
          function_dataframe["percent_community_entered_term_applied"] = [percent_community_entered_term_applied]
          
          percent_community_entered_term_app_completed = round(community_entered_term_app_completed / total_users_in_comm_master_df,3)   
          function_dataframe["percent_community_entered_term_app_completed"] = [percent_community_entered_term_app_completed]
          
          percent_community_entered_term_accepted = round(community_entered_term_accepted / total_users_in_comm_master_df,3)   
          function_dataframe["percent_community_entered_term_accepted"] = [percent_community_entered_term_accepted]
          
          percent_community_entered_term_committed = round(community_entered_term_committed / total_users_in_comm_master_df,3)   
          function_dataframe["percent_community_entered_term_committed"] = [percent_community_entered_term_committed]
          
          percent_community_entered_term_stage_missing = round(community_entered_term_stage_missing / total_users_in_comm_master_df,3)   
          function_dataframe["percent_community_entered_term_stage_missing"] = [percent_community_entered_term_stage_missing]
            
     else:
          function_dataframe["percent_community_entered_term_pre_inquired"] = [""]
          function_dataframe["percent_community_entered_term_inquired"] = [""]
          function_dataframe["percent_community_entered_term_applied"] = [""]
          function_dataframe["percent_community_entered_term_app_completed"] = [""]
          function_dataframe["percent_community_entered_term_accepted"] = [""]
          function_dataframe["percent_community_entered_term_committed"] = [""]
          function_dataframe["percent_community_entered_term_stage_missing"] = [""]
          
     return function_dataframe
