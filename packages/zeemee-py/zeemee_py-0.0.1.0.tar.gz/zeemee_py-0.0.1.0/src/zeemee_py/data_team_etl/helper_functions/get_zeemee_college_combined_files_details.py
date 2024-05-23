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

def get_files_in_combined_files_folder():
     
     import glob
     import pandas as pd
     from pandas import read_sql
     import sys
     import importlib
     
     BASE_PATH = "/home/luis/Zemee College_data_project/data-team/data_team_etl"
     
     schools_not_to_use = ['1b6df6cd-4343-4573-b6bf-4c140f6fdfe3', #Credible
                          '3d10240b-2a50-432d-8a4e-2be507e1286f', #diversity and inclusion
                          'a0a0aaa9-0e0b-423e-ae5a-8440ec5513e6', #test org zeemee
                          '1c54cbc5-0deb-4372-896a-1f766d10ff7a', #XeeMeeTest
                          '7fdbfdda-4756-4b59-8d96-5d628c4e76fa', #xirimiri
                          '2c470590-8a66-480e-8b56-bfb3251e27c8', #Your Institution
                          '9d0298c7-5f01-4a72-88ed-53e30758e635', #ZeeMee Ambassadors
                          'c54e72a8-6e5a-43db-a308-a868e8632c9d', #ZeeMee Counselors
                          '007e2c79-9118-4a22-8084-ec7a14ab08aa', #ZeeMee University
                         ]
     
     str_schools_not_to_use = "','".join(schools_not_to_use)
     str_schools_not_to_use = "'" + str_schools_not_to_use + "'"
     
     function_base_path = BASE_PATH + '/helper_functions/'
     sys.path.insert(0,function_base_path)
     import query_athena_with_retry
     importlib.reload(query_athena_with_retry)
     
     
     query_string = """
     select id as organization_id, name as org_name, partner_community, partner_pro_community  from
     silver.prod_follower_organizations_latest
     where partner_community = 'true'
     and id not in ({})
     and org_type is null
     order by org_name
     """.format(str_schools_not_to_use)
     
     partner_df  = query_athena_with_retry.run_query_in_athena(query_string)
     
     
     list_of_files_in_dir = glob.glob("/home/luis/Zemee College_data_project/data-team/data_team_etl/data_store/zeemee_college_combined_files/*")
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
     
     combined_file_path = partner_df.merge(combined_files_info,
                                            on = 'organization_id',
                                            how = 'left')
     
     return combined_file_path
