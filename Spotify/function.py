import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

# Force reload of environment variables
load_dotenv(override=True)

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")


controller = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI,    scope="user-modify-playback-state,user-read-playback-state,user-read-currently-playing,playlist-read-private,playlist-read-collaborative,playlist-modify-private,playlist-modify-public,user-follow-modify,user-follow-read,user-read-playback-position,user-top-read,user-read-recently-played,user-library-modify,user-library-read"))

def verify_credentials():
    """Verify Spotify credentials are properly configured"""
    if not all([CLIENT_ID, CLIENT_SECRET, REDIRECT_URI]):
        raise ValueError(
            "Missing Spotify credentials. Please check your .env file contains:\n"
            "SPOTIFY_CLIENT_ID\n"
            "SPOTIFY_CLIENT_SECRET\n"
            "SPOTIFY_REDIRECT_URI"
        )
    
    try:
        # Test the connection and token
        controller.current_user()
    except Exception as e:
        print(e)
        raise


def play_song(query: str) -> None:
    
    
    results = controller.search(q=query, limit=1, type='track')
    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']
        controller.start_playback(uris=[track_uri])
        return{
            "type": "text",
            "data": "Song played successfully"
        }
    else:
        return{
            "type": "text",
            "data": "Song not found."
        }



def search_tracks(query: str) -> None:
    
    results = controller.search(q=query, limit=5, type="track")
    if results['tracks']['items']:
        print(f"  Search Results for '{query}':")
        for i, track in enumerate(results['tracks']['items'], start=1):
            print(f"{i}. {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}")
        return{
            "type": "text",
            "data": "Search results for '{query}'"
        }
    else:
        print("  No results found.")
        return{
            "type": "text",
            "data": "No results found."
        }
def pause_playback() -> None:
    
    controller.pause_playback()
    
    return{
        "type": "text",
        "data": "Playback paused"
    }


def resume_playback() -> None:
    
    controller.start_playback()
    return{
        "type": "text",
        "data": "Playback resumed"
    }

if __name__ == "__main__":
    try:
        verify_credentials()
        play_song("kandaraja pandharichacha", "Sudhir Phadke")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
    