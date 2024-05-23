

def get_op_values_enrolled_community_entered_values(zeemee_tp_data):
     import pandas as pd
     import sys
     import importlib
     
     sys.dont_write_bytecode = True
     
     #__________________________________
     
     function_dataframe = pd.DataFrame()
     zeemee_tp_data['Community.Join.Stage'] = zeemee_tp_data['Community.Join.Stage'].replace('','07 DATE OF INITIAL CONTACT MISSING')
     enrolled_zeemee_tp_data = zeemee_tp_data[zeemee_tp_data['ZM.Enrolled'] == 1].reset_index(drop = True)
     #___________________________________ 1
     
     [
          'enrolled_community_entered_pre_inquired',
          'enrolled_community_entered_inquired',
          'enrolled_community_entered_applied',
          'enrolled_community_entered_app_complete',
          'enrolled_community_entered_accepted',
          'enrolled_community_entered_committed',
          'enrolled_community_entered_stage_missing'
          ]
          
          
     enrolled_community_entered_pre_inquired = len(enrolled_zeemee_tp_data[enrolled_zeemee_tp_data['Community.Join.Stage'] == '01 PRE-INQUIRED'])
     enrolled_community_entered_inquired = len(enrolled_zeemee_tp_data[enrolled_zeemee_tp_data['Community.Join.Stage'] == '02 INQUIRED'])
     enrolled_community_entered_applied = len(enrolled_zeemee_tp_data[enrolled_zeemee_tp_data['Community.Join.Stage'] == '03 APPLIED'])
     enrolled_community_entered_app_complete = len(enrolled_zeemee_tp_data[enrolled_zeemee_tp_data['Community.Join.Stage'] == '04 APP COMPLETE'])
     enrolled_community_entered_accepted = len(enrolled_zeemee_tp_data[enrolled_zeemee_tp_data['Community.Join.Stage'] == '05 ACCEPTED'])
     enrolled_community_entered_committed = len(enrolled_zeemee_tp_data[enrolled_zeemee_tp_data['Community.Join.Stage'] == '06 COMMITTED'])
     enrolled_community_entered_stage_missing = len(enrolled_zeemee_tp_data[enrolled_zeemee_tp_data['Community.Join.Stage'] == '07 DATE OF INITIAL CONTACT MISSING'])
     
     function_dataframe['enrolled_community_entered_pre_inquired'] = [enrolled_community_entered_pre_inquired]
     function_dataframe['enrolled_community_entered_inquired'] = [enrolled_community_entered_inquired]
     function_dataframe['enrolled_community_entered_applied'] = [enrolled_community_entered_applied]
     function_dataframe['enrolled_community_entered_app_complete'] = [enrolled_community_entered_app_complete]
     function_dataframe['enrolled_community_entered_accepted'] = [enrolled_community_entered_accepted]
     function_dataframe['enrolled_community_entered_committed'] = [enrolled_community_entered_committed]
     function_dataframe['enrolled_community_entered_stage_missing'] = [enrolled_community_entered_stage_missing]
     
     
     #___________________________________ 2
     
     [
          'percent_enrolled_community_entered_pre_inquired',
          'percent_enrolled_community_entered_inquired',
          'percent_enrolled_community_entered_applied',
          'percent_enrolled_community_entered_app_complete',
          'percent_enrolled_community_entered_accepted',
          'percent_enrolled_community_entered_committed',
          'percent_enrolled_community_entered_stage_missing'
          ]
          
     total_enrolled = len(enrolled_zeemee_tp_data)
     
     if total_enrolled> 0:
          percent_enrolled_community_entered_pre_inquired = enrolled_community_entered_pre_inquired/total_enrolled
          percent_enrolled_community_entered_inquired = enrolled_community_entered_inquired/total_enrolled
          percent_enrolled_community_entered_applied = enrolled_community_entered_applied/total_enrolled
          percent_enrolled_community_entered_app_complete = enrolled_community_entered_app_complete/total_enrolled
          percent_enrolled_community_entered_accepted = enrolled_community_entered_accepted/total_enrolled
          percent_enrolled_community_entered_committed = enrolled_community_entered_committed/total_enrolled
          percent_enrolled_community_entered_stage_missing = enrolled_community_entered_stage_missing/total_enrolled
     else:
          percent_enrolled_community_entered_pre_inquired = ""
          percent_enrolled_community_entered_inquired = ""
          percent_enrolled_community_entered_applied = ""
          percent_enrolled_community_entered_app_complete = ""
          percent_enrolled_community_entered_accepted = ""
          percent_enrolled_community_entered_committed = ""
          percent_enrolled_community_entered_stage_missing = ""
          
     
     function_dataframe['percent_enrolled_community_entered_pre_inquired'] = [percent_enrolled_community_entered_pre_inquired]
     function_dataframe['percent_enrolled_community_entered_inquired'] = [percent_enrolled_community_entered_inquired]
     function_dataframe['percent_enrolled_community_entered_applied'] = [percent_enrolled_community_entered_applied]
     function_dataframe['percent_enrolled_community_entered_app_complete'] = [percent_enrolled_community_entered_app_complete]
     function_dataframe['percent_enrolled_community_entered_accepted'] = [percent_enrolled_community_entered_accepted]
     function_dataframe['percent_enrolled_community_entered_committed'] = [percent_enrolled_community_entered_committed]
     function_dataframe['percent_enrolled_community_entered_stage_missing'] = [percent_enrolled_community_entered_stage_missing]
     
     #___________________________________ 
     
     
     return function_dataframe
