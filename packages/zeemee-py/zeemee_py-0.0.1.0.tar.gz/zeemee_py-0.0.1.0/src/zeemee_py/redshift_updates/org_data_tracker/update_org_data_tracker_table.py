
def update_organization_data_table():
     import importlib
     import os
     
     from zeemee_py.helper_functions import get_config
     importlib.reload(get_config)
     cohort_year, accesskeyid, accesskey = get_config.get_creds("current_cohort_year_for_database_tables", "accesskeyid", "accesskey")
     
     org_data_tracker_file_in_s3 = "s3://zeemee-data-team-files/zeemee_py/operations/org_data_tracker.csv"
     s3_filename_for_update = os.path.join("s3://zeemee-data-team-files/zeemee_py/redshift_tables/", "org_data_tracker.csv")
     
     from zeemee_py.helper_functions import connect_duckdb
     importlib.reload(connect_duckdb)
     org_data_tracker_df = connect_duckdb.get_file_df(organization_data_file_in_s3)
     
     org_data_tracker_df = org_data_tracker_df[org_data_tracker_df["zm_cohort_year"] >= cohort_year].reset_index(drop = True)
     
     column_list = [
          "slug", 
          "organization_id", 
          "zm_funnel_states", 
          "zm_stealth_check",
          "zm_race_check", 
          "zm_firstgen_check", 
          "zm_campus_visit_check",
          "zm_join_stage_check", 
          "zm_inq_date_check", 
          "zm_app_date_check",
          "zm_acc_date_check", 
          "zm_comm_date_check", 
          "zm_leads_present",
          "zm_acc_delay_present", 
          "partner_data_download_location",
          "data_frequency", 
          "full_pipeline", 
          "full_pipeline_run", 
          "auto_ingest",
          "current_cohort_included", 
          "hard_admit_delay", 
          "keep_leads",
          "admit_delay_days", 
          "Note"
          ]
     
     #data clean-up to load into Redshift
     #int_columns = [
     #     ]
          
     #for col in int_columns:
     #    for i in range(len(org_data_tracker_df)):
     #        org_data_tracker_df.loc[i, col] = str(org_data_tracker_df.loc[i, col]).split(".")[0]
     
     org_data_tracker_df =  org_data_tracker_df.replace("nan", "") 
     org_data_tracker_df =  org_data_tracker_df.fillna("") 
     org_data_tracker_df = org_data_tracker_df[column_list]
     column_list_str = ",".join(column_list)
     
     print("org data tracker columns needed:", len(column_list))
     print("columns in dataframe after subsetting-", len(org_data_tracker_df.columns))
     
     from zeemee_py.helper_functions import send_dataframe_to_s3
     importlib.reload(send_dataframe_to_s3)
     send_dataframe_to_s3.send_dataframe_to_s3(s3_filename_for_update, org_data_tracker_df)
     
     from zeemee_py.helper_functions import connect_redshift
     importlib.reload(connect_redshift)
     con = connect_redshift.establish_redshift_connection()
     cur = con.cursor()
     
     create_staging_table = """
     create temp table staging_org_data_tracker (
          slug varchar(200),
          organization_id varchar(200),
          zm_funnel_states varchar(200), 
          zm_stealth_check varchar(200),
          zm_race_check varchar(200), 
          zm_firstgen_check varchar(200), 
          zm_campus_visit_check varchar(200),
          zm_join_stage_check varchar(200), 
          zm_inq_date_check varchar(200), 
          zm_app_date_check varchar(200),
          zm_acc_date_check varchar(200), 
          zm_comm_date_check varchar(200), 
          zm_leads_present varchar(200),
          zm_acc_delay_present varchar(200), 
          partner_data_download_location varchar(200),
          data_frequency varchar(200), 
          full_pipeline varchar(200), 
          full_pipeline_run varchar(200), 
          auto_ingest varchar(200),
          current_cohort_included varchar(200), 
          hard_admit_delay varchar(200), 
          keep_leads varchar(200),
          admit_delay_days varchar(200), 
          Note varchar(200)
          )
     """
     cur.execute(create_staging_table)
     con.commit()
     print("staging created")
          
     
     staging_table_copy_command = """COPY staging_org_data_tracker ({})
     FROM '{}'
     credentials 'aws_access_key_id= {};aws_secret_access_key={}'
     DATEFORMAT 'YYYY-MM-DD'
     CSV
     ignoreheader 1;""".format(column_list_str,
                               s3_filename_for_update,
                               accesskeyid,
                               accesskey)
     cur.execute(staging_table_copy_command)
     con.commit()
     print("data copied to staging")
     
     
     delete_rows_to_be_updated = """
     delete from data_team.org_data_tracker
     using staging_org_data_tracker
     where 
     data_team.org_data_tracker.organization_id = staging_org_data_tracker.organization_id and 
     data_team.organization_data.zm_cohort_year = staging_organization_data.zm_cohort_year
     """
     cur.execute(delete_rows_to_be_updated)
     con.commit()
     print("duplicate data deleted from main table")
     
     
     insert_into_table = """
     insert into data_team.org_data_tracker
           ({})
     select {} 
     from staging_org_data_tracker;
     """.format(
          column_list_str,
          column_list_str
          )
     cur.execute(insert_into_table)
     con.commit()
     print("data inserted into main table")
     
     
     drop_staging_table = """
     drop table staging_org_data_tracker
     """
     cur.execute(drop_staging_table)
     con.commit()
     print("org_data_tracker table update complete")
     
     con.close()
















