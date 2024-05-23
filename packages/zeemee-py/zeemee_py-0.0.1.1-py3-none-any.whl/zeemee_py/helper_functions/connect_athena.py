def run_query_in_athena(query_string):
     #import awswrangler as wr  
     from pyathena import connect
     from pyathena.pandas.util import as_pandas
     from zeemee_py.helper_functions import get_config
     import time
     
     s3stagingdir, regionnameathena = get_config.get_creds("s3stagingdir", "regionnameathena")
     
     cursor = connect(
                      s3_staging_dir= s3stagingdir,
                      region_name= regionnameathena
                      ).cursor()
                      
     max_attempts = 3
     attempt = 1
     
     while attempt <= max_attempts:
          try:
               if attempt != 1:
                    print('athena query attempt:', attempt)
               cursor.execute(query_string)
               df = as_pandas(cursor)
               attempt = attempt + max_attempts
               
          except Exception as e:
               error_string = str(e)
               print('attempt:', attempt, error_string)
               if 'does not exist' in error_string:
                    time.sleep(3 ** attempt)
                    attempt = attempt + 1
               else:
                    print("error does not qualify for retrying")
                    attempt = attempt + max_attempts
        
     cursor.close()
     
     return df
