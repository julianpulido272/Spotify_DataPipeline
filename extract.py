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
returns a JSON format data, so we will convert it to pandas dataframe with only useful information

also contains methods to connect to api using user credentials
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


def extract_relevant_data(current_playback):
  """
  Since API returns a boatload of unecessary data, we will 
  extract the song name, artist, time played, and timestamp of songs
  """
  #create a list of size of our current playback
  size = len(current_playback["items"])

  #create lists of each data feature we want to collect
  song_names = []
  artist_names = []
  played_at_list = []
  album = []
  id = []

  #parse through the JSON data and collect our information. 
  for i in range (size):
    song_names.append(current_playback["items"][i]["track"]["name"])
    id.append(current_playback["items"][i]["track"]["id"])
    artist_names.append(current_playback["items"][i]["track"]["album"]["artists"][0]["name"])
    played_at_list.append(current_playback["items"][i]["played_at"])
    album.append(current_playback["items"][i]["track"]["album"]["name"])
  
  #get our song popularity
  popularity = extract_popularity(id)

        
  # Prepare a dictionary in order to turn it into a pandas dataframe below       
  song_dict = {
      "song_name" : song_names,
      "id" : id,
      "popularity" : popularity,
      "artist_name": artist_names,
      "album" : album,
      "played_at" : played_at_list
  }


  #create and return our df
  song_df = pd.DataFrame(song_dict, columns = ["song_name", "id" ,"popularity" ,"artist_name", "played_at", "album"])
  return song_df
  
def extract_popularity(song_id_list: list[str]) ->list[str]:
  """
  given a list of song id's, extract the genre for each
  """
  #create new client connection to spotify api. you dont actually need client auth since we are just looking up track
  sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id= client_id,
                                               client_secret= client_secret,
                                               redirect_uri= "https://www.google.com",
                                               scope= "user-read-recently-played"))
  
  #get data of tracks we have recently listened to 
  data = sp.tracks(song_id_list)
  popularity = []

  #get the popularity for each track
  for song in data["tracks"]:
    popularity.append(song["popularity"])
  return popularity
  



def extract_recent_songs():
  """
    creates a user connection to the spotify api and returns a json formatted data of recently played songs
  """
  #create a spotify API user using our credentials. assure that your URI is the same as in your dashboard
  sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id= client_id,
                                               client_secret= client_secret,
                                               redirect_uri= "https://www.google.com",
                                               scope= "user-read-recently-played"))
  

  #collect our JSON data 
  results = sp.current_user_recently_played(limit =2)
  return results

def get_df():
  """
  returns a cleaned dataframe of our recently played songs
  """
  json_data = extract_recent_songs()
  return (extract_relevant_data(json_data))



