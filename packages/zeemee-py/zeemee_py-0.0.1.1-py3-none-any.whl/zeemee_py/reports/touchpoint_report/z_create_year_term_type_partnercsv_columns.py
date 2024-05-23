
def create_year_term_type_partnercsv_columns(touchpoint_df):
     
     adjusted_entry_term_partner_csv = list()
     adjusted_entry_year_partner_csv = list()
     adjusted_student_type_partner_csv = list()
     
     touchpoint_df["uos_start_term"] = touchpoint_df["uos_start_term"].fillna("")
     touchpoint_df["uos_cohort_year"] = touchpoint_df["uos_cohort_year"].fillna("")
     touchpoint_df["uos_transfer_status"] = touchpoint_df["uos_transfer_status"].fillna("")
     
     for i in range(len(touchpoint_df)):
          if touchpoint_df['in_csv_file'][i] == '':
               adjusted_entry_term_partner_csv.append('')
               adjusted_entry_year_partner_csv.append('')
               adjusted_student_type_partner_csv.append('')
          else:
               adjusted_entry_term_partner_csv.append(touchpoint_df["uos_start_term"][i])
               adjusted_entry_year_partner_csv.append(touchpoint_df["uos_cohort_year"][i])
               adjusted_student_type_partner_csv.append(touchpoint_df["uos_transfer_status"][i])
               
     touchpoint_df["entry_term_partnercsv"] = adjusted_entry_term_partner_csv
     touchpoint_df["entry_year_partnercsv"] = adjusted_entry_year_partner_csv
     touchpoint_df["student_type_partnercsv"] = adjusted_student_type_partner_csv
     
     return touchpoint_df
