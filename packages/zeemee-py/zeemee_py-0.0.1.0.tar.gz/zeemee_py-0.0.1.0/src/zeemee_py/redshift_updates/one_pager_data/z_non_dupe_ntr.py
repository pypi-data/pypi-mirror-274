
def get_non_dupe_ntr_data(zeemee_tp_data):

     """
     The non dupe ntr is looking at everyone who is organic, 
     community matched and pre-inquired and removing duplicates as someone can be one or more.   
     That way we have a unique count between all three.
     """
     import pandas as pd
     import numpy as np
     df = pd.DataFrame()
     zeemee_tp_data_copy = zeemee_tp_data.copy()
     zeemee_tp_data_copy.replace("", np.nan, inplace=True)
     
     ntr_df = zeemee_tp_data_copy[
          (zeemee_tp_data_copy['created_by_csv'].notnull()) |
          (zeemee_tp_data_copy['organic_at'].notnull()) |
          (zeemee_tp_data_copy['ZM.Joined.Stage'] == '01 PRE-INQUIRED')
          ].reset_index(drop = True)
                        
     #print(len(ntr_df), len(zeemee_tp_data))
     
     num_nondupe_ntr_inquired = len(ntr_df[ntr_df['ZM.Inquired'] == 1])
     df['num_nondupe_ntr_inquired'] = [num_nondupe_ntr_inquired]
     
     num_nondupe_ntr_applied = len(ntr_df[ntr_df['ZM.Applied'] == 1])
     df['num_nondupe_ntr_applied'] = [num_nondupe_ntr_applied]
     
     num_nondupe_ntr_accepted  = len(ntr_df[ntr_df['ZM.Accepted'] == 1])
     df['num_nondupe_ntr_accepted'] = [num_nondupe_ntr_accepted]
     
     num_nondupe_ntr_committed  =len(ntr_df[ntr_df['ZM.Committed'] == 1])
     df['num_nondupe_ntr_committed'] = [num_nondupe_ntr_committed]
     
     num_nondupe_ntr_enrolled  = len(ntr_df[ntr_df['ZM.Enrolled'] == 1])
     df['num_nondupe_ntr_enrolled'] = [num_nondupe_ntr_enrolled]
     
     #starting % count calculations
     community_funnel_inquired = len(zeemee_tp_data[zeemee_tp_data['ZM.Inquired'] == 1])
     community_funnel_applied = len(zeemee_tp_data[zeemee_tp_data['ZM.Applied'] == 1])
     community_funnel_accepted = len(zeemee_tp_data[zeemee_tp_data['ZM.Accepted'] == 1])
     community_funnel_committed = len(zeemee_tp_data[zeemee_tp_data['ZM.Committed'] == 1])
     community_funnel_enrolled = len(zeemee_tp_data[zeemee_tp_data['ZM.Enrolled'] == 1])
     
     if community_funnel_inquired > 0: 
          per_nondupe_ntr_inquired =	num_nondupe_ntr_inquired / community_funnel_inquired	
          df['per_nondupe_ntr_inquired'] = [per_nondupe_ntr_inquired]
     else:
          df['per_nondupe_ntr_inquired'] = ['']
     
     if community_funnel_applied > 0: 
          per_nondupe_ntr_applied	= num_nondupe_ntr_applied / community_funnel_applied	
          df['per_nondupe_ntr_applied'] = [per_nondupe_ntr_applied]
     else:
          df['per_nondupe_ntr_applied'] = ['']
          
     if community_funnel_accepted > 0: 
          per_nondupe_ntr_accepted =	num_nondupe_ntr_accepted / community_funnel_accepted
          df['per_nondupe_ntr_accepted'] = [per_nondupe_ntr_accepted]
     else:
          df['per_nondupe_ntr_accepted'] = ['']
     
     if community_funnel_committed > 0: 
          per_nondupe_ntr_committed	= num_nondupe_ntr_committed / community_funnel_committed	
          df['per_nondupe_ntr_committed'] = [per_nondupe_ntr_committed]
     else:
          df['per_nondupe_ntr_committed'] = ['']
     
     if community_funnel_enrolled > 0: 
          per_nondupe_ntr_enrolled =	num_nondupe_ntr_enrolled / community_funnel_enrolled
          df['per_nondupe_ntr_enrolled'] = [per_nondupe_ntr_enrolled]
     else:
          df['per_nondupe_ntr_enrolled'] = ['']
     
     return df
