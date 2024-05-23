import pandas as pd
import importlib

continuous_variable_columns = [
     #'ZeeMee.ID',
     'messages_in_other_orgs',
     'users_following_other_orgs_followed_by_user',
     'users_following_organization_followed_by_our_user',
     'engaged_any'
     ]

categotical_var = [   
    'going_going', 
    'going_notgoing',
    'public_profile_enabled_t',
    'interested_t', 
    'created_by_csv_t',
    'uos_transfer_status_t', 
    'roommate_match_quiz_t']

touchpoint_df = pd.read_csv("/home/mayur/data/reports/alfred-university_touchpoint.csv")

from zeemee_py.redshift_updates.prediction_model import z_clean_data
importlib.reload(z_clean_data)
touchpoint_df = z_clean_data.clean_data(touchpoint_df)
print(touchpoint_df[continuous_variable_columns].iloc[:10,:])

from zeemee_py.redshift_updates.prediction_model import z_scaling
importlib.reload(z_scaling)
df_continuous_var_scaled = z_scaling.scaling(touchpoint_df, continuous_variable_columns)
print(df_continuous_var_scaled.iloc[:10,:])

from zeemee_py.redshift_updates.prediction_model import z_one_hot_encoding
importlib.reload(z_one_hot_encoding)
one_hot_df = z_one_hot_encoding.one_hot_encoding(touchpoint_df)
print(one_hot_df.iloc[:10,:])
