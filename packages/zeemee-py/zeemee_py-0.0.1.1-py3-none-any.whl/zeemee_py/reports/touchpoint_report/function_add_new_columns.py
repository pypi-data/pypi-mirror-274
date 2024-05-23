
def add_new_columns(touchpoint_df, organization_id):
     import importlib
     
     from zeemee_py.reports.touchpoint_report import z_create_last_engaged_column
     importlib.reload(z_create_last_engaged_column)
     touchpoint_df = z_create_last_engaged_column.create_last_engaged_date_column(touchpoint_df)
     
     from zeemee_py.reports.touchpoint_report import z_create_friendfinder_rmmatch_column
     importlib.reload(z_create_friendfinder_rmmatch_column)
     touchpoint_df = z_create_friendfinder_rmmatch_column.create_ff_and_rmmatch_flag_column(touchpoint_df)
     
     from zeemee_py.reports.touchpoint_report import z_create_fname_lname_column
     importlib.reload(z_create_fname_lname_column)
     touchpoint_df = z_create_fname_lname_column.create_fname_lname_columns(touchpoint_df)
     
     from zeemee_py.reports.touchpoint_report import z_create_engaged_week_column
     importlib.reload(z_create_engaged_week_column)
     touchpoint_df = z_create_engaged_week_column.create_engaged_week_column(touchpoint_df)
     
     from zeemee_py.reports.touchpoint_report import z_create_engaged_any_column
     importlib.reload(z_create_engaged_any_column)
     touchpoint_df = z_create_engaged_any_column.create_engaged_any_column(touchpoint_df)
     
     from zeemee_py.reports.touchpoint_report import z_create_login_week_column
     importlib.reload(z_create_login_week_column)
     touchpoint_df = z_create_login_week_column.create_login_week_column(touchpoint_df)
     
     from zeemee_py.reports.touchpoint_report import z_create_incsv_column
     importlib.reload(z_create_incsv_column)
     touchpoint_df = z_create_incsv_column.create_incsv_column(touchpoint_df)
     
     from zeemee_py.reports.touchpoint_report import z_create_year_term_type_partnercsv_columns
     importlib.reload(z_create_year_term_type_partnercsv_columns)
     touchpoint_df = z_create_year_term_type_partnercsv_columns.create_year_term_type_partnercsv_columns(touchpoint_df)
     
     from zeemee_py.reports.touchpoint_report import z_create_information_column
     importlib.reload(z_create_information_column)
     touchpoint_df = z_create_information_column.create_information_column(touchpoint_df, organization_id)
     
     return touchpoint_df
