def modify_id_number_values(touchpoint_df, organization_id, org_additional_df):
     
     import numpy as np
     org_additional_df["slate_id_number"] = org_additional_df["slate_id_number"].str.strip()
     
     if org_additional_df.loc[0, "slate_id_number"] == "PAD Zeros":
          #function to add leading zeros to college id for easier matching with their ids in crm/ databse
          #we do this by converting the id to a string
          switcher = {
          1: "00000000",
          2: "0000000",
          3: "000000",
          4: "00000",
          5: "0000",
          6: "000",
          7: "00",
          8: "0"    
          }
          
          cleaned_ids = list()
          id_number_df = pd.DataFrame(
               data = {
                    "ID.Number": touchpoint_df["ID.Number"]
                    }
                    )
          id_number_df["ID.Number"] = id_number_df["ID.Number"].astype(str)
          id_number_df["ID.Number"] = id_number_df["ID.Number"].str.split(".").str[0]
          id_number_df["ID.Number"] = id_number_df["ID.Number"].replace(r"^\s*$", np.nan, regex=True)
          id_number_df["ID.Number"] = id_number_df["ID.Number"].str.replace("@","", regex = False)
          id_number_df["ID.Number"] = id_number_df["ID.Number"].fillna(0)
          
          for i in range(len(id_number_df)):   
               id_number_i = id_number_df["ID.Number"][i]
               if len(str(int(id_number_i)))>0:
                    id_number_i_string = str(int(a["ID.Number"][i]))
                    if len(id_number_i_string) <9:
                         id_number_i_string = switcher[len(id_number_i_string)] + id_number_i_string
                         cleaned_ids.append(id_number_i_string)
                    else: 
                         cleaned_ids.append(id_number_i_string)
               else:
                    cleaned_ids.append("")
                    
          touchpoint_df["ID.Number"] = cleaned_ids
          
     return touchpoint_df
