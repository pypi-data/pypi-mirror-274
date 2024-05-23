
def create_incsv_column(touchpoint_df):
    import numpy as np
    import pandas as pd
    
    incsv_list = list()
    touchpoint_df['csv_import_id'] = pd.to_numeric(touchpoint_df['csv_import_id'])
    
    try:
        max_id = int(np.nanmax(list(touchpoint_df['csv_import_id'])))
    except:
        max_id = 0

    
    for i in touchpoint_df['csv_import_id']:
        if i == max_id:
            incsv_list.append('In.CSV.File')
        else:
            incsv_list.append('')
            
    touchpoint_df['in_csv_file'] = incsv_list
    
    return touchpoint_df
