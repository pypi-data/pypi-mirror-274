
def get_community_funnel_counts(zeemee_tp_data):
     import pandas as pd
     df = pd.DataFrame()
     
     community_funnel_inquired = len(zeemee_tp_data[zeemee_tp_data['ZM.Inquired'] == 1])
     df['community_funnel_inquired_1'] = [community_funnel_inquired]
     
     community_funnel_applied = len(zeemee_tp_data[zeemee_tp_data['ZM.Applied'] == 1])
     df['community_funnel_applied_1'] = [community_funnel_applied]
     
     community_funnel_accepted = len(zeemee_tp_data[zeemee_tp_data['ZM.Accepted'] == 1])
     df['community_funnel_accepted_1'] = [community_funnel_accepted]
     
     community_funnel_committed = len(zeemee_tp_data[zeemee_tp_data['ZM.Committed'] == 1])
     df['community_funnel_committed_1'] = [community_funnel_committed]
     
     community_funnel_enrolled = len(zeemee_tp_data[zeemee_tp_data['ZM.Enrolled'] == 1])
     df['community_funnel_enrolled_1'] = [community_funnel_enrolled]
     
     return df
