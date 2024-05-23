
def get_comm_entered_preinquired_data(zeemee_tp_data):
     import pandas as pd
     df = pd.DataFrame()
     pre_inq_df = zeemee_tp_data[(zeemee_tp_data['ZM.Joined.Stage'] == '01 PRE-INQUIRED')].reset_index(drop = True)
     
     num_preinq_inquired = len(pre_inq_df[pre_inq_df['ZM.Inquired'] == 1])
     df['num_preinq_inquired'] = [num_preinq_inquired]
     
     num_preinq_applied = len(pre_inq_df[pre_inq_df['ZM.Applied'] == 1])
     df['num_preinq_applied'] = [num_preinq_applied]
     
     num_preinq_accepted  = len(pre_inq_df[pre_inq_df['ZM.Accepted'] == 1])
     df['num_preinq_accepted'] = [num_preinq_accepted]
     
     num_preinq_committed  = len(pre_inq_df[pre_inq_df['ZM.Committed'] == 1])
     df['num_preinq_committed'] = [num_preinq_committed]
     
     num_preinq_enrolled  = len(pre_inq_df[pre_inq_df['ZM.Enrolled'] == 1])
     df['num_preinq_enrolled'] = [num_preinq_enrolled]
     
     
     #starting % count calculations
     community_funnel_inquired = len(zeemee_tp_data[zeemee_tp_data['ZM.Inquired'] == 1])
     community_funnel_applied = len(zeemee_tp_data[zeemee_tp_data['ZM.Applied'] == 1])
     community_funnel_accepted = len(zeemee_tp_data[zeemee_tp_data['ZM.Accepted'] == 1])
     community_funnel_committed = len(zeemee_tp_data[zeemee_tp_data['ZM.Committed'] == 1])
     community_funnel_enrolled = len(zeemee_tp_data[zeemee_tp_data['ZM.Enrolled'] == 1])
     
     if community_funnel_inquired > 0: 
          per_preinq_inquired	= num_preinq_inquired / community_funnel_inquired	
          df['per_preinq_inquired'] = [per_preinq_inquired]
     else:
          df['per_preinq_inquired'] = ['']
     
     if community_funnel_applied > 0: 
          per_preinq_applied = 	num_preinq_applied / community_funnel_applied	
          df['per_preinq_applied'] = [per_preinq_applied]
     else:
          df['per_preinq_applied'] = ['']
     
     if community_funnel_accepted > 0: 
          per_preinq_accepted	= num_preinq_accepted / community_funnel_accepted	
          df['per_preinq_accepted'] = [per_preinq_accepted]
     else:
          df['per_preinq_accepted'] = ['']
     
     if community_funnel_committed > 0: 
          per_preinq_committed =	num_preinq_committed / community_funnel_committed
          df['per_preinq_committed'] = [per_preinq_committed]
     else:
          df['per_preinq_committed'] = ['']
     
     if community_funnel_enrolled > 0: 
          per_preinq_enrolled	= num_preinq_enrolled / community_funnel_enrolled	
          df['per_preinq_enrolled'] = [per_preinq_enrolled]
     else:
          df['per_preinq_enrolled'] = ['']

     return df
