import importlib
import os

from zeemee_py.helper_functions import get_config
importlib.reload(get_config)
datateams3bucket = get_config.get_creds("datateams3bucket")

from zeemee_py.helper_functions import connect_duckdb
importlib.reload(connect_duckdb)

org_data_tracker_path_in_s3 = os.path.join("s3://", datateams3bucket,"zeemee_py/operations/org_data_tracker.csv")
print(org_data_tracker_path_in_s3)
print("s3://" + datateams3bucket +"/zeemee_py/operations/org_data_tracker.csv")
