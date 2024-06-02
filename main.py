import configparser
import requests


#create parser object
parser = configparser.ConfigParser()
parser.read("credentials.conf")

#read credentials
client_id = parser.get("spotify_credentials" , "CLIENT_ID")
client_secret = parser.get("spotify_credentials" , "CLIENT_SECRET")

# Token endpoint URL
token_url = "https://accounts.spotify.com/api/token"

# POST request with client credentials and authorization code
auth_data = {
    "grant_type": "authorization_code",
    "code": auth_code,
    "redirect_uri": "YOUR_REDIRECT_URI",  # Replace with your redirect URI
    "client_id": client_id,
    "client_secret": client_secret,
}

response = requests.post(token_url, data=auth_data)