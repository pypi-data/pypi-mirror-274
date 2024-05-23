def get_applied_entered_term_df(master_df, master_df_filtered, not_in_community_df):
     import pandas as pd
     import numpy as np
     pd.options.mode.chained_assignment = None
     
     list_applied_entered_term = [
          'applied_community_entered_term_pre_inquired',
          'applied_community_entered_term_inquired',
          'applied_community_entered_term_applied',
          'applied_community_entered_term_app_complete',
          'applied_community_entered_term_accepted',
          'applied_community_entered_term_committed',
          'applied_community_entered_term_stage_missing',
          
          'percent_applied_community_entered_term_pre_inquired',
          'percent_applied_community_entered_term_inquired',
          'percent_applied_community_entered_term_applied',
          'percent_applied_community_entered_term_app_complete',
          'percent_applied_community_entered_term_accepted',
          'percent_applied_community_entered_term_committed',
          'percent_applied_community_entered_term_stage_missing'
          ]

     
     list_12_values = list()

     master_df_filtered['ZM.Applied'] = master_df_filtered['ZM.Applied'].astype(int)
     in_comm_applied = master_df_filtered[(master_df_filtered['ZM.Applied'] == 1)] #in community already filtered
     in_comm_applied.fillna({'ZM.Joined.Stage': '07 DATE OF INITIAL CONTACT MISSING'}, inplace=True)
     
     if len(in_comm_applied) == 0:
          list_12_values.append(np.NaN)
          list_12_values.append(np.NaN)
          list_12_values.append(np.NaN)
          list_12_values.append(np.NaN)
          list_12_values.append(np.NaN)
          list_12_values.append(np.NaN)
          list_12_values.append(np.NaN)
          
          list_12_values.append(np.NaN)
          list_12_values.append(np.NaN)
          list_12_values.append(np.NaN)
          list_12_values.append(np.NaN)
          list_12_values.append(np.NaN)
          list_12_values.append(np.NaN)
          list_12_values.append(np.NaN)
     else:
          list_12_values.append(str(int(len(in_comm_applied[in_comm_applied['ZM.Joined.Stage'] == '01 PRE-INQUIRED']))))
          list_12_values.append(str(int(len(in_comm_applied[in_comm_applied['ZM.Joined.Stage'] == '02 INQUIRED']))))
          list_12_values.append(str(int(len(in_comm_applied[in_comm_applied['ZM.Joined.Stage'] == '03 APPLIED']))))
          list_12_values.append(str(int(len(in_comm_applied[in_comm_applied['ZM.Joined.Stage'] == '04 APP COMPLETE']))))
          list_12_values.append(str(int(len(in_comm_applied[in_comm_applied['ZM.Joined.Stage'] == '05 ACCEPTED']))))
          list_12_values.append(str(int(len(in_comm_applied[in_comm_applied['ZM.Joined.Stage'] == '06 COMMITTED']))))
          list_12_values.append(str(int(len(in_comm_applied[in_comm_applied['ZM.Joined.Stage'] == '07 DATE OF INITIAL CONTACT MISSING']))))
          
          total_applied = len(in_comm_applied)
          
          list_12_values.append(str(int(len(in_comm_applied[in_comm_applied['ZM.Joined.Stage'] == '01 PRE-INQUIRED']))/total_applied))
          list_12_values.append(str(int(len(in_comm_applied[in_comm_applied['ZM.Joined.Stage'] == '02 INQUIRED']))/total_applied))
          list_12_values.append(str(int(len(in_comm_applied[in_comm_applied['ZM.Joined.Stage'] == '03 APPLIED']))/total_applied))
          list_12_values.append(str(int(len(in_comm_applied[in_comm_applied['ZM.Joined.Stage'] == '04 APP COMPLETE']))/total_applied))
          list_12_values.append(str(int(len(in_comm_applied[in_comm_applied['ZM.Joined.Stage'] == '05 ACCEPTED']))/total_applied))
          list_12_values.append(str(int(len(in_comm_applied[in_comm_applied['ZM.Joined.Stage'] == '06 COMMITTED']))/total_applied))
          list_12_values.append(str(int(len(in_comm_applied[in_comm_applied['ZM.Joined.Stage'] == '07 DATE OF INITIAL CONTACT MISSING']))/total_applied))

     function_df = pd.DataFrame()
     for i in range(len(list_applied_entered_term)):
          function_df[list_applied_entered_term[i]] = [list_12_values[i]]
          
     return function_df
    
