


def upload_to_sftp(organization_id, organization_slug, engagement_data_df, dated_engagement_data_s3path_for_admin):
     import importlib
     import requests
     import os
     
     filename_in_sftp = dated_engagement_data_s3path_for_admin.split("/")[-1] 
     
     from zeemee_py.helper_functions import get_data_folder_path
     importlib.reload(get_data_folder_path)
     data_folder_path = get_data_folder_path.get_data_folder_path()
     
     local_file_path = os.path.join(data_folder_path, "reports", filename_in_sftp)
     engagement_data_df.to_csv(local_file_path, index = False)
     
     from zeemee_py.helper_functions import get_config
     importlib.reload(get_config)
     evurl, accesskeyev, accesstokenev = get_config.get_creds("evurl", "accesskeyev", "accesstokenev")
     
     from zeemee_py.helper_functions import get_org_additional_data_file
     importlib.reload(get_org_additional_data_file)
     org_additional_df = get_org_additional_data_file.get_file()
     org_additional_df = org_additional_df[org_additional_df["org_id"] == organization_id].reset_index(drop = True)
     
     sftp_location =  org_additional_df.fillna("").loc[0, "deliverable_exavault"].strip()
     print(sftp_location)
     
     if sftp_location in ["yes_rnl", "yes_both", "yes"]:
          
          if sftp_location in ["yes_both", "yes"]:
               #upload to folders in home directory
               
               response = requests.get(
                    evurl + "list",
                    params={
                         'resource': '/',
                         'limit': 100
                         },
                    headers = {
                         'ev-api-key': accesskeyev,
                         'ev-access-token': accesstokenev
               })
               
               #parsing the response to get names of folders
               parse_json = response.json()
               parse_json = parse_json['data']
               
               name_list = list()
               for i in parse_json:
                    try:
                         name_list.append(i['attributes']['name'])
                    except:
                         print('error in parse_json loop in sftp function', i)
               
               #if the folder school_slug exists in the list, upload the file
               #else send an error message to slack data-reports
               
               if organization_slug in name_list:
                    file_size = os.path.getsize(local_file_path)
               
                    response = requests.post(
                         evurl + "upload",
                         params={
                              'path': organization_slug + "/" + filename_in_sftp,
                              'fileSize': file_size
                              },
                              headers = {
                                   'ev-api-key': accesskeyev,
                                   'ev-access-token': accesstokenev
                                   },
                              files = {
                                   'file': (filename_in_sftp, open(local_file_path, 'rb'))
                                        }
                                        )
               
                    slack_message = "Touchpoints for {organization_slug} uploaded to Home folder on files.com".format(organization_slug = organization_slug)
                    print(slack_message)
                    
                    from zeemee_py.helper_functions import send_to_slack
                    importlib.reload(send_to_slack)
                    send_to_slack.send_message_to_slack( "data-reports", slack_message)
               
               else:
                    slack_message = "Touchpoints for {organization_slug} FAILED to upload to files.com: school folder doesn't exist in Home folder".format(organization_slug = organization_slug)
                    print(slack_message)
               
                    from zeemee_py.helper_functions import send_to_slack
                    importlib.reload(send_to_slack)
                    send_message_to_slack.send_to_slack( "data-reports", slack_message)
                    
          if sftp_location in ["yes_both", "yes_rnl"]:
               #upload to folders in home directory
               
               response = requests.get(
                    evurl + "list",
                    params={
                         'resource': '/ruffalo-noel-levitz/Outbound/',
                         'limit': 100
                         },
                    headers = {
                         'ev-api-key': accesskeyev,
                         'ev-access-token': accesstokenev
               })
               
               #parsing the response to get names of folders
               parse_json = response.json()
               parse_json = parse_json['data']
               
               name_list = list()
               for i in parse_json:
                    try:
                         name_list.append(i['attributes']['name'])
                    except:
                         print('error in parse_json loop in sftp function', i)
               
               #if the folder school_slug exists in the list, upload the file
               #else send an error message to slack data-reports
               
               if organization_slug in name_list:
                    file_size = os.path.getsize(local_file_path)
               
                    response = requests.post(
                         evurl + "upload",
                         params={
                              'path': "/ruffalo-noel-levitz/Outbound/" + organization_slug + "/" + filename_in_sftp,
                              'fileSize': file_size
                              },
                              headers = {
                                   'ev-api-key': accesskeyev,
                                   'ev-access-token': accesstokenev
                                   },
                              files = {
                                   'file': (filename_in_sftp, open(local_file_path, 'rb'))
                                        }
                                        )
               
                    slack_message = "Touchpoints for {organization_slug} uploaded to files.com".format(organization_slug = organization_slug)
                    print(slack_message)
                    
                    from zeemee_py.helper_functions import send_to_slack
                    importlib.reload(send_to_slack)
                    send_to_slack.send_message_to_slack( "data-reports", slack_message)
               
               else:
                    slack_message = "Touchpoints for {organization_slug} FAILED to upload to outbound folder on files.com: school folder doesn't exist in RNL Outbound folder".format(organization_slug = organization_slug)
                    print(slack_message)
               
                    from zeemee_py.helper_functions import send_to_slack
                    importlib.reload(send_to_slack)
                    send_message_to_slack.send_to_slack( "data-reports", slack_message)
               
     else:
          slack_message = "Touchpoints for {organization_slug} FAILED uploaded to files.com: specified folder location doesn't exist".format(organization_slug = organization_slug)
          print(slack_message)
     
          from zeemee_py.helper_functions import send_to_slack
          importlib.reload(send_to_slack)
          send_message_to_slack.send_to_slack( "data-reports", slack_message)
          

#organization_id = "3cf6f1fa-56bc-4f49-9ba0-93a72a5cde5a"
#organization_slug = "amda-college-of-the-performing-arts"
#organization_slug = "amda-college-of-the-performing-arts"
#local_file_path = "/home/mayur/data/reports/amda-college-of-the-performing-arts_engagement_data.csv"

#upload_to_sftp(organization_id, organization_slug, organization_slug, local_file_path)
