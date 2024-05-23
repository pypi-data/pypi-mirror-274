
import importlib

from zeemee_py.helper_functions import connect_redshift
importlib.reload(connect_redshift)
con = connect_redshift.establish_redshift_connection()

cancel_query = """ 
drop table #systemctl 
status cron
data_team.persisted_all_partner_additional_fields_org_data_combined_first_time_fall_only

"""

cur = con.cursor()
#cur.execute(cancel_query) #uncomment this when running
con.commit()
