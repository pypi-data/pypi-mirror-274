"""
function_base_path = '/home/luis/Zemee College_data_project/database_table_update/data_team_athena_code/helper_functions/'
sys.path.insert(0,function_base_path)
import query_athena_without_retry
importlib.reload(query_athena_without_retry)
query_df  = query_athena_without_retry.run_query_in_athena(query_string)
"""

def run_query_in_athena(query_string):
     import awswrangler as wr  
     from pyathena import connect
     from pyathena.pandas.util import as_pandas
     import time
     
     cursor = connect(
                      s3_staging_dir="s3://prod-zeemee-data-lake",
                      region_name="us-east-1").cursor()
     
     cursor.execute(query_string)
     df = as_pandas(cursor)
               
               
     return df

