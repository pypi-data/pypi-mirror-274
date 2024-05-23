def get_op2_values(BASE_PATH, zeemee_college_data):
     import pandas as pd
     import sys
     import importlib
     
     sys.dont_write_bytecode = True
     
     function_dataframe = pd.DataFrame()
     
     sys.path.insert(0,BASE_PATH + '/one_pager_data_part2/op2_module_data_processing/')
     import function_common_op2_calculate_values_enrolled_community_entered_counts
     importlib.reload(function_common_op2_calculate_values_enrolled_community_entered_counts)
     function_dataframe_enrolled_community_entered = function_common_op2_calculate_values_enrolled_community_entered_counts.get_op_values_enrolled_community_entered_values(zeemee_college_data)
     
     sys.path.insert(0,BASE_PATH + '/one_pager_data_part2/op2_module_data_processing/')
     import function_common_op2_calculate_values_committed_community_entered_counts
     importlib.reload(function_common_op2_calculate_values_committed_community_entered_counts)
     function_dataframe_committed_community_entered = function_common_op2_calculate_values_committed_community_entered_counts.get_op_values_committed_community_entered_values(zeemee_college_data)
     
     sys.path.insert(0,BASE_PATH + '/one_pager_data_part2/op2_module_data_processing/')
     import function_common_op2_calculate_values_accepted_community_entered_counts
     importlib.reload(function_common_op2_calculate_values_accepted_community_entered_counts)
     function_dataframe_accepted_community_entered = function_common_op2_calculate_values_accepted_community_entered_counts.get_op_values_accepted_community_entered_values(zeemee_college_data)
     
     sys.path.insert(0,BASE_PATH + '/one_pager_data_part2/op2_module_data_processing/')
     import function_common_op2_calculate_values_applied_community_entered_counts
     importlib.reload(function_common_op2_calculate_values_applied_community_entered_counts)
     function_dataframe_applied_community_entered = function_common_op2_calculate_values_applied_community_entered_counts.get_op_values_applied_community_entered_values(zeemee_college_data)
     
     sys.path.insert(0,BASE_PATH + '/one_pager_data_part2/op2_module_data_processing/')
     import function_common_op2_calculate_values_inquired_community_entered_counts
     importlib.reload(function_common_op2_calculate_values_inquired_community_entered_counts)
     function_dataframe_inquired_community_entered = function_common_op2_calculate_values_inquired_community_entered_counts.get_op_values_inquired_community_entered_values(zeemee_college_data)
     
     function_dataframe = pd.concat([function_dataframe, function_dataframe_enrolled_community_entered], axis=1)
     function_dataframe = pd.concat([function_dataframe, function_dataframe_committed_community_entered], axis=1)
     function_dataframe = pd.concat([function_dataframe, function_dataframe_accepted_community_entered], axis=1)
     function_dataframe = pd.concat([function_dataframe, function_dataframe_applied_community_entered], axis=1)
     function_dataframe = pd.concat([function_dataframe, function_dataframe_inquired_community_entered], axis=1)
     
     return function_dataframe

if __name__ == "__main__":
     import pandas as pd
     BASE_PATH = "/home/luis/Zemee College_data_project/data-team/data_team_etl"
     zeemee_college_data = pd.read_csv('/home/luis/Zemee College_data_project/data-team/data_team_etl/data_store/zeemee_college_combined_files/Augsburg University_zeemee_college_combined.csv')
     function_dataframe = get_op2_values(BASE_PATH, zeemee_college_data)
     function_dataframe.to_csv("/home/luis/Zemee College_data_project/data-team/data_team_etl/one_pager_data_part2/op2_module_data_processing/test_data.csv", index = False)
     
     
