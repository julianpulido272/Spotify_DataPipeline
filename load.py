import extract
import transform
import sqlalchemy
import pandas as pd 
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3
import os


if __name__ == "__main__":
  #import songs from transform.py
  df = transform.transform()
  wd = os.getcwd()

  #Loading into database
  conn = sqlite3.connect('music.db')

  #create SQL table
  sql_query1 = """
      CREATE TABLE IF NOT EXISTS my_played_tracks(
        song_name VARCHAR(200),
        id VARCHAR(200),
        popularity SMALLINT(255),
        artist_name VARCHAR(200),
        played_at VARCHAR(200),
        album VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
    )
  """

  #execute sql query
  conn.execute(sql_query1)

  #add our df to the table in the database
  try:
    df.to_sql("my_played_tracks", conn, index = False, if_exists='append')
  except:
    print("data already exists in database")

  conn.close()
  print("Closed database successfully")
