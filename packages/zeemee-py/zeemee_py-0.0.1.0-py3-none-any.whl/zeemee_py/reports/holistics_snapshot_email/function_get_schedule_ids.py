def get_schedule_ids():
     import requests
     import importlib
     import os
     
     from zeemee_py.helper_functions import get_config
     importlib.reload(get_config)
     holisticskey, holisticsurl = get_config.get_creds("holisticskey", "holisticsurl") 
     
     headers = {"X-Holistics-Key": holisticskey, "Content-Type": "application/json"}
     
     all_schedule_ids = {}
     next_cursor = None
     keep_going = True
     
     while(keep_going):
          list_parameters = {"limit":2, "after":next_cursor}
          list_response = requests.get(
               url=os.path.join(holisticsurl, "data_schedules"), 
               headers=headers, 
               params=list_parameters
               )
                              
          print(list_response.json())
          
          for cur in list_response.json()["data_schedules"]:
               if(cur["source_id"] in all_schedule_ids):
                    all_schedule_ids[cur["source_id"]].append(cur["id"])
               else:
                    all_schedule_ids[cur["source_id"]] = [cur["id"]]
                    next_cursor = list_response.json()["cursors"]["next"]
                    keep_going = next_cursor is not None
                    
     return all_schedule_ids
