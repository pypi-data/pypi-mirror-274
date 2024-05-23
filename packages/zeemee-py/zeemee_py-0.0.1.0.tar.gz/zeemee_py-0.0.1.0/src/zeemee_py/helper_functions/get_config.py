
def get_creds( *args, project = "default", profile = "zeemee_dev"):
     import yaml
     import os
     import importlib
     
     from zeemee_py.helper_functions import get_data_folder_path
     importlib.reload(get_data_folder_path)
     data_folder_path = get_data_folder_path.get_data_folder_path()
     
     config_file_path = os.path.join(data_folder_path, "config.yml")
     
     with open(config_file_path, "r") as file:
         creds = yaml.safe_load(file)
         
     credential_list = list()
     
     for i in args:
          credential_list.append(creds[project][profile][i])
          
     if len(credential_list) == 1:
          return credential_list[0]
     else:
          return credential_list

