def calculate_values(master_df):
     
     import pandas as pd
     import importlib
     
     function_dataframe = pd.DataFrame()
     
     non_comm_master_df = master_df[master_df['ZM.Community'] == 'Not in Community'].reset_index(drop = True)
     comm_master_df = master_df[master_df['ZM.Community'] == 'Community'].reset_index(drop = True)

     #__________________________________
     total_funnel_inquired = len(master_df[master_df['ZM.Inquired'] == 1])
     total_funnel_applied = len(master_df[master_df['ZM.Applied'] == 1])
     total_funnel_comp_app = len(master_df[master_df['ZM.AppComplete'] == 1])
     total_funnel_accepted = len(master_df[master_df['ZM.Accepted'] == 1])
     total_funnel_committed = len(master_df[master_df['ZM.Committed'] == 1])
     total_funnel_net_committed_enrolled = len(master_df[master_df['ZM.Enrolled'] == 1])
     
     function_dataframe['total_funnel_inquired'] = [total_funnel_inquired]
     function_dataframe['total_funnel_applied'] = [total_funnel_applied]
     function_dataframe['total_funnel_comp_app'] = [total_funnel_comp_app]
     function_dataframe['total_funnel_accepted'] = [total_funnel_accepted]
     function_dataframe['total_funnel_deposit'] = [total_funnel_committed]
     function_dataframe['total_funnel_net_dep_enrolled'] = [total_funnel_net_committed_enrolled]
     #___________________________________
     
     
     #___________________________________
     non_comm_funnel_inquired = len(non_comm_master_df[non_comm_master_df['ZM.Inquired'] == 1])
     non_comm_funnel_applied = len(non_comm_master_df[non_comm_master_df['ZM.Applied'] == 1])
     non_comm_funnel_comp_app = len(non_comm_master_df[non_comm_master_df['ZM.AppComplete'] == 1])
     non_comm_funnel_accepted = len(non_comm_master_df[non_comm_master_df['ZM.Accepted'] == 1])
     non_comm_funnel_committed = len(non_comm_master_df[non_comm_master_df['ZM.Committed'] == 1])
     non_comm_funnel_net_committed_enrolled = len(non_comm_master_df[non_comm_master_df['ZM.Enrolled'] == 1])
     
     function_dataframe['non_comm_funnel_inquired'] = [non_comm_funnel_inquired]
     function_dataframe['non_comm_funnel_applied'] = [non_comm_funnel_applied]
     function_dataframe['non_comm_funnel_comp_app'] = [non_comm_funnel_comp_app]
     function_dataframe['non_comm_funnel_accepted'] = [non_comm_funnel_accepted]
     function_dataframe['non_comm_funnel_deposit'] = [non_comm_funnel_committed]
     function_dataframe['non_comm_funnel_net_dep_enrolled'] = [non_comm_funnel_net_committed_enrolled]
     #___________________________________

     
     #___________________________________
     comm_funnel_inquired = len(comm_master_df[comm_master_df['ZM.Inquired'] == 1])
     comm_funnel_applied = len(comm_master_df[comm_master_df['ZM.Applied'] == 1])
     comm_funnel_comp_app = len(comm_master_df[comm_master_df['ZM.AppComplete'] == 1])
     comm_funnel_accepted = len(comm_master_df[comm_master_df['ZM.Accepted'] == 1])
     comm_funnel_committed = len(comm_master_df[comm_master_df['ZM.Committed'] == 1])
     comm_funnel_net_committed_enrolled = len(comm_master_df[comm_master_df['ZM.Enrolled'] == 1])
     
     function_dataframe['community_funnel_inquired'] = [comm_funnel_inquired]
     function_dataframe['community_funnel_applied'] = [comm_funnel_applied]
     function_dataframe['community_funnel_comp_app'] = [comm_funnel_comp_app]
     function_dataframe['community_funnel_accepted'] = [comm_funnel_accepted]
     function_dataframe['community_funnel_deposit'] = [comm_funnel_committed]
     function_dataframe['community_funnel_net_dep_enrolled'] = [comm_funnel_net_committed_enrolled]
     #___________________________________
     
     
     #___________________________________
     if total_funnel_inquired > 0:
          percent_inquired_in_community = round(comm_funnel_inquired/total_funnel_inquired,3)
     else: percent_inquired_in_community = ''
     
     if total_funnel_applied > 0:
          percent_apps_in_community = round(comm_funnel_applied/total_funnel_applied,3)
     else: percent_apps_in_community = ''
     
     if total_funnel_comp_app > 0:
          percent_comp_app_in_community = round(comm_funnel_comp_app/total_funnel_comp_app,3)
     else: percent_comp_app_in_community = ''
     
     if total_funnel_accepted > 0:
          percent_accepts_in_community = round(comm_funnel_accepted/total_funnel_accepted,3)
     else: percent_accepts_in_community = ''
     
     if total_funnel_committed > 0:
          percent_commits_in_community = round(comm_funnel_committed/total_funnel_committed,3)
     else: percent_commits_in_community = ''
     
     if total_funnel_net_committed_enrolled > 0:
          percent_net_committed_enrolled_in_community = round(comm_funnel_net_committed_enrolled/total_funnel_net_committed_enrolled,3)
     else: percent_net_committed_enrolled_in_community = ''
     
     function_dataframe['percent_inq_in_community'] = [percent_inquired_in_community]
     function_dataframe['percent_apps_in_community'] = [percent_apps_in_community]
     function_dataframe['percent_comp_app_in_community'] = [percent_comp_app_in_community]
     function_dataframe['percent_accept_in_community'] = [percent_accepts_in_community]
     function_dataframe['percent_deposit_in_community'] = [percent_commits_in_community]
     function_dataframe['percent_net_dep_enr_in_community'] = [percent_net_committed_enrolled_in_community]
     #___________________________________

     #___________________________________
     
     if non_comm_funnel_inquired > 0:
          unadjusted_non_comm_app_rate = round(non_comm_funnel_applied/non_comm_funnel_inquired,3)
     else: unadjusted_non_comm_app_rate = ''
     
     if comm_funnel_inquired > 0:
          unadjusted_community_app_rate = round(comm_funnel_applied/comm_funnel_inquired,3)
     else: unadjusted_community_app_rate = ''
     
     if non_comm_funnel_accepted > 0:
          unadjusted_non_comm_committed_rate = round(non_comm_funnel_committed/non_comm_funnel_accepted,3)
     else: unadjusted_non_comm_committed_rate = ''
     
     if comm_funnel_accepted > 0:
          unadjusted_community_committed_rate = round(comm_funnel_committed/comm_funnel_accepted,3)
     else: unadjusted_community_committed_rate = ''
     
     if non_comm_funnel_committed > 0:
          unadjusted_non_comm_melt_rate = round(non_comm_funnel_net_committed_enrolled/non_comm_funnel_committed,3)
     else: unadjusted_non_comm_melt_rate = ''
     
     if comm_funnel_committed > 0:
          unadjusted_community_melt_rate = round(comm_funnel_net_committed_enrolled/comm_funnel_committed,3)
     else: unadjusted_community_melt_rate = ''
     
     if non_comm_funnel_accepted > 0:
          unadjusted_non_comm_yield_rate = round(non_comm_funnel_net_committed_enrolled/non_comm_funnel_accepted,3)
     else: unadjusted_non_comm_yield_rate = ''
     
     if comm_funnel_accepted > 0:
          unadjusted_community_yield_rate = round(comm_funnel_net_committed_enrolled/comm_funnel_accepted,3)
     else: unadjusted_community_yield_rate = ''
     
     function_dataframe['unadjusted_non_comm_app_rate'] = [unadjusted_non_comm_app_rate]
     function_dataframe['unadjusted_community_app_rate'] = [unadjusted_community_app_rate]
     function_dataframe['unadjusted_non_comm_dep_rate'] = [unadjusted_non_comm_committed_rate]
     function_dataframe['unadjusted_community_dep_rate'] = [unadjusted_community_committed_rate]
     function_dataframe['unadjusted_non_comm_melt_rate'] = [unadjusted_non_comm_melt_rate]
     function_dataframe['unadjusted_community_melt_rate'] = [unadjusted_community_melt_rate]
     function_dataframe['unadjusted_non_comm_yield_rate'] = [unadjusted_non_comm_yield_rate]
     function_dataframe['unadjusted_community_yield_rate'] = [unadjusted_community_yield_rate]
     #___________________________________

     #___________________________________
     
     try:
          comm_delta_app_rate_unadjusted  = round(unadjusted_community_app_rate - unadjusted_non_comm_app_rate,3)
     except: comm_delta_app_rate_unadjusted = ''
     
     try:
          comm_delta_committed_rate_unadjusted = round(unadjusted_community_committed_rate - unadjusted_non_comm_committed_rate,3)
     except: comm_delta_committed_rate_unadjusted= ''
     
     try:
          comm_delta_melt_rate_unadjusted = round(unadjusted_community_melt_rate - unadjusted_non_comm_melt_rate,3)
     except: comm_delta_melt_rate_unadjusted = ''
     
     try:
          comm_delta_yield_rate_unadjusted = round(unadjusted_community_yield_rate - unadjusted_non_comm_yield_rate,3)
     except: comm_delta_yield_rate_unadjusted= ''
     
     function_dataframe['comm_delta_app_rate_unadjusted'] = [comm_delta_app_rate_unadjusted]
     function_dataframe['comm_delta_dep_rate_unadjusted'] = [comm_delta_committed_rate_unadjusted]
     function_dataframe['comm_delta_melt_rate_unadjusted'] = [comm_delta_melt_rate_unadjusted]
     function_dataframe['comm_delta_yield_rate_unadjusted'] = [comm_delta_yield_rate_unadjusted]
    
     return function_dataframe
