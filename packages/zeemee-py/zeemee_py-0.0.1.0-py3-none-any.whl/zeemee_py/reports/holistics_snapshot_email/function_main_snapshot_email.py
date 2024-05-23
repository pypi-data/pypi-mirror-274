
def main_function():
     import datetime
     import importlib
     
     print(datetime.datetime.now())
     
     from zeemee_py.report.holistics_snapshot_email import function_get_email_list
     importlib.reload(function_get_email_list)
     email_df = function_get_email_list.get_email_list()
     
     """
     from zeemee_py.helper_functions import get_config
     importlib.reload(get_config)
     cohort_year = get_config.get_creds("current_cohort_year_for_reports") 
     
     from zeemee_py.helper_function import get_org_additional_data_file
     importlib.reload(get_org_additional_data_file)
     org_additional_df = get_org_additional_data_file.get_file()
     org_additional_df = org_additional_df[org_additional_df['zm_cohort_year'] == cohort_year].reset_index(drop = True)
     org_additional_df = org_additional_df[org_additional_df['zm_launch_date'].notnull()].reset_index(drop = True)
     org_additional_df = org_additional_df[org_additional_df['zm_launch_date'] < datetime.datetime.now().strftime("%Y-%m-%d")].reset_index(drop = True)
     org_additional_orgs = list(org_additional_data['org_id'])
     #email_df = email_df[email_df['organization_id'].isin(org_additional_data_orgs)].reset_index(drop = True)
     """
     
     print("No. of schools:", len(email_df))

     from zeemee_py.report.holistics_snapshot_email import function_get_schedule_ids
     importlib.reload(function_get_schedule_ids)
     all_schedule_ids = function_get_schedule_ids.get_all_schedule_ids()
     
     non_email_dash_ids = list()
     email_dash_ids = list()
     for dashboard_ids in all_schedule_ids:
          if dashboard_ids != 56648:
               non_email_dash_ids.extend(all_schedule_ids[dashboard_ids])
          if dashboard_ids == 56648:
               email_dash_ids.extend(all_schedule_ids[dashboard_ids])
               
     from zeemee_py.helper_functions import connect_athena
     importlib.reload(connect_athena)

     for i in range(len(emails)):
          try:
               current_organization_id = emails.loc[i,'organization_id']
               quer_string = """
                    select cs.email from 
                    prod_follower.cs_reps cs inner join prod_follower.organizations o on o.cs_rep_id = cs.id
                    and o.id = '{}'
                    """.format(current_organization_id)
               cs_rep_email = connect_athena.run_query_in_athena(query_string)
               if len(cs_rep_email) != 1:
                    cs_rep_email = pd.DataFrame({'email': ['will@zeemee.com,courtney@zeemee.com,devon@zeemee.com,kellys@zeemee.com, mayur@zeemee.com']})
               current_email_string = emails.loc[i,'email_list'] + "," + cs_rep_email.loc[0,'email']
               current_email_list = current_email_string.split(',')
               current_email_list = [j.strip() for j in current_email_list]
               current_org_name = emails.loc[i,'org_name']
     
               new_schedule_id = i
               while new_schedule_id in email_dash_ids or new_schedule_id in non_email_dash_ids:
                    new_schedule_id = new_schedule_id + 1
               email_dash_ids.append(new_schedule_id)
          
               
               ##### schedule a cron job 2 mins after current time UTC
               time_now = datetime.datetime.now()
               cron_hour = int(time_now.hour)%24
               cron_minute = time_now.minute + 3
          
               if cron_minute > 60:
                    cron_hour = int(cron_hour + 1)%24
                    cron_minute = cron_minute%60
               schedule_time = str(cron_minute) + ' ' + str(cron_hour) + " * * *"
               schedule_time
          
               print("{} {} {} {} {}".format(new_schedule_id, current_org_name, current_organization_id, current_email_list, schedule_time))
               
               
               from zeemee_py.report.holistics_snapshot_email import function_create_schedule
               importlib.reload(holistics_create_schedule_function)
               print(new_schedule_id, current_organization_id, cohort_year, schedule_time, current_email_list, current_org_name)
               holistics_create_schedule_function.create_schedule(new_schedule_id, current_organization_id, cohort_year, schedule_time, current_email_list, current_org_name)
               
               if response_status_code not in (200, 201):
                    print("_____________________________ email schedule creation failed for", current_organization_id)
                    
               if i%50 == 0 and i !=0: 
                    print(datetime.datetime.now())
                    print(i, "sleeping for 7200 seconds")
                    time.sleep(7200)
                    
                    print("getting exisitng schedules")
                    
                    from zeemee_py.report.holistics_snapshot_email import function_get_schedule_ids
                    importlib.reload(function_get_schedule_ids)
                    exisiting_schedule_ids = exisiting_all_schedule_ids.get_schedule_ids()
                    
                    schdule_ids_to_be_deleted = exisiting_schedule_ids[56648]
                    
                    from zeemee_py.report.holistics_snapshot_email import function_delete_schedule
                    importlib.reload(function_delete_schedule)
                    
                    for ids in schdule_ids_to_be_deleted:
                         delete_response_code = function_delete_schedule.delete_schedule(ids)
                         if delete_response_code not in (200, 201):
                              print("_____________________________ email schedule deletion failed for",ids )
                         else:
                              print("email schedule deleted", ids)
          
          except Exception as e:
               print("error for {} {} {}".format(current_org_name, current_organization_id, current_email_list))
     
     print(datetime.datetime.now())
     print("sleeping for 7200 seconds before final deletion")
     
     time.sleep(7200)
     from zeemee_py.report.holistics_snapshot_email import function_get_schedule_ids
     importlib.reload(function_get_schedule_ids)
     exisiting_schedule_ids = exisiting_all_schedule_ids.get_schedule_ids()
     
     schdule_ids_to_be_deleted = exisiting_schedule_ids[56648]
     
     from zeemee_py.report.holistics_snapshot_email import function_delete_schedule
     importlib.reload(function_delete_schedule)
     
     for ids in schdule_ids_to_be_deleted:
          delete_response_code = function_delete_schedule.delete_schedule(ids)
          if delete_response_code not in (200, 201):
               print("_____________________________email schedule deletion failed for",ids )
          else:
               print("email schedule deleted", ids)
     
     print(datetime.datetime.now())
     print("email snapshot script complete")











