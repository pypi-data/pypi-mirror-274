
def create_fname_lname_columns(touchpoint_df):
     
     username_list = list(touchpoint_df['user_name'])
     first_name = list()
     last_name = list()
     
     for i in range(len(username_list)):
          full_name = str(username_list[i])
          full_name = full_name.strip()
          full_name_list = full_name.split(" ")
          
          if len(full_name_list) == 2:
               first_name.append(full_name_list[0])
               last_name.append(full_name_list[1])
          
          elif len(full_name_list) >2:
               first_name.append(full_name_list[0])
               l_name = ''
               for j in range(1,len(full_name_list)):
                    l_name = l_name + ' '+ full_name_list[j]
               l_name = l_name.strip()
               last_name.append(l_name)
          
          else:
            first_name.append(full_name_list[0])
            last_name.append("")

     touchpoint_df['first_name'] = first_name
     touchpoint_df['last_name'] = last_name

     return touchpoint_df
