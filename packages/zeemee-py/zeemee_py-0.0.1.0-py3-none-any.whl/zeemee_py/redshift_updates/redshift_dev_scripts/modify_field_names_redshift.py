
import sys
import importlib
import pandas as pd
from pandas import read_sql

from zeemee_py.helper_functions import connect_redshift
importlib.reload(connect_redshift)
con = connect_redshift.establish_redshift_connection()


old_col_names = [
     "community_funnel_inquired",
     "community_funnel_applied",
     "community_funnel_accepted",
     "community_funnel_committed",
     "community_funnel_enrolled"
     ]

new_col_names = [
     "community_funnel_inquired_1",
     "community_funnel_applied_1",
     "community_funnel_accepted_1",
     "community_funnel_committed_1",
     "community_funnel_enrolled_1"
     ]

for i in range(len(new_col_names)):
     from zeemee_py.helper_functions import connect_redshift
     importlib.reload(connect_redshift)
     con = connect_redshift.establish_redshift_connection()
     
     add_column_to_touchpoint_dash_data = """
     ALTER TABLE data_team.one_pager_data RENAME COLUMN {} TO {};
     """.format(old_col_names[i], new_col_names[i])
     
     cur = con.cursor()
     #cur.execute(add_column_to_touchpoint_dash_data) #uncomment this when running
     con.commit()
     con.close()
     
     print("mofified:",new_col_names[i])
   
print("modification complete")

