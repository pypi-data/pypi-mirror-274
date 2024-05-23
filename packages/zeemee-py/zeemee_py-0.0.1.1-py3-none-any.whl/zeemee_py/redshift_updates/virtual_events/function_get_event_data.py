
def get_event_data(event_id, group_id, organization_id, event_start_time_string, event_end_time_string):
     import importlib
     import datetime
     import pandas as pd
     
     from zeemee_py.helper_functions import connect_athena
     importlib.reload(connect_athena)
     
     query_string = """
     select gpm.group_id, 
     mr.display_name, mr.network_id as org_id,
     sum(case when gpm.role = 'member' then 1 else 0 end) as "member",
     sum(case when gpm.role = 'moderator' then 1 else 0 end) as "moderator"
     
     from silver.ejabberdproduction_group_members_latest gpm ,
     silver.ejabberdproduction_muc_room_latest mr
     where mr.name = gpm.group_id
     and mr.name = '{group_id}'
     
     group by 1,2,3
     limit 2
     """.format(
          group_id = group_id
          )
     chat_room_details_df = connect_athena.run_query_in_athena(query_string)
     
     query_string= """
     select 
     p.username_from, 
     uos.user_id as zeemee_id, 
     u.name as "zeemee_name", 
     uos.crm_student_id as "student_id_partnercsv",
     u.type, 
     uos.zm_status_analysis, 
     u.official_organization_id,
     sum(case when p.content_type = 'poll' then 1 else 0 end) as poll,
     sum(case when p.content_type = 'text' then 1 else 0 end) as text,
     sum(case when p.content_type = 'video' then 1 else 0 end) as video,
     sum(case when p.content_type = 'reaction' then 1 else 0 end) as reaction,
     sum(case when p.content_type = 'image' then 1 else 0 end) as image
     
     from silver.ejabberdproduction_packets_latest p,
     silver.ejabberdproduction_muc_room_latest mr, 
     silver.prod_follower_users_latest u,
     silver.prod_follower_user_organization_statuses_latest uos
     
     where p.username_from = u.uuid 
     and mr.name = p.group_id
     and u.id = uos.user_id
     and p.packet_type = 'groupchat'
     and uos.organization_id = '{organization_id}'
     and mr.name = '{group_id}'
     and p.created_at >= parse_datetime('{event_start_time_string}','yyyy-MM-dd H:m:s')
     and p.created_at <= parse_datetime('{event_end_time_string}','yyyy-MM-dd H:m:s')
     and u.employee = 'false'
     and  u.email not like '%zeemee%'
     
     group by 1,2,3,4,5,6,7
     """.format(
          organization_id = organization_id,
          group_id = group_id,
          event_start_time_string = event_start_time_string,
          event_end_time_string = event_end_time_string
          )
     messages_df = connect_athena.run_query_in_athena(query_string)
     
     query_string = """
     with group_open_logs_cte as (
     select user_id as username,
     properties['group id'] as group_id,
     replace(replace(timestamp,'T',' '),'Z','') as created_at
     from silver.segment_android_app_latest
     where timestamp >= '{event_start_time_string}'
     and event = 'Opened Chat Channel'
     
     union all
     
     select user_id as username,
     properties['group id'] as group_id,
     replace(replace(timestamp,'T',' '),'Z','') as created_at
     from silver.segment_ios_app_latest
     where timestamp >= '{event_start_time_string}'
     and event = 'Opened Chat Channel'
     )
     
     select 
     gol.username as username_from, 
     uos.user_id as zeemee_id, 
     u.name as "zeemee_name", 
     uos.crm_student_id as "student_id_partnercsv",
     u.type, 
     uos.zm_status_analysis, 
     u.official_organization_id, 
     count(gol.group_id) as seen_target
     
     from group_open_logs_cte gol,
     silver.ejabberdproduction_muc_room_latest mr, 
     silver.prod_follower_users_latest u,
     silver.prod_follower_user_organization_statuses_latest uos
     
     where gol.username = u.uuid 
     and mr.name = gol.group_id
     and u.id = uos.user_id
     and uos.organization_id = '{organization_id}'
     and mr.name = '{group_id}'
     and gol.created_at >= '{event_start_time_string}'
     and gol.created_at <= '{event_end_time_string}'
     and u.employee = 'false'
     and  u.email not like '%zeemee%'
     
     group by 1,2,3,4,5,6,7
     order by 1
     """.format(
          organization_id = organization_id,
          group_id = group_id,
          event_start_time_string = event_start_time_string,
          event_end_time_string = event_end_time_string
          )
     channel_opens_df = connect_athena.run_query_in_athena(query_string)
     
     df = messages_df.merge(
          channel_opens_df, 
          how = "outer", 
          on= [
               "username_from", 
               "zeemee_id", 
               "zeemee_name",
               "student_id_partnercsv", 
               "type", 
               "zm_status_analysis", 
               "official_organization_id"
               ]
               )
     df[["poll", "text","video","reaction","image","seen_target"]] = df[["poll", "text","video","reaction","image","seen_target"]].fillna(0)
     
     
     #------after event data-----------
     time_6_hours_after_event_end_string = (datetime.datetime.strptime(event_end_time_string, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours = 6)).strftime("%Y-%m-%d %H:%M:%S")
     
     query_string= """
     select 
     p.username_from, 
     uos.user_id as zeemee_id, 
     u.name as "zeemee_name", 
     uos.crm_student_id as "student_id_partnercsv",
     u.type, 
     uos.zm_status_analysis, 
     u.official_organization_id,
     sum(case when p.content_type = 'poll' then 1 else 0 end) as poll,
     sum(case when p.content_type = 'text' then 1 else 0 end) as text,
     sum(case when p.content_type = 'video' then 1 else 0 end) as video,
     sum(case when p.content_type = 'reaction' then 1 else 0 end) as reaction,
     sum(case when p.content_type = 'image' then 1 else 0 end) as image
     
     from silver.ejabberdproduction_packets_latest p,
     silver.ejabberdproduction_muc_room_latest mr, 
     silver.prod_follower_users_latest u,
     silver.prod_follower_user_organization_statuses_latest uos
     
     where p.username_from = u.uuid 
     and mr.name = p.group_id
     and u.id = uos.user_id
     and p.packet_type = 'groupchat'
     and uos.organization_id = '{organization_id}'
     and mr.name = '{group_id}'
     and p.created_at >= parse_datetime('{event_end_time_string}','yyyy-MM-dd H:m:s')
     and p.created_at <= parse_datetime('{time_6_hours_after_event_end_string}','yyyy-MM-dd H:m:s')
     and u.employee = 'false'
     and  u.email not like '%zeemee%'
     
     group by 1,2,3,4,5,6,7
     """.format(
          organization_id = organization_id,
          group_id = group_id,
          event_end_time_string = event_end_time_string,
          time_6_hours_after_event_end_string = time_6_hours_after_event_end_string
          )
     messages_after_event_df = connect_athena.run_query_in_athena(query_string)
     
     query_string = """
     with group_open_logs_cte as (
     select user_id as username,
     properties['group id'] as group_id,
     replace(replace(timestamp,'T',' '),'Z','') as created_at
     from silver.segment_android_app_latest
     where timestamp >= '{event_end_time_string}'
     and event = 'Opened Chat Channel'
     
     union all
     
     select user_id as username,
     properties['group id'] as group_id,
     replace(replace(timestamp,'T',' '),'Z','') as created_at
     from silver.segment_ios_app_latest
     where timestamp >= '{event_end_time_string}'
     and event = 'Opened Chat Channel'
     )
     
     select 
     gol.username as username_from, 
     uos.user_id as zeemee_id, 
     u.name as "zeemee_name", 
     uos.crm_student_id as "student_id_partnercsv",
     u.type, 
     uos.zm_status_analysis, 
     u.official_organization_id, 
     count(gol.group_id) as seen_target
     
     from group_open_logs_cte gol,
     silver.ejabberdproduction_muc_room_latest mr, 
     silver.prod_follower_users_latest u,
     silver.prod_follower_user_organization_statuses_latest uos
     
     where gol.username = u.uuid 
     and mr.name = gol.group_id
     and u.id = uos.user_id
     and uos.organization_id = '{organization_id}'
     and mr.name = '{group_id}'
     and gol.created_at >= '{event_end_time_string}'
     and gol.created_at <= '{time_6_hours_after_event_end_string}'
     and u.employee = 'false'
     and  u.email not like '%zeemee%'
     
     group by 1,2,3,4,5,6,7
     order by 1
     """.format(
          organization_id = organization_id,
          group_id = group_id,
          event_end_time_string = event_end_time_string,
          time_6_hours_after_event_end_string = time_6_hours_after_event_end_string
          )
     channel_opens_after_event_df = connect_athena.run_query_in_athena(query_string)
    
     df_after_event = messages_after_event_df.merge(
          channel_opens_after_event_df, 
          how = "outer", 
          on= [
               "username_from", 
               "zeemee_id", 
               "zeemee_name", 
               "student_id_partnercsv", 
               "type", 
               "zm_status_analysis", 
               "official_organization_id"
               ]
               )
     
     df_after_event[["poll", "text","video","reaction","image","seen_target"]] = df_after_event[["poll", "text","video","reaction","image","seen_target"]].fillna(0)
     
     date_of_update = datetime.datetime.now().strftime("%Y-%m-%d")
     
     event_df = pd.DataFrame()
     
     event_df["event_id"] = [event_id]
     event_df["date_of_update"] = [date_of_update]
     event_df["moderators_in_channel"] = [str(chat_room_details_df.loc[0,"moderator"])]
     event_df["students_in_channel"] = [str(chat_room_details_df.loc[0,"member"])]
     event_df["total_participants_in_event"] = [str(len(df))]
     event_df["total_texts"] = [str(int(sum(df["text"])))]
     event_df["total_channel_views"] = [str(int(sum(df["seen_target"])))]
     event_df["total_reactions"] = [str(int(sum(df["reaction"])))]
     event_df["total_polls"] = [str(int(sum(df["poll"])))]
     event_df["total_images"] = [str(int(sum(df["image"])))]
     event_df["total_videos"] = [str(int(sum(df["video"])))]
     
     df_student = df[(df["type"] == "Student") & (df["official_organization_id"].isnull())].reset_index(drop = True)
     
     event_df["students_participating_in_event"] = [str(len(df_student))]
     
     event_df["unique_students_texting_or_reacting"] = [
          str(len(df_student[(df_student["text"] >0) | 
          (df_student["reaction"] >0) | 
          (df_student["video"] >0) |
          (df_student["image"] >0)]
          ))
          ]
     
     event_df["unique_students_texting_or_reacting"] = [
          str(len(df_student[
          (df_student["text"] >0) | 
          (df_student["reaction"] >0) | 
          (df_student["video"] >0) |
          (df_student["image"] >0)]
          ))]
          
     event_df["texts_by_students"] = [str(int(sum(df_student["text"])))]
     event_df["chat_channel_views_by_students"] = [str(int(sum(df_student["seen_target"])))]
     event_df["reactions_by_students"] = [str(int(sum(df_student["reaction"])))]
     event_df["polls_by_students"] = [str(int(sum(df_student["poll"])))]
     event_df["images_by_students"] = [str(int(sum(df_student["image"])))]
     event_df["videos_by_students"] = [str(int(sum(df_student["video"])))]
     
     committed_and_after = ["Enrolled", "Committed", "Commitment Withdrawn"]
     accepted_and_after = ["Acceptance Declined", "Accepted"]
     accepted_and_after.extend(committed_and_after)
     applied_and_after = [
          "Deferred Withdrawn", 
          "Deferred", 
          "Waitlisted Withdrawn", 
          "Waitlisted", 
          "Denied", 
          "Application Complete Withdrawn", 
          "Application Complete",
          "Application Canceled", 
          "Applied"
          ]
     applied_and_after.extend(accepted_and_after)
     
     event_df["applied_and_after_students"] = [str(  len(df_student[df_student["zm_status_analysis"].isin(applied_and_after)]) )]
     event_df["accepted_and_after_students"] = [str(  len(df_student[df_student["zm_status_analysis"].isin(applied_and_after)]) )]
     event_df["committed_and_after_students"] = [str(  len(df_student[df_student["zm_status_analysis"].isin(committed_and_after)]) )]
     
     #finding users who didnt attend the event but checked it after the event
     df_after_event_student = df_after_event[(df_after_event["type"] == "Student") & (df_after_event["official_organization_id"].isnull())].reset_index(drop = True)
     
     event_df["users_after_event_who_didnt_participate"] = [str(  len(list(set(df_after_event_student["username_from"]).difference(set(df["username_from"])))) )]
     event_df["texts_after_event"] = [str(int(sum(df_after_event_student["text"])))]
     event_df["chat_channel_views_after_event"] = [str(int(sum(df_after_event_student["seen_target"])))]
     event_df["reactions_after_event"] = [str(int(sum(df_after_event_student["reaction"])))]

     
     participants_df= df_student[["zeemee_id", "zm_status_analysis"]]
     participants_df["event_id"] = [event_id] * len(participants_df)
     participants_df["date_of_update"] = [date_of_update] * len(participants_df)
          
     return event_df, participants_df














