def calculate_values(master_df):
     import pandas as pd
     import importlib
     
     [
          "zm_race_ethnicity_asian",
          "zm_race_ethnicity_american_indian_or_alaska_native",
          "zm_race_ethnicity_black_or_african_american",
          "zm_race_ethnicity_hispanic_of_any_race",
          "zm_race_ethnicity_native_hawaiian_or_other_pacific",
          "zm_race_ethnicity_white",
          "zm_race_ethnicity_nonresident_alien",
          "zm_race_ethnicity_prefer_not_to_respond"
          "zm_race_ethnicity_race_ethnicity_unknown",
          "zm_race_ethnicity_two_or_more_races"
          ]
          
     function_dataframe = pd.DataFrame()
     
     zm_race_ethnicity_asian = len(master_df[
          (master_df['ZM.Race.Ethnicity'] == 'Asian') &
          (master_df['ZM.Inquired'] == 1)
          ])
     function_dataframe['zm_race_ethnicity_asian'] = [zm_race_ethnicity_asian]
     
     zm_race_ethnicity_american_indian_or_alaska_native = len(master_df[
          (master_df['ZM.Race.Ethnicity'] == 'American Indian or Alaskan Native') &
          (master_df['ZM.Inquired'] == 1)
          ])
     function_dataframe['zm_race_ethnicity_american_indian_or_alaska_native'] = [zm_race_ethnicity_american_indian_or_alaska_native]
     
     zm_race_ethnicity_black_or_african_american = len(master_df[
          (master_df['ZM.Race.Ethnicity'] =='Black or African American') &
          (master_df['ZM.Inquired'] == 1)
          ])
     function_dataframe['zm_race_ethnicity_black_or_african_american'] = [zm_race_ethnicity_black_or_african_american]
     
     zm_race_ethnicity_hispanic_of_any_race = len(master_df[
          (master_df['ZM.Race.Ethnicity'] == 'Hispanic of any race') &
          (master_df['ZM.Inquired'] == 1)
          ])
     function_dataframe['zm_race_ethnicity_hispanic_of_any_race'] = [zm_race_ethnicity_hispanic_of_any_race]
     
     zm_race_ethnicity_native_hawaiian_or_other_pacific = len(master_df[
          (master_df['ZM.Race.Ethnicity'] == 'Native Hawaiian or Other Pacific') &
          (master_df['ZM.Inquired'] == 1)
          ])
     function_dataframe['zm_race_ethnicity_native_hawaiian_or_other_pacific'] = [zm_race_ethnicity_native_hawaiian_or_other_pacific]
     
     zm_race_ethnicity_white = len(master_df[
          (master_df['ZM.Race.Ethnicity'] == 'White') &
          (master_df['ZM.Inquired'] == 1)
          ])
     function_dataframe['zm_race_ethnicity_white'] = [zm_race_ethnicity_white]
     
     zm_race_ethnicity_nonresident_alien = len(master_df[
          (master_df['ZM.Race.Ethnicity'] == 'Nonresident Alien') &
          (master_df['ZM.Inquired'] == 1)
          ])
     function_dataframe['zm_race_ethnicity_nonresident_alien'] = [zm_race_ethnicity_nonresident_alien]
     
     zm_race_ethnicity_prefer_not_to_respond = len(master_df[
          (master_df['ZM.Race.Ethnicity'] == 'Prefer not to respond') &
          (master_df['ZM.Inquired'] == 1)
          ])
     function_dataframe['zm_race_ethnicity_prefer_not_to_respond'] = [zm_race_ethnicity_prefer_not_to_respond]
     
     zm_race_ethnicity_race_ethnicity_unknown = len(master_df[
          (master_df['ZM.Race.Ethnicity'] == 'Race/Ethnicty Unknown') &
          (master_df['ZM.Inquired'] == 1)
          ])
     function_dataframe['zm_race_ethnicity_race_ethnicity_unknown'] = [zm_race_ethnicity_race_ethnicity_unknown]
     
     zm_race_ethnicity_two_or_more_races = len(master_df[
          (master_df['ZM.Race.Ethnicity'] == 'Two or more races') &
          (master_df['ZM.Inquired'] == 1)
          ])
     function_dataframe['zm_race_ethnicity_two_or_more_races'] = [zm_race_ethnicity_two_or_more_races]
     
     return function_dataframe
    
