
import importlib

from zeemee_py.helper_functions import connect_redshift
importlib.reload(connect_redshift)
con = connect_redshift.establish_redshift_connection()

cancel_query = """ 
delete from data_team.all_partner_data where table_unique_id in (216550, 124397)
and entry_year = 2023
and org_id = '0a04abd6-90ed-446b-8c3f-84a6a03c9ce7'

"""

cur = con.cursor()
#cur.execute(cancel_query) #uncomment this when running
con.commit()
