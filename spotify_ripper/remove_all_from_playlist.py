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
client_credentials_manager = None
spotInstanceClient = None


def remove_all_from_playlist(username, playlistURI):
    tracks = get_playlist_tracks(username, playlistURI)

    track_ids = []
    for i, item in enumerate(tracks['items']):
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
    
    global client_credentials_manager
    client_credentials_manager = SpotifyClientCredentials()
    
    global spotInstanceClient
    spotInstanceClient = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    print('Getting Results')
    if p3 == username:
        results = spotInstance.user_playlist(p3, rPlaylistID, fields="tracks,next")
    else:
        results = spotInstanceClient.user_playlist(p3, rPlaylistID, fields="tracks,next")

    tracks = results['tracks']
    
    while tracks['next']:
        if p3 == username:
          tracks = spotInstance.next(tracks)
        else:
          tracks = spotInstanceClient.next(tracks)

    return tracks
