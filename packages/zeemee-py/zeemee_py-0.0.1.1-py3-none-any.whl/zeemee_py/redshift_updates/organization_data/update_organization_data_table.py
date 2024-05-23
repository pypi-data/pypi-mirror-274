
def update_organization_data_table():
     import importlib
     import os
     
     from zeemee_py.helper_functions import get_config
     importlib.reload(get_config)
     cohort_year, accesskeyid, accesskey = get_config.get_creds("current_cohort_year_for_database_tables", "accesskeyid", "accesskey")
     
     organization_data_file_in_s3 = "s3://zeemee-data-team-files/zeemee_py/operations/org_additional_table_data_current.csv"
     s3_filename_for_update = os.path.join("s3://zeemee-data-team-files/zeemee_py/redshift_tables/", "organization_data.csv")
     
     from zeemee_py.helper_functions import connect_duckdb
     importlib.reload(connect_duckdb)
     organization_data_df = connect_duckdb.get_file_df(organization_data_file_in_s3)
     
     organization_data_df = organization_data_df[organization_data_df['zm_cohort_year'] >= cohort_year].reset_index(drop = True)
     
     column_list = [
          'org_name', 
          'top_of_funnel', 
          'org_id', 
          'ipeds_id', 
          'zm_cohort_year',
          'ipeds_enrollment_aid_term', 
          'ipeds_ntr_per_student',
          'ipeds_carnegie_description', 
          'ipeds_instituion_size_description',
          'ipeds_control_description', 
          'ipeds_locale_description',
          'ipeds_obereg_region_description', 
          'ipeds_sector_description',
          'zm_type',
          'zm_region',
          'us_news_category', 
          'us_news_type', 
          'us_news_denomination',
          'zm_church_related', 
          'us_news_setting', 
          'zm_launch_date',
          'zm_launch_season', 
          'zm_funnel_states', 
          'zm_stealth_check',
          'zm_race_check', 
          'zm_firstgen_check', 
          'zm_campus_visit_check',
          'zm_join_stage_check', 
          'zm_inq_date_check', 
          'zm_app_date_check',
          'zm_acc_date_check', 
          'zm_comm_date_check',
          'slug',
          'zm_termination_date', 
          'partner_crm', 
          'partner_data_download_location',
          'partner_data_files_num', 
          'partner_file_type', 
          'slate_id_number',
          'deliverable', 
          'tp_status', 
          'ready_for_touchpoint_monday',
          'deliverable_admin', 
          'deliverable_exavault', 
          'deliverable_api',
          'tp_notes', 
          'ipeds_org_name', 
          'ipeds_state_abbr', 
          'ipeds_state_nm',
          'ipeds_inst_category_description',
          'ipeds_discount_rate_per_student',
          'ipeds_percent_freshman_w_grant',
          'ipeds_total_firsttime_enrolled',
          'ipeds_total_firsttime_enrolled_grouping',
          'ipeds_total_undergrad_count', 
          'ipeds_percent_in_state',
          'ipeds_tuition_differential', 
          'zm_date_processed',
          'zm_freshman_class_goal', 
          'zm_transfers_class_goal', 
          'Contact1',
          'Contact2', 
          'Contact3', 
          'Contact4', 
          'Contact5', 
          'AnalysisOverallDistro',
          'AnalysisJoinStage', 
          'AnalysisAppRate', 
          'AnalysisCommitRate',
          'AnalysisYield', 
          'AnalysisMelt',
          'exclude_from_engage_consolidated',
          'two_tp_ids', 
          'zm_melt_data_check',  
          'zm_type_2',
          'zm_type_3', 
          'zm_type_4', 
          'ipeds_partner_zip'
          ]
     
     #data clean-up to load into Redshift
     int_columns = [
          "ipeds_id", 
          "zm_cohort_year", 
          "ipeds_enrollment_aid_term", 
          "ipeds_total_firsttime_enrolled", 
          "ipeds_total_undergrad_count", 
          "zm_freshman_class_goal", 
          "zm_transfers_class_goal", 
          "ipeds_partner_zip"
          ]
     
     organization_data_df["zm_launch_date"] =  organization_data_df["zm_launch_date"].replace("tba", "")
          
     for col in int_columns:
         for i in range(len(organization_data_df)):
             organization_data_df.loc[i, col] = str(organization_data_df.loc[i, col]).split(".")[0]
     
     organization_data_df =  organization_data_df.replace("nan", "") 
     organization_data_df =  organization_data_df.fillna("") 
     organization_data_df = organization_data_df[column_list]
     column_list_str = ",".join(column_list)
     
     print("organization data columns needed:", len(column_list))
     print("columns in dataframe after subsetting-", len(organization_data_df.columns))
     
     from zeemee_py.helper_functions import send_dataframe_to_s3
     importlib.reload(send_dataframe_to_s3)
     send_dataframe_to_s3.send_dataframe_to_s3(s3_filename_for_update, organization_data_df)
     
     from zeemee_py.helper_functions import connect_redshift
     importlib.reload(connect_redshift)
     con = connect_redshift.establish_redshift_connection()
     cur = con.cursor()
     
     create_staging_table = """
     create temp table staging_organization_data (
          org_name varchar(80),
          org_id varchar(45),
          ipeds_id int,
          zm_cohort_year int,
          ipeds_enrollment_aid_term int,
          ipeds_ntr_per_student DECIMAL,
          ipeds_freshman_class_size int,
          ipeds_carnegie_description varchar(200),
          ipeds_instituion_size_description varchar(80),
          ipeds_control_description varchar(80),
          ipeds_locale_description varchar(80),
          ipeds_obereg_region_description varchar(80),
          ipeds_sector_description varchar(80),
          zm_outreach_partner varchar(45),
          zm_type varchar(40),
          zm_region varchar(40),
          us_news_Category varchar(80),
          us_news_type varchar(80),
          us_news_denomination varchar(80),
          zm_church_related varchar(40),
          us_news_setting varchar(40),
          zm_launch_date DATE,
          zm_launch_season varchar(40),
          zm_fall_enrollment_goal decimal,
          zm_funnel_states varchar(80),
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
          slug varchar(200),
          zm_termination_date DATE,
          partner_crm varchar(200),
          partner_data_download_location varchar(200),
          partner_data_files_num varchar(200),
          partner_file_type varchar(200),
          slate_id_number varchar(200),
          deliverable varchar(200),
          tp_status varchar(200),
          ready_for_touchpoint_monday varchar(200),
          deliverable_admin varchar(200),
          deliverable_exavault varchar(200),
          deliverable_api varchar(200),
          tp_notes varchar(200),
          ipeds_org_name varchar(200),
          ipeds_state_abbr varchar(200),
          ipeds_state_nm varchar(200),
          ipeds_inst_category_description varchar(200),
          ipeds_discount_rate_per_student numeric(10,8),
          ipeds_percent_freshman_w_grant numeric(5,2),
          ipeds_total_firsttime_enrolled int,
          ipeds_total_undergrad_count int,
          ipeds_percent_in_state numeric(5,2),
          ipeds_tuition_differential numeric(8,2),
          zm_date_processed DATE,
          zm_freshman_class_goal int,
          zm_transfers_class_goal int,
          Contact1 varchar(200),
          Contact2 varchar(200),
          Contact3 varchar(200),
          Contact4 varchar(200),
          top_of_funnel varchar (80),
          Contact5 varchar(200),
          AnalysisOverallDistro varchar(80),
          AnalysisJoinStage varchar(80),
          AnalysisAppRate varchar(80),
          AnalysisCommitRate varchar(80),
          AnalysisYield varchar(80),
          AnalysisMelt varchar(80),
          exclude_from_engage_consolidated varchar(80),
          two_tp_ids varchar(80),
          ipeds_total_firsttime_enrolled_grouping varchar(80),
          zm_melt_data_check varchar(80),  
          zm_type_2 varchar(80),
          zm_type_3 varchar(80), 
          zm_type_4 varchar(80), 
          ipeds_partner_zip int
          )
     """
     cur.execute(create_staging_table)
     con.commit()
     print('staging created')
          
     
     staging_table_copy_command = """COPY staging_organization_data ({})
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
     print('data copied to staging')
     
     
     delete_rows_to_be_updated = """
     delete from data_team.organization_data
     using staging_organization_data
     where 
     data_team.organization_data.org_id = staging_organization_data.org_id and 
     data_team.organization_data.zm_cohort_year = staging_organization_data.zm_cohort_year
     """
     cur.execute(delete_rows_to_be_updated)
     con.commit()
     print('duplicate data deleted from main table')
     
     
     insert_into_table = """
     insert into data_team.organization_data
           ({})
     select {} 
     from staging_organization_data;
     """.format(
          column_list_str,
          column_list_str
          )
     cur.execute(insert_into_table)
     con.commit()
     print('data inserted into main table')
     
     
     drop_staging_table = """
     drop table staging_organization_data
     """
     cur.execute(drop_staging_table)
     con.commit()
     print("organization data table update complete")
     
     con.close()
















