"""
Spotify Integration Package

This package provides a comprehensive interface to interact with the Spotify API,
offering various functionalities for music playback and control.

The package exports the following functions:
    - verify_credentials(): Validates Spotify API credentials
    - play_song(query): Searches and plays a specific song
    - search_tracks(query): Searches for tracks and displays results
    - pause_playback(): Pauses current playback
    - resume_playback(): Resumes paused playback

Dependencies:
    - spotipy: Spotify Web API wrapper
    - python-dotenv: Environment variable management

Environment Variables Required:
    - SPOTIFY_CLIENT_ID: Your Spotify API client ID
    - SPOTIFY_CLIENT_SECRET: Your Spotify API client secret
    - SPOTIFY_REDIRECT_URI: Your Spotify API redirect URI

Example Usage:
    >>> from Spotify import play_song, search_tracks
    >>> play_song("Shape of You")
    >>> search_tracks("Ed Sheeran")
"""

from .function import (
    verify_credentials,
    play_song,
    search_tracks,
    pause_playback,
    resume_playback
)

__all__ = [
    'verify_credentials',
    'play_song',
    'search_tracks',
    'pause_playback',
    'resume_playback'
]

__version__ = '1.0.0'