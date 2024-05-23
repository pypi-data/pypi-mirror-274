def update_redshift_table(df):
     
     import pandas as pd
     import importlib
     import os
     
     s3_filename_for_update = "s3://zeemee-data-team-files/zeemee_py/redshift_tables/one_pager_table_data.csv"
     s3_file_name = s3_filename_for_update.split("/")[-1]
     
     #ensuring columns are always rearranged
     column_list = [
          "org_id",
          "cohort_year",
          "student_type", 
          "entry_term",
          "num_comm_match_inquired",
          "num_comm_match_applied",
          "num_comm_match_accepted",
          "num_comm_match_committed",
          "num_comm_match_enrolled",
          "num_preinq_inquired",
          "num_preinq_applied",
          "num_preinq_accepted",
          "num_preinq_committed",
          "num_preinq_enrolled",
          "num_organic_inquired",
          "num_organic_applied",
          "num_organic_accepted",
          "num_organic_committed",
          "num_organic_enrolled",
          "num_nondupe_ntr_inquired",
          "num_nondupe_ntr_applied",
          "num_nondupe_ntr_accepted",
          "num_nondupe_ntr_committed",
          "num_nondupe_ntr_enrolled",
          "community_funnel_inquired_1",
          "community_funnel_applied_1",
          "community_funnel_accepted_1",
          "community_funnel_committed_1",
          "community_funnel_enrolled_1",
          "per_comm_match_inquired",
          "per_comm_match_applied",
          "per_comm_match_accepted",
          "per_comm_match_committed",
          "per_comm_match_enrolled",
          "per_preinq_inquired",
          "per_preinq_applied",
          "per_preinq_accepted",
          "per_preinq_committed",
          "per_preinq_enrolled",
          "per_organic_inquired",
          "per_organic_applied",
          "per_organic_accepted",
          "per_organic_committed",
          "per_organic_enrolled",
          "per_nondupe_ntr_inquired",
          "per_nondupe_ntr_applied",
          "per_nondupe_ntr_accepted",
          "per_nondupe_ntr_committed",
          "per_nondupe_ntr_enrolled"
     ]
     
     #data clean-up to load into Redshift
     int_columns = [
          "cohort_year",
          "num_comm_match_inquired",
          "num_comm_match_applied",
          "num_comm_match_accepted",
          "num_comm_match_committed",
          "num_comm_match_enrolled",
          "num_preinq_inquired",
          "num_preinq_applied",
          "num_preinq_accepted",
          "num_preinq_committed",
          "num_preinq_enrolled",
          "num_organic_inquired",
          "num_organic_applied",
          "num_organic_accepted",
          "num_organic_committed",
          "num_organic_enrolled",
          "num_nondupe_ntr_inquired",
          "num_nondupe_ntr_applied",
          "num_nondupe_ntr_accepted",
          "num_nondupe_ntr_committed",
          "num_nondupe_ntr_enrolled",
          "community_funnel_inquired_1",
          "community_funnel_applied_1",
          "community_funnel_accepted_1",
          "community_funnel_committed_1",
          "community_funnel_enrolled_1"
          ]
          
     for col in int_columns:
         for i in range(len(df)):
             df.loc[i, col] = str(df.loc[i, col]).split(".")[0]
     
     df =  df.replace("nan", "") 
     df =  df.fillna("") 
     df = df[column_list]
     df_columns_str = ",".join(df.columns)
     
     print("one_pager_table columns needed:", len(column_list))
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
          create temp table staging_one_pager_data (  
          org_id varchar(80),
          cohort_year int,
          student_type varchar(40), 
          entry_term varchar(40),
          num_comm_match_inquired int,
          num_comm_match_applied int,
          num_comm_match_accepted int,
          num_comm_match_committed int,
          num_comm_match_enrolled int,
          num_preinq_inquired int,
          num_preinq_applied int,
          num_preinq_accepted int,
          num_preinq_committed int,
          num_preinq_enrolled int,
          num_organic_inquired int,
          num_organic_applied int,
          num_organic_accepted int,
          num_organic_committed int,
          num_organic_enrolled int,
          num_nondupe_ntr_inquired int,
          num_nondupe_ntr_applied int,
          num_nondupe_ntr_accepted int,
          num_nondupe_ntr_committed int,
          num_nondupe_ntr_enrolled int,
          community_funnel_inquired_1 int,
          community_funnel_applied_1 int,
          community_funnel_accepted_1 int,
          community_funnel_committed_1 int,
          community_funnel_enrolled_1 int,
          per_comm_match_inquired numeric(6,4),
          per_comm_match_applied numeric(6,4),
          per_comm_match_accepted numeric(6,4),
          per_comm_match_committed numeric(6,4),
          per_comm_match_enrolled numeric(6,4),
          per_preinq_inquired numeric(6,4),
          per_preinq_applied numeric(6,4),
          per_preinq_accepted numeric(6,4),
          per_preinq_committed numeric(6,4),
          per_preinq_enrolled numeric(6,4),
          per_organic_inquired numeric(6,4),
          per_organic_applied numeric(6,4),
          per_organic_accepted numeric(6,4),
          per_organic_committed numeric(6,4),
          per_organic_enrolled numeric(6,4),
          per_nondupe_ntr_inquired numeric(6,4),
          per_nondupe_ntr_applied numeric(6,4),
          per_nondupe_ntr_accepted numeric(6,4),
          per_nondupe_ntr_committed numeric(6,4),
          per_nondupe_ntr_enrolled numeric(6,4)
          )
     """
     cur.execute(create_staging_table)
     con.commit()
     
     print("staging table created")
     
     #copy data from S3 to staging table
     staging_table_copy_command = """
     COPY staging_one_pager_data ({})
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
     delete from data_team.one_pager_data
     using staging_one_pager_data
     where 
     data_team.one_pager_data.org_id = staging_one_pager_data.org_id
     and data_team.one_pager_data.cohort_year = staging_one_pager_data.cohort_year
     and data_team.one_pager_data.entry_term = staging_one_pager_data.entry_term
     and data_team.one_pager_data.student_type = staging_one_pager_data.student_type
     """
     cur.execute(delete_rows_to_be_updated)
     con.commit()
     print("rows to be updated deleted from main table")
     
     
     #insert data from staging table into actual table
     insert_into_table = """
     insert into data_team.one_pager_data
     ({})
     select {} from staging_one_pager_data;
     """.format(
          df_columns_str,df_columns_str
          )
     cur.execute(insert_into_table)
     con.commit()
     print("copied data to main table from staging")
     
     #drop staging table
     drop_staging_table = """
     drop table staging_one_pager_data
     """
     cur.execute(drop_staging_table)
     con.commit()
     print("staging table dropped")
     con.close()
     
     print("one_pager_data table Redshift update completed")
