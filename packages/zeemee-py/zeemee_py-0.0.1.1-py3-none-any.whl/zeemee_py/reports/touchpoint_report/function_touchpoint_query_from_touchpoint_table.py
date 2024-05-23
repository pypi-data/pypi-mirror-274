
def touchpoint_from_touchpoint_table(organization_id, cohort_year):
     import datetime
     import importlib
     
     query_start_time =  datetime.datetime.now()
     print("starting touchpoint query:", query_start_time.strftime("%H:%M:%S"))
     
     query_string = """
     select * 
     from gold.touchpoint_report_latest
     where org_id = '{organization_id}'
     """.format(
          organization_id = organization_id
          )
     
     from zeemee_py.helper_functions import connect_athena
     importlib.reload(connect_athena)
     touchpoint_df = connect_athena.run_query_in_athena(query_string)
     
     query_end_time = datetime.datetime.now()
     print("ending touchpoint query:  ", query_end_time.strftime("%H:%M:%S"))
     print("total query time:", query_end_time - query_start_time)
     
     return touchpoint_df
