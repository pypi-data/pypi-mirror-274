

def get_op_values_inquired_community_entered_values(zeemee_tp_data):
     import pandas as pd
     import sys
     import importlib
     
     sys.dont_write_bytecode = True
     
     #__________________________________
     
     function_dataframe = pd.DataFrame()
     zeemee_tp_data['Community.Join.Stage'] = zeemee_tp_data['Community.Join.Stage'].replace('','07 DATE OF INITIAL CONTACT MISSING')
     inquired_zeemee_tp_data = zeemee_tp_data[zeemee_tp_data['ZM.Inquired'] == 1].reset_index(drop = True)
     #___________________________________ 1
     
     [
          'inquired_community_entered_pre_inquired',
          'inquired_community_entered_inquired',
          'inquired_community_entered_applied',
          'inquired_community_entered_app_complete',
          'inquired_community_entered_accepted',
          'inquired_community_entered_committed',
          'inquired_community_entered_stage_missing'
          ]
          
          
     inquired_community_entered_pre_inquired = len(inquired_zeemee_tp_data[inquired_zeemee_tp_data['Community.Join.Stage'] == '01 PRE-INQUIRED'])
     inquired_community_entered_inquired = len(inquired_zeemee_tp_data[inquired_zeemee_tp_data['Community.Join.Stage'] == '02 INQUIRED'])
     inquired_community_entered_applied = len(inquired_zeemee_tp_data[inquired_zeemee_tp_data['Community.Join.Stage'] == '03 APPLIED'])
     inquired_community_entered_app_complete = len(inquired_zeemee_tp_data[inquired_zeemee_tp_data['Community.Join.Stage'] == '04 APP COMPLETE'])
     inquired_community_entered_accepted = len(inquired_zeemee_tp_data[inquired_zeemee_tp_data['Community.Join.Stage'] == '05 ACCEPTED'])
     inquired_community_entered_committed = len(inquired_zeemee_tp_data[inquired_zeemee_tp_data['Community.Join.Stage'] == '06 COMMITTED'])
     inquired_community_entered_stage_missing = len(inquired_zeemee_tp_data[inquired_zeemee_tp_data['Community.Join.Stage'] == '07 DATE OF INITIAL CONTACT MISSING'])
     
     function_dataframe['inquired_community_entered_pre_inquired'] = [inquired_community_entered_pre_inquired]
     function_dataframe['inquired_community_entered_inquired'] = [inquired_community_entered_inquired]
     function_dataframe['inquired_community_entered_applied'] = [inquired_community_entered_applied]
     function_dataframe['inquired_community_entered_app_complete'] = [inquired_community_entered_app_complete]
     function_dataframe['inquired_community_entered_accepted'] = [inquired_community_entered_accepted]
     function_dataframe['inquired_community_entered_committed'] = [inquired_community_entered_committed]
     function_dataframe['inquired_community_entered_stage_missing'] = [inquired_community_entered_stage_missing]
     
     
     #___________________________________ 2
     
     [
          'percent_inquired_community_entered_pre_inquired',
          'percent_inquired_community_entered_inquired',
          'percent_inquired_community_entered_applied',
          'percent_inquired_community_entered_app_complete',
          'percent_inquired_community_entered_accepted',
          'percent_inquired_community_entered_committed',
          'percent_inquired_community_entered_stage_missing'
          ]
          
     total_inquired = len(inquired_zeemee_tp_data)
     
     if total_inquired> 0:
          percent_inquired_community_entered_pre_inquired = inquired_community_entered_pre_inquired/total_inquired
          percent_inquired_community_entered_inquired = inquired_community_entered_inquired/total_inquired
          percent_inquired_community_entered_applied = inquired_community_entered_applied/total_inquired
          percent_inquired_community_entered_app_complete = inquired_community_entered_app_complete/total_inquired
          percent_inquired_community_entered_accepted = inquired_community_entered_accepted/total_inquired
          percent_inquired_community_entered_committed = inquired_community_entered_committed/total_inquired
          percent_inquired_community_entered_stage_missing = inquired_community_entered_stage_missing/total_inquired
     else:
          percent_inquired_community_entered_pre_inquired = ""
          percent_inquired_community_entered_inquired = ""
          percent_inquired_community_entered_applied = ""
          percent_inquired_community_entered_app_complete = ""
          percent_inquired_community_entered_accepted = ""
          percent_inquired_community_entered_committed = ""
          percent_inquired_community_entered_stage_missing = ""
          
     
     function_dataframe['percent_inquired_community_entered_pre_inquired'] = [percent_inquired_community_entered_pre_inquired]
     function_dataframe['percent_inquired_community_entered_inquired'] = [percent_inquired_community_entered_inquired]
     function_dataframe['percent_inquired_community_entered_applied'] = [percent_inquired_community_entered_applied]
     function_dataframe['percent_inquired_community_entered_app_complete'] = [percent_inquired_community_entered_app_complete]
     function_dataframe['percent_inquired_community_entered_accepted'] = [percent_inquired_community_entered_accepted]
     function_dataframe['percent_inquired_community_entered_committed'] = [percent_inquired_community_entered_committed]
     function_dataframe['percent_inquired_community_entered_stage_missing'] = [percent_inquired_community_entered_stage_missing]
     
     #___________________________________ 
     
     
     return function_dataframe
