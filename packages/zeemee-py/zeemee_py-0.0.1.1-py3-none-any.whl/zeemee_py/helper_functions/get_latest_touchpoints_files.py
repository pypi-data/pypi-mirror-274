"""
dataframe_columns = [
     organization_id,
     organization_slug,
     partner_community,
     partner_pro_community,
     filepath_in_s3
]
"""
def get_latest_files():
     import pandas as pd
     import importlib
     import boto3
     
     from zeemee_py.helper_functions import connect_athena
     importlib.reload(connect_athena)
     
     from zeemee_py.helper_functions import get_config
     importlib.reload(get_config)
     datateams3bucket, accesskeyid, accesskey = get_config.get_creds("datateams3bucket", "accesskeyid", "accesskey")
     
     schools_not_to_use = [
          "1b6df6cd-4343-4573-b6bf-4c140f6fdfe3", #Credible
          "3d10240b-2a50-432d-8a4e-2be507e1286f", #diversity and inclusion
          "a0a0aaa9-0e0b-423e-ae5a-8440ec5513e6", #test org zeemee
          "1c54cbc5-0deb-4372-896a-1f766d10ff7a", #XeeMeeTest
          "7fdbfdda-4756-4b59-8d96-5d628c4e76fa", #xirimiri
          "2c470590-8a66-480e-8b56-bfb3251e27c8", #Your Institution
          "9d0298c7-5f01-4a72-88ed-53e30758e635", #ZeeMee Ambassadors
          "c54e72a8-6e5a-43db-a308-a868e8632c9d", #ZeeMee Counselors
          "007e2c79-9118-4a22-8084-ec7a14ab08aa", #ZeeMee University
          ]
     
     str_schools_not_to_use = "','".join(schools_not_to_use)
     str_schools_not_to_use = "'" + str_schools_not_to_use + "'"
     
     query_string = """
          select id as organization_id, slug as organization_slug, partner_community, partner_pro_community  
          from
          silver.prod_follower_organizations_latest
          where 
          partner_community = 'true'
          and id not in ({})
          and org_type is null
          """.format(
          str_schools_not_to_use
          )
          
     partner_df = connect_athena.run_query_in_athena(query_string)
     
     s3 = boto3.resource(
          "s3",
          aws_access_key_id= accesskeyid, 
          aws_secret_access_key= accesskey
          )
     bucket = s3.Bucket(datateams3bucket)
     
     touchpoints_file_path_in_s3 = list()
     for files in bucket.objects.filter(Prefix="zeemee_py/reports/latest_touchpoint_files/").all():
         touchpoints_file_path_in_s3.append("s3://" + datateams3bucket + "/" + files.key)

     touchpoints_file_path_in_s3 = list(sorted(touchpoints_file_path_in_s3))
     org_id_of_file = list()
     s3_file_path = list()
     
     for i in touchpoints_file_path_in_s3:
          try:
               from zeemee_py.helper_functions import connect_duckdb
               file_df = connect_duckdb.get_file_df(i)
               org_id_of_file.append(file_df.loc[0,"organization_id"])
               s3_file_path.append(i)
               
          except:
               continue
     
     latest_touchpoints_files_info = pd.DataFrame()
     latest_touchpoints_files_info["organization_id"] = org_id_of_file
     latest_touchpoints_files_info["filepath_in_s3"] = s3_file_path
     
     latest_touchpoints_files_info = partner_df.merge(
          latest_touchpoints_files_info,
          on = "organization_id",
          how = "left"
          )
     
     return latest_touchpoints_files_info
