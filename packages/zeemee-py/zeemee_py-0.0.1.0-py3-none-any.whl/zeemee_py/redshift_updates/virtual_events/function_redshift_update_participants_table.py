def update_redshift_table(df):
     import pandas as pd
     import importlib
     import os
     
     s3_filename_for_update = "s3://zeemee-data-team-files/zeemee_py/redshift_tables/virtual_event_participants.csv"
     s3_file_name = s3_filename_for_update.split("/")[-1]
     
     #ensuring columns are always rearranged
     column_list = [
          "zeemee_id",
          "zm_status_analysis",
          "event_id",
          "date_of_update" 
          ]
     
     #data clean-up to load into Redshift
     int_columns = [
          "zeemee_id",
          "event_id"
          ]
          
     for col in int_columns:
         for i in range(len(df)):
             df.loc[i, col] = str(df.loc[i, col]).split(".")[0]
     
     df =  df.replace("nan", "") 
     df =  df.fillna("") 
     df = df[column_list]
     df_columns_str = ",".join(df.columns)
     
     print("virtual_event_participants columns needed:", len(column_list))
     print("columns in df after subsetting-", len(df.columns))
     
     from zeemee_py.helper_functions import send_dataframe_to_s3
     importlib.reload(send_dataframe_to_s3)
     send_dataframe_to_s3.send_dataframe_to_s3(s3_filename_for_update, df)
     
     from zeemee_py.helper_functions import get_config
     accesskeyid, accesskey, bucket_name = get_config.get_creds("accesskeyid", "accesskey", "datateams3bucket")
     
     from zeemee_py.helper_functions import connect_redshift
     importlib.reload(connect_redshift)
     con = connect_redshift.establish_redshift_connection()
     cur = con.cursor()

     #create staging table
     create_staging_table = """
     create temp table staging_virtual_participants_data (
     zeemee_id int,
     zm_status_analysis varchar(80),
     event_id int,
     date_of_update Date
     )
     """
     cur.execute(create_staging_table)
     con.commit()
     print("staging created")

     #copy data from S3 to staging table
     staging_table_copy_command = """
     COPY staging_virtual_participants_data ({})
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
     print("copied data to staging table")

     #delete rows in actual table which are to be replaced
     delete_rows_to_be_updated = """
     delete from data_team.virtual_event_participants
     using staging_virtual_participants_data
     where data_team.virtual_event_participants.event_id = staging_virtual_participants_data.event_id
     """
     cur.execute(delete_rows_to_be_updated)
     con.commit()
     print("rows to be updated deleted from main table")

     #insert data from staging table into actual table
     insert_into_table = """
     insert into data_team.virtual_event_participants
          ({})
     select {} from staging_virtual_participants_data;
     """.format(df_columns_str,df_columns_str)
     cur.execute(insert_into_table)
     con.commit()
     print('copied data to main table from staging')

     #drop staging table
     drop_staging_table = """
     drop table staging_virtual_participants_data
     """
     cur.execute(drop_staging_table)
     con.commit()
     print("staging table dropped")
     
     con.close()
     
     print("staging_virtual_participants_data table Redshift update completed")

