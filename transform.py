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
  
def remove_missing_rows(df: pd.DataFrame)-> pd.DataFrame:
  """
  remove rows that have missing values in id or time they are played at
  """
  return df.dropna(subset=['id', 'played_at'])

def transform() -> pd.DataFrame:
  """
  gets data extraction from extract.py and combines all data quality checks into one singular method
  removes duplicates and removes missings rows
  note: in future may add more to improve data analysis
  """
  df = extract.get_df()
  df = remove_duplicates(df)
  df = remove_missing_rows(df)
  return df




if __name__ == "__main__":
  df = transform()
  print(df)

  


