

def get_op_values_committed_community_entered_values(zeemee_tp_data):
     import pandas as pd
     import sys
     import importlib
     
     sys.dont_write_bytecode = True
     
     #__________________________________
     
     function_dataframe = pd.DataFrame()
     zeemee_tp_data['Community.Join.Stage'] = zeemee_tp_data['Community.Join.Stage'].replace('','07 DATE OF INITIAL CONTACT MISSING')
     committed_zeemee_tp_data = zeemee_tp_data[zeemee_tp_data['ZM.Committed'] == 1].reset_index(drop = True)
     #___________________________________ 1
     
     [
          'committed_community_entered_pre_inquired',
          'committed_community_entered_inquired',
          'committed_community_entered_applied',
          'committed_community_entered_app_complete',
          'committed_community_entered_accepted',
          'committed_community_entered_committed',
          'committed_community_entered_stage_missing'
          ]
          
          
     committed_community_entered_pre_inquired = len(committed_zeemee_tp_data[committed_zeemee_tp_data['Community.Join.Stage'] == '01 PRE-INQUIRED'])
     committed_community_entered_inquired = len(committed_zeemee_tp_data[committed_zeemee_tp_data['Community.Join.Stage'] == '02 INQUIRED'])
     committed_community_entered_applied = len(committed_zeemee_tp_data[committed_zeemee_tp_data['Community.Join.Stage'] == '03 APPLIED'])
     committed_community_entered_app_complete = len(committed_zeemee_tp_data[committed_zeemee_tp_data['Community.Join.Stage'] == '04 APP COMPLETE'])
     committed_community_entered_accepted = len(committed_zeemee_tp_data[committed_zeemee_tp_data['Community.Join.Stage'] == '05 ACCEPTED'])
     committed_community_entered_committed = len(committed_zeemee_tp_data[committed_zeemee_tp_data['Community.Join.Stage'] == '06 COMMITTED'])
     committed_community_entered_stage_missing = len(committed_zeemee_tp_data[committed_zeemee_tp_data['Community.Join.Stage'] == '07 DATE OF INITIAL CONTACT MISSING'])
     
     function_dataframe['committed_community_entered_pre_inquired'] = [committed_community_entered_pre_inquired]
     function_dataframe['committed_community_entered_inquired'] = [committed_community_entered_inquired]
     function_dataframe['committed_community_entered_applied'] = [committed_community_entered_applied]
     function_dataframe['committed_community_entered_app_complete'] = [committed_community_entered_app_complete]
     function_dataframe['committed_community_entered_accepted'] = [committed_community_entered_accepted]
     function_dataframe['committed_community_entered_committed'] = [committed_community_entered_committed]
     function_dataframe['committed_community_entered_stage_missing'] = [committed_community_entered_stage_missing]
     
     
     #___________________________________ 2
     
     [
          'percent_committed_community_entered_pre_inquired',
          'percent_committed_community_entered_inquired',
          'percent_committed_community_entered_applied',
          'percent_committed_community_entered_app_complete',
          'percent_committed_community_entered_accepted',
          'percent_committed_community_entered_committed',
          'percent_committed_community_entered_stage_missing'
          ]
          
     total_committed = len(committed_zeemee_tp_data)
     
     if total_committed> 0:
          percent_committed_community_entered_pre_inquired = committed_community_entered_pre_inquired/total_committed
          percent_committed_community_entered_inquired = committed_community_entered_inquired/total_committed
          percent_committed_community_entered_applied = committed_community_entered_applied/total_committed
          percent_committed_community_entered_app_complete = committed_community_entered_app_complete/total_committed
          percent_committed_community_entered_accepted = committed_community_entered_accepted/total_committed
          percent_committed_community_entered_committed = committed_community_entered_committed/total_committed
          percent_committed_community_entered_stage_missing = committed_community_entered_stage_missing/total_committed
     else:
          percent_committed_community_entered_pre_inquired = ""
          percent_committed_community_entered_inquired = ""
          percent_committed_community_entered_applied = ""
          percent_committed_community_entered_app_complete = ""
          percent_committed_community_entered_accepted = ""
          percent_committed_community_entered_committed = ""
          percent_committed_community_entered_stage_missing = ""
          
     
     function_dataframe['percent_committed_community_entered_pre_inquired'] = [percent_committed_community_entered_pre_inquired]
     function_dataframe['percent_committed_community_entered_inquired'] = [percent_committed_community_entered_inquired]
     function_dataframe['percent_committed_community_entered_applied'] = [percent_committed_community_entered_applied]
     function_dataframe['percent_committed_community_entered_app_complete'] = [percent_committed_community_entered_app_complete]
     function_dataframe['percent_committed_community_entered_accepted'] = [percent_committed_community_entered_accepted]
     function_dataframe['percent_committed_community_entered_committed'] = [percent_committed_community_entered_committed]
     function_dataframe['percent_committed_community_entered_stage_missing'] = [percent_committed_community_entered_stage_missing]
     
     #___________________________________ 
     
     
     return function_dataframe
