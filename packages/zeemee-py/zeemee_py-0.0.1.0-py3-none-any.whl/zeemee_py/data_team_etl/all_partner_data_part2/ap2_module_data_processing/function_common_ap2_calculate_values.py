def get_ap2_values(BASE_PATH, master_df):
     import pandas as pd
     import sys
     import importlib
     
     sys.dont_write_bytecode = True
     
     function_dataframe = pd.DataFrame()
     
     sys.path.insert(0,BASE_PATH + '/all_partner_data_part2/ap2_module_data_processing/')
     import function_common_ap2_calculate_values_first_gen
     importlib.reload(function_common_ap2_calculate_values_first_gen)
     function_dataframe_first_gen = function_common_ap2_calculate_values_first_gen.get_ap_values_first_gen(master_df)
     
     sys.path.insert(0,BASE_PATH + '/all_partner_data_part2/ap2_module_data_processing/')
     import function_common_ap2_calculate_values_not_first_gen
     importlib.reload(function_common_ap2_calculate_values_not_first_gen)
     function_dataframe_not_first_gen = function_common_ap2_calculate_values_not_first_gen.get_ap_values_not_first_gen(master_df)
     
     sys.path.insert(0,BASE_PATH + '/all_partner_data_part2/ap2_module_data_processing/')
     import function_common_ap2_calculate_values_campus_visit
     importlib.reload(function_common_ap2_calculate_values_campus_visit)
     function_dataframe_campus_visit = function_common_ap2_calculate_values_campus_visit.get_ap_values_campus_visit(master_df)
     
     sys.path.insert(0,BASE_PATH + '/all_partner_data_part2/ap2_module_data_processing/')
     import function_common_ap2_calculate_values_not_campus_visit
     importlib.reload(function_common_ap2_calculate_values_not_campus_visit)
     function_dataframe_not_campus_visit = function_common_ap2_calculate_values_not_campus_visit.get_ap_values_not_campus_visit(master_df)
     
     function_dataframe = pd.concat([function_dataframe, function_dataframe_first_gen], axis=1)
     function_dataframe = pd.concat([function_dataframe, function_dataframe_not_first_gen], axis=1)
     function_dataframe = pd.concat([function_dataframe, function_dataframe_campus_visit], axis=1)
     function_dataframe = pd.concat([function_dataframe, function_dataframe_not_campus_visit], axis=1)
     
     return function_dataframe

if __name__ == "__main__":
     import pandas as pd
     BASE_PATH = "/home/luis/Zemee College_data_project/etl_code/data_team_etl"
     master_df = pd.read_csv('/home/luis/Zemee College_data_project/rawDataCurrent/Alfred University_college.csv')
     function_dataframe = get_ap_values(BASE_PATH, master_df)
     function_dataframe.to_csv("/home/luis/Zemee College_data_project/etl_code/data_team_etl/all_partner_data_part2/ap2_module_data_processing/test_data.csv", index = False)
     
     
