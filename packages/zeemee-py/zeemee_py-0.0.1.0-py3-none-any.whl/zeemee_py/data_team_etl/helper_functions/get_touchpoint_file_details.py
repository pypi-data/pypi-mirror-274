

def get_files_in_touchpoints_latest_report_folder():
          
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
     select id as org_id, name as org_name, partner_community, partner_pro_community  from
     silver.prod_follower_organizations_latest
     where partner_community = 'true'
     and id not in ({})
     and org_type is null
     order by org_name
     """.format(str_schools_not_to_use)
     
     partner_df  = query_athena_with_retry.run_query_in_athena(query_string)
     
     
     list_of_files_in_dir = glob.glob("/home/luis/Zemee College_data_project/python_report_projects/data_processed_touchpoints/latest_reports/*")
     zeemee_data_files_in_latest_report = [s for s in list_of_files_in_dir if s[-15:] == 'zeemee_data.csv' ]
     engagement_file_path = list()
     zeemee_file_path = list()
     org_id_of_file = list()
     for i in zeemee_data_files_in_latest_report:
          data_in_file = pd.read_csv(i, low_memory=False)
          org_id_of_file.append(data_in_file.loc[0,'organization_id'])
          zeemee_file_path.append(i)
          engagement_file_path.append("".join([i[:-15],'engagement_data.csv']))
     
     touchpoint_files_info = pd.DataFrame()
     touchpoint_files_info['org_id'] = org_id_of_file
     touchpoint_files_info['engagement_file_path'] = engagement_file_path
     touchpoint_files_info['zeemee_file_path'] = zeemee_file_path
     
     touchpoint_files_info = partner_df.merge(touchpoint_files_info,
                                            on = 'org_id',
                                            how = 'left')

     return touchpoint_files_info
