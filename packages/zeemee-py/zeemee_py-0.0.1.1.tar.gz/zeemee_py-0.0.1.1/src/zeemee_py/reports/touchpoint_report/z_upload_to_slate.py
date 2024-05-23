    #only touchpoints supposed to be uploaded to slate. 
    #Be very very careful while using/testing this function
    #wrong update might mess up client crm data BIG BIG issue
    #need to build an inside check to test and ensure correct touchpoints is being uploaded whithout that do not put in production
    
def upload_to_slate(organization_id, organization_slug, engagement_data_df, dated_engagement_data_s3path_for_admin)    
     import boto3
     import requests
     import os
     
     filename_in_slate = dated_engagement_data_s3path_for_admin.split("/")[-1] 
     
     from zeemee_py.helper_functions import get_data_folder_path
     importlib.reload(get_data_folder_path)
     data_folder_path = get_data_folder_path.get_data_folder_path()
     
     local_file_path = os.path.join(data_folder_path, "reports", filename_in_slate)
     engagement_data_df.to_csv(local_file_path, index = False)
     
     from zeemee_py.helper_functions import get_config
     accesskeyid, accesskey  = get_config.get_creds("accesskeyid", "accesskey")
    
     ssm = boto3.client(
          "ssm",
          region_name = "us-west-2",
          aws_access_key_id = accesskeyid,
          aws_secret_access_key = accesskey
          )
     
     upload_url_in_parameter_store = os.path.join("/data_team/slate-details/", organization_id, "/link1/upload_url")
     parameter = ssm.get_parameter(
          Name= upload_url_path_in_parameter_store,
          WithDecryption=True
          )
          
     endpoint_url = parameter["Parameter"]["Value"]
     
     if len(endpoint_url) > 0:
          certificate_file= os.path.join("data_folder_path", certificates, "slate_zeemee.pem") 
          certificate_key = os.path.join("data_folder_path", certificates, "slate_zeemee.key") 
          cert = (certificate_file, certificate_key)
          
          with open(local_file_path,'rb') as f:
                    response = requests.post(
                         endpoint_url + "&filename={filename_in_slate}".format(
                              filename_in_slate = filename_in_slate), 
                         data= f, 
                         headers= {
                              "Content-Type": "text/csv" }, 
                              cert=cert, auth = ("zeemee", ""),
                                     )
          print("slate response", response)
          if response.status_code == 200:
              slack_message = "Touchpoints for {organization_slug} uploaded to slate api".format(organization_slug = organization_slug)
              print(slack_message)
              import time
              time.sleep(1)

          else:
              slack_message = "Touchpoints for {organization_slug} Failed to upload to slate api".format(organization_slug = organization_slug)
              print(slack_message)
              import time
              time.sleep(1)
              
     else:
          slack_message = "Touchpoints for {organization_slug} Failed to upload to slate api, no upload url in AWS paramenter store".format(organization_slug = organization_slug)
          print(slack_message)
          import time
          time.sleep(1)

    
    
    
    
    
    
    
    
    
