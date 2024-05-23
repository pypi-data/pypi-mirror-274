def get_file():
     import importlib
     import os
     
     from zeemee_py.helper_functions import get_config
     importlib.reload(get_config)
     datateams3bucket = get_config.get_creds("datateams3bucket")
     
     from zeemee_py.helper_functions import connect_duckdb
     importlib.reload(connect_duckdb)
     
     org_additional_path_in_s3 = os.path.join("s3://", datateams3bucket,"zeemee_py/operations/org_additional_table_data_current.csv")
     org_additional_df = connect_duckdb.get_file_df(org_additional_path_in_s3)
     
     return org_additional_df
