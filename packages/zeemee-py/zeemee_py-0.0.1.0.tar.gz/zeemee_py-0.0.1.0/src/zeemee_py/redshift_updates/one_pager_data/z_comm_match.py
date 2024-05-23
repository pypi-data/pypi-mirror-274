
def get_comm_match_data(zeemee_tp_data):
     import pandas as pd
     df = pd.DataFrame()
     num_comm_match_inquired = len(zeemee_tp_data[(zeemee_tp_data['created_by_csv'] == 'Community Match') & (zeemee_tp_data['ZM.Inquired'] == 1)])
     df['num_comm_match_inquired'] = [num_comm_match_inquired]
     
     num_comm_match_applied = len(zeemee_tp_data[(zeemee_tp_data['created_by_csv'] == 'Community Match') & (zeemee_tp_data['ZM.Applied'] == 1)])
     df['num_comm_match_applied'] = [num_comm_match_applied]
     
     num_comm_match_accepted = len(zeemee_tp_data[(zeemee_tp_data['created_by_csv'] == 'Community Match') & (zeemee_tp_data['ZM.Accepted'] == 1)])
     df['num_comm_match_accepted'] = [num_comm_match_accepted]
     
     num_comm_match_committed = len(zeemee_tp_data[(zeemee_tp_data['created_by_csv'] == 'Community Match') & (zeemee_tp_data['ZM.Committed'] == 1)])
     df['num_comm_match_committed'] = [num_comm_match_committed]
     
     num_comm_match_enrolled = len(zeemee_tp_data[(zeemee_tp_data['created_by_csv'] == 'Community Match') & (zeemee_tp_data['ZM.Enrolled'] == 1)])
     df['num_comm_match_enrolled'] = [num_comm_match_enrolled]
     
     
     #starting % count calculations
     community_funnel_inquired = len(zeemee_tp_data[zeemee_tp_data['ZM.Inquired'] == 1])
     community_funnel_applied = len(zeemee_tp_data[zeemee_tp_data['ZM.Applied'] == 1])
     community_funnel_accepted = len(zeemee_tp_data[zeemee_tp_data['ZM.Accepted'] == 1])
     community_funnel_committed = len(zeemee_tp_data[zeemee_tp_data['ZM.Committed'] == 1])
     community_funnel_enrolled = len(zeemee_tp_data[zeemee_tp_data['ZM.Enrolled'] == 1])
     
     if community_funnel_inquired > 0:
          per_comm_match_inquired = 	num_comm_match_inquired / community_funnel_inquired
          df['per_comm_match_inquired'] = [per_comm_match_inquired]
     else:
          df['per_comm_match_inquired'] = ['']
     
     if community_funnel_applied > 0: 
          per_comm_match_applied = 	num_comm_match_applied / community_funnel_applied	
          df['per_comm_match_applied'] = [per_comm_match_applied]
     else:
          df['per_comm_match_applied'] = ['']
     
     if community_funnel_accepted > 0: 
          per_comm_match_accepted = 	num_comm_match_accepted / community_funnel_accepted
          df['per_comm_match_accepted'] = [per_comm_match_accepted]
     else:
          df['per_comm_match_accepted'] = ['']
     
     if community_funnel_committed > 0: 
          per_comm_match_committed = 	num_comm_match_committed / community_funnel_committed	
          df['per_comm_match_committed'] = [per_comm_match_committed]
     else:
          df['per_comm_match_committed'] = ['']
     
     if community_funnel_enrolled > 0: 
          per_comm_match_enrolled = num_comm_match_enrolled / community_funnel_enrolled	
          df['per_comm_match_enrolled'] = [per_comm_match_enrolled]
     else:
          df['per_comm_match_enrolled'] = ['']
          
     
     return df
