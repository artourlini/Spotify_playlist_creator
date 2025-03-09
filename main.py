from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "YOUR OWN ID"
CLIENT_SECRET = "YOUR OWN SECRET"
REDIRECT_URI = "YOUR OWN URI"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope="playlist-modify-private"))
user_id = sp.current_user()["id"]
print(user_id)

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
song_year = input("What year would you like to travel back to? Type it in this format YYYY-MM-DD: ")
response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{song_year}/", headers=header)
songs_webpage = response.text
soup = BeautifulSoup(songs_webpage, "html.parser")
song_tags = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_tags]
print(f"song names: {song_names}")
year = song_year.split("-")[0]
uri_list = []
for song in song_names:
    song_uri = sp.search(q=f"track: {song} year: {year}", type="track")["tracks"]["items"][0]["uri"]
    uri_list.append(song_uri)
print(f"uri list: {uri_list}")

new_playlist = sp.user_playlist_create(user = user_id,
                        name = f"{song_year} Billboard 100",
                        public = False,
                        description = "A playlist straight out from the Billboard 100")
print(new_playlist)
sp.playlist_add_items(playlist_id=new_playlist["id"], items=uri_list)




