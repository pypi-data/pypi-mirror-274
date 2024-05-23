
def create_dataframe_for_given_school(master_df, cohort_year, entry_term, student_type, organization_id):
     
     import pandas as pd
     import importlib
     import warnings
     warnings.simplefilter(action='ignore', category=FutureWarning)
     
     master_df[["ZM.Inquired", "ZM.Applied", "ZM.Accepted", "ZM.Committed", "ZM.Enrolled"]] = master_df[["ZM.Inquired", "ZM.Applied", "ZM.Accepted", "ZM.Committed", "ZM.Enrolled"]].fillna(0)
     master_df[["ZM.Inquired", "ZM.Applied", "ZM.Accepted", "ZM.Committed", "ZM.Enrolled"]] = master_df[["ZM.Inquired", "ZM.Applied", "ZM.Accepted", "ZM.Committed", "ZM.Enrolled"]].replace("NA",0)
     master_df[["ZM.Inquired", "ZM.Applied", "ZM.Accepted", "ZM.Committed", "ZM.Enrolled"]] = master_df[["ZM.Inquired", "ZM.Applied", "ZM.Accepted", "ZM.Committed", "ZM.Enrolled"]].astype(int)
     
     from zeemee_py.helper_functions import connect_athena
     importlib.reload(connect_athena)
     
     query_string = """
     select slug 
     from silver.prod_follower_organizations_latest
     where id = '{}'""".format(organization_id)
     
     organization_slug_df = connect_athena.run_query_in_athena(query_string)
     organization_slug = organization_slug_df.iloc[0,0]
     
     from zeemee_py.redshift_updates.one_pager_data import function_calculate_individual_dfs_onepager_data
     importlib.reload(function_calculate_individual_dfs_onepager_data)
     
     print("processing " + organization_slug)
     function_df = function_calculate_individual_dfs_onepager_data.combine_individual_dfs(master_df, cohort_year, entry_term, student_type)
     
     final_df = pd.DataFrame()

     final_df["org_id"] = [organization_id]
     final_df["cohort_year"] = [cohort_year]
     final_df["student_type"] = [student_type]
     final_df["entry_term"] = [entry_term]
     final_df = pd.concat([final_df,function_df], axis = 1).reset_index(drop = True)
     
     return final_df
