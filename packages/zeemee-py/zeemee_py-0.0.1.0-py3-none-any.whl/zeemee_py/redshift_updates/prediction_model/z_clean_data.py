def clean_data(touchpoint_df):

     touchpoint_df["messages_in_other_orgs"] = touchpoint_df[
          "total_chat_messages_sent_all_orgs"] - touchpoint_df["chat_messages_sent_in_org"]
     touchpoint_df["users_following_other_orgs_followed_by_user"] = touchpoint_df[
          "total_users_followed_by_our_user"] - touchpoint_df["users_following_organization_followed_by_our_user"]
     touchpoint_df["chats_in_org_sent_viewed"] = touchpoint_df["chat_messages_sent_in_org"] + touchpoint_df["chat_messages_in_org_viewed"]
     
     touchpoint_df["public_profile_enabled"] = touchpoint_df["public_profile_enabled"].replace(
          {
               "Public Profile": "t",
               "Private Profile": "f",
               "": "f"})
     
     touchpoint_df["interested"] = touchpoint_df["interested"].replace(
          {"In Community - Following" :"t",
          "No Longer in Community - Unfollowed": "f",
          "": "f"})
     
     touchpoint_df["uos_transfer_status"] = touchpoint_df["uos_transfer_status"].fillna("f")
     touchpoint_df["uos_transfer_status"] = touchpoint_df["uos_transfer_status"].replace(
          {"Transfer": "t",
          "First Time": "f",
          "": "f"})
     
     touchpoint_df["going"] = touchpoint_df["going"].fillna("Undecided")
     touchpoint_df["going"] = touchpoint_df["going"].replace(
          {"Going": "going",
          "Not Going": "notgoing",
          "Undecided": "undecided",
          "": "undecided"})
     
     touchpoint_df["created_by_csv"] = touchpoint_df["created_by_csv"].fillna("f")
     touchpoint_df["created_by_csv"] = touchpoint_df["created_by_csv"].replace(
          {"Community Match": "t",
          "": "f"})
     
     touchpoint_df["roommate_match_quiz"] = touchpoint_df["roommate_match_quiz"].fillna("f")
     touchpoint_df["roommate_match_quiz"] = touchpoint_df["roommate_match_quiz"].replace(
          { "Roommate Quiz Completed": "t",
          "": "f"})

     return touchpoint_df


