
def send_dataframe_to_s3(filepath_in_s3, data_df):
     import duckdb
     import importlib
     
     from zeemee_py.helper_functions import get_config
     importlib.reload(get_config)
     datateams3bucket, accesskeyid, accesskey = get_config.get_creds("datateams3bucket", "accesskeyid", "accesskey")
     
     con = duckdb.connect(database=':memory:', read_only=False)
     
     set_connection = """
          INSTALL httpfs;
          LOAD httpfs;
          CREATE SECRET secret1 (
               TYPE S3,
               KEY_ID '{accesskeyid}',
               SECRET '{accesskey}',
               REGION 'us-east-1'
               );
          """.format(
               accesskeyid = accesskeyid,
               accesskey = accesskey
          )
          
     con.sql(set_connection)
     
     try:
          file_df = con.sql(
               """COPY data_df TO '{filepath_in_s3}' (HEADER, DELIMITER ',');""".format(
                    filepath_in_s3 = filepath_in_s3
                    )
                    )
     except:
          print("unable to create file to s3 using duckdb:", filepath_in_s3)
     
