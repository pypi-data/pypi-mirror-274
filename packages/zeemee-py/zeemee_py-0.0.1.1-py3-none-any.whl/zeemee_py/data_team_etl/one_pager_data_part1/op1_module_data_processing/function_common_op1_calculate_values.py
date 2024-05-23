def get_op1_values(BASE_PATH, zeemee_college_data):
     import pandas as pd
     import sys
     import importlib
     
     sys.dont_write_bytecode = True
     
     function_dataframe = pd.DataFrame()
     
     sys.path.insert(0,BASE_PATH + '/one_pager_data_part1/op1_module_data_processing/')
     import function_common_op1_calculate_values_comm_match
     importlib.reload(function_common_op1_calculate_values_comm_match)
     function_dataframe_comm_match = function_common_op1_calculate_values_comm_match.get_op_values_comm_match(zeemee_college_data)
     
     sys.path.insert(0,BASE_PATH + '/one_pager_data_part1/op1_module_data_processing/')
     import function_common_op1_calculate_values_non_dupe_ntr
     importlib.reload(function_common_op1_calculate_values_non_dupe_ntr)
     function_dataframe_non_dupe_ntr = function_common_op1_calculate_values_non_dupe_ntr.get_op_values_non_dupe_ntr(zeemee_college_data)
     
     sys.path.insert(0,BASE_PATH + '/one_pager_data_part1/op1_module_data_processing/')
     import function_common_op1_calculate_values_organic
     importlib.reload(function_common_op1_calculate_values_organic)
     function_dataframe_organic = function_common_op1_calculate_values_organic.get_op_values_organic(zeemee_college_data)

     function_dataframe = pd.concat([function_dataframe, function_dataframe_comm_match], axis=1)
     function_dataframe = pd.concat([function_dataframe, function_dataframe_non_dupe_ntr], axis=1)
     function_dataframe = pd.concat([function_dataframe, function_dataframe_organic], axis=1)
     
     return function_dataframe

if __name__ == "__main__":
     import pandas as pd
     BASE_PATH = "/home/luis/Zemee College_data_project/data-team/data_team_etl"
     zeemee_college_data = pd.read_csv('/home/luis/Zemee College_data_project/etl_code/data_team_etl/data_store/zeemee_college_combined_files/Augsburg University_zeemee_college_combined.csv')
     function_dataframe = get_op1_values(BASE_PATH, zeemee_college_data)
     function_dataframe.to_csv("/home/luis/Zemee College_data_project/etl_code/data_team_etl/one_pager_data_part1/op1_module_data_processing/test_data.csv", index = False)
     
     
