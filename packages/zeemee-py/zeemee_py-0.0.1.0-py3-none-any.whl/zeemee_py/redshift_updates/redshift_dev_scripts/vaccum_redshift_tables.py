import sys
import importlib
import pandas as pd
from pandas import read_sql
import pandas as pd

table_list_df = read_sql(
"""
select table_name from information_schema.tables
where table_schema = 'data_team'
""", con = con)

slack_text = ""

for i in range(len(df)):

     from zeemee_py.helper_functions import connect_redshift
     importlib.reload(connect_redshift)
     con = connect_redshift.establish_redshift_connection()
     
     execute_vaccume = """
     END TRANSACTION;
     vacuum data_team.{};
     """.format(table_list_df.loc[i,'table_name'])
     
     cur = con.cursor()
     cur.execute(execute_vaccume)
     con.commit()
     con.close()
     
     print_text = 'vacuum done for {}'.format(table_list_df.loc[i,'table_name']))
     print(print_text)
     slack_text = slack_text + print_text + '\n'


from zeemee_py.helper_functions import send_to_slack
importlib.reload(send_to_slack)
con = send_to_slack.send_message_to_slack("data-team", slack_text)



