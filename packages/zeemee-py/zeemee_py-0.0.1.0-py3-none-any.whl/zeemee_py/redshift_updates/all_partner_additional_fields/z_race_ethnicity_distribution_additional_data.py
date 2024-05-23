def get_race_ethnicity_distribution_df(master_df, master_df_filtered, not_in_community_df):
    import pandas as pd
    import numpy as np
    
    list_enthnicity = [
        'in_comm_asian',
        'in_comm_american_indian_alaska_native',
        'in_comm_black_african_american',
        'in_comm_hispanic_any_race',
        'in_comm_native_hawaiian_other_pacific',
        'in_comm_white',
        'in_comm_nonresident_alien',
        'in_comm_two_or_more_races',
        'in_comm_prefer_not_to_respond',
        'in_comm_race_ethnicity_unknown',

        'in_comm_applied_asian',
        'in_comm_applied_american_indian_alaska_native',
        'in_comm_applied_black_african_american',
        'in_comm_applied_hispanic_any_race',
        'in_comm_applied_native_hawaiian_other_pacific',
        'in_comm_applied_white',
        'in_comm_applied_nonresident_alien',
        'in_comm_applied_two_or_more_races',
        'in_comm_applied_prefer_not_to_respond',
        'in_comm_applied_race_ethnicity_unknown',

        'in_comm_accepted_asian',
        'in_comm_accepted_american_indian_alaska_native',
        'in_comm_accepted_black_african_american',
        'in_comm_accepted_hispanic_any_race',
        'in_comm_accepted_native_hawaiian_other_pacific',
        'in_comm_accepted_white',
        'in_comm_accepted_nonresident_alien',
        'in_comm_accepted_two_or_more_races',
        'in_comm_accepted_prefer_not_to_respond',
        'in_comm_accepted_race_ethnicity_unknown',

        'in_comm_committed_asian',
        'in_comm_committed_american_indian_alaska_native',
        'in_comm_committed_black_african_american',
        'in_comm_committed_hispanic_any_race',
        'in_comm_committed_native_hawaiian_other_pacific',
        'in_comm_committed_white',
        'in_comm_committed_nonresident_alien',
        'in_comm_committed_two_or_more_races',
        'in_comm_committed_prefer_not_to_respond',
        'in_comm_committed_race_ethnicity_unknown',

        'in_comm_enrolled_asian',
        'in_comm_enrolled_american_indian_alaska_native',
        'in_comm_enrolled_black_african_american',
        'in_comm_enrolled_hispanic_any_race',
        'in_comm_enrolled_native_hawaiian_other_pacific',
        'in_comm_enrolled_white',
        'in_comm_enrolled_nonresident_alien',
        'in_comm_enrolled_two_or_more_races',
        'in_comm_enrolled_prefer_not_to_respond',
        'in_comm_enrolled_race_ethnicity_unknown'

    ]


    list_12_values = list()

    list_12_values.append(str(int(len(master_df_filtered[(master_df_filtered['ZM.Race.Ethnicity'] == 'Asian')])) ))
    list_12_values.append(str(
        int(len(master_df_filtered[(master_df_filtered['ZM.Race.Ethnicity'] == 'American Indian or Alaska Native')])) +
        int(len(master_df_filtered[(master_df_filtered['ZM.Race.Ethnicity'] == 'American Indian or Alaskan Native')]))
    ))
    list_12_values.append(str(int(len(master_df_filtered[(master_df_filtered['ZM.Race.Ethnicity'] == 'Black or African American')])) ))
    list_12_values.append(str(int(len(master_df_filtered[(master_df_filtered['ZM.Race.Ethnicity'] == 'Hispanic of any race')])) ))
    list_12_values.append(str(int(len(master_df_filtered[(master_df_filtered['ZM.Race.Ethnicity'] == 'Native Hawaiian or Other Pacific')])) ))
    list_12_values.append(str(int(len(master_df_filtered[(master_df_filtered['ZM.Race.Ethnicity'] == 'White')])) ))
    list_12_values.append(str(int(len(master_df_filtered[(master_df_filtered['ZM.Race.Ethnicity'] == 'Nonresident Alien')])) ))
    list_12_values.append(str(int(len(master_df_filtered[(master_df_filtered['ZM.Race.Ethnicity'] == 'Two or more races')])) ))
    list_12_values.append(str(int(len(master_df_filtered[(master_df_filtered['ZM.Race.Ethnicity'] == 'Prefer not to respond')])) ))
    list_12_values.append(str(int(len(master_df_filtered[(master_df_filtered['ZM.Race.Ethnicity'] == 'Race/Ethnicty Unknown')])) )) #in community already filtered


    master_df_filtered_applied = master_df_filtered[master_df_filtered['ZM.Applied'] == 1].reset_index(drop = True)

    list_12_values.append(str(int(len(master_df_filtered_applied[(master_df_filtered_applied['ZM.Race.Ethnicity'] == 'Asian')])) ))
    list_12_values.append(str(
        int(len(master_df_filtered_applied[(master_df_filtered_applied['ZM.Race.Ethnicity'] == 'American Indian or Alaska Native')])) + int(len(master_df_filtered_applied[(master_df_filtered_applied['ZM.Race.Ethnicity'] == 'American Indian or Alaskan Native')])) 
    ))
    list_12_values.append(str(int(len(master_df_filtered_applied[(master_df_filtered_applied['ZM.Race.Ethnicity'] == 'Black or African American')])) ))
    list_12_values.append(str(int(len(master_df_filtered_applied[(master_df_filtered_applied['ZM.Race.Ethnicity'] == 'Hispanic of any race')])) ))
    list_12_values.append(str(int(len(master_df_filtered_applied[(master_df_filtered_applied['ZM.Race.Ethnicity'] == 'Native Hawaiian or Other Pacific')])) ))
    list_12_values.append(str(int(len(master_df_filtered_applied[(master_df_filtered_applied['ZM.Race.Ethnicity'] == 'White')])) ))
    list_12_values.append(str(int(len(master_df_filtered_applied[(master_df_filtered_applied['ZM.Race.Ethnicity'] == 'Nonresident Alien')])) ))
    list_12_values.append(str(int(len(master_df_filtered_applied[(master_df_filtered_applied['ZM.Race.Ethnicity'] == 'Two or more races')])) ))
    list_12_values.append(str(int(len(master_df_filtered_applied[(master_df_filtered_applied['ZM.Race.Ethnicity'] == 'Prefer not to respond')])) ))
    list_12_values.append(str(int(len(master_df_filtered_applied[(master_df_filtered_applied['ZM.Race.Ethnicity'] == 'Race/Ethnicty Unknown')])) )) #in community already filtered


    master_df_filtered_accepted = master_df_filtered[master_df_filtered['ZM.Accepted'] == 1].reset_index(drop = True)

    list_12_values.append(str(int(len(master_df_filtered_accepted[(master_df_filtered_accepted['ZM.Race.Ethnicity'] == 'Asian')])) ))
    list_12_values.append(str(
        int(len(master_df_filtered_accepted[(master_df_filtered_accepted['ZM.Race.Ethnicity'] == 'American Indian or Alaska Native')])) + int(len(master_df_filtered_accepted[(master_df_filtered_accepted['ZM.Race.Ethnicity'] == 'American Indian or Alaskan Native')])) 
    ))
    list_12_values.append(str(int(len(master_df_filtered_accepted[(master_df_filtered_accepted['ZM.Race.Ethnicity'] == 'Black or African American')])) ))
    list_12_values.append(str(int(len(master_df_filtered_accepted[(master_df_filtered_accepted['ZM.Race.Ethnicity'] == 'Hispanic of any race')])) ))
    list_12_values.append(str(int(len(master_df_filtered_accepted[(master_df_filtered_accepted['ZM.Race.Ethnicity'] == 'Native Hawaiian or Other Pacific')])) ))
    list_12_values.append(str(int(len(master_df_filtered_accepted[(master_df_filtered_accepted['ZM.Race.Ethnicity'] == 'White')])) ))
    list_12_values.append(str(int(len(master_df_filtered_accepted[(master_df_filtered_accepted['ZM.Race.Ethnicity'] == 'Nonresident Alien')])) ))
    list_12_values.append(str(int(len(master_df_filtered_accepted[(master_df_filtered_accepted['ZM.Race.Ethnicity'] == 'Two or more races')])) ))
    list_12_values.append(str(int(len(master_df_filtered_accepted[(master_df_filtered_accepted['ZM.Race.Ethnicity'] == 'Prefer not to respond')])) ))
    list_12_values.append(str(int(len(master_df_filtered_accepted[(master_df_filtered_accepted['ZM.Race.Ethnicity'] == 'Race/Ethnicty Unknown')]))  ))#in community already filtered


    master_df_filtered_committed = master_df_filtered[master_df_filtered['ZM.Committed'] == 1].reset_index(drop = True)

    list_12_values.append(str(int(len(master_df_filtered_committed[(master_df_filtered_committed['ZM.Race.Ethnicity'] == 'Asian')])) ))
    list_12_values.append(str(
        int(len(master_df_filtered_committed[(master_df_filtered_committed['ZM.Race.Ethnicity'] == 'American Indian or Alaska Native')])) + int(len(master_df_filtered_committed[(master_df_filtered_committed['ZM.Race.Ethnicity'] == 'American Indian or Alaskan Native')]))
    ))
    list_12_values.append(str(int(len(master_df_filtered_committed[(master_df_filtered_committed['ZM.Race.Ethnicity'] == 'Black or African American')])) ))
    list_12_values.append(str(int(len(master_df_filtered_committed[(master_df_filtered_committed['ZM.Race.Ethnicity'] == 'Hispanic of any race')])) ))
    list_12_values.append(str(int(len(master_df_filtered_committed[(master_df_filtered_committed['ZM.Race.Ethnicity'] == 'Native Hawaiian or Other Pacific')])) ))
    list_12_values.append(str(int(len(master_df_filtered_committed[(master_df_filtered_committed['ZM.Race.Ethnicity'] == 'White')])) ))
    list_12_values.append(str(int(len(master_df_filtered_committed[(master_df_filtered_committed['ZM.Race.Ethnicity'] == 'Nonresident Alien')])) ))
    list_12_values.append(str(int(len(master_df_filtered_committed[(master_df_filtered_committed['ZM.Race.Ethnicity'] == 'Two or more races')])) ))
    list_12_values.append(str(int(len(master_df_filtered_committed[(master_df_filtered_committed['ZM.Race.Ethnicity'] == 'Prefer not to respond')])) ))
    list_12_values.append(str(int(len(master_df_filtered_committed[(master_df_filtered_committed['ZM.Race.Ethnicity'] == 'Race/Ethnicty Unknown')])) )) #in community already filtered


    master_df_filtered_enrolled = master_df_filtered[master_df_filtered['ZM.Enrolled'] == 1].reset_index(drop = True)

    list_12_values.append(str(int(len(master_df_filtered_enrolled[(master_df_filtered_enrolled['ZM.Race.Ethnicity'] == 'Asian')])) ))
    list_12_values.append(str(
        int(len(master_df_filtered_enrolled[(master_df_filtered_enrolled['ZM.Race.Ethnicity'] == 'American Indian or Alaska Native')])) + int(len(master_df_filtered_enrolled[(master_df_filtered_enrolled['ZM.Race.Ethnicity'] == 'American Indian or Alaskan Native')])) 
    ))
    list_12_values.append(str(int(len(master_df_filtered_enrolled[(master_df_filtered_enrolled['ZM.Race.Ethnicity'] == 'Black or African American')])) ))
    list_12_values.append(str(int(len(master_df_filtered_enrolled[(master_df_filtered_enrolled['ZM.Race.Ethnicity'] == 'Hispanic of any race')])) ))
    list_12_values.append(str(int(len(master_df_filtered_enrolled[(master_df_filtered_enrolled['ZM.Race.Ethnicity'] == 'Native Hawaiian or Other Pacific')])) ))
    list_12_values.append(str(int(len(master_df_filtered_enrolled[(master_df_filtered_enrolled['ZM.Race.Ethnicity'] == 'White')])) ))
    list_12_values.append(str(int(len(master_df_filtered_enrolled[(master_df_filtered_enrolled['ZM.Race.Ethnicity'] == 'Nonresident Alien')])) ))
    list_12_values.append(str(int(len(master_df_filtered_enrolled[(master_df_filtered_enrolled['ZM.Race.Ethnicity'] == 'Two or more races')])) ))
    list_12_values.append(str(int(len(master_df_filtered_enrolled[(master_df_filtered_enrolled['ZM.Race.Ethnicity'] == 'Prefer not to respond')])) ))
    list_12_values.append(str(int(len(master_df_filtered_enrolled[(master_df_filtered_enrolled['ZM.Race.Ethnicity'] == 'Race/Ethnicty Unknown')])) )) #in community already filtered

    function_df = pd.DataFrame()
    for i in range(len(list_enthnicity)):
         function_df[list_enthnicity[i]] = [list_12_values[i]]

    return function_df
