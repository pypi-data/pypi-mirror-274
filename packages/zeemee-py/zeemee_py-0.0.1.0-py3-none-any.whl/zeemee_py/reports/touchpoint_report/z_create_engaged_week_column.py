
def create_engaged_week_column(touchpoint_df):
     import datetime
     import pandas as pd
     
     today_date = datetime.datetime.today()
     todays_date_string = today_date.strftime('%Y-%m-%d')
     
     touchpoint_df["last_engaged_date"] = pd.to_datetime(touchpoint_df["last_engaged_date"], errors='coerce')
     days_since_last_engaged = (today_date - touchpoint_df["last_engaged_date"]).dt.days
     days_since_last_engaged = days_since_last_engaged.fillna(70000).astype(int)
     
     weeks_since_last_engaged = list()
     
     for i in range(len(days_since_last_engaged)):
          if days_since_last_engaged[i] < 8:
               weeks_since_last_engaged.append('1 week')
          elif (days_since_last_engaged[i] >= 8) & (days_since_last_engaged[i] <= 14):
               weeks_since_last_engaged.append('2 weeks')
          elif (days_since_last_engaged[i] >= 15) & (days_since_last_engaged[i] <= 21):
               weeks_since_last_engaged.append('3 weeks')
          elif (days_since_last_engaged[i] >= 22) & (days_since_last_engaged[i] <= 28):
               weeks_since_last_engaged.append('4 weeks')
          elif (days_since_last_engaged[i] >= 29) & (days_since_last_engaged[i] <= 60):
               weeks_since_last_engaged.append('5 - 60 days or less')
          elif (days_since_last_engaged[i] >= 60) & (days_since_last_engaged[i] <= 90):
               weeks_since_last_engaged.append('6 - 90 days or less')
          elif (days_since_last_engaged[i] >= 90) & (days_since_last_engaged[i] < 70000):
               weeks_since_last_engaged.append('7 - more than 90 days')
          else: weeks_since_last_engaged.append('')
          
     touchpoint_df['engaged_week'] = weeks_since_last_engaged
     #we replace blanks with NA in the first line when we chage the column to datetime type. So
     #need to revert to blanks 
     touchpoint_df["last_engaged_date"] = touchpoint_df["last_engaged_date"].fillna("")
     
     return touchpoint_df
