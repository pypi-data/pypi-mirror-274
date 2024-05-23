def combine_individual_dfs(touchpoint_df, cohort_year, organization_id, entry_term, student_type):
     import pandas as pd
     import importlib
     import numpy as np
     
     organization_name = touchpoint_df.loc[0, "org_name"]
     
     print('Processing touchpoint dash data for {organization_name} \nFilters: {cohort_year}'.format(
               organization_name = organization_name, 
               cohort_year = cohort_year
               )
               )
               
     final_df = pd.DataFrame()
     
     from zeemee_py.redshift_updates.touchpoint_dash import z_calculate_values_01
     importlib.reload(z_calculate_values_01)
     df = z_calculate_values_01.calculate_values(touchpoint_df, cohort_year, organization_id, entry_term, student_type)
     final_df = pd.concat([final_df,df], axis=1).reset_index(drop = True)
     
     final_df = final_df.reset_index(drop = True)
     final_df = final_df.replace('nan', np.NaN)
     
     return final_df
