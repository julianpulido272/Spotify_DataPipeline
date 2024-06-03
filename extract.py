import configparser
import json
import pandas as pd
import requests 
import base64
from datetime import datetime
import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

"""
extract.py is desgined to extract recently played songs from spotify. Naturally the spotify api
returns a JSON format data, so we will convert it to CSV for pandas 
"""

#create parser object
parser = configparser.ConfigParser()
parser.read("credentials.conf")

#read credentials
client_id = parser.get("spotify_credentials" , "CLIENT_ID")
client_secret = parser.get("spotify_credentials" , "CLIENT_SECRET")


def get_token():
  """
  Get a token based on credentials 
  """

  #combine our client id and password
  authString = client_id + ":" + client_secret

  #encode to base64
  auth_bytes = authString.encode("utf-8")
  auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

  #url we will be posting our requests to 
  url = "https://accounts.spotify.com/api/token"


  headers = {
    "Authorization" : "Basic " + auth_base64,
    "Content-Type" : "application/x-www-form-urlencoded"
  }

  data = {"grant_type": "client_credentials"}

  #post our request
  result = requests.post(url, headers=headers, data=data)

  json_result = json.loads(result.content)
  token = json_result["access_token"]
  return token

def get_auth_header(token):
  """
  returns a header containing our token for requests 
  """
  return {"Authorization": f"Bearer {token}"}

def get_recently_played():
  """
  retrives a json list of recently played tracks from yesterday given a user header credentials
  """
  today = datetime.datetime.now()
  yesterday = today - datetime.timedelta(days=2)
  yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

  #r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp), headers = getAuthHeader(header))
  #endpoint = "https://api.spotify.com/v1/me/players/recently-played"
  #r = requests.get(endpoint, headers = getAuthHeader(header))
  current_playbacks = sp.current_user_recently_played(after = yesterday_unix_timestamp)
  return current_playbacks

def extract_relevant_data(current_playback):
  """
  Since API returns a boatload of unecessary data, we will 
  extract the song name, artist, time played, and timestamp of songs
  """
  #create a list of size of our current playback
  size = len(current_playback)

  song_names = []
  artist_names = []
  played_at_list = []
  album = []

  for i in range (size):
    song_names.append(current_playback[i]["track"]["name"])
    artist_names.append(current_playback[i]["track"]["album"]["artists"][0]["name"])
    played_at_list.append(current_playback[i]["played_at"])
    album.append(current_playback[i]["track"]["album"]["name"])
        
    # Prepare a dictionary in order to turn it into a pandas dataframe below       
  song_dict = {
      "song_name" : song_names,
      "artist_name": artist_names,
      "album" : album,
      "played_at" : played_at_list
  }
  song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at", "album"])
  return song_df
      



sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id= client_id,
                                               client_secret= client_secret,
                                               redirect_uri= "https://www.google.com",
                                               scope= "user-read-recently-played"))
  
results = sp.current_user_recently_played(limit =2)
df = extract_relevant_data(results["items"])
print(df)