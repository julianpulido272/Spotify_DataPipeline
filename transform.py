import extract
import pandas as pd
"""
transfrom.py transforms the extracted data into clean and insightful model to be analyzed.
-checks for empty df or null values
-deduplicates values
"""

def remove_duplicates(df):
  """
  removes duplicates if the song song played at the same time
  """

  #check if each time stamp is unique
  if(pd.Series(df["played_at"]).is_unique):
    return df
  #if not we remove one of them
  else:
    return df.drop_duplicates(subset = ['played_at'])



if __name__ == "__main__":
  #df = extract.get_df()
  #remove_duplicates(df)
  #print(df)
  df = pd.DataFrame({
    'brand': ['Yum Yum', 'Yum Yum', 'Indomie', 'Indomie', 'Indomie'],
    'played_at': ['cup', 'cup', 'cup', 'pack', 'pack'],
    'rating': [4, 4, 3.5, 15, 5]
  })
  print(df)
  df =remove_duplicates(df)
  #df = df.drop_duplicates(subset = ['played_at'])
  print(df)
  


