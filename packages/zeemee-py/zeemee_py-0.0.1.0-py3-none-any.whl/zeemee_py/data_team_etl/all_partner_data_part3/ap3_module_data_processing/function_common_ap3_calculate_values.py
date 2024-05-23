def get_ap3_values(BASE_PATH, master_df):
     import pandas as pd
     import sys
     import importlib
     
     sys.dont_write_bytecode = True
     
     function_dataframe = pd.DataFrame()
     
     sys.path.insert(0,BASE_PATH + '/all_partner_data_part3/ap3_module_data_processing/')
     import function_common_ap3_calculate_values_commitment_rate
     importlib.reload(function_common_ap3_calculate_values_commitment_rate)
     function_dataframe_commitment_rate = function_common_ap3_calculate_values_commitment_rate.get_ap_values_commitment_rate(master_df)
     
     sys.path.insert(0,BASE_PATH + '/all_partner_data_part3/ap3_module_data_processing/')
     import function_common_ap3_calculate_values_melt_rate
     importlib.reload(function_common_ap3_calculate_values_melt_rate)
     function_dataframe_melt_rate = function_common_ap3_calculate_values_melt_rate.get_ap_values_melt_rate(master_df)
     
     sys.path.insert(0,BASE_PATH + '/all_partner_data_part3/ap3_module_data_processing/')
     import function_common_ap3_calculate_values_yield_rate
     importlib.reload(function_common_ap3_calculate_values_yield_rate)
     function_dataframe_yield_rate = function_common_ap3_calculate_values_yield_rate.get_ap_values_yield_rate(master_df)
     
     sys.path.insert(0,BASE_PATH + '/all_partner_data_part3/ap3_module_data_processing/')
     import function_common_ap3_calculate_values_app_rate
     importlib.reload(function_common_ap3_calculate_values_app_rate)
     function_dataframe_app_rate = function_common_ap3_calculate_values_app_rate.get_ap_values_app_rate(master_df)
     
     sys.path.insert(0,BASE_PATH + '/all_partner_data_part3/ap3_module_data_processing/')
     import function_common_ap3_calculate_values_missing_dates
     importlib.reload(function_common_ap3_calculate_values_missing_dates)
     function_dataframe_missing_dates = function_common_ap3_calculate_values_missing_dates.get_ap_values_missing_dates(master_df)
     
     function_dataframe = pd.concat([function_dataframe, function_dataframe_commitment_rate], axis=1)
     function_dataframe = pd.concat([function_dataframe, function_dataframe_melt_rate], axis=1)
     function_dataframe = pd.concat([function_dataframe, function_dataframe_yield_rate], axis=1)
     function_dataframe = pd.concat([function_dataframe, function_dataframe_app_rate], axis=1)
     function_dataframe = pd.concat([function_dataframe, function_dataframe_missing_dates], axis=1)
     
     return function_dataframe

if __name__ == "__main__":
     import pandas as pd
     BASE_PATH = "/home/luis/Zemee College_data_project/etl_code/data_team_etl"
     master_df = pd.read_csv('/home/luis/Zemee College_data_project/rawDataCurrent/Alfred University_college.csv')
     function_dataframe = get_ap3_values(BASE_PATH, master_df)
     function_dataframe.to_csv("/home/luis/Zemee College_data_project/etl_code/data_team_etl/all_partner_data_part3/ap3_module_data_processing/test_data.csv", index = False)
     
     
