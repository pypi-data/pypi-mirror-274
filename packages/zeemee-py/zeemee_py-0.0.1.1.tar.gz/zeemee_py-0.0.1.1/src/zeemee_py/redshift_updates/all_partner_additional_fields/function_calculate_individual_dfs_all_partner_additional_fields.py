
def combine_individual_dfs(master_df, cohort_year, entry_term, student_type, organization_id):
     import pandas as pd
     import importlib
     import numpy as np

     organization_name = master_df.loc[0,'ZM.Institution']
     entry_term = entry_term.lower()
     student_type = student_type.lower()
     
     
     ##clean up input to include all cases of filters
     if entry_term == 'fall':
          entry_term = "Fall"
     if entry_term == 'spring':
          entry_term = "Spring"
     
     if student_type == "first time":
          student_type = 'First time'
     if student_type == "transfer":
          student_type = 'transfer'
     
     master_df = master_df[
          (master_df['Entry.Year'] ==  cohort_year) & 
          (master_df['ActualDup'] !=  True) & 
          (master_df['Student.Type'] == student_type) & 
          (master_df['Entry.Term'] == entry_term)
          ].reset_index(drop = True)
     
     master_df_filtered = master_df[(master_df['ZM.Community'] == 'Community')].reset_index(drop = True)
     not_in_community_df = master_df[(master_df['ZM.Community'] == 'Not in Community')]
     
     print('Processing all partner additional fields for {organization_name} \nFilters: {cohort_year} {student_type} {entry_term} count = {masterdf_len}'.format(
               organization_name = organization_name, 
               cohort_year = cohort_year, 
               student_type = student_type, 
               entry_term = entry_term, 
               masterdf_len = len(master_df)
               )
               )
               
     final_df = pd.DataFrame()
     
     from zeemee_py.redshift_updates.all_partner_additional_fields import z_first_gen_additional_fields
     importlib.reload(z_first_gen_additional_fields)
     df = z_first_gen_additional_fields.get_first_gen_related_df(master_df, master_df_filtered, not_in_community_df)
     final_df = pd.concat([final_df,df], axis=1).reset_index(drop = True)
     
     from zeemee_py.redshift_updates.all_partner_additional_fields import z_campus_visit_additional_data
     importlib.reload(z_campus_visit_additional_data)
     df = z_campus_visit_additional_data.get_campus_related_related_df(master_df, master_df_filtered, not_in_community_df)
     final_df = pd.concat([final_df,df], axis=1).reset_index(drop = True)
     
     from zeemee_py.redshift_updates.all_partner_additional_fields import z_known_race_additional_data
     importlib.reload(z_known_race_additional_data)
     df = z_known_race_additional_data.get_known_race_related_df(master_df, master_df_filtered, not_in_community_df)
     final_df = pd.concat([final_df,df], axis=1).reset_index(drop = True)
     
     from zeemee_py.redshift_updates.all_partner_additional_fields import z_URM_additional_data
     importlib.reload(z_URM_additional_data)
     df = z_URM_additional_data.get_URM_race_related_df(master_df, master_df_filtered, not_in_community_df)
     final_df = pd.concat([final_df,df], axis=1).reset_index(drop = True)
     
     from zeemee_py.redshift_updates.all_partner_additional_fields import z_caucasian_additional_data
     importlib.reload(z_caucasian_additional_data)
     df = z_caucasian_additional_data.get_Caucasian_race_related_df(master_df, master_df_filtered, not_in_community_df)
     final_df = pd.concat([final_df,df], axis=1).reset_index(drop = True)
     
     from zeemee_py.redshift_updates.all_partner_additional_fields import z_race_ethnicity_distribution_additional_data
     importlib.reload(z_race_ethnicity_distribution_additional_data)
     df = z_race_ethnicity_distribution_additional_data.get_race_ethnicity_distribution_df(master_df, master_df_filtered, not_in_community_df)
     final_df = pd.concat([final_df,df], axis=1).reset_index(drop = True)
     
     from zeemee_py.redshift_updates.all_partner_additional_fields import z_enrolled_comm_entered_additional_data
     importlib.reload(z_enrolled_comm_entered_additional_data)
     df = z_enrolled_comm_entered_additional_data.get_enrolled_entered_term_df(master_df, master_df_filtered, not_in_community_df)
     final_df = pd.concat([final_df,df], axis=1).reset_index(drop = True)
     
     from zeemee_py.redshift_updates.all_partner_additional_fields import z_accepted_entered_stage_additional_data
     importlib.reload(z_accepted_entered_stage_additional_data)
     df = z_accepted_entered_stage_additional_data.get_accepted_entered_stage_df(master_df, master_df_filtered, not_in_community_df)
     final_df = pd.concat([final_df,df], axis=1).reset_index(drop = True)
     
     from zeemee_py.redshift_updates.all_partner_additional_fields import z_applied_comm_entered_additional_data
     importlib.reload(z_applied_comm_entered_additional_data)
     df = z_applied_comm_entered_additional_data.get_applied_entered_term_df(master_df, master_df_filtered, not_in_community_df)
     final_df = pd.concat([final_df,df], axis=1).reset_index(drop = True)
     
     from zeemee_py.redshift_updates.all_partner_additional_fields import z_non_FG_CV_and_URM
     importlib.reload(z_non_FG_CV_and_URM)
     df = z_non_FG_CV_and_URM.non_FG_CV_URM_function(master_df, master_df_filtered, not_in_community_df)
     final_df = pd.concat([final_df,df], axis=1).reset_index(drop = True)
     
     
     final_df = final_df.reset_index(drop = True)
     final_df = final_df.replace('nan', np.NaN)
     
     return final_df
