def update_redshift_table(df):
                      
     import pandas as pd
     import os
     import importlib
     
     s3_filename_for_update = "s3://zeemee-data-team-files/zeemee_py/redshift_tables/touchpoint_dash.csv"
     s3_file_name = s3_filename_for_update.split("/")[-1]
     
     #ensuring columns are always arranged correctly
     column_list = [
          "org_id",
          "cohort_year",
          "total_students_all", 
          "community_matched_all", 
          "count_current_cohort_year_all", 
          "engaged_any_all", 
          "engaged_any_null_all", 
          "engaged_1_week_all", 
          "engaged_2_week_all", 
          "engaged_3_week_all", 
          "engaged_4_week_all", 
          "engaged_5_60_days_or_less_all", 
          "engaged_6_90_days_or_less_all", 
          "engaged_7_more_than_90_days_all", 
          "login_1_week_all", 
          "login_2_week_all", 
          "login_3_week_all", 
          "login_4_week_all", 
          "login_5_60_days_or_less_all", 
          "login_6_90_days_or_less_all", 
          "login_7_more_than_90_days_all", 
          "going_going_all", 
          "going_not_all", 
          "going_undecided_all", 
          "community_joined_stage_pre_inquired_all", 
          "community_joined_stage_inquired_all", 
          "community_joined_stage_applied_all", 
          "community_joined_stage_app_complete_all", 
          "community_joined_stage_accepted_all", 
          "community_joined_stage_committed_all", 
          "community_joined_stage_missing_all", 
          "friend_finder_used_all", 
          "roommate_quiz_completed_all", 
          "total_students_accepted_comm", 
          "community_matched_accepted_comm", 
          "count_current_cohort_year_accepted_comm", 
          "engaged_any_accepted_comm", 
          "engaged_any_null_accepted_comm", 
          "engaged_1_week_accepted_comm", 
          "engaged_2_week_accepted_comm", 
          "engaged_3_week_accepted_comm", 
          "engaged_4_week_accepted_comm", 
          "engaged_5_60_days_or_less_accepted_comm", 
          "engaged_6_90_days_or_less_accepted_comm", 
          "engaged_7_more_than_90_days_accepted_comm", 
          "login_1_week_accepted_comm", 
          "login_2_week_accepted_comm", 
          "login_3_week_accepted_comm", 
          "login_4_week_accepted_comm", 
          "login_5_60_days_or_less_accepted_comm", 
          "login_6_90_days_or_less_accepted_comm", 
          "login_7_more_than_90_days_accepted_comm", 
          "going_going_accepted_comm", 
          "going_not_accepted_comm", 
          "going_undecided_accepted_comm", 
          "community_joined_stage_pre_inquired_accepted_comm",
          "community_joined_stage_inquired_accepted_comm", 
          "community_joined_stage_applied_accepted_comm", 
          "community_joined_stage_app_complete_accepted_comm", 
          "community_joined_stage_accepted_accepted_comm", 
          "community_joined_stage_committed_accepted_comm", 
          "community_joined_stage_missing_accepted_comm", 
          "friend_finder_used_accepted_comm", 
          "roommate_quiz_completed_accepted_comm", 
          "low_zm_index_accepted_comm", 
          "medium_zm_index_accepted_comm", 
          "high_zm_index_accepted_comm", 
          "low_going_zm_index_accepted_comm", 
          "medium_going_zm_index_accepted_comm", 
          "high_going_zm_index_accepted_comm", 
          "low_undecided_zm_index_accepted_comm", 
          "medium_undecided_zm_index_accepted_comm", 
          "high_undecided_zm_index_accepted_comm", 
          "low_not_going_zm_index_accepted_comm", 
          "medium_not_going_zm_index_accepted_comm", 
          "high_not_going_zm_index_accepted_comm",
          "non_crm_id_users",
          "high_zm_index_committed_accepted_comm",
          "high_zm_index_non_committed_accepted_comm",
          "medium_zm_index_committed_accepted_comm",
          "medium_zm_index_non_committed_accepted_comm", 
          "low_zm_index_committed_accepted_comm",
          "low_zm_index_non_committed_accepted_comm",
          "entry_term",
          "student_type",
          "with_student_id_count_accepted_comm",
          "with_student_id_count_all",
          "date_of_report",
          "high_zm_index_committed_all",
          "high_zm_index_non_committed_all",
          "medium_zm_index_committed_all",
          "medium_zm_index_non_committed_all",
          "low_zm_index_committed_all",
          "low_zm_index_non_committed_all",
          "going_not_committed",
          "high_zm_index_committed_non_accepted_community",
          "high_zm_index_non_committed_non_accepted_community",
          "medium_zm_index_committed_non_accepted_community",
          "medium_zm_index_non_committed_non_accepted_community",
          "low_zm_index_committed_non_accepted_community",
          "low_zm_index_non_committed_non_accepted_community"
               ]
               
     #data clean-up to load into Redshift
     int_columns = [
          "cohort_year",
          "total_students_all", 
          "community_matched_all", 
          "count_current_cohort_year_all", 
          "engaged_any_all", 
          "engaged_any_null_all", 
          "engaged_1_week_all", 
          "engaged_2_week_all", 
          "engaged_3_week_all", 
          "engaged_4_week_all", 
          "engaged_5_60_days_or_less_all", 
          "engaged_6_90_days_or_less_all", 
          "engaged_7_more_than_90_days_all", 
          "login_1_week_all", 
          "login_2_week_all", 
          "login_3_week_all", 
          "login_4_week_all", 
          "login_5_60_days_or_less_all", 
          "login_6_90_days_or_less_all", 
          "login_7_more_than_90_days_all", 
          "going_going_all", 
          "going_not_all", 
          "going_undecided_all", 
          "community_joined_stage_pre_inquired_all", 
          "community_joined_stage_inquired_all", 
          "community_joined_stage_applied_all", 
          "community_joined_stage_app_complete_all", 
          "community_joined_stage_accepted_all", 
          "community_joined_stage_committed_all", 
          "community_joined_stage_missing_all", 
          "friend_finder_used_all", 
          "roommate_quiz_completed_all", 
          "total_students_accepted_comm", 
          "community_matched_accepted_comm", 
          "count_current_cohort_year_accepted_comm", 
          "engaged_any_accepted_comm", 
          "engaged_any_null_accepted_comm", 
          "engaged_1_week_accepted_comm", 
          "engaged_2_week_accepted_comm", 
          "engaged_3_week_accepted_comm", 
          "engaged_4_week_accepted_comm", 
          "engaged_5_60_days_or_less_accepted_comm", 
          "engaged_6_90_days_or_less_accepted_comm", 
          "engaged_7_more_than_90_days_accepted_comm", 
          "login_1_week_accepted_comm", 
          "login_2_week_accepted_comm", 
          "login_3_week_accepted_comm", 
          "login_4_week_accepted_comm", 
          "login_5_60_days_or_less_accepted_comm", 
          "login_6_90_days_or_less_accepted_comm", 
          "login_7_more_than_90_days_accepted_comm", 
          "going_going_accepted_comm", 
          "going_not_accepted_comm", 
          "going_undecided_accepted_comm", 
          "community_joined_stage_pre_inquired_accepted_comm",
          "community_joined_stage_inquired_accepted_comm", 
          "community_joined_stage_applied_accepted_comm", 
          "community_joined_stage_app_complete_accepted_comm", 
          "community_joined_stage_accepted_accepted_comm", 
          "community_joined_stage_committed_accepted_comm", 
          "community_joined_stage_missing_accepted_comm", 
          "friend_finder_used_accepted_comm", 
          "roommate_quiz_completed_accepted_comm", 
          "low_zm_index_accepted_comm", 
          "medium_zm_index_accepted_comm", 
          "high_zm_index_accepted_comm", 
          "low_going_zm_index_accepted_comm", 
          "medium_going_zm_index_accepted_comm", 
          "high_going_zm_index_accepted_comm", 
          "low_undecided_zm_index_accepted_comm", 
          "medium_undecided_zm_index_accepted_comm", 
          "high_undecided_zm_index_accepted_comm", 
          "low_not_going_zm_index_accepted_comm", 
          "medium_not_going_zm_index_accepted_comm", 
          "high_not_going_zm_index_accepted_comm",
          "non_crm_id_users",
          "high_zm_index_committed_accepted_comm",
          "high_zm_index_non_committed_accepted_comm",
          "medium_zm_index_committed_accepted_comm",
          "medium_zm_index_non_committed_accepted_comm", 
          "low_zm_index_committed_accepted_comm",
          "low_zm_index_non_committed_accepted_comm",
          "with_student_id_count_accepted_comm",
          "with_student_id_count_all",
          "high_zm_index_committed_all",
          "high_zm_index_non_committed_all",
          "medium_zm_index_committed_all",
          "medium_zm_index_non_committed_all",
          "low_zm_index_committed_all",
          "low_zm_index_non_committed_all",
          "going_not_committed",
          "high_zm_index_committed_non_accepted_community",
          "high_zm_index_non_committed_non_accepted_community",
          "medium_zm_index_committed_non_accepted_community",
          "medium_zm_index_non_committed_non_accepted_community",
          "low_zm_index_committed_non_accepted_community",
          "low_zm_index_non_committed_non_accepted_community"
          ]
     
     for col in int_columns:
         for i in range(len(df)):
             df.loc[i, col] = str(df.loc[i, col]).split(".")[0]
     
     df =  df.replace("nan", "") 
     df =  df.fillna("") 
     df = df[column_list]
     df_columns_str = ",".join(df.columns)
     
     print("touchpoint_dash columns needed:", len(column_list))
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
     create temp table staging_touchpoint_dash_data (  
     org_id varchar(80),
     cohort_year int,
     total_students_all int, 
     community_matched_all int, 
     count_current_cohort_year_all int, 
     engaged_any_all int, 
     engaged_any_null_all int, 
     engaged_1_week_all int, 
     engaged_2_week_all int, 
     engaged_3_week_all int, 
     engaged_4_week_all int, 
     engaged_5_60_days_or_less_all int, 
     engaged_6_90_days_or_less_all int, 
     engaged_7_more_than_90_days_all int, 
     login_1_week_all int, 
     login_2_week_all int, 
     login_3_week_all int, 
     login_4_week_all int, 
     login_5_60_days_or_less_all int, 
     login_6_90_days_or_less_all int, 
     login_7_more_than_90_days_all int, 
     going_going_all int, 
     going_not_all int, 
     going_undecided_all int, 
     community_joined_stage_pre_inquired_all int, 
     community_joined_stage_inquired_all int, 
     community_joined_stage_applied_all int, 
     community_joined_stage_app_complete_all int, 
     community_joined_stage_accepted_all int, 
     community_joined_stage_committed_all int, 
     community_joined_stage_missing_all int, 
     friend_finder_used_all int, 
     roommate_quiz_completed_all int, 
     total_students_accepted_comm int, 
     community_matched_accepted_comm int, 
     count_current_cohort_year_accepted_comm int, 
     engaged_any_accepted_comm int, 
     engaged_any_null_accepted_comm int, 
     engaged_1_week_accepted_comm int, 
     engaged_2_week_accepted_comm int, 
     engaged_3_week_accepted_comm int, 
     engaged_4_week_accepted_comm int, 
     engaged_5_60_days_or_less_accepted_comm int, 
     engaged_6_90_days_or_less_accepted_comm int, 
     engaged_7_more_than_90_days_accepted_comm int, 
     login_1_week_accepted_comm int, 
     login_2_week_accepted_comm int, 
     login_3_week_accepted_comm int, 
     login_4_week_accepted_comm int, 
     login_5_60_days_or_less_accepted_comm int, 
     login_6_90_days_or_less_accepted_comm int, 
     login_7_more_than_90_days_accepted_comm int, 
     going_going_accepted_comm int, 
     going_not_accepted_comm int, 
     going_undecided_accepted_comm int, 
     community_joined_stage_pre_inquired_accepted_comm int,
     community_joined_stage_inquired_accepted_comm int, 
     community_joined_stage_applied_accepted_comm int, 
     community_joined_stage_app_complete_accepted_comm int, 
     community_joined_stage_accepted_accepted_comm int, 
     community_joined_stage_committed_accepted_comm int, 
     community_joined_stage_missing_accepted_comm int, 
     friend_finder_used_accepted_comm int, 
     roommate_quiz_completed_accepted_comm int, 
     low_zm_index_accepted_comm int, 
     medium_zm_index_accepted_comm int, 
     high_zm_index_accepted_comm int, 
     low_going_zm_index_accepted_comm int, 
     medium_going_zm_index_accepted_comm int, 
     high_going_zm_index_accepted_comm int, 
     low_undecided_zm_index_accepted_comm int, 
     medium_undecided_zm_index_accepted_comm int, 
     high_undecided_zm_index_accepted_comm int, 
     low_not_going_zm_index_accepted_comm int, 
     medium_not_going_zm_index_accepted_comm int, 
     high_not_going_zm_index_accepted_comm int,
     non_crm_id_users int,
     high_zm_index_committed_accepted_comm int,
     high_zm_index_non_committed_accepted_comm int,
     medium_zm_index_committed_accepted_comm int,
     medium_zm_index_non_committed_accepted_comm int, 
     low_zm_index_committed_accepted_comm int,
     low_zm_index_non_committed_accepted_comm int,
     entry_term varchar(40),
     student_type varchar(40),
     with_student_id_count_accepted_comm int,
     with_student_id_count_all int,
     date_of_report date,
     high_zm_index_committed_all int,
     high_zm_index_non_committed_all int,
     medium_zm_index_committed_all int,
     medium_zm_index_non_committed_all int,
     low_zm_index_committed_all int,
     low_zm_index_non_committed_all int,
     going_not_committed int,
     high_zm_index_committed_non_accepted_community int,
     high_zm_index_non_committed_non_accepted_community int,
     medium_zm_index_committed_non_accepted_community int,
     medium_zm_index_non_committed_non_accepted_community int,
     low_zm_index_committed_non_accepted_community int,
     low_zm_index_non_committed_non_accepted_community int
     )
     """
     cur.execute(create_staging_table)
     con.commit()
     print('staging created')
     
     #copy data from S3 to staging table
     staging_table_copy_command = """
     COPY staging_touchpoint_dash_data ({})
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
     delete from data_team.touchpoint_dash_data
     using staging_touchpoint_dash_data
     where data_team.touchpoint_dash_data.org_id = staging_touchpoint_dash_data.org_id
     and data_team.touchpoint_dash_data.cohort_year = staging_touchpoint_dash_data.cohort_year
     and data_team.touchpoint_dash_data.entry_term = staging_touchpoint_dash_data.entry_term
     and data_team.touchpoint_dash_data.student_type = staging_touchpoint_dash_data.student_type
     """
     cur.execute(delete_rows_to_be_updated)
     con.commit()
     print('rows to be updated deleted from main table')
     
     
     #insert data from staging table into actual table
     insert_into_table = """
     insert into data_team.touchpoint_dash_data
        ({})
     select {} from staging_touchpoint_dash_data;
     """.format(df_columns_str,df_columns_str)
     cur.execute(insert_into_table)
     con.commit()
     print('copied data to main script from staging')
     
     #drop staging table
     drop_staging_table = """
     drop table staging_touchpoint_dash_data
     """
     cur.execute(drop_staging_table)
     con.commit()
     print('staging table dropped')
     
     con.close()
     
     print('touchpoint dash table Redshift update completed')
     
     
