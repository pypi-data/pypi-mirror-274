
def create_information_column(touchpoint_df, organization_id):
     
     import pandas as pd
     touchpoint_df["date_of_report"] = pd.Timestamp.today().strftime('%Y-%m-%d')
     touchpoint_df["organization_id"] = [organization_id] * len(touchpoint_df)
     
     return touchpoint_df
