
def get_data_folder_path():
     import os
     from pathlib import Path
     
     data_folder_path = os.getcwd()
     data_folder_found = False
     
     try:
          while data_folder_found == False:
               files_in_folder = os.listdir(data_folder_path)
               if "data" in files_in_folder:
                    data_folder_found = True
               else:
                    data_folder_path = str(Path(data_folder_path).parents[0])
     except:
          print("error: unable to find the data folder")
          data_folder_path = ""
     
     return os.path.join(data_folder_path, "data")
