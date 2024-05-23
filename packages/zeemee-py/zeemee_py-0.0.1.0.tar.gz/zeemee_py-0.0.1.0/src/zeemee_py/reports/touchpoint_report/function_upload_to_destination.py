
def upload_report_to_destination(organization_id, touchpoint_df, engagement_data_df, org_additional_df, upload_to_partner_destination):
     print("")
     import datetime
     import importlib
     import os
     
     #geting variables tp write csv files
     organization_slug = org_additional_df.loc[0,"slug"]
     organization_slug = organization_slug.replace(" ", "_")
     organization_slug = organization_slug.replace("'", "")
     date_today_string = datetime.datetime.now().strftime("%Y-%m-%d")
     
     from zeemee_py.helper_functions import send_dataframe_to_s3
     importlib.reload(send_dataframe_to_s3)
     
     latest_touchpoint_s3path = os.path.join("s3://zeemee-data-team-files/zeemee_py/reports/latest_touchpoint_files/", organization_slug + "_touchpoint.csv")
     dated_touchpoint_s3path =  os.path.join("s3://zeemee-data-team-files/zeemee_py/reports/dated_touchpoints/touchpoint_report/", organization_slug,  organization_slug + "_" + date_today_string + "_touchpoint.csv")
     dated_engagement_data_s3path = os.path.join("s3://zeemee-data-team-files/zeemee_py/reports/dated_touchpoints/touchpoint_report/", organization_slug, organization_slug + "_" + date_today_string + "_engagement_data.csv")
      
     send_dataframe_to_s3.send_dataframe_to_s3(latest_touchpoint_s3path, touchpoint_df)
     send_dataframe_to_s3.send_dataframe_to_s3(dated_touchpoint_s3path, touchpoint_df)
     send_dataframe_to_s3.send_dataframe_to_s3(dated_engagement_data_s3path, engagement_data_df)
     
     if upload_to_partner_destination == "yes":
          dated_engagement_data_s3path_for_admin =  os.path.join("s3://zeemee-csv-auto-production/", organization_slug, organization_slug + "_" + date_today_string + "_engagement_data.csv")
          send_dataframe_to_s3.send_dataframe_to_s3(dated_engagement_data_s3path_for_admin, engagement_data_df)
          
          if len(org_additional_df) == 1:
               org_additional_df["deliverable"] = org_additional_df["deliverable"].str.strip()
               org_additional_df["deliverable_admin"] = org_additional_df["deliverable_admin"].str.strip()
               org_additional_df["deliverable_exavault"] = org_additional_df["deliverable_exavault"].str.strip()
               org_additional_df["deliverable_api"] = org_additional_df["deliverable_api"].str.strip()
               
               deliverable = org_additional_df.loc[0,"deliverable"]
               if deliverable is None:
                    deliverable = "Engagements-TouchPoints"
               
               deliverable_admin = org_additional_df.loc[0,"deliverable_admin"]
               deliverable_exavault = org_additional_df.loc[0,"deliverable_exavault"]
               deliverable_api = org_additional_df.loc[0,"deliverable_api"]
          else:
               print("Record not found or multiple records in org_additional_df, using default upload variables")
               deliverable = "Engagements-TouchPoints"
               deliverable_admin = "yes"
               deliverable_exavault = "no"
               deliverable_api = "no"

          print("deliverable_admin:", deliverable_admin)
          print("deliverable_exavault:", deliverable_exavault)
          print("deliverable_api:", deliverable_api)
          
          if deliverable == "Engagements-TouchPoints":
               if deliverable_admin == "yes":
                    from zeemee_py.reports.touchpoint_report import z_upload_to_admin
                    importlib.reload(z_upload_to_admin)
                    z_upload_to_admin.upload_engagement_data_to_admin(organization_id, organization_slug, dated_engagement_data_s3path_for_admin)
                                                                      
               if deliverable_exavault in ("yes", "yes_rnl", "yes_both"):
                    from zeemee_py.reports.touchpoint_report import z_upload_to_sftp
                    importlib.reload(z_upload_to_sftp)
                    z_upload_to_sftp.upload_to_sftp(organization_id, organization_slug, engagement_data_df,  dated_engagement_data_s3path_for_admin)
               
               if deliverable_api == "yes":
                    print("write api code")
                    
          else:
               print("No known 'deliverable' field value in org_additional_data, so not uploaded to any destination")
               
     else:
          print("upload_to_partner_destination is 'no', file created in S3 only") 
