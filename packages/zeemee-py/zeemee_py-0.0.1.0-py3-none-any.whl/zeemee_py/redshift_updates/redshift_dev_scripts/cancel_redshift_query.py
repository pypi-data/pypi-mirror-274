
import importlib

from zeemee_py.helper_functions import connect_redshift
importlib.reload(connect_redshift)
con = connect_redshift.establish_redshift_connection()

cancel_query = """ 
ALTER TABLE /*skru-7f9b58e8-ba97-4ad0-a8b0-3879fe0410e8-g0-0*/ "data_team"."pred_model_latest" 
ALTER SORTKEY ("org_id")

"""

cur = con.cursor()
cur.execute(cancel_query)
con.commit()
