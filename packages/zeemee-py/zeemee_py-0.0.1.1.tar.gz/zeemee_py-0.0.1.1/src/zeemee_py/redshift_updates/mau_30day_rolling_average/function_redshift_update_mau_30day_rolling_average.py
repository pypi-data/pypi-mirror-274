
def update_redshift_table(df):
     import pandas as pd
     import os
     import importlib
     
     s3_filename_for_update = "s3://zeemee-data-team-files/zeemee_py/redshift_tables/mau_30day_rolling_average_table.csv"
     s3_file_name = s3_filename_for_update.split("/")[-1]
     
     #ensuring columns are always arranged correctly
     column_list = [
          "date",
          "mau",
          "platform",
          "aggregation_type"
          ]
     
     #data clean-up to load into Redshift
     int_columns = [
          "mau"
          ]
     
     for col in int_columns:
         for i in range(len(df)):
             df.loc[i, col] = str(df.loc[i, col]).split(".")[0]
     
     df =  df.replace("nan", "") 
     df =  df.fillna("") 
     df = df[column_list]
     df_columns_str = ",".join(df.columns)
     
     print("additional_fields_all_partner_table columns needed:", len(column_list))
     print("columns in df after subsetting-", len(df.columns))
     
     from zeemee_py.helper_functions import send_dataframe_to_s3
     importlib.reload(send_dataframe_to_s3)
     send_dataframe_to_s3.send_dataframe_to_s3(s3_filename_for_update, df)
     
     from zeemee_py.helper_functions import get_config
     accesskeyid, accesskey, bucket_name = get_config.get_creds('accesskeyid', 'accesskey', 'datateams3bucket')
     
     #establishing connection with redshift
     #sys.path.insert(0,'/home/luis/Zemee College_data_project/python_report_projects/helper_functions/')
     from zeemee_py.helper_functions import connect_redshift
     importlib.reload(connect_redshift)
     con = connect_redshift.establish_redshift_connection()
     cur = con.cursor()
     
     #create staging table
     create_staging_table = """
     create temp table staging_mau_data (
     date date,
     mau int,
     platform varchar(80),
     aggregation_type varchar(80)
          )
          """
     cur.execute(create_staging_table)
     con.commit()
     print("staging created")
     
     #copy data from S3 to staging table
     staging_table_copy_command = """
     COPY staging_mau_data ({})
     FROM '{}'
     credentials 'aws_access_key_id= {};aws_secret_access_key={}'
     CSV
     NULL 'NaN'
     DATEFORMAT 'YYYY-MM-DD'
     ignoreheader 1;""".format(
          df_columns_str,
          s3_filename_for_update,
          accesskeyid,
          accesskey
          )
     cur.execute(staging_table_copy_command)
     con.commit()
     print('copied data to staging')
     
     #delete rows in actual table which are to be replaced
     delete_rows_to_be_updated = """
     delete from data_team.mau_data
     using staging_mau_data
     where 
     data_team.mau_data.date = staging_mau_data.date and 
     data_team.mau_data.platform = staging_mau_data.platform and 
     data_team.mau_data.aggregation_type = staging_mau_data.aggregation_type
     """
     cur.execute(delete_rows_to_be_updated)
     con.commit()
     
     #insert data from staging table into actual table
     insert_into_table = """
     insert into data_team.mau_data
     ({})
     select {} from staging_mau_data;
     """.format(df_columns_str,df_columns_str)
     cur.execute(insert_into_table)
     con.commit()
     print('copied data to main script')
     
     #drop staging table
     drop_staging_table = """
     drop table staging_mau_data
     """
     cur.execute(drop_staging_table)
     con.commit()
     
     con.close()
     print('staging table dropped')
     
     print('mau_data table Redshift update completed')
     
          
