def get_rolling_average(end_date_string):
     import datetime
     import pandas as pd
     import importlib
     
     end_date = datetime.datetime.strptime(end_date_string, '%Y-%m-%d')
     
     start_date = end_date + datetime.timedelta(days=-30)
     start_date_string = start_date.strftime('%Y-%m-%d')
     
     from zeemee_py.helper_functions import connect_athena
     importlib.reload(connect_athena)
     
     print("start_date:", start_date_string, "    end_date:", end_date_string)
     
     #get ios counts
     ios_mau_query_string = """
          select
          count(distinct REPLACE(user_id, '@x.zeemee.com', ''))
          from
          silver.segment_ios_app_latest as ios
          where 
          ios.timestamp >= '{start_date_string}'
          and ios.timestamp < '{end_date_string}'
          and ios.event = 'App Launched'
          """.format(
               start_date_string = start_date_string,
               end_date_string = end_date_string
          )
     
     ios_mau_df = connect_athena.run_query_in_athena(ios_mau_query_string)
     ios_mau = ios_mau_df.iloc[0,0]
     
     #get android counts
     android_mau_query_string = """
          select
          count(distinct user_id)
          from
          silver.segment_android_app_latest as android
          where 
          android.timestamp >= '{start_date_string}'
          and android.timestamp < '{end_date_string}'
          and android.event in ('App Launched', 'App Opened', 'Application Opened')
          """.format(
               start_date_string = start_date_string,
               end_date_string = end_date_string
          )
     
     android_mau_df = connect_athena.run_query_in_athena(android_mau_query_string)
     android_mau = android_mau_df.iloc[0,0]
     
     #get web counts
     web_mau_query_string = """
          select
          count(distinct user_id)
          from
          silver.zeemee_production_website_pages_latest as ios
          where 
          date(ios.timestamp) >= date('{start_date_string}')
          and date(ios.timestamp) < date('{end_date_string}')
          """.format(
               start_date_string = start_date_string,
               end_date_string = end_date_string
          )
     
     web_mau_df = connect_athena.run_query_in_athena(web_mau_query_string)
     web_mau = web_mau_df.iloc[0,0]

     mau_df = pd.DataFrame()
     mau_df["date"] =  [end_date_string] * 3
     mau_df["mau"] =  [ios_mau, android_mau, web_mau]
     mau_df["platform"] =  ["ios", "android", "web"]
     mau_df["aggregation_type"] =  ["30 day rolling"] * 3
     
     return mau_df

     
