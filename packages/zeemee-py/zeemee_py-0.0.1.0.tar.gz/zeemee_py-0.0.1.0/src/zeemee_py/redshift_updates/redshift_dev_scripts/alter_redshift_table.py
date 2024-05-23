
import importlib

from zeemee_py.helper_functions import connect_redshift
importlib.reload(connect_redshift)
con = connect_redshift.establish_redshift_connection()

"""
varchar(80)
numeric(6,4)
"""

new_col_names = [
     "zm_melt_data_check varchar(80)",  
     "zm_type_2 varchar(80)",
     "zm_type_3 varchar(80)", 
     "zm_type_4 varchar(80)", 
     "ipeds_partner_zip int"
]

for i in range(len(new_col_names)):
     from zeemee_py.helper_functions import connect_redshift
     importlib.reload(connect_redshift)
     con = connect_redshift.establish_redshift_connection()
   
     add_column_to_touchpoint_dash_dat = """
     alter table data_team.organization_data
     add column {}
     default NULL;
     """.format(new_col_names[i])
     
     cur = con.cursor()
     #cur.execute(add_column_to_touchpoint_dash_dat) #uncomment this when running
     con.commit()
     con.close()
   
     print("added:",new_col_names[i])
   
print("done")

