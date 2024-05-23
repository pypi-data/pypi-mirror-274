
def modify_column_values(touchpoint_df, organization_id, org_additional_df):
     import numpy as np
     import importlib
    
     touchpoint_df["public_profile_enabled"] = touchpoint_df["public_profile_enabled"].replace(
          {
               "t": "Public Profile",
               "f": "Private Profile"
               }
               )
     
     touchpoint_df["interested"] = touchpoint_df["interested"].replace(
          {
               "t": "In Community - Following",
               "f": "No Longer in Community - Unfollowed"
               }
               )
     
     touchpoint_df["uos_transfer_status"] = touchpoint_df["uos_transfer_status"].fillna(0)
     touchpoint_df["uos_transfer_status"] =touchpoint_df["uos_transfer_status"].replace(
          {
               "t": "Transfer",
               "f": "First Time",
               0: "First Time",
               "": "First Time"
               }
               )
     
     
     touchpoint_df["going"] = touchpoint_df["going"].fillna("Undecided")
     touchpoint_df["going"] = touchpoint_df["going"].replace(
          {
               "going": "Going",
               "notgoing": "Not Going",
               "undecided": "Undecided"
               }
               )
     
     touchpoint_df["created_by_csv"] = touchpoint_df["created_by_csv"].replace(
          {
               "t": "Community Match",
               "": "",
               "f": ""
               }
               )
     
     touchpoint_df["roommate_match_quiz"] = touchpoint_df["roommate_match_quiz"].fillna("")
     touchpoint_df["roommate_match_quiz"] = touchpoint_df["roommate_match_quiz"].replace(
          {
               "t": "Roommate Quiz Completed",
               "f": ""
               }
               )
     
     touchpoint_df["accepted"] = touchpoint_df["accepted"].replace(
          {
               "t": "In Accepted Community",
               "f": ""
               }
               )
     
     touchpoint_df["uos_added_by"] = np.where(
          touchpoint_df["uos_added_by"].isin(["Competitor Match"]), 
          touchpoint_df["uos_added_by"], 
          ""
          )
          
     from zeemee_py.reports.touchpoint_report import z_modify_id_number_values
     importlib.reload(z_modify_id_number_values)
     touchpoint_df = z_modify_id_number_values.modify_id_number_values(touchpoint_df, organization_id, org_additional_df)
     
     return touchpoint_df
