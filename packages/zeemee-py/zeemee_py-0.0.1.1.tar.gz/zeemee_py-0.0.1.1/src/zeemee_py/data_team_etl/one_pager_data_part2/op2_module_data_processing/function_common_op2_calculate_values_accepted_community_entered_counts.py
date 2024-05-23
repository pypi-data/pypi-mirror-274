

def get_op_values_accepted_community_entered_values(zeemee_tp_data):
     import pandas as pd
     import sys
     import importlib
     
     sys.dont_write_bytecode = True
     
     #__________________________________
     
     function_dataframe = pd.DataFrame()
     zeemee_tp_data['Community.Join.Stage'] = zeemee_tp_data['Community.Join.Stage'].replace('','07 DATE OF INITIAL CONTACT MISSING')
     accepted_zeemee_tp_data = zeemee_tp_data[zeemee_tp_data['ZM.Accepted'] == 1].reset_index(drop = True)
     #___________________________________ 1
     
     [
          'accepted_community_entered_pre_inquired',
          'accepted_community_entered_inquired',
          'accepted_community_entered_applied',
          'accepted_community_entered_app_completed',
          'accepted_community_entered_accepted',
          'accepted_community_entered_committed',
          'accepted_community_entered_stage_missing'
          ]
          
          
     accepted_community_entered_pre_inquired = len(accepted_zeemee_tp_data[accepted_zeemee_tp_data['Community.Join.Stage'] == '01 PRE-INQUIRED'])
     accepted_community_entered_inquired = len(accepted_zeemee_tp_data[accepted_zeemee_tp_data['Community.Join.Stage'] == '02 INQUIRED'])
     accepted_community_entered_applied = len(accepted_zeemee_tp_data[accepted_zeemee_tp_data['Community.Join.Stage'] == '03 APPLIED'])
     accepted_community_entered_app_complete = len(accepted_zeemee_tp_data[accepted_zeemee_tp_data['Community.Join.Stage'] == '04 APP COMPLETE'])
     accepted_community_entered_accepted = len(accepted_zeemee_tp_data[accepted_zeemee_tp_data['Community.Join.Stage'] == '05 ACCEPTED'])
     accepted_community_entered_committed = len(accepted_zeemee_tp_data[accepted_zeemee_tp_data['Community.Join.Stage'] == '06 COMMITTED'])
     accepted_community_entered_stage_missing = len(accepted_zeemee_tp_data[accepted_zeemee_tp_data['Community.Join.Stage'] == '07 DATE OF INITIAL CONTACT MISSING'])
     
     function_dataframe['accepted_community_entered_pre_inquired'] = [accepted_community_entered_pre_inquired]
     function_dataframe['accepted_community_entered_inquired'] = [accepted_community_entered_inquired]
     function_dataframe['accepted_community_entered_applied'] = [accepted_community_entered_applied]
     function_dataframe['accepted_community_entered_app_complete'] = [accepted_community_entered_app_complete]
     function_dataframe['accepted_community_entered_accepted'] = [accepted_community_entered_accepted]
     function_dataframe['accepted_community_entered_committed'] = [accepted_community_entered_committed]
     function_dataframe['accepted_community_entered_stage_missing'] = [accepted_community_entered_stage_missing]
     
     
     #___________________________________ 2
     
     [
          'percent_accepted_community_entered_pre_inquired',
          'percent_accepted_community_entered_inquired',
          'percent_accepted_community_entered_applied',
          'percent_accepted_community_entered_app_complete',
          'percent_accepted_community_entered_accepted',
          'percent_accepted_community_entered_committed',
          'percent_accepted_community_entered_stage_missing'
          ]
          
     total_accepted = len(accepted_zeemee_tp_data)
     
     if total_accepted> 0:
          percent_accepted_community_entered_pre_inquired = accepted_community_entered_pre_inquired/total_accepted
          percent_accepted_community_entered_inquired = accepted_community_entered_inquired/total_accepted
          percent_accepted_community_entered_applied = accepted_community_entered_applied/total_accepted
          percent_accepted_community_entered_app_complete = accepted_community_entered_app_complete/total_accepted
          percent_accepted_community_entered_accepted = accepted_community_entered_accepted/total_accepted
          percent_accepted_community_entered_committed = accepted_community_entered_committed/total_accepted
          percent_accepted_community_entered_stage_missing = accepted_community_entered_stage_missing/total_accepted
     else:
          percent_accepted_community_entered_pre_inquired = ""
          percent_accepted_community_entered_inquired = ""
          percent_accepted_community_entered_applied = ""
          percent_accepted_community_entered_app_complete = ""
          percent_accepted_community_entered_accepted = ""
          percent_accepted_community_entered_committed = ""
          percent_accepted_community_entered_stage_missing = ""
          
     
     function_dataframe['percent_accepted_community_entered_pre_inquired'] = [percent_accepted_community_entered_pre_inquired]
     function_dataframe['percent_accepted_community_entered_inquired'] = [percent_accepted_community_entered_inquired]
     function_dataframe['percent_accepted_community_entered_applied'] = [percent_accepted_community_entered_applied]
     function_dataframe['percent_accepted_community_entered_app_complete'] = [percent_accepted_community_entered_app_complete]
     function_dataframe['percent_accepted_community_entered_accepted'] = [percent_accepted_community_entered_accepted]
     function_dataframe['percent_accepted_community_entered_committed'] = [percent_accepted_community_entered_committed]
     function_dataframe['percent_accepted_community_entered_stage_missing'] = [percent_accepted_community_entered_stage_missing]
     
     #___________________________________ 
     
     
     return function_dataframe
