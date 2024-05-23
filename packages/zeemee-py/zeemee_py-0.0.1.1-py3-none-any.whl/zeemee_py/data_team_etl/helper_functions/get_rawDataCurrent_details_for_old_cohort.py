"""
This function is used to get information about the college and zeemee files in old cohort foloder.
Just point to the path of the old cohort folder and it returns a DataFrame 
containing the org_id and paths to zeemee and college files for those orgs

to get this data use the following code

function_base_path = '/home/luis/Zemee College_data_project/etl_code/data_team_etl/helper_functions/'
sys.path.insert(0,function_base_path)
import rawDataCurrent_files_details_for_old_cohort
importlib.reload(rawDataCurrent_files_details_for_old_cohort)
rawDataCurrent_files_info = rawDataCurrent_files_details_for_old_cohort.get_files_in_old_cohort_folder(PATH_TO_OLD_COHORT_DATA_FILES)
"""

def get_files_in_old_cohort_folder(PATH_TO_OLD_COHORT_DATA_FILES):
     
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
     select id as org_id, name as org_name, partner_community, partner_pro_community  from
     silver.prod_follower_organizations_latest
     where org_type is null
     order by org_name
     """
     
     org_df  = query_athena_with_retry.run_query_in_athena(query_string)
     
     list_of_files_in_dir = glob.glob(PATH_TO_OLD_COHORT_DATA_FILES + "*")
     zeemee_data_files_in_rawDataCurrent = [s for s in list_of_files_in_dir if s[-10:] == 'zeemee.csv' ]
     college_data_path = list()
     zeemee_data_path = list()
     org_id_of_file = list()
     for i in zeemee_data_files_in_rawDataCurrent:
          data_in_file = pd.read_csv(i, low_memory=False)
          org_id_of_file.append(data_in_file.loc[0,'organization_id'])
          zeemee_data_path.append(i)
          college_data_path.append("".join([i[:-10],'college.csv']))
     
     rawDataCurrent_files_info = pd.DataFrame()
     rawDataCurrent_files_info['org_id'] = org_id_of_file
     rawDataCurrent_files_info['college_data_path'] = college_data_path
     rawDataCurrent_files_info['zeemee_data_path'] = zeemee_data_path
     
     rawDataCurrent_files_info = rawDataCurrent_files_info.merge(org_df,
                                            on = 'org_id',
                                            how = 'left')
                                            
     return rawDataCurrent_files_info

if __name__ == '__main__':
     BASE_PATH = "/home/luis/Zemee College_data_project/data-team/data_team_etl"
     PATH_TO_OLD_COHORT_DATA_FILES = "/home/luis/Zemee College_data_project/old_cohort_data/cohort_2022/files_csv/"
     rawDataCurrent_files_info = get_files_in_old_cohort_folder(PATH_TO_OLD_COHORT_DATA_FILES)




