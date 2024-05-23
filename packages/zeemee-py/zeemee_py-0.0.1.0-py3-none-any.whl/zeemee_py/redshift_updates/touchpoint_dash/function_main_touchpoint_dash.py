
def create_dataframe_for_given_school(touchpoint_df, cohort_year, organization_id, entry_term, student_type):
     
     import pandas as pd
     import importlib
     import warnings
     warnings.simplefilter(action='ignore', category=FutureWarning)
     
     touchpoint_df[["ZM.Inquired", "ZM.Applied", "ZM.Accepted", "ZM.Committed", "ZM.Enrolled"]] = touchpoint_df[["ZM.Inquired", "ZM.Applied", "ZM.Accepted", "ZM.Committed", "ZM.Enrolled"]].fillna(0)
     touchpoint_df[["ZM.Inquired", "ZM.Applied", "ZM.Accepted", "ZM.Committed", "ZM.Enrolled"]] = touchpoint_df[["ZM.Inquired", "ZM.Applied", "ZM.Accepted", "ZM.Committed", "ZM.Enrolled"]].replace("NA",0)
     touchpoint_df[["ZM.Inquired", "ZM.Applied", "ZM.Accepted", "ZM.Committed", "ZM.Enrolled"]] = touchpoint_df[["ZM.Inquired", "ZM.Applied", "ZM.Accepted", "ZM.Committed", "ZM.Enrolled"]].astype(int)
     
     organization_name = touchpoint_df.loc[0,"org_name"]
     
     from zeemee_py.redshift_updates.touchpoint_dash import function_calculate_individual_dfs_touchpoint_dash
     importlib.reload(function_calculate_individual_dfs_touchpoint_dash)
     
     print('processing ' + organization_name)
     final_df = function_calculate_individual_dfs_touchpoint_dash.combine_individual_dfs(touchpoint_df, cohort_year, organization_id, entry_term, student_type)

     final_df.to_csv("/home/mayur/data/test.csv")
     return final_df


    
