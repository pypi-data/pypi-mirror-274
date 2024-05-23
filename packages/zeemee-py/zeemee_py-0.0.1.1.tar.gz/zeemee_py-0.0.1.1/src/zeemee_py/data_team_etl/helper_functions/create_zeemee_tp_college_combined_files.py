
def create_master_touchpoint_files_list():
          
     import pandas as pd
     import sys
     import importlib
     
     BASE_PATH = "/home/luis/Zemee College_data_project/data-team/data_team_etl"
     
     sys.path.insert(0,BASE_PATH + "/helper_functions/")
     import get_zeemee_tp_and_college_file_details_in_one_table
     importlib.reload(get_zeemee_tp_and_college_file_details_in_one_table)
     combined_files_info = get_zeemee_tp_and_college_file_details_in_one_table.get_combined_list()
     
     for i in range(len(combined_files_info)):
          try:
               college_file = pd.read_csv(combined_files_info["college_data_path"][i], low_memory=False)
               college_file = college_file[college_file["ZM.Community"] == "Community"].reset_index(drop = True)
               
               #facing inconsistencies here (raw college data's ZeemeeUserID)
               #has a value like XXXXXX and YYYYYYY, so cannot convert to string directly
               #so will have a string which can be converted into int64 and then the two dataframes can be joined
               #change in onepager as well if the logic below changes
               for j in range(len(college_file)):
                  temp_id = str(college_file.loc[j,'ZeemeeUserID']).split(' ')[0]
                  temp_id = temp_id.split('.')[0]
                  college_file.loc[j,'ZeemeeUserID'] = temp_id
               college_file["ZeemeeUserID"] = college_file["ZeemeeUserID"].astype(int)
               
               #we keep only specific columns in combined files as there are 
               #duplicate columns leading to suffix _x and _y. Adding specific columns will 
               #keep things simple and avoid that
               college_file = college_file[["ZeemeeUserID", "Gender", "Entry.Year", "ActualDup", "Entry.Term", "Student.Type"]].reset_index(drop = True)
               
               zeemee_tp_file = pd.read_csv(combined_files_info["zeemee_file_path"][i], low_memory=False)
               
               zeemee_college_file = pd.merge(zeemee_tp_file, college_file, how = "left", left_on = "ZeeMee.ID", right_on = "ZeemeeUserID")
               
               org_name = combined_files_info["org_name"][i]
               zeemee_college_file.to_csv("/home/luis/Zemee College_data_project/etl_code/data_team_etl/data_store/zeemee_college_combined_files/" + org_name + "_zeemee_college_combined.csv")
          except:
               print("Error in creating zeemee_college_file for", combined_files_info["org_name"][i])
          
if __name__ == "__main__":
     create_master_touchpoint_files_list()

