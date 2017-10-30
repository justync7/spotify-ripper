import spotipy
import spotipy.util as util
import spotipy.client
import os
from spotipy.oauth2 import SpotifyClientCredentials

redirect_uri = 'http://www.purple.com'
client_id = ''
client_secret = ''
scope = 'playlist-modify-public playlist-modify-private playlist-read-collaborative'

# client_id = os.environ["SPOTIPY_CLIENT_ID"] 
# client_secret = os.environ["SPOTIPY_CLIENT_SECRET"]
# redirect_uri = os.environ["SPOTIPY_REDIRECT_URI"]

token = None
spotInstance = None


def remove_all_from_playlist(username, playlistURI):
    tracks = get_playlist_tracks(username, playlistURI)

    track_ids = []
    for i, item in enumerate(tracks):
        track = item['track']
        tid = track['id']
        track_ids.append(tid)
    results = spotInstance.user_playlist_remove_all_occurrences_of_tracks(username, rPlaylistID, track_ids)


def get_playlist_tracks(username, playlistURI):
    global rPlaylistID
    p1, p2, p3, p4, rPlaylistID = playlistURI.split(':', 5)

    global token 
    token = util.prompt_for_user_token(username, scope)

    global spotInstance 
    spotInstance = spotipy.Spotify(auth=token)
    spotInstance.trace = False

    print('Getting Results')
    results = spotInstance.user_playlist(p3, rPlaylistID, fields="tracks,next")

    tracks = results['tracks']
    items = tracks['items']
    
    while tracks['next']:
        tracks = spotInstance.next(tracks)
        items = items + tracks['items']
    
    print("Got " + str(len(items)) + " Tracks from " + playlistURI)
    tracks['items'] = items
    
    return tracks
