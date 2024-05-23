
import importlib

from zeemee_py.helper_functions import connect_redshift
importlib.reload(connect_redshift)
con = connect_redshift.establish_redshift_connection()

cancel_query = """ 
SELECT pg_cancel_backend(blocking.pid)
FROM pg_locks AS waiting
LEFT JOIN pg_locks AS blocking
     ON ( (waiting. "database" = blocking. "database"
     AND (waiting.relation = blocking.relation
     OR blocking.relation IS NULL
     OR waiting.relation IS NULL))
     OR waiting.TRANSACTION = blocking.TRANSACTION)
WHERE 1 = 1
AND  NOT waiting.GRANTED
AND  waiting.pid <> blocking.pid
AND  blocking.GRANTED = 't'
"""

cur = con.cursor()
cur.execute(cancel_query)
con.commit()
