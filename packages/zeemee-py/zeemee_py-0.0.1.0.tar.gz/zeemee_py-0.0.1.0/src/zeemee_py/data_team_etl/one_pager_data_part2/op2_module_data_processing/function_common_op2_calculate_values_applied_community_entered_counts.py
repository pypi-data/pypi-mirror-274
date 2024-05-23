

def get_op_values_applied_community_entered_values(zeemee_tp_data):
     import pandas as pd
     import sys
     import importlib
     
     sys.dont_write_bytecode = True
     
     #__________________________________
     
     function_dataframe = pd.DataFrame()
     zeemee_tp_data['Community.Join.Stage'] = zeemee_tp_data['Community.Join.Stage'].replace('','07 DATE OF INITIAL CONTACT MISSING')
     applied_zeemee_tp_data = zeemee_tp_data[zeemee_tp_data['ZM.Applied'] == 1].reset_index(drop = True)
     #___________________________________ 1
     
     [
          'applied_community_entered_pre_inquired',
          'applied_community_entered_inquired',
          'applied_community_entered_applied',
          'applied_community_entered_app_completed',
          'applied_community_entered_accepted',
          'applied_community_entered_committed',
          'applied_community_entered_stage_missing'
          ]
          
          
     applied_community_entered_pre_inquired = len(applied_zeemee_tp_data[applied_zeemee_tp_data['Community.Join.Stage'] == '01 PRE-INQUIRED'])
     applied_community_entered_inquired = len(applied_zeemee_tp_data[applied_zeemee_tp_data['Community.Join.Stage'] == '02 INQUIRED'])
     applied_community_entered_applied = len(applied_zeemee_tp_data[applied_zeemee_tp_data['Community.Join.Stage'] == '03 APPLIED'])
     applied_community_entered_app_complete = len(applied_zeemee_tp_data[applied_zeemee_tp_data['Community.Join.Stage'] == '04 APP COMPLETE'])
     applied_community_entered_accepted = len(applied_zeemee_tp_data[applied_zeemee_tp_data['Community.Join.Stage'] == '05 ACCEPTED'])
     applied_community_entered_committed = len(applied_zeemee_tp_data[applied_zeemee_tp_data['Community.Join.Stage'] == '06 COMMITTED'])
     applied_community_entered_stage_missing = len(applied_zeemee_tp_data[applied_zeemee_tp_data['Community.Join.Stage'] == '07 DATE OF INITIAL CONTACT MISSING'])
     
     function_dataframe['applied_community_entered_pre_inquired'] = [applied_community_entered_pre_inquired]
     function_dataframe['applied_community_entered_inquired'] = [applied_community_entered_inquired]
     function_dataframe['applied_community_entered_applied'] = [applied_community_entered_applied]
     function_dataframe['applied_community_entered_app_complete'] = [applied_community_entered_app_complete]
     function_dataframe['applied_community_entered_accepted'] = [applied_community_entered_accepted]
     function_dataframe['applied_community_entered_committed'] = [applied_community_entered_committed]
     function_dataframe['applied_community_entered_stage_missing'] = [applied_community_entered_stage_missing]
     
     
     #___________________________________ 2
     
     [
          'percent_applied_community_entered_pre_inquired',
          'percent_applied_community_entered_inquired',
          'percent_applied_community_entered_applied',
          'percent_applied_community_entered_app_complete',
          'percent_applied_community_entered_accepted',
          'percent_applied_community_entered_committed',
          'percent_applied_community_entered_stage_missing'
          ]
          
     total_applied = len(applied_zeemee_tp_data)
     
     if total_applied> 0:
          percent_applied_community_entered_pre_inquired = applied_community_entered_pre_inquired/total_applied
          percent_applied_community_entered_inquired = applied_community_entered_inquired/total_applied
          percent_applied_community_entered_applied = applied_community_entered_applied/total_applied
          percent_applied_community_entered_app_complete = applied_community_entered_app_complete/total_applied
          percent_applied_community_entered_accepted = applied_community_entered_accepted/total_applied
          percent_applied_community_entered_committed = applied_community_entered_committed/total_applied
          percent_applied_community_entered_stage_missing = applied_community_entered_stage_missing/total_applied
     else:
          percent_applied_community_entered_pre_inquired = ""
          percent_applied_community_entered_inquired = ""
          percent_applied_community_entered_applied = ""
          percent_applied_community_entered_app_complete = ""
          percent_applied_community_entered_accepted = ""
          percent_applied_community_entered_committed = ""
          percent_applied_community_entered_stage_missing = ""
          
     
     function_dataframe['percent_applied_community_entered_pre_inquired'] = [percent_applied_community_entered_pre_inquired]
     function_dataframe['percent_applied_community_entered_inquired'] = [percent_applied_community_entered_inquired]
     function_dataframe['percent_applied_community_entered_applied'] = [percent_applied_community_entered_applied]
     function_dataframe['percent_applied_community_entered_app_complete'] = [percent_applied_community_entered_app_complete]
     function_dataframe['percent_applied_community_entered_accepted'] = [percent_applied_community_entered_accepted]
     function_dataframe['percent_applied_community_entered_committed'] = [percent_applied_community_entered_committed]
     function_dataframe['percent_applied_community_entered_stage_missing'] = [percent_applied_community_entered_stage_missing]
     
     #___________________________________ 
     
     
     return function_dataframe
