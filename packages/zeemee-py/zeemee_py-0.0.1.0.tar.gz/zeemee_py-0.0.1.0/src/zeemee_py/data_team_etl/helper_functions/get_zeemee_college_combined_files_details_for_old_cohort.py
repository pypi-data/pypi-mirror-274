"""
This function is used to get information about the files in the all partner data report.
It returns a DataFrame containing the org_id and paths to zeemee and college files for those orgs

to get this data use the following code

function_base_path = '/home/luis/Zemee College_data_project/database_table_update/data_team_athena_code/helper_functions/'
sys.path.insert(0,function_base_path)
import rawDataCurrent_files_details
importlib.reload(rawDataCurrent_files_details)
rawDataCurrent_files_info = rawDataCurrent_files_details.get_files_in_rawDataCurrent_folder()
"""

def get_files_in_combined_files_folder(PATH_TO_OLD_COHORT_COMBINED_FILES):
          
     import glob
     import pandas as pd
     from pandas import read_sql
     import sys
     import importlib
     
     BASE_PATH = "/home/luis/Zemee College_data_project/data-team/data_team_etl"
     
     function_base_path = BASE_PATH + '/helper_functions/'
     sys.path.insert(0,function_base_path)
     import query_athena_with_retry
     importlib.reload(query_athena_with_retry)
     
     
     query_string = """
     select id as organization_id, name as org_name, partner_community, partner_pro_community  from
     silver.prod_follower_organizations_latest
     where org_type is null
     order by org_name
     """
     
     org_df  = query_athena_with_retry.run_query_in_athena(query_string)
     
     
     list_of_files_in_dir = glob.glob(PATH_TO_OLD_COHORT_COMBINED_FILES + "*")
     combined_files_in_folder = [s for s in list_of_files_in_dir if s[-12:] == 'combined.csv' ]
     combined_file_path = list()
     org_id_of_file = list()
     for i in combined_files_in_folder:
          try:
               data_in_file = pd.read_csv(i, low_memory=False)
               org_id_of_file.append(data_in_file.loc[0,'organization_id'])
               combined_file_path.append(i)
          except:
               print(i)
     
     combined_files_info = pd.DataFrame()
     combined_files_info['organization_id'] = org_id_of_file
     combined_files_info['combined_file_path'] = combined_file_path
     
     combined_file_path = combined_files_info.merge(org_df,
                                            on = 'organization_id',
                                            how = 'left')
     
     return combined_file_path

if __name__ == "__main__":
     cohort_year = 2022
     PATH_TO_OLD_COHORT_COMBINED_FILES = "/home/luis/Zemee College_data_project/old_cohort_data/cohort_2022/zeemee_college_combined_files/"
     create_master_touchpoint_files_list(cohort_year)
