def get_enrolled_entered_term_df(master_df, master_df_filtered, not_in_community_df):
    import pandas as pd
    import numpy as np
    pd.options.mode.chained_assignment = None
    
    list_enrolled_entered_term = ['enrolled_community_entered_term_pre_inquired',
                      'enrolled_community_entered_term_inquired',
                      'enrolled_community_entered_term_applied',
                      'enrolled_community_entered_term_app_complete',
                      'enrolled_community_entered_term_accepted',
                      'enrolled_community_entered_term_committed',
                      'enrolled_community_entered_term_stage_missing',
                      
                      'percent_enrolled_community_entered_term_pre_inquired',
                      'percent_enrolled_community_entered_term_inquired',
                      'percent_enrolled_community_entered_term_applied',
                      'percent_enrolled_community_entered_term_app_complete',
                      'percent_enrolled_community_entered_term_accepted',
                      'percent_enrolled_community_entered_term_committed',
                      'percent_enrolled_community_entered_term_stage_missing',
                      
                      'committed_community_entered_term_pre_inquired',
                      'committed_community_entered_term_inquired',
                      'committed_community_entered_term_applied',
                      'committed_community_entered_term_app_complete',
                      'committed_community_entered_term_accepted',
                      'committed_community_entered_term_committed',
                      'committed_community_entered_term_stage_missing',
                      
                      'percent_committed_community_entered_term_pre_inquired',
                      'percent_committed_community_entered_term_inquired',
                      'percent_committed_community_entered_term_applied',
                      'percent_committed_community_entered_term_app_complete',
                      'percent_committed_community_entered_term_accepted',
                      'percent_committed_community_entered_term_committed',
                      'percent_committed_community_entered_term_stage_missing'
                     ]
    
    
    list_12_values = list()
    #master_df_filtered['ZM.Joined.Stage'] = master_df_filtered['ZM.Joined.Stage'].fillna('07 DATE OF INITIAL CONTACT MISSING')
    master_df_filtered.fillna({'ZM.Joined.Stage': '07 DATE OF INITIAL CONTACT MISSING'}, inplace=True)
    
    in_comm_enrolled = master_df_filtered[(master_df_filtered['ZM.Enrolled'] == 1)] #in community already filtered
    
    
    if len(in_comm_enrolled) == 0:
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
        list_12_values.append(str(int(len(in_comm_enrolled[in_comm_enrolled['ZM.Joined.Stage'] == '01 PRE-INQUIRED']))))
        list_12_values.append(str(int(len(in_comm_enrolled[in_comm_enrolled['ZM.Joined.Stage'] == '02 INQUIRED']))))
        list_12_values.append(str(int(len(in_comm_enrolled[in_comm_enrolled['ZM.Joined.Stage'] == '03 APPLIED']))))
        list_12_values.append(str(int(len(in_comm_enrolled[in_comm_enrolled['ZM.Joined.Stage'] == '04 APP COMPLETE']))))
        list_12_values.append(str(int(len(in_comm_enrolled[in_comm_enrolled['ZM.Joined.Stage'] == '05 ACCEPTED']))))
        list_12_values.append(str(int(len(in_comm_enrolled[in_comm_enrolled['ZM.Joined.Stage'] == '06 COMMITTED']))))
        list_12_values.append(str(int(len(in_comm_enrolled[in_comm_enrolled['ZM.Joined.Stage'] == '07 DATE OF INITIAL CONTACT MISSING']))))
        
        total_enrolled = len(in_comm_enrolled)
        
        list_12_values.append(str(int(len(in_comm_enrolled[in_comm_enrolled['ZM.Joined.Stage'] == '01 PRE-INQUIRED']))/total_enrolled))
        list_12_values.append(str(int(len(in_comm_enrolled[in_comm_enrolled['ZM.Joined.Stage'] == '02 INQUIRED']))/total_enrolled ))
        list_12_values.append(str(int(len(in_comm_enrolled[in_comm_enrolled['ZM.Joined.Stage'] == '03 APPLIED']))/total_enrolled ))
        list_12_values.append(str(int(len(in_comm_enrolled[in_comm_enrolled['ZM.Joined.Stage'] == '04 APP COMPLETE']))/total_enrolled ))
        list_12_values.append(str(int(len(in_comm_enrolled[in_comm_enrolled['ZM.Joined.Stage'] == '05 ACCEPTED']))/total_enrolled ))
        list_12_values.append(str(int(len(in_comm_enrolled[in_comm_enrolled['ZM.Joined.Stage'] == '06 COMMITTED']))/total_enrolled ))
        list_12_values.append(str(int(len(in_comm_enrolled[in_comm_enrolled['ZM.Joined.Stage'] == '07 DATE OF INITIAL CONTACT MISSING']))/total_enrolled ))
        
    in_comm_committed = master_df_filtered[(master_df_filtered['ZM.Committed'] == 1)] #in community already filtered
    
    if len(in_comm_committed) == 0:
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
        list_12_values.append(str(int(len(in_comm_committed[in_comm_committed['ZM.Joined.Stage'] == '01 PRE-INQUIRED']))))
        list_12_values.append(str(int(len(in_comm_committed[in_comm_committed['ZM.Joined.Stage'] == '02 INQUIRED']))))
        list_12_values.append(str(int(len(in_comm_committed[in_comm_committed['ZM.Joined.Stage'] == '03 APPLIED']))))
        list_12_values.append(str(int(len(in_comm_committed[in_comm_committed['ZM.Joined.Stage'] == '04 APP COMPLETE']))))
        list_12_values.append(str(int(len(in_comm_committed[in_comm_committed['ZM.Joined.Stage'] == '05 ACCEPTED']))))
        list_12_values.append(str(int(len(in_comm_committed[in_comm_committed['ZM.Joined.Stage'] == '06 COMMITTED']))))
        list_12_values.append(str(int(len(in_comm_committed[in_comm_committed['ZM.Joined.Stage'] == '07 DATE OF INITIAL CONTACT MISSING']))))
        
        total_committed = len(in_comm_committed)
        
        list_12_values.append(str(int(len(in_comm_committed[in_comm_committed['ZM.Joined.Stage'] == '01 PRE-INQUIRED']))/total_committed))
        list_12_values.append(str(int(len(in_comm_committed[in_comm_committed['ZM.Joined.Stage'] == '02 INQUIRED']))/total_committed ))
        list_12_values.append(str(int(len(in_comm_committed[in_comm_committed['ZM.Joined.Stage'] == '03 APPLIED']))/total_committed ))
        list_12_values.append(str(int(len(in_comm_committed[in_comm_committed['ZM.Joined.Stage'] == '04 APP COMPLETE']))/total_committed ))
        list_12_values.append(str(int(len(in_comm_committed[in_comm_committed['ZM.Joined.Stage'] == '05 ACCEPTED']))/total_committed ))
        list_12_values.append(str(int(len(in_comm_committed[in_comm_committed['ZM.Joined.Stage'] == '06 COMMITTED']))/total_committed ))
        list_12_values.append(str(int(len(in_comm_committed[in_comm_committed['ZM.Joined.Stage'] == '07 DATE OF INITIAL CONTACT MISSING']))/total_committed ))
    
    function_df = pd.DataFrame()
    for i in range(len(list_enrolled_entered_term)):
         function_df[list_enrolled_entered_term[i]] = [list_12_values[i]]
      
    return function_df
