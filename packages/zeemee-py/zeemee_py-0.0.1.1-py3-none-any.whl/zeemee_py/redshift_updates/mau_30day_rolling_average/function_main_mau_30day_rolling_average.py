def main_function():
     import datetime
     import importlib
     import pandas as pd
     import warnings
     warnings.simplefilter(action='ignore', category=FutureWarning)
     
     end_date = datetime.datetime.now()
     
     final_mau_df = pd.DataFrame()
     
     for i in range(3):
          from zeemee_py.redshift_updates.mau_30day_rolling_average import z_calculate_30day_rolling_average
          importlib.reload(z_calculate_30day_rolling_average)
          
          end_date_string = end_date.strftime('%Y-%m-%d')
          mau_df = z_calculate_30day_rolling_average.get_rolling_average(end_date_string)
          final_mau_df = pd.concat([final_mau_df, mau_df]).reset_index(drop = True)
          
          end_date = end_date + datetime.timedelta(days = -1)
     
     print("")
     print(final_mau_df)
     
     from zeemee_py.redshift_updates.mau_30day_rolling_average import function_redshift_update_mau_30day_rolling_average
     importlib.reload(function_redshift_update_mau_30day_rolling_average)
     function_redshift_update_mau_30day_rolling_average.update_redshift_table(final_mau_df)
     
     text_for_slack = "mau_data redshift table updated"
     from zeemee_py.helper_functions import send_to_slack
     importlib.reload(send_to_slack)
     send_to_slack.send_message_to_slack("data-reports", text_for_slack)
