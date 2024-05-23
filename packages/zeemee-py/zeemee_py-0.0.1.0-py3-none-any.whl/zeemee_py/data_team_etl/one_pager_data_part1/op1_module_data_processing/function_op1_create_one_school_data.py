"""
"""


def complie_op1_dataframe_for_given_school(cohort_year, entry_term, student_type, zeemee_college_file_path, BASE_PATH, table_name):
     import json
     import os
     import pandas as pd
     import sys
     import importlib
     
     sys.dont_write_bytecode = True
     #table_name = "one_pager_data_part1_by_gender"
     #BASE_PATH = "/home/luis/Zemee College_data_project/etl_code/data_team_etl" 
     
     table_schema_path = BASE_PATH +  "/athena_code/" + table_name + "_table_schema.json"
     table_schema_json_object = open(table_schema_path)
     table_schema_json = json.load(table_schema_json_object)
     column_list = table_schema_json[table_name]
     
     #print('filters:', cohort_year, entry_term, student_type)
     master_df = pd.read_csv(zeemee_college_file_path, low_memory=False)
     zeemee_college_file_length = len(master_df)
     #print("rawdatacurrent length:", len(master_df))
     master_df = master_df[(master_df['Entry.Year'] ==  cohort_year)].reset_index(drop = True)
     #print("after cohort filter:", len(master_df))
     master_df = master_df[(master_df['ActualDup'] != True)].reset_index(drop = True)
     #print("after ActualDup filter:", len(master_df))
     master_df = master_df[(master_df['Entry.Term'] ==  entry_term)].reset_index(drop = True)
     #print("after entry_term filter:", len(master_df))
     master_df = master_df[(master_df['Student.Type'] ==  student_type)].reset_index(drop = True)
     #print("after student_type filter:", len(master_df))
     after_all_filters = len(master_df)
     #print("after all filters:", len(master_df))
     print("\t\trawdatacurrent length: "+ str(len(master_df)) + ", After all filters: " + str(len(master_df)))
     
     organization_id = [master_df.loc[0,'organization_id']]
     
     final_df_for_org = pd.DataFrame()
     schools_with_no_data_for_filters = list()
     
     if len(master_df) <= 0:
          print("No data for given filters for", organization_id)
          schools_with_no_data_for_filters.append( organization_id + ' ' + str(cohort_year) + ' ' + entry_term + ' ' + student_type.replace(' ','_').lower())
     else:
          
          op_for_current_df = pd.DataFrame()
          op_for_current_df['org_id'] = organization_id
          op_for_current_df['cohort_year'] = [cohort_year]
          op_for_current_df['entry_term'] = [entry_term]
          op_for_current_df['student_type'] = [student_type]

          sys.path.insert(0,BASE_PATH + '/one_pager_data_part_1/op1_module_data_processing/')
          import function_common_op1_calculate_values
          importlib.reload(function_common_op1_calculate_values)
          current_file_values_df = function_common_op1_calculate_values.get_op1_values(BASE_PATH, master_df)
          
          op_for_current_df = pd.concat([op_for_current_df, current_file_values_df], axis=1)
          final_df_for_org = pd.concat([final_df_for_org, op_for_current_df])

     return final_df_for_org

if __name__ == "__main__":
     cohort_year = 2023
     entry_term = "Fall"
     student_type = "First time"
     zeemee_college_file_path = "/home/luis/Zemee College_data_project/etl_code/data_team_etl/data_store/zeemee_college_combined_files/Augsburg University_zeemee_college_combined.csv"
     BASE_PATH = "/home/luis/Zemee College_data_project/etl_code/data_team_etl"
     table_name = "one_pager_data_part1"
     file = complie_op1_dataframe_for_given_school(cohort_year, entry_term, student_type, zeemee_college_file_path, BASE_PATH, table_name)
     file.to_csv("/home/luis/Zemee College_data_project/etl_code/data_team_etl/one_pager_data_part1/op1_module_data_processing/test_data.csv", index = False)
     
