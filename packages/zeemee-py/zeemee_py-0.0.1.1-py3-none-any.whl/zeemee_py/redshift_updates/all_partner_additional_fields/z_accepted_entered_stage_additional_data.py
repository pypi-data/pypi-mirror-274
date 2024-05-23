def get_accepted_entered_stage_df(master_df, master_df_filtered, not_in_community_df):
     import pandas as pd
     import numpy as np
     pd.options.mode.chained_assignment = None
     
     accepted_entered_stage_list = [
     'accepted_community_entered_term_pre_inquired',
     'accepted_community_entered_term_inquired',
     'accepted_community_entered_term_applied',
     'accepted_community_entered_term_app_completed',
     'accepted_community_entered_term_accepted',
     'accepted_community_entered_term_committed',
     'accepted_community_entered_term_stage_missing',
     
     'percent_accepted_community_entered_term_pre_inquired',
     'percent_accepted_community_entered_term_inquired',
     'percent_accepted_community_entered_term_applied',
     'percent_accepted_community_entered_term_app_completed',
     'percent_accepted_community_entered_term_accepted',
     'percent_accepted_community_entered_term_committed',
     'percent_accepted_community_entered_term_stage_missing'
     ]
     
     in_comm_accepted = master_df[(master_df['ZM.Community'] == 'Community') &
                                  (master_df['ZM.Accepted'] == 1)].reset_index(drop = True)
     
     #in_comm_accepted['ZM.Joined.Stage'] = in_comm_accepted['ZM.Joined.Stage'
     #                                                          ].fillna('07 DATE OF INITIAL CONTACT MISSING')
                                                          
     in_comm_accepted.fillna({'ZM.Joined.Stage': '07 DATE OF INITIAL CONTACT MISSING'}, inplace=True)
     
     list_4_values = list()
     
     if len(in_comm_accepted) == 0:
          list_4_values.append(np.NaN)
          list_4_values.append(np.NaN)
          list_4_values.append(np.NaN)
          list_4_values.append(np.NaN)
          list_4_values.append(np.NaN)
          list_4_values.append(np.NaN)
          list_4_values.append(np.NaN)
          
          list_4_values.append(np.NaN)
          list_4_values.append(np.NaN)
          list_4_values.append(np.NaN)
          list_4_values.append(np.NaN)
          list_4_values.append(np.NaN)
          list_4_values.append(np.NaN)
          list_4_values.append(np.NaN)
        
     else:
          list_4_values.append(str(int(len(in_comm_accepted[in_comm_accepted['ZM.Joined.Stage'] == '01 PRE-INQUIRED']))))
          list_4_values.append(str(int(len(in_comm_accepted[in_comm_accepted['ZM.Joined.Stage'] == '02 INQUIRED']))))
          list_4_values.append(str(int(len(in_comm_accepted[in_comm_accepted['ZM.Joined.Stage'] == '03 APPLIED']))))
          list_4_values.append(str(int(len(in_comm_accepted[in_comm_accepted['ZM.Joined.Stage'] == '04 APP COMPLETE']))))
          list_4_values.append(str(int(len(in_comm_accepted[in_comm_accepted['ZM.Joined.Stage'] == '05 ACCEPTED']))))
          list_4_values.append(str(int(len(in_comm_accepted[in_comm_accepted['ZM.Joined.Stage'] == '06 COMMITTED']))))
          list_4_values.append(str(int(len(in_comm_accepted[in_comm_accepted['ZM.Joined.Stage'] == '07 DATE OF INITIAL CONTACT MISSING']))))
                                                       
                                                       
          total_accepted = len(in_comm_accepted)
          
          list_4_values.append(len(in_comm_accepted[in_comm_accepted['ZM.Joined.Stage'] == '01 PRE-INQUIRED'])/total_accepted )
          list_4_values.append(len(in_comm_accepted[in_comm_accepted['ZM.Joined.Stage'] == '02 INQUIRED'])/total_accepted )
          list_4_values.append(len(in_comm_accepted[in_comm_accepted['ZM.Joined.Stage'] == '03 APPLIED'])/total_accepted )
          list_4_values.append(len(in_comm_accepted[in_comm_accepted['ZM.Joined.Stage'] == '04 APP COMPLETE'])/total_accepted )
          list_4_values.append(len(in_comm_accepted[in_comm_accepted['ZM.Joined.Stage'] == '05 ACCEPTED'])/total_accepted )
          list_4_values.append(len(in_comm_accepted[in_comm_accepted['ZM.Joined.Stage'] == '06 COMMITTED'])/total_accepted )
          list_4_values.append(len(in_comm_accepted[in_comm_accepted['ZM.Joined.Stage'] == '07 DATE OF INITIAL CONTACT MISSING'])/total_accepted )                                                        

     function_df = pd.DataFrame()
     for i in range(len(accepted_entered_stage_list)):
          function_df[accepted_entered_stage_list[i]] = [list_4_values[i]]
     
     return function_df
     


