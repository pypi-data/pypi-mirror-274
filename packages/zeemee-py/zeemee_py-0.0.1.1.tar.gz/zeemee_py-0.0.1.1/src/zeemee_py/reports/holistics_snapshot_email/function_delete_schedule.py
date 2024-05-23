
def delete_schedule(schedule_id):
     import requests
     import importlib
     import os
     
     from zeemee_py.helper_functions import get_config
     importlib.reload(get_config)
     holisticskey, holisticsurl = get_config.get_creds("holisticskey", "holisticsurl") 
     
     headers = {"X-Holistics-Key": holisticskey, "Content-Type": "application/json"}
     
     delete_response = requests.delete(
          url=os.path.join(holisticsurl, "data_schedules/{id}".format(id = schedule_id)), 
          headers=headers
          )

     return delete_response.status_code
