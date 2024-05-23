
def create_dataframe_for_given_school(master_df, cohort_year, entry_term, student_type, organization_id):
     
     import pandas as pd
     import importlib
     import warnings
     warnings.simplefilter(action='ignore', category=FutureWarning)
     
     master_df[["ZM.Inquired", "ZM.Applied", "ZM.AppComplete", "ZM.Accepted", "ZM.Committed", "ZM.Enrolled"]] = master_df[["ZM.Inquired", "ZM.Applied", "ZM.AppComplete", "ZM.Accepted", "ZM.Committed", "ZM.Enrolled"]].fillna(0)
     master_df[["ZM.Inquired", "ZM.Applied", "ZM.AppComplete", "ZM.Accepted", "ZM.Committed", "ZM.Enrolled"]] = master_df[["ZM.Inquired", "ZM.Applied", "ZM.AppComplete", "ZM.Accepted", "ZM.Committed", "ZM.Enrolled"]].replace("NA",0)
     master_df[["ZM.Inquired", "ZM.Applied", "ZM.AppComplete", "ZM.Accepted", "ZM.Committed", "ZM.Enrolled"]] = master_df[["ZM.Inquired", "ZM.Applied", "ZM.AppComplete", "ZM.Accepted", "ZM.Committed", "ZM.Enrolled"]].astype(int)
     
     from zeemee_py.helper_functions import connect_athena
     importlib.reload(connect_athena)
     
     query_string = """
     select name 
     from silver.prod_follower_organizations_latest
     where id = '{organization_id}'""".format(
          organization_id = organization_id
          )
     
     organization_name_df = connect_athena.run_query_in_athena(query_string)
     organization_name = organization_name_df.iloc[0,0]
     
     from zeemee_py.redshift_updates.all_partner_data import function_calculate_individual_dfs_all_partner_data
     importlib.reload(function_calculate_individual_dfs_all_partner_data)
     
     print('processing ' + organization_name)
     function_df = function_calculate_individual_dfs_all_partner_data.combine_individual_dfs(master_df, cohort_year, entry_term, student_type, organization_id)
     
     query_string = """
     select date(max(csv_updated_at)) 
     from silver.prod_follower_user_organization_statuses_latest
     where organization_id = '{organization_id}'
     """.format(
          organization_id = organization_id
          )
     csv_update_date_df = connect_athena.run_query_in_athena(query_string)
     
     if csv_update_date_df.iloc[0,0] != None:
          final_df = pd.DataFrame()
          
          final_df['org_id'] = [organization_id]
          final_df['org_name'] = [organization_name]
          final_df['entry_year'] = [cohort_year]
          final_df['student_type'] = [student_type]
          final_df['entry_term'] = [entry_term]
          final_df['csv_update_date'] = [csv_update_date_df.iloc[0,0]]
          
          final_df = pd.concat([final_df,function_df], axis = 1).reset_index(drop = True)
     else:
          print("all partner data not processed for {organization_name}, csv_update_date is null".format(
               organization_name = organization_name
               ))

     final_df.to_csv("/home/mayur/data/test.csv")
     return final_df


    
