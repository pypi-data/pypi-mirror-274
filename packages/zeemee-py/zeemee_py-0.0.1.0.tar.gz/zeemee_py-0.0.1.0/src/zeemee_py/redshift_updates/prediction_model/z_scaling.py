
def scaling(touchpoint_df, continuous_variable_columns):
     import importlib
     import pickle
     import pandas as pd
     import os
     
     from zeemee_py.helper_functions import get_data_folder_path
     importlib.reload(get_data_folder_path)
     data_folder_path = get_data_folder_path.get_data_folder_path()
     scalar_file = os.path.join(data_folder_path,"prediction_model/RF_model_2ndshortlist_scaler_onlycontvar.pickle")
     
     zeemee_ids = list(touchpoint_df['id'])
     #scaling continuous variable
     scaler = pickle.load(open(scalar_file, "rb"))
     df_continuous_var_before_scaling = touchpoint_df[continuous_variable_columns]
     df_continuous_var_before_scaling = df_continuous_var_before_scaling.fillna(0)
     df_continuous_var_before_scaling.replace(
          to_replace=[""],
          value=0,
          inplace=True
          )
     df_continuous_var_scaled = scaler.fit_transform(df_continuous_var_before_scaling)
     df_continuous_var_scaled = pd.DataFrame(df_continuous_var_scaled)
     df_continuous_var_scaled.columns =  continuous_variable_columns
     df_continuous_var_scaled["id"] = zeemee_ids
     
     print("scaling for pred model complete")
     
     return df_continuous_var_scaled
