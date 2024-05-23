"""
function_base_path = '/home/luis/Zemee College_data_project/data-team/data_team_etl/helper_functions/'
sys.path.insert(0,function_base_path)
import query_athena_with_retry
importlib.reload(query_athena_with_retry)
query_df  = query_athena_with_retry.run_query_in_athena(query_string)
"""

def run_query_in_athena(query_string):
     import awswrangler as wr  
     from pyathena import connect
     from pyathena.pandas.util import as_pandas
     import time
     
     cursor = connect(
                      s3_staging_dir="s3://prod-zeemee-data-lake",
                      region_name="us-east-1").cursor()
     
     max_attempts = 3
     attempt = 1
     while attempt <= max_attempts:
          try:
               print('athena query attempt:', attempt)
               cursor.execute(query_string)
               df = as_pandas(cursor)
               attempt = attempt + max_attempts
               
          except Exception as e:
               print(e)
               error_string = str(e)
               print(e)
               if 'does not exist' in error_string:
                    print('sleeping for 5 seconds')
                    time.sleep(3 ** attempt)
               print('attempt:', attempt, e)
               attempt = attempt + 1
               
     return df

