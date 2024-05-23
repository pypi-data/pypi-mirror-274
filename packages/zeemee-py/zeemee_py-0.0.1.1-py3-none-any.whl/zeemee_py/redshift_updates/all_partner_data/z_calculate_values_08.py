def calculate_values(master_df):
     import pandas as pd
     import importlib

     [
        'stealth_appsnon_community_inquired',
        'stealth_appsnon_community_applied',
        'zm_cv_flag_campus_visit',
        "zm_first_gen_first_generation",
        "zm_text_opt_out_text_opt_out",
        "zm_email_opt_out_email_opt_out"
     ]
     
     function_dataframe = pd.DataFrame()

     stealth_appsnon_community_inquired = len(master_df[
          (master_df['ZM.Community'] == 'Not in Community') &
          (master_df['Student.Type'] == 'First time') &
          (master_df['ZM.Inquired'] == 1) &
          (master_df['ZM.Stealth.App'] == 'Stealth')]
          )
     function_dataframe["stealth_appsnon_community_inquired"] = [stealth_appsnon_community_inquired]
     
     stealth_appsnon_community_applied = len(master_df[
          (master_df['ZM.Community'] == 'Not in Community') &
          (master_df['Student.Type'] == 'First time') &
          (master_df['ZM.Applied'] == 1) &
          (master_df['ZM.Stealth.App'] == 'Stealth')]
          )
     function_dataframe["stealth_appsnon_community_applied"] = [stealth_appsnon_community_applied]
     
     
     zm_cv_flag_campus_visit = len(master_df[
          (master_df['ZM.CV.Flag'] == 'Campus Visit') &
          (master_df['ZM.Inquired'] == 1)
          ])
     function_dataframe["zm_cv_flag_campus_visit"] = [zm_cv_flag_campus_visit]
     
     zm_first_gen_first_generation = len(master_df[
          (master_df['ZM.First.Gen'] == 'First Generation') &
          (master_df['ZM.Inquired'] == 1)
          ])
     function_dataframe["zm_first_gen_first_generation"] = [zm_first_gen_first_generation]
     
     zm_text_opt_out_text_opt_out = len(master_df[
          (master_df['ZM.Text.Opt.Out'] == 'Text Opt Out') &
          (master_df['ZM.Inquired'] == 1)
          ])
     function_dataframe["zm_text_opt_out_text_opt_out"] = [zm_text_opt_out_text_opt_out]
     
     zm_email_opt_out_email_opt_out = len(master_df[
          (master_df['ZM.Email.Opt.Out'] == 'Email Opt Out') &
          (master_df['ZM.Inquired'] == 1)
          ])
     function_dataframe["zm_email_opt_out_email_opt_out"] = [zm_email_opt_out_email_opt_out]
     
     return function_dataframe
