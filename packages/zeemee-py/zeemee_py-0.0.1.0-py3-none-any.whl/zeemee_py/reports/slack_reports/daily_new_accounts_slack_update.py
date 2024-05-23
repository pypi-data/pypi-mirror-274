
def main_function():
     import datetime
     import importlib
     
     days_to_complete_target = 31
     new_account_target = 25019
     month_starts_after = '2024-05-01'
     month_ends_before =  '2024-06-01'
     
     from zeemee_py.helper_functions import connect_athena
     importlib.reload(connect_athena)
     
     
     query_string = """
     select count(uuid) from 
     silver.prod_follower_users_latest
     where 
     date(created_at) >= date('{month_starts_after}') and 
     date(created_at) < date('{month_ends_before}') and 
     perm_org_official = 'false'
     """.format(
          month_starts_after = month_starts_after,
          month_ends_before = month_ends_before
     )
     
     new_accounts_df = connect_athena.run_query_in_athena(query_string)
     new_accounts = new_accounts_df.iloc[0,0]
     
     today = datetime.datetime.now()
     day_of_the_month = int(today.strftime("%d"))
     day_of_the_month = day_of_the_month - 1
     
     
     expected_new_accounts = int(new_account_target/days_to_complete_target) * day_of_the_month
     
     percent_days_elapsed_15_day_target = round(day_of_the_month * 100 /days_to_complete_target,2)
     percent_days_elapsed_15_day_target
     
     percent_target_complete_15_day_target = round(new_accounts * 100 /new_account_target,2)
     percent_target_complete_15_day_target
     
     new_accounts_to_match_expected_target = int((percent_days_elapsed_15_day_target - percent_target_complete_15_day_target) * new_account_target/100)
     new_accounts_to_match_expected_target
     new_accounts_to_match_expected_target = max(new_accounts_to_match_expected_target,0) + int(new_account_target/days_to_complete_target)
     new_accounts_to_match_expected_target
     
     new_accounts_daily_to_reach_expected_target = int((new_account_target - new_accounts)/(days_to_complete_target - day_of_the_month))
     new_accounts_daily_to_reach_expected_target
      
     #assuming 2.3% conversion rate
     sms_to_be_sent_assuming_2_7_conversion_rate_catch_up = int(new_accounts_to_match_expected_target/.027)
     sms_to_be_sent_assuming_2_7_conversion_rate_catch_up
     
     slack_message = """
     Monthly Goal Update:
     New accounts in May 2023 = 25,019
     
     Day of the month = {day_of_the_month}
     Expected new accounts = {expected_new_accounts}
     New accounts this month = {new_accounts}
     
     Expected target completion % to be on track = {percent_days_elapsed_15_day_target}%
     Actual target completed % = {percent_target_complete_15_day_target}%
     
     Aim for new accounts today to catch up (including today's avg target)= {new_accounts_to_match_expected_target}
     SMS count to be sent to catch up assuming 2.7% install rate = {sms_to_be_sent_assuming_2_7_conversion_rate_catch_up}
     
     Daily new accounts needed from today to reach the target (balance target spread across the remaining days)= {new_accounts_daily_to_reach_expected_target}
     
     
     """.format(
          day_of_the_month = day_of_the_month,
          expected_new_accounts = expected_new_accounts,
          new_accounts = new_accounts,
          percent_days_elapsed_15_day_target = percent_days_elapsed_15_day_target,
          percent_target_complete_15_day_target = percent_target_complete_15_day_target,
          new_accounts_to_match_expected_target = new_accounts_to_match_expected_target,
          sms_to_be_sent_assuming_2_7_conversion_rate_catch_up = sms_to_be_sent_assuming_2_7_conversion_rate_catch_up,
          new_accounts_daily_to_reach_expected_target = new_accounts_daily_to_reach_expected_target)
     
     from zeemee_py.helper_functions import send_to_slack
     importlib.reload(send_to_slack)
     send_to_slack.send_message_to_slack("comms", slack_message)
