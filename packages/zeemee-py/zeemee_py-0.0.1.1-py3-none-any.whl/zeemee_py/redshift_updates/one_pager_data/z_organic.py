
def get_organic_data(zeemee_tp_data):
     import pandas as pd
     df = pd.DataFrame()
     
     num_organic_inquired = len(zeemee_tp_data[(zeemee_tp_data['organic_at'].notnull()) & (zeemee_tp_data['ZM.Inquired'] == 1)])
     df['num_organic_inquired'] = [num_organic_inquired]
     
     num_organic_applied = len(zeemee_tp_data[(zeemee_tp_data['organic_at'].notnull()) & (zeemee_tp_data['ZM.Applied'] == 1)])
     df['num_organic_applied'] = [num_organic_applied]
     
     num_organic_accepted = len(zeemee_tp_data[(zeemee_tp_data['organic_at'].notnull()) & (zeemee_tp_data['ZM.Accepted'] == 1)])
     df['num_organic_accepted'] = [num_organic_accepted]
     
     num_organic_committed = len(zeemee_tp_data[(zeemee_tp_data['organic_at'].notnull()) & (zeemee_tp_data['ZM.Committed'] == 1)])
     df['num_organic_committed'] = [num_organic_committed]
     
     num_organic_enrolled = len(zeemee_tp_data[(zeemee_tp_data['organic_at'].notnull()) & (zeemee_tp_data['ZM.Enrolled'] == 1)])
     df['num_organic_enrolled'] = [num_organic_enrolled]
     
     #starting % count calculations
     community_funnel_inquired = len(zeemee_tp_data[zeemee_tp_data['ZM.Inquired'] == 1])
     community_funnel_applied = len(zeemee_tp_data[zeemee_tp_data['ZM.Applied'] == 1])
     community_funnel_accepted = len(zeemee_tp_data[zeemee_tp_data['ZM.Accepted'] == 1])
     community_funnel_committed = len(zeemee_tp_data[zeemee_tp_data['ZM.Committed'] == 1])
     community_funnel_enrolled = len(zeemee_tp_data[zeemee_tp_data['ZM.Enrolled'] == 1])
     
     if community_funnel_inquired > 0: 
          per_organic_inquired =	num_organic_inquired / community_funnel_inquired	
          df['per_organic_inquired'] = [per_organic_inquired]
     else:
          df['per_organic_inquired'] = ['']
     
     if community_funnel_applied > 0: 
          per_organic_applied =	num_organic_applied / community_funnel_applied	
          df['per_organic_applied'] = [per_organic_applied]
     else:
          df['per_organic_applied'] = ['']
     
     if community_funnel_accepted > 0: 
          per_organic_accepted =	num_organic_accepted / community_funnel_accepted		
          df['per_organic_accepted'] = [per_organic_accepted]
     else:
          df['per_organic_accepted'] = ['']
     
     if community_funnel_committed > 0: 
          per_organic_committed	= num_organic_committed / community_funnel_committed
          df['per_organic_committed'] = [per_organic_committed]
     else:
          df['per_organic_committed'] = ['']
     
     if community_funnel_enrolled > 0: 
          per_organic_enrolled	= num_organic_enrolled / community_funnel_enrolled
          df['per_organic_enrolled'] = [per_organic_enrolled]
     else:
          df['per_organic_enrolled'] = ['']
          
     return df
