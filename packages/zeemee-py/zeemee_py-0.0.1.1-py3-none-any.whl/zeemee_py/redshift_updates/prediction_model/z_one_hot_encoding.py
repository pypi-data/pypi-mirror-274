def one_hot_encoding(touchpoint_df):
     import importlib
     import pickle
     import pandas as pd
     import numpy as np
     import os
     
     from zeemee_py.helper_functions import get_data_folder_path
     importlib.reload(get_data_folder_path)
     data_folder_path = get_data_folder_path.get_data_folder_path()
     
     onehot_encoder_going_filename = os.path.join(data_folder_path,"prediction_model/RF_model_2ndshortlist_ohe_going.pickle")
     onehot_encoder_going = pickle.load(open(onehot_encoder_going_filename, 'rb'))
     print(onehot_encoder_going)
     one_hot_encoder_tf_filename = os.path.join(data_folder_path,"prediction_model/RF_model_2ndshortlist_ohe_tf.pickle")
     one_hot_encoder_tf = pickle.load(open(one_hot_encoder_tf_filename, 'rb'))
     
     one_hot_df = pd.DataFrame()
     one_hot_df["id"] = touchpoint_df["id"]
     
     touchpoint_df.replace(
        to_replace=[""],
        value= np.NaN,
        inplace=True )
     
     #onehot_encoder_going = OneHotEncoder(sparse=False, categories="auto", drop = "first", handle_unknown = "error")
     encoded_going = onehot_encoder_going.transform(
          touchpoint_df["going"].fillna("undecided").values.reshape(-1,1)
          )
     going = pd.DataFrame(encoded_going, columns = ["Going" + i[2:] for i in onehot_encoder_going.get_feature_names()])
     going = going[["going_going", "going_notgoing"]]
     one_hot_df = pd.concat([one_hot_df, going], axis = 1)
     
     #one_hot_encoder_tf = OneHotEncoder(sparse=False, categories="auto", drop = "first", handle_unknown = "error")
     encoded_public_profile_enabled = one_hot_encoder_tf.transform(
          touchpoint_df["public_profile_enabled"].fillna("").values.reshape(-1,1)
          )
     public_profile_enabled = pd.DataFrame(
          encoded_public_profile_enabled, 
          columns = ["public_profile_enabled" + i[2:] for i in one_hot_encoder_tf.get_feature_names()]
          )
     one_hot_df = pd.concat([one_hot_df, public_profile_enabled], axis = 1)
     
     encoded_interested = one_hot_encoder_tf.transform(
          touchpoint_df["interested"].fillna("f").values.reshape(-1,1)
          )
     interested = pd.DataFrame(
          encoded_interested, 
          columns = ["interested" + i[2:] for i in one_hot_encoder_tf.get_feature_names()]
          )
     one_hot_df = pd.concat([one_hot_df, interested], axis = 1)
     
     encoded_created_by_csv = one_hot_encoder_tf.transform(
          touchpoint_df["created_by_csv"].fillna("f").values.reshape(-1,1)
          )
     created_by_csv = pd.DataFrame(
          encoded_created_by_csv, 
          columns = ["created_by_csv" + i[2:] for i in one_hot_encoder_tf.get_feature_names()]
          )
     one_hot_df = pd.concat([one_hot_df, created_by_csv], axis = 1)
     
     
     encoded_transfer_status = one_hot_encoder_tf.transform(
          touchpoint_df["uos_transfer_status"].fillna("f").values.reshape(-1,1)
          )
     transfer_status = pd.DataFrame(
          encoded_transfer_status, 
          columns = ["uos_transfer_status" + i[2:] for i in one_hot_encoder_tf.get_feature_names()]
          )
     one_hot_df = pd.concat([one_hot_df, transfer_status], axis = 1)
     
     encoded_rm_quiz = one_hot_encoder_tf.transform(
          touchpoint_df["roommate_match_quiz"].fillna("f").values.reshape(-1,1)
          )
     roommate_match_quiz = pd.DataFrame(
          encoded_transfer_status, 
          columns = ["roommate_match_quiz" + i[2:] for i in one_hot_encoder_tf.get_feature_names()]
          )
     one_hot_df = pd.concat([one_hot_df, roommate_match_quiz], axis = 1)
     
     print("one hot encoding for pred model complete")
     
     return one_hot_df
