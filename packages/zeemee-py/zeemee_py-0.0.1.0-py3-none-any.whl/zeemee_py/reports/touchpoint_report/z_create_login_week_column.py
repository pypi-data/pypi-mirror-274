
def create_login_week_column(touchpoint_df):
     import datetime
     import pandas as pd
     
     today_date = datetime.datetime.today()
     todays_date_string = today_date.strftime('%Y-%m-%d')
     
     
     touchpoint_df["last_login"] = pd.to_datetime(touchpoint_df["last_login"], errors='coerce')
     days_since_last_login = (today_date - touchpoint_df["last_login"]).dt.days
     days_since_last_login = days_since_last_login.fillna(70000).astype(int)
     
     weeks_since_last_login = list()
     
     for i in range(len(days_since_last_login)):
          if days_since_last_login[i] < 8:
               weeks_since_last_login.append('1 week')
          elif (days_since_last_login[i] >= 8) & (days_since_last_login[i] <= 14):
               weeks_since_last_login.append('2 weeks')
          elif (days_since_last_login[i] >= 15) & (days_since_last_login[i] <= 21):
               weeks_since_last_login.append('3 weeks')
          elif (days_since_last_login[i] >= 22) & (days_since_last_login[i] <= 28):
               weeks_since_last_login.append('4 weeks')
          elif (days_since_last_login[i] >= 29) & (days_since_last_login[i] <= 60):
               weeks_since_last_login.append('5 - 60 days or less')
          elif (days_since_last_login[i] >= 60) & (days_since_last_login[i] <= 90):
               weeks_since_last_login.append('6 - 90 days or less')
          elif (days_since_last_login[i] >= 90) & (days_since_last_login[i] < 70000):
               weeks_since_last_login.append('7 - more than 90 days')
          else: weeks_since_last_login.append('')
          
     touchpoint_df['login_week'] = weeks_since_last_login
     #we replace blanks with NA in the first line when we chage the column to datetime type. So
     #need to revert to blanks 
     touchpoint_df["last_login"] = touchpoint_df["last_login"].fillna("")
     
     return touchpoint_df
