
def main_function(event_info_df, skip_filters):
     import datetime
     import importlib
     import warnings
     from pandas.errors import SettingWithCopyWarning
     warnings.simplefilter(action='ignore', category=FutureWarning) 
     warnings.simplefilter(action='ignore', category=SettingWithCopyWarning)
     
     event_id = event_info_df.loc[0,"id"]
     date_of_event = datetime.datetime.strftime(event_info_df.loc[0,"date"], "%Y-%m-%d")
     group_id = event_info_df.loc[0,"muc_room_name"]
     event_start_time_string = datetime.datetime.strftime(event_info_df.loc[0,"start_time"], "%Y-%m-%d %H:%M:%S")
     event_end_time_string = datetime.datetime.strftime(event_info_df.loc[0,"end_time"], "%Y-%m-%d %H:%M:%S")
     organization_id = event_info_df.loc[0,'organization_id']
     
     from zeemee_py.helper_functions import connect_athena
     importlib.reload(connect_athena)
     
     query_string = """
     select 
     o.name as organization_name, 
     cs.email as ps_email
     from silver.prod_follower_organizations_latest o
     left join silver.prod_follower_cs_reps_latest cs on cs.id = o.cs_rep_id
     where o.id = '{organization_id}'
     """.format(organization_id = organization_id)
     
     organization_info_df = connect_athena.run_query_in_athena(query_string)
     organization_name = organization_info_df.loc[0,'organization_name']
     ps_email = organization_info_df.loc[0,'ps_email']
     print(ps_email)
     ps_email = "mayur@zeemee.com"
     
     print(event_id, organization_name, group_id, event_start_time_string, event_end_time_string)
          
     from zeemee_py.redshift_updates.virtual_events import function_get_event_data
     importlib.reload(function_get_event_data)
     event_df, participants_df = function_get_event_data.get_event_data(
          event_id,
          group_id, 
          organization_id, 
          event_start_time_string, 
          event_end_time_string)
     
     students_participating_in_event = event_df["students_participating_in_event"][0]
     texts_by_students = event_df["texts_by_students"][0]
     users_after_event_who_didnt_participate = event_df["users_after_event_who_didnt_participate"][0]
     texts_after_event = event_df["texts_after_event"][0]
     
     """
      In case of following scenarios, we won't add the data to reshift and will get a message to review the info
      if number of participating students is < 4
      if students after events are more than during event
      if texts during events is < 5
      if texts after events are more than texts during event
      if users_after_event_who_didnt_participate/students_participating_in_event +1 > 0.5
      if users_after_event_who_didnt_participate/students_participating_in_event +1 > 0.2 and users_after_event_who_didnt_participate >10
     """
     from zeemee_py.helper_functions import send_email
     importlib.reload(send_email)
     common_email_message = """Hello!\n\nThis is an automated email to inform you that the following event data update has failed. 
     This might be because:\n  
     1. We don't have the correct event date, time or channel in admin. You can get the correct info
        by checking the actual event messages on the app. Please update the event info in admin
        and then ask a data-team member to update the event data.\n
     2. The event didn't happen/ was canceled - please delete the event from admin to keep
        our data clean
     
     Event update failure details:\n
     """
     
     if skip_filters == "no": 
          if (int(students_participating_in_event) < 4):
               slack_message = "students_participating_in_event < 4 for event_id = {event_id} on {date_of_event} for {organization_name}, not added to redshift".format(
                    event_id = event_id, 
                    date_of_event = date_of_event, 
                    organization_name = organization_name
                    )
               
               send_email.send_email(
                    [ps_email], 
                    "Alert: Virtual Event Update failed for {organization_name}".format(
                         organization_name = organization_name), 
                    common_email_message + slack_message
                    )
          elif (int(students_participating_in_event) < int(users_after_event_who_didnt_participate)):
               slack_message = "students_participating_in_event < users_after_event_who_didnt_participate for event_id = {event_id} on {date_of_event} for {organization_name}, not added to redshift".format(
                    event_id = event_id, 
                    date_of_event = date_of_event, 
                    organization_name = organization_name
                    )
               send_email.send_email(
                    [ps_email], 
                    "Alert: Virtual Event Update failed for {organization_name}".format(
                         organization_name = organization_name), 
                    common_email_message + slack_message
                    )
          elif (int(texts_by_students) < 5):
               slack_message = "texts_by_students < 5 for event_id = {event_id} on {date_of_event} for {organization_name}, not added to redshift".format(
                    event_id = event_id, 
                    date_of_event = date_of_event, 
                    organization_name = organization_name
                    )
               send_email.send_email(
                    [ps_email], 
                    "Alert: Virtual Event Update failed for {organization_name}".format(
                         organization_name = organization_name), 
                    common_email_message + slack_message
                    )
          elif (int(texts_by_students) < int(texts_after_event)):
               slack_message = "texts_by_students < texts_after_event for event_id = {event_id} on {date_of_event} for {organization_name}, not added to redshift".format(
                    event_id = event_id, 
                    date_of_event = date_of_event, 
                    organization_name = organization_name
                    )
               send_email.send_email(
                    [ps_email], 
                    "Alert: Virtual Event Update failed for {organization_name}".format(
                         organization_name = organization_name), 
                    common_email_message + slack_message
                    )
          elif (int(users_after_event_who_didnt_participate)/(int(students_participating_in_event) + 1) > 0.5):
               slack_message = "users_after_event/ during event > 0.5 for event_id = {event_id} on {date_of_event} for {organization_name}, not added to redshift".format(
                    event_id = event_id, 
                    date_of_event = date_of_event, 
                    organization_name = organization_name
                    )
               send_email.send_email(
                    [ps_email], 
                    "Alert: Virtual Event Update failed for {organization_name}".format(
                         organization_name = organization_name), 
                    common_email_message + slack_message
                    )
          elif ((int(users_after_event_who_didnt_participate)/(int(students_participating_in_event) + 1) > 0.2 ) & int(users_after_event_who_didnt_participate) > 10):
               slack_message = "users_after_event_/ during event > 0.2 and >5 for event_id = {event_id} on {date_of_event} for {organization_name}, not added to redshift".format(
                    event_id = event_id, 
                    date_of_event = date_of_event, 
                    organization_name = organization_name
                    )
               send_email.send_email(
                    [ps_email], 
                    "Alert: Virtual Event Update failed for {organization_name}".format(
                         organization_name = organization_name), 
                    common_email_message + slack_message
                    )
          else:
               from zeemee_py.redshift_updates.virtual_events import function_redshift_update_virtual_events_data_table
               importlib.reload(function_redshift_update_virtual_events_data_table)
               function_redshift_update_virtual_events_data_table.update_redshift_table(event_df)
               
               from zeemee_py.redshift_updates.virtual_events import function_redshift_update_participants_table
               importlib.reload(function_redshift_update_participants_table)
               function_redshift_update_participants_table.update_redshift_table(participants_df)
               
               slack_message = "virtual_event table updated for event_id = {event_id} on {date_of_event} for {organization_name}, added to redshift".format(
                    event_id = event_id, 
                    date_of_event = date_of_event, 
                    organization_name = organization_name
                    )
     else:
          #add to redshift
          slack_message = "filters skipped for event_id = {event_id} on {date_of_event} for {organization_name}, added to redshift".format(
                    event_id = event_id, 
                    date_of_event = date_of_event, 
                    organization_name = organization_name
                    )
                    
          from zeemee_py.redshift_updates.virtual_events import function_redshift_update_virtual_events_data_table
          importlib.reload(function_redshift_update_virtual_events_data_table)
          function_redshift_update_virtual_events_data_table.update_redshift_table(event_df)
          
          from zeemee_py.redshift_updates.virtual_events import function_redshift_update_participants_table
          importlib.reload(function_redshift_update_participants_table)
          function_redshift_update_participants_table.update_redshift_table(participants_df)
                    
     from zeemee_py.helper_functions import send_to_slack
     send_to_slack.send_message_to_slack("comms", slack_message )
          
          
          
          
          
          
          
          
          
