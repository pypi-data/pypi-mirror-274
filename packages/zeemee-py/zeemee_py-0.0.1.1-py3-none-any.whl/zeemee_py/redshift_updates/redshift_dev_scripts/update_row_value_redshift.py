
import importlib

from zeemee_py.helper_functions import connect_redshift
importlib.reload(connect_redshift)
con = connect_redshift.establish_redshift_connection()

modify_row_value = """
update data_team.organization_data
set analysisapprate = 'YesISSUE'
where org_id in ('5031e44d-c71f-4ca9-8ac0-06cd6ddd5b10',
'0a28a220-07dc-464d-acad-1474ae325a5b',
'773f3d2d-fc10-421d-92d0-1c6a4b0b3e7b',
'8658ae07-7283-4a81-b69f-ee90f511db83',
'52f12328-6888-4b3a-9e78-ecbca43a4d22',
'f2c35542-0b8a-4d47-a2a7-c1b1b24f5d49')
and zm_cohort_year = 2022;
"""

cur = con.cursor()
#cur.execute(modify_row_value) #uncomment this when running
con.commit()
con.close()
