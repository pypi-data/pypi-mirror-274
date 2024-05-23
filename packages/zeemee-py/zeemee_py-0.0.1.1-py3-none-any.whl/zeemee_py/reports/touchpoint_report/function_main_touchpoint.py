def get_touchpoint_report(organization_id, cohort_year, upload_to_partner_destination):

     import importlib
     import datetime
     import pandas as pd
     
     from zeemee_py.helper_functions import get_org_additional_data_file
     importlib.reload(get_org_additional_data_file)
     org_additional_df = get_org_additional_data_file.get_file()
     org_additional_df = org_additional_df[
          (org_additional_df["zm_cohort_year"] == cohort_year) &
          (org_additional_df["org_id"] == organization_id)
          ].reset_index(drop = True)
     
     organization_slug = org_additional_df.loc[0,"slug"]
     
     print("")
     print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
     print("touchpoint report for {organization_slug}".format(organization_slug = organization_slug))
     
     from zeemee_py.reports.touchpoint_report import function_touchpoint_query_from_touchpoint_table 
     importlib.reload(function_touchpoint_query_from_touchpoint_table) 
     touchpoint_df = function_touchpoint_query_from_touchpoint_table.touchpoint_from_touchpoint_table(organization_id, cohort_year)
          
     if len(touchpoint_df) <= 0:
          print("data not present in touchpoint_table, running individual queries")
          #-- run individual queries in athena
          
     print("query result length:", len(touchpoint_df))
     
     from zeemee_py.helper_functions import get_latest_postwrangler_files
     importlib.reload(get_latest_postwrangler_files)
     latest_postwrangler_files = get_latest_postwrangler_files.get_latest_files()

     latest_postwrangler_files = latest_postwrangler_files[
          latest_postwrangler_files["organization_id"] == organization_id].reset_index(drop = True)
     postwrangler_file_path_in_s3 = latest_postwrangler_files.loc[0, "filepath_in_s3"]
     
     from zeemee_py.helper_functions import connect_duckdb
     postwrangler_df = connect_duckdb.get_file_df(postwrangler_file_path_in_s3)

     #keep only in community records and remove duplicates
     postwrangler_df = postwrangler_df[
          (postwrangler_df["ActualDup"] != True) &
          (postwrangler_df["ZM.Community"] == "Community")
          ].reset_index(drop = True)
     
     
     columns_for_postwrangler_df = [
          "ZeemeeUserID", 
          "ID.Number",
          "ZM.Joined.Stage", 
          "Entry.Term", 
          "Entry.Year", 
          "Student.Type", 
          "ZM.Status.Analysis",
          "Current.Status", 
          "Student.ID", #added school.id here for non two school ids too so that we can send RNL or blanks for non two id schools
          "ZM.Inquired", 
          "ZM.Applied", 
          "ZM.Accepted", 
          "ZM.Committed", 
          "ZM.Enrolled"
          ]
     
     postwrangler_df = postwrangler_df[columns_for_postwrangler_df]

     # we want to use the bigger of the two zeemee_ids so that
     # the latest signed up user will be in the file
     for i in range(len(postwrangler_df)):
          temp_id_1 = int(str(postwrangler_df.loc[i,"ZeemeeUserID"]).split(" ")[0])
          try:
               temp_id_2 = int(str(postwrangler_df.loc[i,"ZeemeeUserID"]).split(" ")[1])
          except:
               temp_id_2 = 1
               
          try:
               temp_id_3 = int(str(postwrangler_df.loc[i,"ZeemeeUserID"]).split(" ")[2])
          except:
               temp_id_3 = 1
               
          temp_id = str(max([temp_id_1, temp_id_2, temp_id_3]))
          temp_id = temp_id.split(".")[0]
          postwrangler_df.loc[i,"ZeemeeUserID"] = temp_id
          
     postwrangler_df["ZeemeeUserID"] = postwrangler_df["ZeemeeUserID"].astype("int64")
     postwrangler_df = postwrangler_df.rename(columns = {"ZeemeeUserID":"id"}) 
     
     touchpoint_df = touchpoint_df.merge(
          postwrangler_df.drop_duplicates(subset=["id"]), 
          on="id",
          how= "left"
          )
     touchpoint_df = touchpoint_df[(touchpoint_df["uos_cohort_year"] >= cohort_year)].reset_index(drop = True)
     
     print("postwranger data added to query result")
     
     from zeemee_py.reports.touchpoint_report import function_add_new_columns
     importlib.reload(function_add_new_columns)
     touchpoint_df = function_add_new_columns.add_new_columns(touchpoint_df, organization_id)
     print("new columns added to touchpoint_df")
     
     from zeemee_py.reports.touchpoint_report import function_modify_column_values
     importlib.reload(function_modify_column_values)
     touchpoint_df = function_modify_column_values.modify_column_values(touchpoint_df, organization_id, org_additional_df)
     print("column valies added to touchpoint_df")
     
     from zeemee_py.reports.touchpoint_report import function_create_engagement_data_df
     importlib.reload(function_create_engagement_data_df)
     touchpoint_df, engagement_data_df = function_create_engagement_data_df.function_create_engagement_data_df(touchpoint_df)
     print("engagement_data_df created")
     
     from zeemee_py.reports.touchpoint_report import function_upload_to_destination
     importlib.reload(function_upload_to_destination)
     function_upload_to_destination.upload_report_to_destination(organization_id, touchpoint_df, engagement_data_df, org_additional_df, upload_to_partner_destination)
     print("touchpoint report complete")
     print("touchpoint report length:", len(touchpoint_df))
     
     """
     student type zm and student type partner csv are same and we create a duplicate column for this- not created in rewrite
     touchpoints["Student.Type.PartnerCSV"] = touchpoints["uos_transfer_status"]
     touchpoints = touchpoints.rename(columns = {
        "public_profile_enabled": "Public.Private.Profile",
        "interested": "Interested",
        "uos_transfer_status": "Student.Type.ZM",
        "going": "Going",
        "created_by_csv": "Community.Match",
        "roommate_match_quiz": "Room.Mate.Quiz",
        "accepted": "Accepted.Community",
        "zeemee.engagement.scores": "ZeeMee.Engagement.Score",
        "zeemee.engagement.index": "ZeeMee.Engagement.Index"
        
    })
    """
