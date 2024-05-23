def create_schedule(schedule_id, organization_id, cohort_year, schedule_time, email_list, org_name):
     
     import datetime
     import requests
     import importlib
     import os
     
     today_date = datetime.datetime.now()
     current_month = today_date.strftime("%B")
     current_year = today_date.strftime("%Y")
     
     from zeemee_py.helper_functions import get_config
     importlib.reload(get_config)
     holisticskey, holisticsurl = get_config.get_creds("holisticskey", "holisticsurl") 
     
     headers = {"X-Holistics-Key": holisticskey, "Content-Type": "application/json"}
     
     email_subject = "ZeeMee Community Snapshot | " + org_name + " | " + current_month + " " + current_year
     
     creation_parameters = {
          "data_schedule": {
               "id": schedule_id, # make sure to change
               "source_type": "Dashboard",
               "source_id": 56648,
               "schedule": {"repeat": schedule_time, "paused": False},
               "dynamic_filter_presets": [
                    {
                         "dynamic_filter_id": 65386, # 65386 is org id filter
                         "preset_condition": {"operator": "is", "values": [organization_id]}
                         },
                    {
                         "dynamic_filter_id": 65387, # 65387 is cohort year filter
                         "preset_condition": {"operator": "is", "values": [cohort_year]}
                         }
                    ],
               "dest": {
                    "type": "EmailDest",
                    "title": email_subject,
                    "recipients": email_list,
                    "options": {
                         "preview": False,
                          "include_header": False,
                         "include_report_link": False,
                         "include_filters": False,
                         "dont_send_when_empty": True,
                         "body_text":  """Here is your Monthly ZeeMee Community Snapshot. This report provides you with valuable data on how your community is performing and what steps you can take to maximize your engagement and recruitment efforts. Access your detailed dashboards at https://admin.zeemee.com/dash""",
                         "attachment_formats": ["png"]
                         }
                         }
                         }
                         }
          
     creation_response = requests.post(
          url= os.path.join(holisticsurl, "data_schedules"), 
          headers=headers, 
          json=creation_parameters
          )
          
     print(creation_response, creation_response.json())
     
     return creation_response.status_code
     

#schedule_id = 4
#organization_id = "ff4e416e-c1a0-44f0-9a1c-ba8312c93610"
#cohort_year = 2023
#schedule_time = "48 16 * * *"
#email_list = ["mayur@zeemee.com"]
#response_status_code = create_schedule(schedule_id, organization_id, cohort_year, schedule_time, email_list)
