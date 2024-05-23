
def combine_individual_dfs(zeemee_tp_data, cohort_year, entry_term, student_type):
     import pandas as pd
     print(set(zeemee_tp_data['uos_transfer_status']))
     zeemee_tp_data = zeemee_tp_data[zeemee_tp_data["uos_start_term"] == entry_term].reset_index(drop = True)
     zeemee_tp_data = zeemee_tp_data[zeemee_tp_data["uos_transfer_status"] == student_type].reset_index(drop = True)
     zeemee_tp_data = zeemee_tp_data[zeemee_tp_data["uos_cohort_year"] == cohort_year].reset_index(drop = True)
     zeemee_tp_data["ZM.Joined.Stage"] = zeemee_tp_data["ZM.Joined.Stage"].fillna("07 DATE OF INITIAL CONTACT MISSING")
     zeemee_tp_data["ZM.Joined.Stage"] = zeemee_tp_data["ZM.Joined.Stage"].replace("","07 DATE OF INITIAL CONTACT MISSING")

     final_df = pd.DataFrame()
     
     from zeemee_py.redshift_updates.one_pager_data import z_comm_entered_preinquired
     df = z_comm_entered_preinquired.get_comm_entered_preinquired_data(zeemee_tp_data)
     final_df = pd.concat([final_df,df], axis=1).reset_index(drop = True)
     
     from zeemee_py.redshift_updates.one_pager_data import z_comm_match
     df = z_comm_match.get_comm_match_data(zeemee_tp_data)
     final_df = pd.concat([final_df,df], axis=1).reset_index(drop = True)
     
     from zeemee_py.redshift_updates.one_pager_data import z_community_funnel_counts
     df = z_community_funnel_counts.get_community_funnel_counts(zeemee_tp_data)
     final_df = pd.concat([final_df,df], axis=1).reset_index(drop = True)
     
     from zeemee_py.redshift_updates.one_pager_data import z_non_dupe_ntr
     df = z_non_dupe_ntr.get_non_dupe_ntr_data(zeemee_tp_data)
     final_df = pd.concat([final_df,df], axis=1).reset_index(drop = True)
     
     from zeemee_py.redshift_updates.one_pager_data import z_organic
     df = z_organic.get_organic_data(zeemee_tp_data)
     final_df = pd.concat([final_df,df], axis=1).reset_index(drop = True)
     
     final_df = final_df.reset_index(drop = True)
     
     return final_df
