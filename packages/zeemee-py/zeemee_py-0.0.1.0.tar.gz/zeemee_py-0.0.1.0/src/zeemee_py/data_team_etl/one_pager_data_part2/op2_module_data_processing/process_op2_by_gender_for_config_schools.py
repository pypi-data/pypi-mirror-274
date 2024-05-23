
def process_by_gender_for_zeemee_college_combined_files(BASE_PATH, table_name):
     
     import pandas as pd
     import json
     import sys
     import importlib
     
     sys.dont_write_bytecode = True
     
     #global BASE_PATH
     
     #BASE_PATH = "/home/luis/Zemee College_data_project/etl_code/data_team_etl"
     #table_name = "all_partner_data_part3_by_gender"
     
     with open(BASE_PATH + "/config.json") as json_data_file:
         json_data = json.load(json_data_file)
     
     cohort_year = json_data['cohort_year']
     entry_term_list = eval(json_data['entry_term'])
     student_type_list = eval(json_data['student_type'])
     
     sys.path.insert(0,BASE_PATH + '/helper_functions/')
     import get_zeemee_college_combined_files_details
     importlib.reload(get_zeemee_college_combined_files_details)
     zeemee_college_combined_files_info = get_zeemee_college_combined_files_details.get_files_in_combined_files_folder()
     
     #drop rows that have null values and record those to list for logging 
     is_null_in_rows = zeemee_college_combined_files_info.isnull().any(axis=1)
     not_processed_reason = list() #list for slack logs
     organizations_not_processed = list() #list for slack logs
     parameter_for_which_processing_failed = list() #list for slack logs
     for i in range(len(is_null_in_rows)):
          if is_null_in_rows[i] == True:
               organizations_not_processed.append(zeemee_college_combined_files_info.loc[i, 'org_name'])
               not_processed_reason.append('null value in zeemee_college_combined_files_info')
               parameter_for_which_processing_failed.append('no parameter applied')
               
     #dropping rows that have NAs to avoid error in running all partner data report
     #these details are added to the organizations_not_processed list
     zeemee_college_combined_files_info = zeemee_college_combined_files_info.dropna().reset_index(drop =True)
     
     sys.path.insert(0,BASE_PATH + '/one_pager_data_part2/op2_module_data_processing/')
     import function_op2_by_gender_create_one_school_data
     importlib.reload(function_op2_by_gender_create_one_school_data)
     
     combined_school_df = pd.DataFrame()
     combined_school_df_file_path_list = list()
     
     for i in entry_term_list:
          for j in student_type_list:
               current_cohort_year = cohort_year
               current_entry_term = i
               current_student_type = j
               combined_school_df_file_path = BASE_PATH + '/data_store/data_in_csv_for_tables/' + table_name + '_' + current_entry_term + current_student_type .replace(' ', '_') + '.csv'
               
               for school_no in range(len(zeemee_college_combined_files_info)):
                    school_name = zeemee_college_combined_files_info.loc[school_no, 'org_name']
                    org_id = zeemee_college_combined_files_info.loc[school_no, 'organization_id']
                    combined_file_path = zeemee_college_combined_files_info.loc[school_no, 'combined_file_path']
                    
                    print("\tRunning for " + school_name + ' ' + org_id + ' ' + str(current_cohort_year) + ' ' + current_entry_term + ' ' + current_student_type.replace(' ', '_'))
                    
                    try:
                         current_school_df  = function_op2_by_gender_create_one_school_data.complie_op2_dataframe_by_gender_for_given_school(current_cohort_year, current_entry_term, current_student_type, combined_file_path, BASE_PATH, table_name)
                         combined_school_df = pd.concat([combined_school_df, current_school_df], ignore_index=True)
                         combined_school_df.to_csv(combined_school_df_file_path, index = False)
                         if combined_school_df_file_path not in combined_school_df_file_path_list:
                              combined_school_df_file_path_list.append(combined_school_df_file_path)
                    except Exception as e:
                         print("\terror in function_ap_create_one_school_data for " + school_name + ' ' + str(current_cohort_year) + current_entry_term + current_student_type.replace(' ', '_') + ' error:' + str(e))
                         organizations_not_processed.append(school_name)
                         not_processed_reason.append('error in function_op2_create_one_school_data')
                         parameter_for_which_processing_failed.append(str(current_cohort_year) + current_entry_term + current_student_type.replace(' ', '_'))
     
     error_logs_df = pd.DataFrame()
     error_logs_df['organizations_not_processed'] = organizations_not_processed
     error_logs_df['not_processed_reason'] = not_processed_reason
     error_logs_df['parameter_for_which_processing_failed'] = parameter_for_which_processing_failed
     error_logs_df['combined_column'] = '\t' + error_logs_df['organizations_not_processed'] + ' ' + error_logs_df['not_processed_reason'] + ' ' + error_logs_df['parameter_for_which_processing_failed']
     
     error_logs_df = error_logs_df.fillna("NULL value")
     
     if len(organizations_not_processed) > 0:
          error_logs_text = '\n'.join(list(error_logs_df['combined_column']))
          print("\n\nErrors:")
          print(error_logs_text)
          
          error_logs_for_slack_df = error_logs_df.groupby(['not_processed_reason', 'parameter_for_which_processing_failed'],as_index=False)['organizations_not_processed'].count()
          error_logs_for_slack_df['combined_column'] = '\t' + error_logs_for_slack_df['not_processed_reason'] + ' ' + error_logs_for_slack_df['parameter_for_which_processing_failed'] + ' ' + error_logs_for_slack_df['organizations_not_processed'].astype(str)
          error_logs_for_slack_text = '\n'.join(list(error_logs_for_slack_df['combined_column']))
          
          slack_text = "Following errors in etl file creation for {table_name}\n".format(table_name = table_name)
          slack_text = slack_text + error_logs_for_slack_text
          
          sys.path.insert(0,BASE_PATH + '/helper_functions/')
          import send_slack_notifications
          importlib.reload(send_slack_notifications)
          send_slack_notifications.send_message_to_slack(slack_text, 'data-reports')

     return combined_school_df_file_path_list
     
     
if __name__ == '__main__':
     BASE_PATH = "/home/luis/Zemee College_data_project/data-team/data_team_etl"
     table_name = 'one_pager_data_part2_by_gender'
     combined_school_df_file_path_list = process_by_gender_for_zeemee_college_combined_files(BASE_PATH, table_name)
     print(combined_school_df_file_path_list)
     #rawdatacurrent_file_path = '/home/luis/Zemee College_data_project/rawDataCurrent/Alfred University_college.csv'
     
