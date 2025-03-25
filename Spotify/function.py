"""
Spotify Integration Module

This module provides functionality to interact with the Spotify API, allowing users to:
- Play songs
- Search for tracks
- Control playback (pause/resume)
- Verify Spotify credentials

Dependencies:
    - spotipy: Spotify Web API wrapper
    - python-dotenv: Environment variable management
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

# Force reload of environment variables
load_dotenv(override=True)

# Spotify API credentials from environment variables
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# Initialize Spotify controller with required scopes
controller = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-modify-playback-state,user-read-playback-state,user-read-currently-playing,"
              "playlist-read-private,playlist-read-collaborative,playlist-modify-private,"
              "playlist-modify-public,user-follow-modify,user-follow-read,user-read-playback-position,"
              "user-top-read,user-read-recently-played,user-library-modify,user-library-read"
    )
)


def verify_credentials():
    """
    Verify that Spotify credentials are properly configured and valid.
    
    Raises:
        ValueError: If any required credentials are missing from .env file
        Exception: If there's an issue connecting to Spotify API
    
    Returns:
        None
    """
    if not all([CLIENT_ID, CLIENT_SECRET, REDIRECT_URI]):
        raise ValueError(
            "Missing Spotify credentials. Please check your .env file contains:\n"
            "SPOTIFY_CLIENT_ID\n"
            "SPOTIFY_CLIENT_SECRET\n"
            "SPOTIFY_REDIRECT_URI"
        )
    
    try:
        # Test the connection and token by fetching current user info
        controller.current_user()
    except Exception as e:
        print(e)
        raise


def play_song(query: str) -> dict:
    """
    Search for and play a song on Spotify.
    
    Args:
        query (str): Search query for the song
        
    Returns:
        dict: Response containing status and message
            {
                "type": "text",
                "data": "Song played successfully" or "Song not found."
            }
    """
    # Search for the song
    results = controller.search(q=query, limit=1, type='track')
    
    if results['tracks']['items']:
        # Get the URI of the first matching track
        track_uri = results['tracks']['items'][0]['uri']
        # Start playback
        controller.start_playback(uris=[track_uri])
        return {
            "type": "text",
            "data": "Song played successfully"
        }
    else:
        return {
            "type": "text",
            "data": "Song not found."
        }


def search_tracks(query: str) -> dict:
    """
    Search for tracks on Spotify and display results.
    
    Args:
        query (str): Search query for tracks
        
    Returns:
        dict: Response containing status and message
            {
                "type": "text",
                "data": "Search results for '{query}'" or "No results found."
            }
    """
    # Search for tracks
    results = controller.search(q=query, limit=5, type="track")
    
    if results['tracks']['items']:
        print(f"  Search Results for '{query}':")
        # Display each track with its name and artists
        for i, track in enumerate(results['tracks']['items'], start=1):
            print(f"{i}. {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}")
        return {
            "type": "text",
            "data": f"Search results for '{query}'"
        }
    else:
        print("  No results found.")
        return {
            "type": "text",
            "data": "No results found."
        }


def pause_playback() -> dict:
    """
    Pause the current Spotify playback.
    
    Returns:
        dict: Response containing status and message
            {
                "type": "text",
                "data": "Playback paused"
            }
    """
    controller.pause_playback()
    
    return {
        "type": "text",
        "data": "Playback paused"
    }


def resume_playback() -> dict:
    """
    Resume the paused Spotify playback.
    
    Returns:
        dict: Response containing status and message
            {
                "type": "text",
                "data": "Playback resumed"
            }
    """
    controller.start_playback()
    return {
        "type": "text",
        "data": "Playback resumed"
    }


if __name__ == "__main__":
    try:
        verify_credentials()
        play_song("kandaraja pandharichacha", "Sudhir Phadke")
    except Exception as e:
        print(f"\nError: {str(e)}")
    