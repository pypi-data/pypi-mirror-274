

def get_op_values_organic(zeemee_college_data):
     import pandas as pd
     import sys
     import importlib
     
     sys.dont_write_bytecode = True
     
     #__________________________________
     
     function_dataframe = pd.DataFrame()
     zeemee_college_data['Community.Join.Stage'] = zeemee_college_data['Community.Join.Stage'].replace('','07 DATE OF INITIAL CONTACT MISSING')
     organic_zeemee_college_data = zeemee_college_data[zeemee_college_data['organic_at'].notnull()].reset_index(drop = True)
     
     #___________________________________ 1
     
     [
          'organic_inquired',
          'organic_applied',
          'organic_accepted',
          'organic_committed',
          'organic_enrolled'
          ]
     
     organic_inquired = len(organic_zeemee_college_data[organic_zeemee_college_data['ZM.Inquired'] == 1])
     organic_applied = len(organic_zeemee_college_data[organic_zeemee_college_data['ZM.Applied'] == 1])
     organic_accepted = len(organic_zeemee_college_data[organic_zeemee_college_data['ZM.Accepted'] == 1])
     organic_committed = len(organic_zeemee_college_data[organic_zeemee_college_data['ZM.Committed'] == 1])
     organic_enrolled = len(organic_zeemee_college_data[organic_zeemee_college_data['ZM.Enrolled'] == 1])
  
     function_dataframe['organic_inquired'] = [organic_inquired]
     function_dataframe['organic_applied'] = [organic_applied]
     function_dataframe['organic_accepted'] = [organic_accepted]
     function_dataframe['organic_committed'] = [organic_committed]
     function_dataframe['organic_enrolled'] = [organic_enrolled]
     
     
     #___________________________________ 2
     
     [
          'percent_organic_inquired',
          'percent_organic_applied',
          'percent_organic_accepted',
          'percent_organic_committed',
          'percent_organic_enrolled'
          ]
          
     community_funnel_inquired = len(zeemee_college_data[zeemee_college_data['ZM.Inquired'] == 1])
     community_funnel_applied = len(zeemee_college_data[zeemee_college_data['ZM.Applied'] == 1])
     community_funnel_accepted = len(zeemee_college_data[zeemee_college_data['ZM.Accepted'] == 1])
     community_funnel_committed = len(zeemee_college_data[zeemee_college_data['ZM.Committed'] == 1])
     community_funnel_enrolled = len(zeemee_college_data[zeemee_college_data['ZM.Enrolled'] == 1])
     
     if community_funnel_inquired > 0:
          percent_organic_inquired = round(organic_inquired / community_funnel_inquired,3)	
     else: percent_organic_inquired = ''
     
     if community_funnel_applied > 0: 
          percent_organic_applied = round(organic_applied / community_funnel_applied,3)
     else: percent_organic_applied = ''
     
     if community_funnel_accepted > 0:
          percent_organic_accepted = round(organic_accepted / community_funnel_accepted,3)
     else: percent_organic_accepted = ''

     if community_funnel_committed > 0:
          percent_organic_committed = round(organic_committed / community_funnel_committed,3)
     else: percent_organic_committed = ''
     
     if community_funnel_enrolled > 0:
          percent_organic_enrolled = round(organic_enrolled / community_funnel_enrolled,3)
     else: percent_organic_enrolled = ''

     function_dataframe['percent_organic_inquired'] = [percent_organic_inquired]
     function_dataframe['percent_organic_applied'] = [percent_organic_applied]
     function_dataframe['percent_organic_accepted'] = [percent_organic_accepted]
     function_dataframe['percent_organic_committed'] = [percent_organic_committed]
     function_dataframe['percent_organic_enrolled'] = [percent_organic_enrolled]
     #___________________________________ 
     
     
     
     return function_dataframe
