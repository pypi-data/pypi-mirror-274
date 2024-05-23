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
     
     print('Processing all partner data for {organization_name} \nFilters: {cohort_year} {student_type} {entry_term} count = {masterdf_len}'.format(
               organization_name = organization_name, 
               cohort_year = cohort_year, 
               student_type = student_type, 
               entry_term = entry_term, 
               masterdf_len = len(master_df)
               )
               )
               
     final_df = pd.DataFrame()
     
     from zeemee_py.redshift_updates.all_partner_data import z_calculate_values_01
     importlib.reload(z_calculate_values_01)
     df = z_calculate_values_01.calculate_values(master_df)
     final_df = pd.concat([final_df,df], axis=1).reset_index(drop = True)
     
     from zeemee_py.redshift_updates.all_partner_data import z_calculate_values_02
     importlib.reload(z_calculate_values_02)
     df = z_calculate_values_02.calculate_values(master_df)
     final_df = pd.concat([final_df,df], axis=1).reset_index(drop = True)
     
     from zeemee_py.redshift_updates.all_partner_data import z_calculate_values_03
     importlib.reload(z_calculate_values_03)
     df = z_calculate_values_03.calculate_values(master_df)
     final_df = pd.concat([final_df,df], axis=1).reset_index(drop = True)
     
     from zeemee_py.redshift_updates.all_partner_data import z_calculate_values_04
     importlib.reload(z_calculate_values_04)
     df = z_calculate_values_04.calculate_values(master_df)
     final_df = pd.concat([final_df,df], axis=1).reset_index(drop = True)
     
     from zeemee_py.redshift_updates.all_partner_data import z_calculate_values_05
     importlib.reload(z_calculate_values_05)
     df = z_calculate_values_05.calculate_values(master_df)
     final_df = pd.concat([final_df,df], axis=1).reset_index(drop = True)
     
     from zeemee_py.redshift_updates.all_partner_data import z_calculate_values_06
     importlib.reload(z_calculate_values_06)
     df = z_calculate_values_06.calculate_values(master_df)
     final_df = pd.concat([final_df,df], axis=1).reset_index(drop = True)
     
     from zeemee_py.redshift_updates.all_partner_data import z_calculate_values_07
     importlib.reload(z_calculate_values_07)
     df = z_calculate_values_07.calculate_values(master_df)
     final_df = pd.concat([final_df,df], axis=1).reset_index(drop = True)
     
     from zeemee_py.redshift_updates.all_partner_data import z_calculate_values_08
     importlib.reload(z_calculate_values_08)
     df = z_calculate_values_08.calculate_values(master_df)
     final_df = pd.concat([final_df,df], axis=1).reset_index(drop = True)
     
     from zeemee_py.redshift_updates.all_partner_data import z_calculate_values_09
     importlib.reload(z_calculate_values_09)
     df = z_calculate_values_09.calculate_values(master_df)
     final_df = pd.concat([final_df,df], axis=1).reset_index(drop = True)
     
     final_df = final_df.reset_index(drop = True)
     final_df = final_df.replace('nan', np.NaN)
     
     return final_df
     
     
     
     
     
     
     
     
     
     
