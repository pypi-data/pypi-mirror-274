

def get_op_values_non_dupe_ntr(zeemee_college_data):
     import pandas as pd
     import sys
     import importlib
     import numpy as np
     
     sys.dont_write_bytecode = True
     
     #__________________________________
     
     function_dataframe = pd.DataFrame()
     zeemee_college_data['Community.Join.Stage'] = zeemee_college_data['Community.Join.Stage'].replace('','07 DATE OF INITIAL CONTACT MISSING')
     
     #non dupe ntr
     """
     The non dupe ntr is looking at everyone who is organic, 
     community matched and pre-inquired and removing duplicates as someone can be one or more.   
     That way we have a unique count between all three.
     """
     
     zeemee_college_data.replace("", np.nan, inplace=True)
     non_dupe_ntr_zeemee_college_data = zeemee_college_data[
          (zeemee_college_data['Community.Match'].notnull()) |
          (zeemee_college_data['organic_at'].notnull()) |
          (zeemee_college_data['Community.Join.Stage'] == '01 PRE-INQUIRED')
          ].reset_index(drop = True)
     
     #___________________________________ 1
     
     [
          'non_dupe_ntr_inquired',
          'non_dupe_ntr_applied',
          'non_dupe_ntr_accepted',
          'non_dupe_ntr_committed',
          'non_dupe_ntr_enrolled'
          ]
     
     non_dupe_ntr_inquired = len(non_dupe_ntr_zeemee_college_data[non_dupe_ntr_zeemee_college_data['ZM.Inquired'] == 1])
     non_dupe_ntr_applied = len(non_dupe_ntr_zeemee_college_data[non_dupe_ntr_zeemee_college_data['ZM.Applied'] == 1])
     non_dupe_ntr_accepted = len(non_dupe_ntr_zeemee_college_data[non_dupe_ntr_zeemee_college_data['ZM.Accepted'] == 1])
     non_dupe_ntr_committed = len(non_dupe_ntr_zeemee_college_data[non_dupe_ntr_zeemee_college_data['ZM.Committed'] == 1])
     non_dupe_ntr_enrolled = len(non_dupe_ntr_zeemee_college_data[non_dupe_ntr_zeemee_college_data['ZM.Enrolled'] == 1])
  
     function_dataframe['non_dupe_ntr_inquired'] = [non_dupe_ntr_inquired]
     function_dataframe['non_dupe_ntr_applied'] = [non_dupe_ntr_applied]
     function_dataframe['non_dupe_ntr_accepted'] = [non_dupe_ntr_accepted]
     function_dataframe['non_dupe_ntr_committed'] = [non_dupe_ntr_committed]
     function_dataframe['non_dupe_ntr_enrolled'] = [non_dupe_ntr_enrolled]
     
     
     #___________________________________ 2
     
     [
          'percent_non_dupe_ntr_inquired',
          'percent_non_dupe_ntr_applied',
          'percent_non_dupe_ntr_accepted',
          'percent_non_dupe_ntr_committed',
          'percent_non_dupe_ntr_enrolled'
          ]
          
     community_funnel_inquired = len(zeemee_college_data[zeemee_college_data['ZM.Inquired'] == 1])
     community_funnel_applied = len(zeemee_college_data[zeemee_college_data['ZM.Applied'] == 1])
     community_funnel_accepted = len(zeemee_college_data[zeemee_college_data['ZM.Accepted'] == 1])
     community_funnel_committed = len(zeemee_college_data[zeemee_college_data['ZM.Committed'] == 1])
     community_funnel_enrolled = len(zeemee_college_data[zeemee_college_data['ZM.Enrolled'] == 1])
     
     if community_funnel_inquired > 0:
          percent_non_dupe_ntr_inquired = round(non_dupe_ntr_inquired / community_funnel_inquired,3)	
     else: percent_non_dupe_ntr_inquired = ''
     
     if community_funnel_applied > 0: 
          percent_non_dupe_ntr_applied = round(non_dupe_ntr_applied / community_funnel_applied,3)
     else: percent_non_dupe_ntr_applied = ''
     
     if community_funnel_accepted > 0:
          percent_non_dupe_ntr_accepted = round(non_dupe_ntr_accepted / community_funnel_accepted,3)
     else: percent_non_dupe_ntr_accepted = ''

     if community_funnel_committed > 0:
          percent_non_dupe_ntr_committed = round(non_dupe_ntr_committed / community_funnel_committed,3)
     else: percent_non_dupe_ntr_committed = ''
     
     if community_funnel_enrolled > 0:
          percent_non_dupe_ntr_enrolled = round(non_dupe_ntr_enrolled / community_funnel_enrolled,3)
     else: percent_non_dupe_ntr_enrolled = ''
     
     function_dataframe['percent_non_dupe_ntr_inquired'] = [percent_non_dupe_ntr_inquired]
     function_dataframe['percent_non_dupe_ntr_applied'] = [percent_non_dupe_ntr_applied]
     function_dataframe['percent_non_dupe_ntr_accepted'] = [percent_non_dupe_ntr_accepted]
     function_dataframe['percent_non_dupe_ntr_committed'] = [percent_non_dupe_ntr_committed]
     function_dataframe['percent_non_dupe_ntr_enrolled'] = [percent_non_dupe_ntr_enrolled]
     #___________________________________ 
     
     
     
     return function_dataframe
