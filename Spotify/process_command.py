import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

controller = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI,    scope="user-modify-playback-state,user-read-playback-state,user-read-currently-playing,playlist-read-private,playlist-read-collaborative,playlist-modify-private,playlist-modify-public,user-follow-modify,user-follow-read,user-read-playback-position,user-top-read,user-read-recently-played,user-library-modify,user-library-read"
))

def process_command(command):
    try:
        action = command.action
    except:
        print("failed")

    if action == "play":
        if command.playType == "song" and command.song:
            query = f"{command.song} {command.artist}"
            results = controller.search(q=query, limit=1, type='track')
            if results['tracks']['items']:
                track_uri = results['tracks']['items'][0]['uri']
                controller.start_playback(uris=[track_uri])
                print(f"  Playing: {command.song} by {command.artist}")
            else:
                print("  Song not found.")

        elif command.playType in ["playlist", "my playlist"] and command.playlist:
            results = controller.search(q=command.playlist, limit=1, type='playlist')
            if results['playlists']['items']:
                playlist_uri = results['playlists']['items'][0]['uri']
                controller.start_playback(context_uri=playlist_uri)
                print(f"  Playing Playlist: {command.playlist}")
            else:
                print("  Playlist not found.")

        elif command.playType == "album" and command.album:
            results = controller.search(q=command.album, limit=1, type='album')
            if results['albums']['items']:
                album_uri = results['albums']['items'][0]['uri']
                controller.start_playback(context_uri=album_uri)
                print(f"  Playing Album: {command.album}")
            else:
                print("  Album not found.")

        else:
            controller.start_playback()
            print("  Resuming playback")

    elif command.action == "pause":
        controller.pause_playback()
        print("  Playback paused")

    elif command.action == "stop":
        controller.pause_playback()
        print("  Playback stopped")

    elif command.action == "next":
        controller.next_track()
        print("  Skipped to next track")

    elif command.action == "previous":
        controller.previous_track()
        print("  Went to previous track")

    elif command.action == "search":
        query = command.search
        results = controller.search(q=query, limit=5, type="track")
        if results['tracks']['items']:
            print(f"  Search Results for '{query}':")
            for i, track in enumerate(results['tracks']['items'], start=1):
                print(f"{i}. {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}")
        else:
            print("  No results found.")

    elif command.action == "volume":
        volume_action = command.volumeAction
        current_volume = controller.current_playback()['device']['volume_percent']
        
        if volume_action == "set" and command.volumeLevel is not None:
            volume = max(0, min(100, command.volumeLevel))
            controller.volume(volume)
            print(f"  Volume set to {volume}%")
        
        elif volume_action == "increase":
            new_volume = min(100, current_volume + 10)
            controller.volume(new_volume)
            print(f"  Volume increased to {new_volume}%")

        elif volume_action == "decrease":
            new_volume = max(0, current_volume - 10)
            controller.volume(new_volume)
            print(f"  Volume decreased to {new_volume}%")

        elif volume_action == "mute":
            controller.volume(0)
            print("  Volume muted")

    elif command.action == "shuffle":
        controller.shuffle(command.shuffle)
        print("  Shuffle toggled")

    elif command.action == "repeat":
        repeat_mode = command.repeatMode
        controller.repeat(repeat_mode)
        print(f"  Repeat mode set to {repeat_mode}")

    else:
        print("Unknown command")
