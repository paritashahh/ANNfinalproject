import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials

# birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# results = spotify.artist_albums(birdy_uri, album_type='album')
# albums = results['items']
# while results['next']:
#     results = spotify.next(results)
#     albums.extend(results['items'])

# for album in albums:
#     print(album['name'])

# open mpd.slide0-000.json
# create a list of each playlist in the file

from cleantext import clean
import nltk 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import emoji

# randomly select 10 numbers from 1 to 1000
# these will be used to select 10 random data slices of playlist datasets to analyze
# provide with seed to replicate results
import random
random.seed(1)
random_numbers = random.sample(range(1, 1000), 10)
print(random_numbers)
# [138!!, 583!!, 868!!, 822!!, 783!!, 65!!, 262!!, 121!!, 508!!, 780!!]

def clean_text(text):
    text = clean(text, no_line_breaks=True, no_urls=True, no_punct=True, no_digits=True, replace_with_punct="", replace_with_digit="")
    text = emoji.replace_emoji(text, replace='')
    text = text.strip()
    text = text.replace('~', '')
    text = text.replace('_', '')
    text_tokens = word_tokenize(text)
    cleaned_tokens = [w for w in text_tokens if not w in stopwords.words('english')]
    text = (" ").join(cleaned_tokens)
    if len(text) < 3:
        return ""
    return text

song_dict = {}
# compile all playlists and songs from the 10 random data slices into a single dictionary
for i in range(1, 11):
    with open('slice' + str(i) + '.json') as f:
        data = json.load(f)
        for playlist in data['playlists']:
            playlist_name = clean_text(playlist['name'])
            for track in playlist['tracks']:
                track_uri = track['track_uri'][14:]
                if len(playlist_name) > 0:
                    if track_uri not in song_dict:
                        song_dict[track_uri] = [playlist_name]
                    else:
                        song_dict[track_uri].append(playlist_name)

# print(song_dict)

# convert dictionary into pandas dataframe, where each row is a song and each column is a playlist, with 1 indicating the song is in the playlist and 0 indicating it is not
import pandas as pd
df = pd.DataFrame.from_dict(song_dict, orient='index')

print(df)

# for each song, get the audio features from spotify

# for song in song_dict:
#     print(song)
#     print(spotify.audio_features(song))

