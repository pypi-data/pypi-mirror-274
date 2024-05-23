
def function_create_engagement_data_df(touchpoint_df):

     engagement_data_df = touchpoint_df.copy(deep = True)
     engagement_data_df = engagement_data_df.rename(
          columns = {
               "id": "ZeeMee.ID",
               "ID.Number": "Student.ID.PartnerCSV", #from postwrangler file
               "Student.ID": "School.ID2", #from postwrangler file
               "in_csv_file": "In.CSV.File",
               "user_name": "Student.Name",
               "first_name": "First.Name",
               "last_name": "Last.Name",
               "email": "Email",
               "phone_number": "Phone.Number",
               "org_name": "Partner.Institution",
               "uos_start_term": "Entry.Term.ZM",
               "entry_term_partnercsv": "Entry.Term.PartnerCSV", 
               "uos_cohort_year": "Entry.Year.ZM",
               "entry_year_partnercsv": "Entry.Year.PartnerCSV", 
               "uos_transfer_status": "Student.Type.ZM",
               "student_type_partnercsv": "Student.Type.PartnerCSV",
               "uos_ceeb_code": "CEEB.Code.PartnerCSV",
               "user_high_school_name": "HS.on.ZM",
               "uos_high_school_name": "HS.in.PartnerCSV",
               "uos_created_at": "Community.Join.Date",
               "ZM.Joined.Stage": "Community.Join.Stage", #from postwrangler file
               "created_by_csv": "Community.Match",
               "uos_added_by": "Competitor.Match",
               "commit_button": "Commit.Button",
               "public_profile_enabled": "Public.Private.Profile",
               "interested": "Interested",
               "accepted": "Accepted.Community",
               "roommate_match_quiz": "Room.Mate.Quiz",
               "friend_finder": "Friend.Finder",
               "going": "Going",
               "total_schools_followed_by_our_user": "Schools.Followed",
               "chat_messages_sent_in_org": "Chats.Sent",
               "chat_messages_in_org_viewed": "Chats.Viewed",
               "videos_liked": "Videos.Liked",
               "videos_viewed_unique": "Videos.Viewed.Unique",
               "official_org_videos_after_1stspet": "Total.Partner.Videos",
               "last_login": "Last.Login.Date",
               "last_engaged_date": "Last.Engaged.Date",
               "engaged_any": "Engaged.Any",
               "zm_major_1": "ZM.Major.1",
               "zm_major_2": "ZM.Major.2",
               "zeemee_engagement_scores": "ZeeMee.Engagement.Score",
               "zeemee_engagement_index": "ZeeMee.Engagement.Index"
               }
               )
     
     engagement_data_df_columns = [
          "ZeeMee.ID", 
          "Student.ID.PartnerCSV", 
          "School.ID2",
          "In.CSV.File", 
          "Student.Name", 
          "First.Name", 
          "Last.Name", 
          "Email", 
          "Phone.Number", 
          "Partner.Institution", 
          "Entry.Term.ZM", 
          "Entry.Term.PartnerCSV", 
          "Entry.Year.ZM", 
          "Entry.Year.PartnerCSV",
          "Student.Type.ZM", 
          "Student.Type.PartnerCSV", 
          "CEEB.Code.PartnerCSV", 
          "HS.on.ZM", 
          "HS.in.PartnerCSV", 
          "Community.Join.Date", 
          "Community.Join.Stage", 
          "Community.Match", 
          "Competitor.Match", 
          "Commit.Button",
          "Public.Private.Profile",
          "Interested", 
          "Accepted.Community",
          "Room.Mate.Quiz",
          "Friend.Finder", 
          "Going", 
          "Schools.Followed", 
          "Chats.Sent",
          "Chats.Viewed",
          "Videos.Liked", 
          "Videos.Viewed.Unique", 
          "Total.Partner.Videos",
          "Last.Login.Date", 
          "Last.Engaged.Date",
          "Engaged.Any", 
          "ZM.Major.1", 
          "ZM.Major.2",
          "ZeeMee.Engagement.Score",
          "ZeeMee.Engagement.Index" 
          ]
          
     engagement_data_df = engagement_data_df[engagement_data_df_columns]
     
     return touchpoint_df, engagement_data_df
          
          
