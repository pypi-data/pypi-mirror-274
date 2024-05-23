
def create_last_engaged_date_column(touchpoint_df):
    
    """check if there is a last engaged date for following candidate dates
    1. videos last engaged
    2. room mate last engaged
    3. messages last engaged
    4. if created_by_csv if false, then consider uos_created_at date for the list
    
    ##update 2022-04-26
    5. dms_within_org_last_engaged
    6. post_views_ios_last_engaged
    7. profile_views_in_org_ios_last_engaged
    8. profile_views_in_org_android_last_engaged
    9. ff_searched_with_college_filter_ios_last_engaged
    10. ff_searched_with_college_filter_android_last_engaged
    """ 
    
    import datetime
    
    engagement_columns_for_last_engaged = [
         'videos_last_engaged',
         'room_mate_match_last_engaged',
         'messages_last_engaged',
         'created_by_csv',
         'uos_created_at',
         'dms_within_org_last_engaged',
         'post_views_ios_last_engaged',
         'post_views_android_last_engaged',
         'profile_views_in_org_ios_last_engaged',
         'profile_views_in_org_android_last_engaged',
         'chat_channel_opens_in_org_last_engaged'
         ]
          
    touchpoint_df[engagement_columns_for_last_engaged] = touchpoint_df[engagement_columns_for_last_engaged].fillna('no value')
    
    last_engaged = list()

    for i in range(len(touchpoint_df)):
        last_engaged_dates_string = list()

        if touchpoint_df.videos_last_engaged[i] != 'no value':
            last_engaged_dates_string.append(touchpoint_df.videos_last_engaged[i])

        if touchpoint_df.room_mate_match_last_engaged[i] != 'no value':
            last_engaged_dates_string.append(touchpoint_df.room_mate_match_last_engaged[i])

        if touchpoint_df.messages_last_engaged[i] != 'no value':
            last_engaged_dates_string.append(touchpoint_df.messages_last_engaged[i])

        if (touchpoint_df.created_by_csv[i] == 'f')  &  (touchpoint_df.uos_created_at[i] != 'no value'):
            last_engaged_dates_string.append(touchpoint_df.uos_created_at[i])
            
        if touchpoint_df.dms_within_org_last_engaged[i] != 'no value':
            last_engaged_dates_string.append(touchpoint_df.dms_within_org_last_engaged[i])
            
        if touchpoint_df.post_views_ios_last_engaged[i] != 'no value':
            last_engaged_dates_string.append(touchpoint_df.post_views_ios_last_engaged[i])
            
        if touchpoint_df.profile_views_in_org_ios_last_engaged[i] != 'no value':
            last_engaged_dates_string.append(touchpoint_df.profile_views_in_org_ios_last_engaged[i])
            
        if touchpoint_df.profile_views_in_org_android_last_engaged[i] != 'no value':
            last_engaged_dates_string.append(touchpoint_df.profile_views_in_org_android_last_engaged[i])
            
        if touchpoint_df.chat_channel_opens_in_org_last_engaged[i] != 'no value':
            last_engaged_dates_string.append(touchpoint_df.chat_channel_opens_in_org_last_engaged[i])
        
        last_engaged_dates = list()
        for i in last_engaged_dates_string:
            if type(i) == str:
                last_engaged_dates.append(datetime.datetime.strptime(i, '%Y-%m-%d').date())
            else:
                if i!= None:
                    last_engaged_dates.append(i)

        if len(last_engaged_dates) >0:
                last_engaged.append(max(last_engaged_dates))
        else: 
            last_engaged.append("")
    
    touchpoint_df['last_engaged_date'] = last_engaged

    return touchpoint_df
    
