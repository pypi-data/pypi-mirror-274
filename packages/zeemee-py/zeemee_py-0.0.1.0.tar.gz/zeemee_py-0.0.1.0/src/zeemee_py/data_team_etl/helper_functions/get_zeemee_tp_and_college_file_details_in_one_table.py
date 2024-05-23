
def get_combined_list():
     
import pandas as pd
import sys
import importlib

BASE_PATH = "/home/luis/Zemee College_data_project/data-team/data_team_etl"

sys.path.insert(0,BASE_PATH + '/helper_functions/')
import get_rawDataCurrent_details
importlib.reload(get_rawDataCurrent_details)
rawDataCurrent_files_info = get_rawDataCurrent_details.get_files_in_rawDataCurrent_folder()

sys.path.insert(0,BASE_PATH + '/helper_functions/')
import get_touchpoint_file_details
importlib.reload(get_touchpoint_file_details)
touchpoint_files_info = get_touchpoint_file_details.get_files_in_touchpoints_latest_report_folder()

college_and_touchpoint_file_info = pd.concat([rawDataCurrent_files_info, touchpoint_files_info], axis=1)
college_and_touchpoint_file_info = college_and_touchpoint_file_info.loc[:,~college_and_touchpoint_file_info.columns.duplicated()].copy()

     return college_and_touchpoint_file_info
