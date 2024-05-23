
def create_ff_and_rmmatch_flag_column(touchpoint_df):
     import numpy as np
     """
     sum the four columns of roommmate match and friend finder (with filter and without filter on ios and
     android), if >0, write the text, else leave it blank
     """
     
     touchpoint_df['friend_finder'] = np.where(touchpoint_df[
          ['ff_searched_ios',
          'ff_searched_android']
          ].sum(axis=1)> 0,
          'Friend Finder Used', '')
     
     touchpoint_df['roommate_finder'] = np.where(touchpoint_df[
          ['roommate_searched_ios',
          'roommate_searched_android']
          ].sum(axis=1)> 0,
          'Roommate Finder used', '')
          
     return touchpoint_df
