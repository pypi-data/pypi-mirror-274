"""

update 1 value of a specific column for current cohort using default file in rawdatacurrent
update 1 value of a specific column for prev cohort using a specific file
update 1 entire row for current or prev cohort
daily updates
add delete table columns


changes from previos version:
     entry_year -> cohort_year
     format all columns to lower case and without special characters
     change deposit word to committed
     add gender column
   
     
function_base_path = '/home/luis/Zemee College_data_project/database_table_update/data_team_athena_code/all_partner_data/'
sys.path.insert(0,function_base_path)
import function_ap_create_one_school_data
importlib.reload(function_ap_create_one_school_data)
df  = function_ap_create_one_school_data.complie_ap_dataframe_for_given_school(cohort_year, entry_term, student_type, rawdatacurrent_file_path)

"""


def complie_ap1_dataframe_for_given_school(cohort_year, entry_term, student_type, rawdatacurrent_file_path, BASE_PATH, table_name):
     import json
     import os
     import pandas as pd
     import sys
     import importlib
     
     sys.dont_write_bytecode = True
     #table_name = "all_partner_data_part1_by_gender"
     #BASE_PATH = "/home/luis/Zemee College_data_project/etl_code/data_team_etl" 
     
     table_schema_path = BASE_PATH +  "/athena_code/" + table_name + "_table_schema.json"
     table_schema_json_object = open(table_schema_path)
     table_schema_json = json.load(table_schema_json_object)
     column_list = table_schema_json[table_name]
     
     #print('filters:', cohort_year, entry_term, student_type)
     master_df = pd.read_csv(rawdatacurrent_file_path, low_memory=False)
     rawdatacurrent_length = len(master_df)
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
          
          ap_for_current_df = pd.DataFrame()
          ap_for_current_df['org_id'] = organization_id
          ap_for_current_df['cohort_year'] = [cohort_year]
          ap_for_current_df['entry_term'] = [entry_term]
          ap_for_current_df['student_type'] = [student_type]

          sys.path.insert(0,BASE_PATH + '/all_partner_data_part_1/ap1_module_data_processing')
          import function_common_ap1_calculate_values
          importlib.reload(function_common_ap1_calculate_values)
          current_file_values_df = function_common_ap1_calculate_values.get_ap_values(master_df)
          
          ap_for_current_df = pd.concat([ap_for_current_df, current_file_values_df], axis=1)
          final_df_for_org = pd.concat([final_df_for_org, ap_for_current_df])

     return final_df_for_org
