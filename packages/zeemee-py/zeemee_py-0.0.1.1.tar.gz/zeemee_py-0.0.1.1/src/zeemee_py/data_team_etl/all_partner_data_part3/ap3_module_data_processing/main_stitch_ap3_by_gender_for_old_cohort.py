

def stitch_function_for_ap3_by_gender_for_old_cohort():
     
     #---------  USER INPUT ---------------

     print("\n\n")     
     cohort_year = 2022
     print(cohort_year)
     PATH_TO_OLD_COHORT_DATA_FILES = "/home/luis/Zemee College_data_project/old_cohort_data/cohort_{cohort_year}/files_csv/".format(cohort_year = str(cohort_year))
     print(PATH_TO_OLD_COHORT_DATA_FILES) # <- verify
     
     #------------------------------------
     

     import sys
     import importlib
     from datetime import datetime
     start_time = datetime.now()
     dt_string = start_time.strftime("%Y-%m-%d %H:%M:%S")
     print("Start time =", dt_string)
     
     sys.dont_write_bytecode = True
          
     BASE_PATH = "/home/luis/Zemee College_data_project/etl_code/data_team_etl"
     table_name = "all_partner_data_part3_by_gender"
     
     print("Starting main stitch for ap3 by gender for config schools")
     sys.path.insert(0,BASE_PATH + '/all_partner_data_part3/ap3_module_data_processing/')
     import process_ap3_by_gender_for_old_cohort
     importlib.reload(process_ap3_by_gender_for_old_cohort)
     combined_school_df_file_path = process_ap3_by_gender_for_old_cohort.process_by_gender_for_rawDataCurrent(BASE_PATH, table_name, cohort_year, PATH_TO_OLD_COHORT_DATA_FILES)
     
     
     if type(combined_school_df_file_path) == str:
          combined_school_df_file_path = [combined_school_df_file_path]
     
     for i in range(len(combined_school_df_file_path)):
          dt_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          print(dt_string)
          combined_school_df_file_path_i = combined_school_df_file_path[i]
          print(combined_school_df_file_path_i)
          
          sys.path.insert(0,BASE_PATH + '/all_partner_data_part3/ap3_module_table_update/')
          import function_ap3_perform_athena_update
          importlib.reload(function_ap3_perform_athena_update)
          function_ap3_perform_athena_update.concat_and_update_athena_table(BASE_PATH, table_name, combined_school_df_file_path_i)
          
     end_time = datetime.now()
     dt_string = end_time.strftime("%Y-%m-%d %H:%M:%S")
     print("ap3 by gender for config schools process complete. \nEnd time =", dt_string)
     print("Total time for processing:", end_time - start_time)

if __name__ == '__main__':
     stitch_function_for_ap3_by_gender_for_old_cohort()
