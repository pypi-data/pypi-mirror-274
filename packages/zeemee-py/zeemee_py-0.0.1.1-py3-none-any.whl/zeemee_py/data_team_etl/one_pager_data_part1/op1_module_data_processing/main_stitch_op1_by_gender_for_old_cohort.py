

def stitch_function_for_op1_by_gender_for_old_cohort():
     
     #---------  USER INPUT ---------------

     print("\n\n")     
     cohort_year = 2022
     print(cohort_year)
     PATH_TO_OLD_COHORT_COMBINED_FILES = "/home/luis/Zemee College_data_project/old_cohort_data/cohort_{cohort_year}/zeemee_college_combined_files/".format(cohort_year = str(cohort_year))
     print(PATH_TO_OLD_COHORT_COMBINED_FILES) # <- verify
     
     #------------------------------------
     

     import sys
     import importlib
     from datetime import datetime
     start_time = datetime.now()
     dt_string = start_time.strftime("%Y-%m-%d %H:%M:%S")
     print("Start time =", dt_string)
     
     sys.dont_write_bytecode = True
          
     BASE_PATH = "/home/luis/Zemee College_data_project/data-team/data_team_etl"
     table_name = "one_pager_data_part1_by_gender"
     
     print("Starting main stitch for op1 by gender for config schools")
     sys.path.insert(0,BASE_PATH + '/one_pager_data_part1/op1_module_data_processing/')
     import process_op1_by_gender_for_old_cohort
     importlib.reload(process_op1_by_gender_for_old_cohort)
     combined_school_df_file_path = process_op1_by_gender_for_old_cohort.process_by_gender_for_zeemee_college_combined_files(BASE_PATH, table_name, cohort_year, PATH_TO_OLD_COHORT_COMBINED_FILES)
     
     
     if type(combined_school_df_file_path) == str:
          combined_school_df_file_path = [combined_school_df_file_path]
     
     for i in range(len(combined_school_df_file_path)):
          dt_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          print(dt_string)
          combined_school_df_file_path_i = combined_school_df_file_path[i]
          print(combined_school_df_file_path_i)
          
          sys.path.insert(0,BASE_PATH + '/one_pager_data_part1/op1_module_table_update/')
          import function_op1_perform_athena_update
          importlib.reload(function_op1_perform_athena_update)
          function_op1_perform_athena_update.concat_and_update_athena_table(BASE_PATH, table_name, combined_school_df_file_path_i)
          
     end_time = datetime.now()
     dt_string = end_time.strftime("%Y-%m-%d %H:%M:%S")
     print("op1 by gender for old_cohort {cohort_year} complete. \nEnd time ={dt_string}".format(cohort_year = str(cohort_year), dt_string = dt_string))
     print("Total time for processing:", end_time - start_time)

if __name__ == '__main__':
     stitch_function_for_op1_by_gender_for_old_cohort()
