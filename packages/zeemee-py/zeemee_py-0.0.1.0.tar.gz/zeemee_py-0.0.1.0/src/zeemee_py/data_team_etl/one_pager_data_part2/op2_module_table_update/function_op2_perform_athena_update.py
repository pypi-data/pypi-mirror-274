
def concat_and_update_athena_table(BASE_PATH, table_name, combined_school_df_file_path):
     import sys
     import importlib
     
     #BASE_PATH = "/home/luis/Zemee College_data_project/etl_code/data_team_etl"
     sys.dont_write_bytecode = True
     
     sys.path.insert(0, BASE_PATH + '/one_pager_data_part2/op2_module_table_update/')
     import function_op2_recreate_full_table
     importlib.reload(function_op2_recreate_full_table)
     path_to_local_csv_file = function_op2_recreate_full_table.recreate_full_table(BASE_PATH, table_name, combined_school_df_file_path)
     print("Full table recreated after deletion and concatenation with new data")
     
     sys.path.insert(0, BASE_PATH + '/athena_code/')
     import create_or_update_athena_tables_for_gold_schema
     importlib.reload(create_or_update_athena_tables_for_gold_schema)
     path_to_local_csv_file = create_or_update_athena_tables_for_gold_schema.main_function(BASE_PATH, table_name, combined_school_df_file_path)
     
if __name__ == '__main__':
     combined_school_df_file_path = '/home/luis/Zemee College_data_project/data-team/data_team_etl/data_store/data_in_csv_for_tables/one_pager_data_part2_FallFirst_time.csv'
     table_name =  "one_pager_data_part2"
     concat_and_update_athena_table(table_name, combined_school_df_file_path)
