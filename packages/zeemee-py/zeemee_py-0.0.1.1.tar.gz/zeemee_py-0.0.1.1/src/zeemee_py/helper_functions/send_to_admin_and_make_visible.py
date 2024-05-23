"""This script contains functions to implement csv loader api here: 
     https://github.com/zeemee/zeemee-docs/blob/master/tech-specs/csv-api.md
     """

def send_to_admin_and_make_visible(organization_id, s3_file_name):
     import requests
     import json
     from zeemee_py.helper_functions import get_config
     
     print(s3_file_name)
     commsun, commspwd, commss3bucket, adminapi  = get_config.get_creds("commsun", "commspwd", "commss3bucket", "adminapi")
     data = {
          "un": commsun,
          "pw": commspwd,
          "org_id": organization_id,
          "s3bucket": commss3bucket,
          "s3key": s3_file_name,
          "visible": "true"
          }
          
     headers = {"Content-Type": "application/json"}
     r = requests.post(adminapi, data= json.dumps(data), headers=headers)
     print(r)
     if r.status_code == 200:
          print("successfully uploaded to admin and made it visible to the partner")
     else: 
          print("error message while uploading to admin and making it visible: ", str(r.statuscode))
          print (r.reason)
          print(r.json())
