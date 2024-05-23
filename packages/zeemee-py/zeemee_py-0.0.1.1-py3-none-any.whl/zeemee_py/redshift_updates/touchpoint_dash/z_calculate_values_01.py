     
def calculate_values(touchpoint_df, current_cohort_year, organization_id, entry_term, student_type): 
     import pandas as pd
     from warnings import simplefilter
     simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
     
     touchpoint_df = touchpoint_df[touchpoint_df["uos_start_term"] == entry_term].reset_index(drop = True)
     touchpoint_df = touchpoint_df[touchpoint_df["uos_transfer_status"] == student_type].reset_index(drop = True)
     touchpoint_df = touchpoint_df[touchpoint_df["uos_cohort_year"] == current_cohort_year].reset_index(drop = True)
     touchpoint_df["ZM.Joined.Stage"] = touchpoint_df["ZM.Joined.Stage"].fillna("07 DATE OF INITIAL CONTACT MISSING")
     touchpoint_df["ZM.Joined.Stage"] = touchpoint_df["ZM.Joined.Stage"].replace("","07 DATE OF INITIAL CONTACT MISSING")
     
     function_dataframe = pd.DataFrame()
     
     function_dataframe["org_id"] = [organization_id]
     function_dataframe["student_type"] = [student_type]
     function_dataframe["entry_term"] = [entry_term]
     function_dataframe["cohort_year"] = [current_cohort_year]
     
     total_students_all = len(touchpoint_df)
     function_dataframe["total_students_all"] = [total_students_all]
     
     community_matched_all = len(touchpoint_df[touchpoint_df["created_by_csv"] == "Community Match"])
     function_dataframe["community_matched_all"] = [community_matched_all]
     
     count_current_cohort_year_all = len(touchpoint_df[touchpoint_df["uos_cohort_year"] == current_cohort_year])
     function_dataframe["count_current_cohort_year_all"] = [count_current_cohort_year_all]
     
     engaged_any_all = len(touchpoint_df[touchpoint_df["engaged_any"] == 1])
     function_dataframe["engaged_any_all"] = [engaged_any_all]
     
     engaged_any_null_all = len(touchpoint_df) - len(touchpoint_df[touchpoint_df["engaged_any"] == 1])
     function_dataframe["engaged_any_null_all"] = [engaged_any_null_all]
     
     engaged_1_week_all = len(touchpoint_df[touchpoint_df["engaged_week"] == "1 week"])
     function_dataframe["engaged_1_week_all"] = [engaged_1_week_all]
     
     engaged_2_week_all = len(touchpoint_df[touchpoint_df["engaged_week"] == "2 weeks"])
     function_dataframe["engaged_2_week_all"] = [engaged_2_week_all]
     
     engaged_3_week_all = len(touchpoint_df[touchpoint_df["engaged_week"] == "3 weeks"])
     function_dataframe["engaged_3_week_all"] = [engaged_3_week_all]
     
     engaged_4_week_all = len(touchpoint_df[touchpoint_df["engaged_week"] == "4 weeks"])
     function_dataframe["engaged_4_week_all"] = [engaged_4_week_all]
     
     engaged_5_60_days_or_less_all = len(touchpoint_df[touchpoint_df["engaged_week"] == "5 - 60 days or less"])
     function_dataframe["engaged_5_60_days_or_less_all"] = [engaged_5_60_days_or_less_all]
     
     engaged_6_90_days_or_less_all = len(touchpoint_df[touchpoint_df["engaged_week"] == "6 - 90 days or less"])
     function_dataframe["engaged_6_90_days_or_less_all"] = [engaged_6_90_days_or_less_all]
     
     engaged_7_more_than_90_days_all = len(touchpoint_df[touchpoint_df["engaged_week"] == "7 - more than 90 days"])
     function_dataframe["engaged_7_more_than_90_days_all"] = [engaged_7_more_than_90_days_all]
     
     #---------------------------------------------
     
     login_1_week_all = len(touchpoint_df[touchpoint_df["login_week"] == "1 week"])
     function_dataframe["login_1_week_all"] = [login_1_week_all]
     
     login_2_week_all = len(touchpoint_df[touchpoint_df["login_week"] == "2 weeks"])
     function_dataframe["login_2_week_all"] = [login_2_week_all]
     
     login_3_week_all = len(touchpoint_df[touchpoint_df["login_week"] == "3 weeks"])
     function_dataframe["login_3_week_all"] = [login_3_week_all]
     
     login_4_week_all = len(touchpoint_df[touchpoint_df["login_week"] == "4 weeks"])
     function_dataframe["login_4_week_all"] = [login_4_week_all]
     
     login_5_60_days_or_less_all = len(touchpoint_df[touchpoint_df["login_week"] == "5 - 60 days or less"])
     function_dataframe["login_5_60_days_or_less_all"] = [login_5_60_days_or_less_all]
     
     login_6_90_days_or_less_all = len(touchpoint_df[touchpoint_df["login_week"] == "6 - 90 days or less"])
     function_dataframe["login_6_90_days_or_less_all"] = [login_6_90_days_or_less_all]
     
     login_7_more_than_90_days_all = len(touchpoint_df[touchpoint_df["login_week"] == "7 - more than 90 days"])
     function_dataframe["login_7_more_than_90_days_all"] = [login_7_more_than_90_days_all]
     
     #---------------------------------------------
     
     going_going_all = len(touchpoint_df[touchpoint_df["going"] == "Going"])
     function_dataframe["going_going_all"] = [going_going_all]
     
     going_not_all = len(touchpoint_df[touchpoint_df["going"] == "Not Going"])
     function_dataframe["going_not_all"] = [going_not_all]
     
     going_undecided_all = len(touchpoint_df[touchpoint_df["going"] == "Undecided"])
     function_dataframe["going_undecided_all"] = [going_undecided_all]
     
     #-----------------------------------------------------
     community_joined_stage_pre_inquired_all = len(touchpoint_df[touchpoint_df["ZM.Joined.Stage"] == "01 PRE-INQUIRED"])
     function_dataframe["community_joined_stage_pre_inquired_all"] = [community_joined_stage_pre_inquired_all]
     
     community_joined_stage_inquired_all = len(touchpoint_df[touchpoint_df["ZM.Joined.Stage"] == "02 INQUIRED"])
     function_dataframe["community_joined_stage_inquired_all"] = [community_joined_stage_inquired_all]
     
     community_joined_stage_applied_all = len(touchpoint_df[touchpoint_df["ZM.Joined.Stage"] == "03 APPLIED"])
     function_dataframe["community_joined_stage_applied_all"] = [community_joined_stage_applied_all]
     
     community_joined_stage_app_complete_all = len(touchpoint_df[touchpoint_df["ZM.Joined.Stage"] == "04 APP COMPLETE"])
     function_dataframe["community_joined_stage_app_complete_all"] = [community_joined_stage_app_complete_all]
     
     community_joined_stage_accepted_all = len(touchpoint_df[touchpoint_df["ZM.Joined.Stage"] == "05 ACCEPTED"])
     function_dataframe["community_joined_stage_accepted_all"] = [community_joined_stage_accepted_all]
     
     community_joined_stage_committed_all = len(touchpoint_df[touchpoint_df["ZM.Joined.Stage"] == "06 COMMITTED"])
     function_dataframe["community_joined_stage_committed_all"] = [community_joined_stage_committed_all]
     
     community_joined_stage_missing_all = len(touchpoint_df[touchpoint_df["ZM.Joined.Stage"] == "07 DATE OF INITIAL CONTACT MISSING"])
     function_dataframe["community_joined_stage_missing_all"] = [community_joined_stage_missing_all]
     
     #---------------------------------------------
     
     friend_finder_used_all = len(touchpoint_df[touchpoint_df["friend_finder"] == "Friend Finder Used"])
     function_dataframe["friend_finder_used_all"] = [friend_finder_used_all]
     
     roommate_quiz_completed_all = len(touchpoint_df[touchpoint_df["roommate_match_quiz"] == "Roommate Quiz Completed"])
     function_dataframe["roommate_quiz_completed_all"] = [roommate_quiz_completed_all]
     
     
     #################################################
     
     #filtering full data for accepted community only
     touchpoint_df_accepted_com = touchpoint_df[touchpoint_df["ZM.Accepted"] == 1].reset_index(drop = True)
     
     #################################################
     
     total_students_accepted_comm = len(touchpoint_df_accepted_com)
     function_dataframe["total_students_accepted_comm"] = [total_students_accepted_comm]
     
     community_matched_accepted_comm = len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["created_by_csv"] == "Community Match"])
     function_dataframe["community_matched_accepted_comm"] = [community_matched_accepted_comm]
     
     count_current_cohort_year_accepted_comm = len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["uos_cohort_year"] == current_cohort_year])
     function_dataframe["count_current_cohort_year_accepted_comm"] = [count_current_cohort_year_accepted_comm]
     
     
     #-------------------------------------------------------
     engaged_any_accepted_comm = len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["engaged_any"] == 1])
     function_dataframe["engaged_any_accepted_comm"] = [engaged_any_accepted_comm]

     engaged_any_null_accepted_comm = len(touchpoint_df_accepted_com) - len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["engaged_any"] == 1])
     function_dataframe["engaged_any_null_accepted_comm"] = [engaged_any_null_accepted_comm]

     engaged_1_week_accepted_comm = len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["engaged_week"] == "1 week"])
     function_dataframe["engaged_1_week_accepted_comm"] = [engaged_1_week_accepted_comm]

     engaged_2_week_accepted_comm = len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["engaged_week"] == "2 weeks"])
     function_dataframe["engaged_2_week_accepted_comm"] = [engaged_2_week_accepted_comm]

     engaged_3_week_accepted_comm = len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["engaged_week"] == "3 weeks"])
     function_dataframe["engaged_3_week_accepted_comm"] = [engaged_3_week_accepted_comm]

     engaged_4_week_accepted_comm = len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["engaged_week"] == "4 weeks"])
     function_dataframe["engaged_4_week_accepted_comm"] = [engaged_4_week_accepted_comm]

     engaged_5_60_days_or_less_accepted_comm = len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["engaged_week"] == "5 - 60 days or less"])
     function_dataframe["engaged_5_60_days_or_less_accepted_comm"] = [engaged_5_60_days_or_less_accepted_comm]

     engaged_6_90_days_or_less_accepted_comm = len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["engaged_week"] == "6 - 90 days or less"])
     function_dataframe["engaged_6_90_days_or_less_accepted_comm"] = [engaged_6_90_days_or_less_accepted_comm]
 
     engaged_7_more_than_90_days_accepted_comm = len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["engaged_week"] == "7 - more than 90 days"])
     function_dataframe["engaged_7_more_than_90_days_accepted_comm"] = [engaged_7_more_than_90_days_accepted_comm]

     #-----------------------------------------------------------
     login_1_week_accepted_comm = len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["login_week"] == "1 week"])
     function_dataframe["login_1_week_accepted_comm"] = [login_1_week_accepted_comm]

     login_2_week_accepted_comm = len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["login_week"] == "2 weeks"])
     function_dataframe["login_2_week_accepted_comm"] = [login_2_week_accepted_comm]

     login_3_week_accepted_comm = len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["login_week"] == "3 weeks"])
     function_dataframe["login_3_week_accepted_comm"] = [login_3_week_accepted_comm]

     login_4_week_accepted_comm = len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["login_week"] == "4 weeks"])
     function_dataframe["login_4_week_accepted_comm"] = [login_4_week_accepted_comm]

     login_5_60_days_or_less_accepted_comm = len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["login_week"] == "5 - 60 days or less"])
     function_dataframe["login_5_60_days_or_less_accepted_comm"] = [login_5_60_days_or_less_accepted_comm]

     login_6_90_days_or_less_accepted_comm = len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["login_week"] == "6 - 90 days or less"])
     function_dataframe["login_6_90_days_or_less_accepted_comm"] = [login_6_90_days_or_less_accepted_comm]

     login_7_more_than_90_days_accepted_comm = len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["login_week"] == "7 - more than 90 days"])
     function_dataframe["login_7_more_than_90_days_accepted_comm"] = [login_7_more_than_90_days_accepted_comm]

     #-------------------------------------------------------------
     going_going_accepted_comm = len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["going"] == "Going"])
     function_dataframe["going_going_accepted_comm"] = [going_going_accepted_comm]

     going_not_accepted_comm = len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["going"] == "Not Going"])
     function_dataframe["going_not_accepted_comm"] = [going_not_accepted_comm]

     going_undecided_accepted_comm = len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["going"] == "Undecided"])
     function_dataframe["going_undecided_accepted_comm"] = [going_undecided_accepted_comm]

     #--------------------------------------------------------------
     community_joined_stage_pre_inquired_accepted_comm = len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["ZM.Joined.Stage"] == "01 PRE-INQUIRED"])
     function_dataframe["community_joined_stage_pre_inquired_accepted_comm"] = [community_joined_stage_pre_inquired_accepted_comm]
     
     community_joined_stage_inquired_accepted_comm = len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["ZM.Joined.Stage"] == "02 INQUIRED"])
     function_dataframe["community_joined_stage_inquired_accepted_comm"] = [community_joined_stage_inquired_accepted_comm]

     community_joined_stage_applied_accepted_comm = len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["ZM.Joined.Stage"] == "03 APPLIED"])
     function_dataframe["community_joined_stage_applied_accepted_comm"] = [community_joined_stage_applied_accepted_comm]
     
     community_joined_stage_app_complete_accepted_comm = len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["ZM.Joined.Stage"] == "04 APP COMPLETE"])
     function_dataframe["community_joined_stage_app_complete_accepted_comm"] = [community_joined_stage_app_complete_accepted_comm]

     community_joined_stage_accepted_accepted_comm = len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["ZM.Joined.Stage"] == "05 ACCEPTED"])
     function_dataframe["community_joined_stage_accepted_accepted_comm"] = [community_joined_stage_accepted_accepted_comm]
     
     community_joined_stage_committed_accepted_comm = len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["ZM.Joined.Stage"] == "06 COMMITTED"])
     function_dataframe["community_joined_stage_committed_accepted_comm"] = [community_joined_stage_committed_accepted_comm]

     community_joined_stage_missing_accepted_comm = len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["ZM.Joined.Stage"] == "07 DATE OF INITIAL CONTACT MISSING"])
     function_dataframe["community_joined_stage_missing_accepted_comm"] = [community_joined_stage_missing_accepted_comm]

     #--------------------------------------------------------------
     
     friend_finder_used_accepted_comm = len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["friend_finder"] == "Friend Finder Used"])
     function_dataframe["friend_finder_used_accepted_comm"] = [friend_finder_used_accepted_comm]
 
     roommate_quiz_completed_accepted_comm = len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["roommate_match_quiz"] == "Roommate Quiz Completed"])
     function_dataframe["roommate_quiz_completed_accepted_comm"] = [roommate_quiz_completed_accepted_comm]
     
     #---------------------------------------------------------------
     #index summary for accepted community only
     low_zm_index_accepted_comm =  len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["zeemee_engagement_index"] == "Low"])
     function_dataframe["low_zm_index_accepted_comm"] = [low_zm_index_accepted_comm]
     
     medium_zm_index_accepted_comm =  len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["zeemee_engagement_index"] == "Medium"])
     function_dataframe["medium_zm_index_accepted_comm"] = [medium_zm_index_accepted_comm]

     high_zm_index_accepted_comm =  len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["zeemee_engagement_index"] == "High"])
     function_dataframe["high_zm_index_accepted_comm"] = [high_zm_index_accepted_comm]

     #-----------------------------------------------
     low_going_zm_index_accepted_comm =  len(touchpoint_df_accepted_com[(touchpoint_df_accepted_com["zeemee_engagement_index"] == "Low") & (touchpoint_df_accepted_com["going"] == "Going")])
     function_dataframe["low_going_zm_index_accepted_comm"] = [low_going_zm_index_accepted_comm]

     medium_going_zm_index_accepted_comm =  len(touchpoint_df_accepted_com[(touchpoint_df_accepted_com["zeemee_engagement_index"] == "Medium") & (touchpoint_df_accepted_com["going"] == "Going")])
     function_dataframe["medium_going_zm_index_accepted_comm"] = [medium_going_zm_index_accepted_comm]
 
     high_going_zm_index_accepted_comm =  len(touchpoint_df_accepted_com[(touchpoint_df_accepted_com["zeemee_engagement_index"] == "High") & (touchpoint_df_accepted_com["going"] == "Going")])
     function_dataframe["high_going_zm_index_accepted_comm"] = [high_going_zm_index_accepted_comm]
     
     #----------------------------------------------=
     low_undecided_zm_index_accepted_comm =  len(touchpoint_df_accepted_com[(touchpoint_df_accepted_com["zeemee_engagement_index"] == "Low") & (touchpoint_df_accepted_com["going"] == "Undecided")])
     function_dataframe["low_undecided_zm_index_accepted_comm"] = [low_undecided_zm_index_accepted_comm]
     
     medium_undecided_zm_index_accepted_comm =  len(touchpoint_df_accepted_com[(touchpoint_df_accepted_com["zeemee_engagement_index"] == "Medium") & (touchpoint_df_accepted_com["going"] == "Undecided")])
     function_dataframe["medium_undecided_zm_index_accepted_comm"] = [medium_undecided_zm_index_accepted_comm]

     high_undecided_zm_index_accepted_comm =  len(touchpoint_df_accepted_com[(touchpoint_df_accepted_com["zeemee_engagement_index"] == "High") & (touchpoint_df_accepted_com["going"] == "Undecided")])
     function_dataframe["high_undecided_zm_index_accepted_comm"] = [high_undecided_zm_index_accepted_comm]

     #------------------------------------------------
     low_not_going_zm_index_accepted_comm =  len(touchpoint_df_accepted_com[(touchpoint_df_accepted_com["zeemee_engagement_index"] == "Low") & (touchpoint_df_accepted_com["going"] == "Not Going")])
     function_dataframe["low_not_going_zm_index_accepted_comm"] = [low_not_going_zm_index_accepted_comm]

     medium_not_going_zm_index_accepted_comm =  len(touchpoint_df_accepted_com[(touchpoint_df_accepted_com["zeemee_engagement_index"] == "Medium") & (touchpoint_df_accepted_com["going"] == "Not Going")])
     function_dataframe["medium_not_going_zm_index_accepted_comm"] = [medium_not_going_zm_index_accepted_comm]

     high_not_going_zm_index_accepted_comm =  len(touchpoint_df_accepted_com[(touchpoint_df_accepted_com["zeemee_engagement_index"] == "High") & (touchpoint_df_accepted_com["going"] == "Not Going")])
     function_dataframe["high_not_going_zm_index_accepted_comm"] = [high_not_going_zm_index_accepted_comm]

     #---------------------------------------------------
     non_crm_id_users =  len(touchpoint_df_accepted_com[touchpoint_df_accepted_com["ID.Number"].isnull()])
     function_dataframe["non_crm_id_users"] = [non_crm_id_users]

     high_zm_index_committed_accepted_comm =  len(touchpoint_df_accepted_com[(touchpoint_df_accepted_com["zeemee_engagement_index"] == "High") & (touchpoint_df_accepted_com["ZM.Status.Analysis"].isin(["Committed", "Enrolled"]))])
     function_dataframe["high_zm_index_committed_accepted_comm"] = [high_zm_index_committed_accepted_comm]

     high_zm_index_non_committed_accepted_comm =  len(touchpoint_df_accepted_com[(touchpoint_df_accepted_com["zeemee_engagement_index"] == "High") & (~touchpoint_df_accepted_com["ZM.Status.Analysis"].isin(["Committed", "Enrolled"]))])
     function_dataframe["high_zm_index_non_committed_accepted_comm"] = [high_zm_index_non_committed_accepted_comm]

     medium_zm_index_committed_accepted_comm =  len(touchpoint_df_accepted_com[(touchpoint_df_accepted_com["zeemee_engagement_index"] == "Medium") & (touchpoint_df_accepted_com["ZM.Status.Analysis"].isin(["Committed", "Enrolled"]))])
     function_dataframe["medium_zm_index_committed_accepted_comm"] = [medium_zm_index_committed_accepted_comm]
 
     medium_zm_index_non_committed_accepted_comm =  len(touchpoint_df_accepted_com[(touchpoint_df_accepted_com["zeemee_engagement_index"] == "Medium") & (~touchpoint_df_accepted_com["ZM.Status.Analysis"].isin(["Committed", "Enrolled"]))])
     function_dataframe["medium_zm_index_non_committed_accepted_comm"] = [medium_zm_index_non_committed_accepted_comm]

     low_zm_index_committed_accepted_comm =  len(touchpoint_df_accepted_com[(touchpoint_df_accepted_com["zeemee_engagement_index"] == "Low") & (touchpoint_df_accepted_com["ZM.Status.Analysis"].isin(["Committed", "Enrolled"]))])
     function_dataframe["low_zm_index_committed_accepted_comm"] = [low_zm_index_committed_accepted_comm]
 
     low_zm_index_non_committed_accepted_comm =  len(touchpoint_df_accepted_com[(touchpoint_df_accepted_com["zeemee_engagement_index"] == "Low") & (~touchpoint_df_accepted_com["ZM.Status.Analysis"].isin(["Committed", "Enrolled"]))])
     function_dataframe["low_zm_index_non_committed_accepted_comm"] = [low_zm_index_non_committed_accepted_comm]

       
     #### Method 1 : column wise count of non missing values---------------------------
     with_student_id_count_accepted_comm = int(touchpoint_df_accepted_com["ID.Number"].notnull().sum())
     function_dataframe["with_student_id_count_accepted_comm"] = [with_student_id_count_accepted_comm]

     with_student_id_count_all = int(touchpoint_df["ID.Number"].notnull().sum())
     function_dataframe["with_student_id_count_all"] = [with_student_id_count_all]

     function_dataframe["date_of_report"] = [touchpoint_df.loc[0,"date_of_report"]]
     
     
     ##----------------- adding new fields after the first draft
     
     high_zm_index_committed_all =  len(touchpoint_df[(touchpoint_df["zeemee_engagement_index"] == "High") & (touchpoint_df["ZM.Status.Analysis"].isin(["Committed", "Enrolled"]))])
     function_dataframe["high_zm_index_committed_all"] = [high_zm_index_committed_all]
     
     high_zm_index_non_committed_all =  len(touchpoint_df[(touchpoint_df["zeemee_engagement_index"] == "High") & (~touchpoint_df["ZM.Status.Analysis"].isin(["Committed", "Enrolled"]))])
     function_dataframe["high_zm_index_non_committed_all"] = [high_zm_index_non_committed_all]

     medium_zm_index_committed_all =  len(touchpoint_df[(touchpoint_df["zeemee_engagement_index"] == "Medium") & (touchpoint_df["ZM.Status.Analysis"].isin(["Committed", "Enrolled"]))])
     function_dataframe["medium_zm_index_committed_all"] = [medium_zm_index_committed_all]

     medium_zm_index_non_committed_all =  len(touchpoint_df[(touchpoint_df["zeemee_engagement_index"] == "Medium") & (~touchpoint_df["ZM.Status.Analysis"].isin(["Committed", "Enrolled"]))])
     function_dataframe["medium_zm_index_non_committed_all"] = [medium_zm_index_non_committed_all]

     low_zm_index_committed_all =  len(touchpoint_df[(touchpoint_df["zeemee_engagement_index"] == "Low") & (touchpoint_df["ZM.Status.Analysis"].isin(["Committed", "Enrolled"]))])
     function_dataframe["low_zm_index_committed_all"] = [low_zm_index_committed_all]

     low_zm_index_non_committed_all =  len(touchpoint_df[(touchpoint_df["zeemee_engagement_index"] == "Low") & (~touchpoint_df["ZM.Status.Analysis"].isin(["Committed", "Enrolled"]))])
     function_dataframe["low_zm_index_non_committed_all"] = [low_zm_index_non_committed_all]
     
     going_not_committed = len(touchpoint_df[(touchpoint_df["going"] == "Going") & (~touchpoint_df["ZM.Status.Analysis"].isin(["Committed", "Enrolled"]))])
     function_dataframe["going_not_committed"] = [going_not_committed]
     
     #################################################
     
     #filtering full data for non accepted community only
     touchpoint_df_non_accepted_com = touchpoint_df[touchpoint_df["accepted"] != "In Accepted Community"].reset_index(drop = True)
     
     #################################################
     
     high_zm_index_committed_non_accepted_community =  len(touchpoint_df_non_accepted_com[(touchpoint_df_non_accepted_com["zeemee_engagement_index"] == "High") & (touchpoint_df_non_accepted_com["ZM.Status.Analysis"].isin(["Committed", "Enrolled"]))])
     function_dataframe["high_zm_index_committed_non_accepted_community"] = [high_zm_index_committed_non_accepted_community]
     
     high_zm_index_non_committed_non_accepted_community =  len(touchpoint_df_non_accepted_com[(touchpoint_df_non_accepted_com["zeemee_engagement_index"] == "High") & (~touchpoint_df_non_accepted_com["ZM.Status.Analysis"].isin(["Committed", "Enrolled"]))])
     function_dataframe["high_zm_index_non_committed_non_accepted_community"] = [high_zm_index_non_committed_non_accepted_community]
     
     medium_zm_index_committed_non_accepted_community =  len(touchpoint_df_non_accepted_com[(touchpoint_df_non_accepted_com["zeemee_engagement_index"] == "Medium") & (touchpoint_df_non_accepted_com["ZM.Status.Analysis"].isin(["Committed", "Enrolled"]))])
     function_dataframe["medium_zm_index_committed_non_accepted_community"] = [medium_zm_index_committed_non_accepted_community]
     
     medium_zm_index_non_committed_non_accepted_community =  len(touchpoint_df_non_accepted_com[(touchpoint_df_non_accepted_com["zeemee_engagement_index"] == "Medium") & (~touchpoint_df_non_accepted_com["ZM.Status.Analysis"].isin(["Committed", "Enrolled"]))])
     function_dataframe["medium_zm_index_non_committed_non_accepted_community"] = [medium_zm_index_non_committed_non_accepted_community]
     
     low_zm_index_committed_non_accepted_community =  len(touchpoint_df_non_accepted_com[(touchpoint_df_non_accepted_com["zeemee_engagement_index"] == "Low") & (touchpoint_df_non_accepted_com["ZM.Status.Analysis"].isin(["Committed", "Enrolled"]))])
     function_dataframe["low_zm_index_committed_non_accepted_community"] = [low_zm_index_committed_non_accepted_community]
     
     low_zm_index_non_committed_non_accepted_community =  len(touchpoint_df_non_accepted_com[(touchpoint_df_non_accepted_com["zeemee_engagement_index"] == "Low") & (~touchpoint_df_non_accepted_com["ZM.Status.Analysis"].isin(["Committed", "Enrolled"]))])
     function_dataframe["low_zm_index_non_committed_non_accepted_community"] = [low_zm_index_non_committed_non_accepted_community]
  
     return function_dataframe
