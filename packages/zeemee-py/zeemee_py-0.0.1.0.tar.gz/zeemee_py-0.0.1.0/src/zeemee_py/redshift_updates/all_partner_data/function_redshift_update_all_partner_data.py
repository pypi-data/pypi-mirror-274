
def update_redshift_table(df):
                      
     import pandas as pd
     import os
     import importlib
     
     s3_filename_for_update = "s3://zeemee-data-team-files/zeemee_py/redshift_tables/all_partner_data.csv"
     s3_file_name = s3_filename_for_update.split("/")[-1]
     
     #ensuring columns are always arranged correctly
     column_list = [
          "org_id",
          "org_name",
          "entry_year",
          "student_type",
          "entry_term",
          "total_funnel_inquired",
          "total_funnel_applied",
          "total_funnel_comp_app",
          "total_funnel_accepted",
          "total_funnel_deposit",
          "total_funnel_net_dep_enrolled",
          "non_comm_funnel_inquired",
          "non_comm_funnel_applied",
          "non_comm_funnel_comp_app",
          "non_comm_funnel_accepted",
          "non_comm_funnel_deposit",
          "non_comm_funnel_net_dep_enrolled",
          "community_funnel_inquired",
          "community_funnel_applied",
          "community_funnel_comp_app",
          "community_funnel_accepted",
          "community_funnel_deposit",
          "community_funnel_net_dep_enrolled",
          "percent_inq_in_community",
          "percent_apps_in_community",
          "percent_comp_app_in_community",
          "percent_accept_in_community",
          "percent_deposit_in_community",
          "percent_net_dep_enr_in_community",
          "unadjusted_non_comm_app_rate",
          "unadjusted_community_app_rate",
          "unadjusted_non_comm_dep_rate",
          "unadjusted_community_dep_rate",
          "unadjusted_non_comm_melt_rate",
          "unadjusted_community_melt_rate",
          "unadjusted_non_comm_yield_rate",
          "unadjusted_community_yield_rate",
          "comm_delta_app_rate_unadjusted",
          "comm_delta_dep_rate_unadjusted",
          "comm_delta_melt_rate_unadjusted",
          "comm_delta_yield_rate_unadjusted",
          "community_entered_term_pre_inquired",
          "community_entered_term_inquired",
          "community_entered_term_applied",
          "community_entered_term_app_completed",
          "community_entered_term_accepted",
          "community_entered_term_committed",
          "community_entered_term_stage_missing",
          "stealth_appsnon_community_inquired",
          "stealth_appsnon_community_applied",
          "missing_inq_date",
          "missing_app_date",
          "missing_comp_app_date",
          "missing_acc_date",
          "missing_commit_date",
          "app_rate_never_in_community",
          "app_rate_never_in_community_sans_stealth",
          "app_rate_never_in_community_with_stealth",
          "app_rate_not_in_comm_in_comm_as_app_after",
          "app_rate_not_in_comm_in_comm_as_app_after_sans_stealth",
          "app_rate_in_comm_in_comm_prior_to_app",
          "commitment_rate_never_in_community",
          "commitment_rate_not_in_comm_in_comm_as_dep",
          "commitment_rate_in_comm_in_comm_prior_to_dep",
          "commitment_rate_in_comm_as_inquired",
          "commitment_rate_in_comm_as_applied",
          "commitment_rate_in_comm_as_comp_app",
          "commitment_rate_in_comm_as_accept",
          "melt_rate_never_in_community",
          "melt_rate_in_communtyall",
          "melt_rate_in_comm_as_inquired",
          "melt_rate_in_comm_as_applied",
          "melt_rate_in_comm_as_comp_app",
          "melt_rate_in_comm_as_comp_accept",
          "melt_rate_in_comm_as_commitment",
          "yield_rate_never_in_community",
          "yield_rate_not_in_comm_in_comm_as_deposit",
          "yield_rate_in_comm_in_comm_prior_to_deposit",
          "yield_rateall_regardless_of_joinstage",
          "yield_rate_in_comm_as_inquired",
          "yield_rate_in_comme_as_applied",
          "yield_rate_in_comm_as_comp_app",
          "yield_rate_in_comm_as_accepted",
          "zm_cv_flag_campus_visit",
          "zm_first_gen_first_generation",
          "zm_text_opt_out_text_opt_out",
          "zm_email_opt_out_email_opt_out",
          "zm_race_ethnicity_asian",
          "zm_race_ethnicity_american_indian_or_alaska_native",
          "zm_race_ethnicity_black_or_african_american",
          "zm_race_ethnicity_hispanic_of_any_race",
          "zm_race_ethnicity_native_hawaiian_or_other_pacific",
          "zm_race_ethnicity_white",
          "zm_race_ethnicity_nonresident_alien",
          "zm_race_ethnicity_prefer_not_to_respond",
          "zm_race_ethnicity_race_ethnicity_unknown",
          "zm_race_ethnicity_two_or_more_races",
          "csv_update_date",
          "yield_rate_in_comm_as_pre_inquired",
          "yield_rate_in_comm_as_deposit",
          "percent_community_entered_term_pre_inquired",
          "percent_community_entered_term_inquired",
          "percent_community_entered_term_applied",
          "percent_community_entered_term_app_completed",
          "percent_community_entered_term_accepted",
          "percent_community_entered_term_committed",
          "percent_community_entered_term_stage_missing"
          ]
          
     #data clean-up to load into Redshift
     int_columns = [
          "total_funnel_inquired", 
          "total_funnel_applied",
          "total_funnel_comp_app", 
          "total_funnel_accepted",
          "total_funnel_deposit", 
          "total_funnel_net_dep_enrolled",
          "non_comm_funnel_inquired", 
          "non_comm_funnel_applied",
          "non_comm_funnel_comp_app", 
          "non_comm_funnel_accepted",
          "non_comm_funnel_deposit", 
          "non_comm_funnel_net_dep_enrolled",
          "community_funnel_inquired", 
          "community_funnel_applied",
          "community_funnel_comp_app", 
          "community_funnel_accepted",
          "community_funnel_deposit", 
          "community_funnel_net_dep_enrolled",
          "community_entered_term_pre_inquired",
          "community_entered_term_inquired", 
          "community_entered_term_applied",
          "community_entered_term_app_completed",
          "community_entered_term_accepted",
          "community_entered_term_committed",
          "community_entered_term_stage_missing",
          "stealth_appsnon_community_inquired",
          "stealth_appsnon_community_applied", 
          "zm_cv_flag_campus_visit", 
          "zm_first_gen_first_generation",
          "zm_text_opt_out_text_opt_out", 
          "zm_email_opt_out_email_opt_out",
          "zm_race_ethnicity_asian",
          "zm_race_ethnicity_american_indian_or_alaska_native",
          "zm_race_ethnicity_black_or_african_american",
          "zm_race_ethnicity_hispanic_of_any_race",
          "zm_race_ethnicity_native_hawaiian_or_other_pacific",
          "zm_race_ethnicity_white", 
          "zm_race_ethnicity_nonresident_alien",
          "zm_race_ethnicity_prefer_not_to_respond",
          "zm_race_ethnicity_race_ethnicity_unknown",
          "zm_race_ethnicity_two_or_more_races"
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
     create temp table staging_all_partner_data (
     org_id varchar(80), 
     org_name varchar(120), 
     entry_year int, 
     student_type varchar(40), 
     entry_term varchar(40),
     total_funnel_inquired int, 
     total_funnel_applied int,
     total_funnel_comp_app int, 
     total_funnel_accepted int,
     total_funnel_deposit int, 
     total_funnel_net_dep_enrolled int,
     non_comm_funnel_inquired int, 
     non_comm_funnel_applied int,
     non_comm_funnel_comp_app int, 
     non_comm_funnel_accepted int,
     non_comm_funnel_deposit int, 
     non_comm_funnel_net_dep_enrolled int,
     community_funnel_inquired int, 
     community_funnel_applied int,
     community_funnel_comp_app int, 
     community_funnel_accepted int,
     community_funnel_deposit int, 
     community_funnel_net_dep_enrolled int,
     percent_inq_in_community numeric(6, 4), 
     percent_apps_in_community numeric(6, 4),
     percent_comp_app_in_community numeric(6, 4), 
     percent_accept_in_community numeric(6, 4),
     percent_deposit_in_community numeric(6, 4), 
     percent_net_dep_enr_in_community numeric(6, 4),
     unadjusted_non_comm_app_rate numeric(6, 4), 
     unadjusted_community_app_rate numeric(6, 4),
     unadjusted_non_comm_dep_rate numeric(6, 4), 
     unadjusted_community_dep_rate numeric(6, 4),
     unadjusted_non_comm_melt_rate numeric(6, 4), 
     unadjusted_community_melt_rate numeric(6, 4),
     unadjusted_non_comm_yield_rate numeric(6, 4), 
     unadjusted_community_yield_rate numeric(6, 4),
     comm_delta_app_rate_unadjusted numeric(6, 4), 
     comm_delta_dep_rate_unadjusted numeric(6, 4),
     comm_delta_melt_rate_unadjusted numeric(6, 4),
     comm_delta_yield_rate_unadjusted numeric(6, 4),
     community_entered_term_pre_inquired int,
     community_entered_term_inquired int, 
     community_entered_term_applied int,
     community_entered_term_app_completed int,
     community_entered_term_accepted int,
     community_entered_term_committed int,
     community_entered_term_stage_missing int,
     stealth_appsnon_community_inquired int,
     stealth_appsnon_community_applied int, 
     missing_inq_date numeric(6, 4),
     missing_app_date numeric(6, 4), 
     missing_comp_app_date numeric(6, 4), 
     missing_acc_date numeric(6, 4),
     missing_commit_date numeric(6, 4), 
     app_rate_never_in_community numeric(6, 4),
     app_rate_never_in_community_sans_stealth numeric(6, 4),
     app_rate_never_in_community_with_stealth numeric(6, 4),
     app_rate_not_in_comm_in_comm_as_app_after numeric(6, 4),
     app_rate_not_in_comm_in_comm_as_app_after_sans_stealth numeric(6, 4),
     app_rate_in_comm_in_comm_prior_to_app numeric(6, 4),
     commitment_rate_never_in_community numeric(6, 4),
     commitment_rate_not_in_comm_in_comm_as_dep numeric(6, 4),
     commitment_rate_in_comm_in_comm_prior_to_dep numeric(6, 4),
     commitment_rate_in_comm_as_inquired numeric(6, 4),
     commitment_rate_in_comm_as_applied numeric(6, 4),
     commitment_rate_in_comm_as_comp_app numeric(6, 4),
     commitment_rate_in_comm_as_accept numeric(6, 4), 
     melt_rate_never_in_community numeric(6, 4),
     melt_rate_in_communtyall numeric(6, 4), 
     melt_rate_in_comm_as_inquired numeric(6, 4),
     melt_rate_in_comm_as_applied numeric(6, 4), 
     melt_rate_in_comm_as_comp_app numeric(6, 4),
     melt_rate_in_comm_as_comp_accept numeric(6, 4), 
     melt_rate_in_comm_as_commitment numeric(6, 4),
     yield_rate_never_in_community numeric(6, 4),
     yield_rate_not_in_comm_in_comm_as_deposit numeric(6, 4),
     yield_rate_in_comm_in_comm_prior_to_deposit numeric(6, 4),
     yield_rateall_regardless_of_joinstage numeric(6, 4),
     yield_rate_in_comm_as_inquired numeric(6, 4), 
     yield_rate_in_comme_as_applied numeric(6, 4),
     yield_rate_in_comm_as_comp_app numeric(6, 4), 
     yield_rate_in_comm_as_accepted numeric(6, 4),
     zm_cv_flag_campus_visit int, 
     zm_first_gen_first_generation int,
     zm_text_opt_out_text_opt_out int, 
     zm_email_opt_out_email_opt_out int,
     zm_race_ethnicity_asian int,
     zm_race_ethnicity_american_indian_or_alaska_native int,
     zm_race_ethnicity_black_or_african_american int,
     zm_race_ethnicity_hispanic_of_any_race int,
     zm_race_ethnicity_native_hawaiian_or_other_pacific int,
     zm_race_ethnicity_white int, 
     zm_race_ethnicity_nonresident_alien int,
     zm_race_ethnicity_prefer_not_to_respond int,
     zm_race_ethnicity_race_ethnicity_unknown int,
     zm_race_ethnicity_two_or_more_races int,
     csv_update_date date default NULL,
     yield_rate_in_comm_as_pre_inquired numeric(6,4),
     yield_rate_in_comm_as_deposit numeric(6,4),
     percent_community_entered_term_pre_inquired numeric(6,4),
     percent_community_entered_term_inquired numeric(6,4),
     percent_community_entered_term_applied numeric(6,4),
     percent_community_entered_term_app_completed numeric(6,4),
     percent_community_entered_term_accepted numeric(6,4),
     percent_community_entered_term_committed numeric(6,4),
     percent_community_entered_term_stage_missing numeric(6,4)
     )
     """
     cur.execute(create_staging_table)
     con.commit()
     print('staging created')
     
     #copy data from S3 to staging table
     staging_table_copy_command = """
     COPY staging_all_partner_data ({})
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
     delete from data_team.all_partner_data
     using staging_all_partner_data
     where data_team.all_partner_data.org_id = staging_all_partner_data.org_id
     and data_team.all_partner_data.entry_year = staging_all_partner_data.entry_year
     and data_team.all_partner_data.student_type = staging_all_partner_data.student_type
     and data_team.all_partner_data.entry_term = staging_all_partner_data.entry_term
     """
     cur.execute(delete_rows_to_be_updated)
     con.commit()
     print('rows to be updated deleted from main table')
     
     #insert data from staging table into actual table
     insert_into_table = """
     insert into data_team.all_partner_data
          ({})
     select {} from staging_all_partner_data;
     """.format(df_columns_str,df_columns_str)
     cur.execute(insert_into_table)
     con.commit()
     print('copied data to main script from staging')
     
     #drop staging table
     drop_staging_table = """
     drop table staging_all_partner_data
     """
     cur.execute(drop_staging_table)
     con.commit()
     con.close()
     
     print('staging table dropped')
     print('additional_fields_all_partner_data table Redshift update completed')
          
          
          
          
          
          
          
          
          
          
          
          
