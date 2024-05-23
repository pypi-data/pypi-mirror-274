
def recreate_full_table(BASE_PATH, table_name, combined_school_df_file_path):
     import sys
     import importlib
     import pandas as pd
     
     #BASE_PATH = "/home/luis/Zemee College_data_project/etl_code/data_team_etl"
     sys.dont_write_bytecode = True
     
     current_school_df = pd.read_csv(combined_school_df_file_path)
     
     
     sys.path.insert(0, BASE_PATH + "/helper_functions/")
     import query_athena_with_retry
     importlib.reload(query_athena_with_retry)
     
     query_string = """select * from gold.data_team_{table_name}_latest""".format(table_name = table_name)
     existing_table_df  = query_athena_with_retry.run_query_in_athena(query_string)

     for i in range(len(current_school_df)):
          org_id_in_current_school_df_row = current_school_df.loc[i, 'org_id']
          cohort_year_in_current_school_df_row = current_school_df.loc[i, 'cohort_year']
          student_type_in_current_school_df_row = current_school_df.loc[i, 'student_type']
          entry_term_in_current_school_df_row = current_school_df.loc[i, 'entry_term']
          
          existing_table_df = existing_table_df[
                                        ~((existing_table_df['org_id'] == org_id_in_current_school_df_row) &
                                        (existing_table_df['cohort_year'] == cohort_year_in_current_school_df_row) & 
                                        (existing_table_df['student_type'] == student_type_in_current_school_df_row) & 
                                        (existing_table_df['entry_term'] == entry_term_in_current_school_df_row))].reset_index(drop = True) 
                                        #we are not considering gender here as all gender rows are linked
                                        # we cannot delete only 1 gender row independently, all gender rows need to be deleted 
                                        #and populated simultaneously
     
     existing_table_df = pd.concat([existing_table_df, current_school_df])
     existing_table_df.to_csv(combined_school_df_file_path, index = False)
     
     path_to_local_csv_file = combined_school_df_file_path
     return path_to_local_csv_file
     
if __name__ == '__main__':
     BASE_PATH = "/home/luis/Zemee College_data_project/etl_code/data_team_etl"
     combined_school_df_file_path = '/home/luis/Zemee College_data_project/etl_code/data_team_etl/data_store/data_in_csv_for_tables/all_partner_data_part2_by_gender_FallFirst_time.csv'
     table_name =  "all_partner_data_part2_by_gender"
     recreate_full_table(combined_school_df_file_path, table_name)
