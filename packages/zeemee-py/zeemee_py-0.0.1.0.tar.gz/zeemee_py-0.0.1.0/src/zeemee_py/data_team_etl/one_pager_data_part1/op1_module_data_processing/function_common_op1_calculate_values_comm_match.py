

def get_op_values_comm_match(zeemee_college_data):
     import pandas as pd
     import sys
     import importlib
     
     sys.dont_write_bytecode = True
     
     #__________________________________
     
     function_dataframe = pd.DataFrame()
     zeemee_college_data['Community.Join.Stage'] = zeemee_college_data['Community.Join.Stage'].replace('','07 DATE OF INITIAL CONTACT MISSING')
     comm_match_zeemee_college_data = zeemee_college_data[zeemee_college_data['Community.Match'] == 'Community Match'].reset_index(drop = True)
     #___________________________________ 1
     
     [
          'comm_match_inquired',
          'comm_match_applied',
          'comm_match_accepted',
          'comm_match_committed',
          'comm_match_enrolled'
          ]
     
     comm_match_inquired = len(comm_match_zeemee_college_data[comm_match_zeemee_college_data['ZM.Inquired'] == 1])
     comm_match_applied = len(comm_match_zeemee_college_data[comm_match_zeemee_college_data['ZM.Applied'] == 1])
     comm_match_accepted = len(comm_match_zeemee_college_data[comm_match_zeemee_college_data['ZM.Accepted'] == 1])
     comm_match_committed = len(comm_match_zeemee_college_data[comm_match_zeemee_college_data['ZM.Committed'] == 1])
     comm_match_enrolled = len(comm_match_zeemee_college_data[comm_match_zeemee_college_data['ZM.Enrolled'] == 1])
  
     function_dataframe['comm_match_inquired'] = [comm_match_inquired]
     function_dataframe['comm_match_applied'] = [comm_match_applied]
     function_dataframe['comm_match_accepted'] = [comm_match_accepted]
     function_dataframe['comm_match_committed'] = [comm_match_committed]
     function_dataframe['comm_match_enrolled'] = [comm_match_enrolled]
     
     
     #___________________________________ 2
     
     [
          'percent_comm_match_inquired',
          'percent_comm_match_applied',
          'percent_comm_match_accepted',
          'percent_comm_match_committed',
          'percent_comm_match_enrolled'
          ]
          
     community_funnel_inquired = len(zeemee_college_data[zeemee_college_data['ZM.Inquired'] == 1])
     community_funnel_applied = len(zeemee_college_data[zeemee_college_data['ZM.Applied'] == 1])
     community_funnel_accepted = len(zeemee_college_data[zeemee_college_data['ZM.Accepted'] == 1])
     community_funnel_committed = len(zeemee_college_data[zeemee_college_data['ZM.Committed'] == 1])
     community_funnel_enrolled = len(zeemee_college_data[zeemee_college_data['ZM.Enrolled'] == 1])
     
     if community_funnel_inquired > 0:
          percent_comm_match_inquired = round(comm_match_inquired / community_funnel_inquired,3)	
     else: percent_comm_match_inquired = ''
     
     if community_funnel_applied > 0: 
          percent_comm_match_applied = round(comm_match_applied / community_funnel_applied,3)	
     else: percent_comm_match_applied = ''
     
     if community_funnel_accepted > 0:
          percent_comm_match_accepted = round(comm_match_accepted / community_funnel_accepted,3)
     else: percent_comm_match_accepted = ''

     if community_funnel_committed > 0:
          percent_comm_match_committed = round(comm_match_committed / community_funnel_committed,3)
     else: percent_comm_match_committed = ''
     
     if community_funnel_enrolled > 0:
          percent_comm_match_enrolled = round(comm_match_enrolled / community_funnel_enrolled,3)
     else: percent_comm_match_enrolled = ''
     
     function_dataframe['percent_comm_match_inquired'] = [percent_comm_match_inquired]
     function_dataframe['percent_comm_match_applied'] = [percent_comm_match_applied]
     function_dataframe['percent_comm_match_accepted'] = [percent_comm_match_accepted]
     function_dataframe['percent_comm_match_committed'] = [percent_comm_match_committed]
     function_dataframe['percent_comm_match_enrolled'] = [percent_comm_match_enrolled]
     #___________________________________ 
     
     
     
     return function_dataframe
