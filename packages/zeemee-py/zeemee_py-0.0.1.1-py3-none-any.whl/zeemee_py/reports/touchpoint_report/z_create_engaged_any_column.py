
def create_engaged_any_column(touchpoint_df):
     
     engaged_any = list()
     touchpoint_df['last_engaged_date'] = touchpoint_df['last_engaged_date'].fillna('')

     for i in range(len(touchpoint_df)):
          if ( touchpoint_df['going'][i] == 'going') | (touchpoint_df['going'][i] == 'notgoing') | (touchpoint_df['roommate_match_quiz'][i] == 't') | ( touchpoint_df['engaged_week'][i] != ''):
               engaged_any.append(1)
          else:
               engaged_any.append("")

     touchpoint_df['engaged_any'] = engaged_any

     return touchpoint_df
