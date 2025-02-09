import os
from . import prompt
from openai import OpenAI
from enum import Enum
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv
from . process_command import process_command
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

class Actions(str, Enum):
    play = "play" 
    pause = "pasues"
    stop = "stops"
    volume = "volume"
    next = "next"
    previous = "previous"
    search = "search"
    shuffle = "shuffle"
    repeat = "repeat"

class Repeat(str, Enum):
    off = "off"
    one = "one"
    all = "all"

class Volume(str, Enum):
    set = "set"
    mute = "mute"
    increase = "increases"
    decrease = "decreases"

class PlayType(str, Enum):
    song = "song"
    my_playlist = "my playlist"
    playist = "playlist"
    album = "album"

class SpotifyActions(BaseModel):
    action: Actions
    playType: Optional[PlayType] = None
    song: Optional[str] = None
    artist: Optional[str] = None
    playlist: Optional[str] = None
    album: Optional[str] = None
    next: Optional[bool] = None
    previous: Optional[bool] = None
    search: Optional[str] = None
    volumeAction: Optional[Volume] = None
    volumeLevel: Optional[int] = None
    repeatMode: Optional[Repeat] = None
    shuffle: Optional[bool] = None

def process_input(command):
    """
    Process a command into an SpotifyActions object.

    Args:
        command (str): The command to process.

    Returns:
        SpotifyActions: The parsed SpotifyActions object.
    """
    response = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": f"{prompt.prompt_for_system}"},
        {"role": "user", "content": f"{prompt.prompt_for_user}: {command}"}
    ],
    response_format=SpotifyActions,
    )
    
    Actions=response.choices[0].message.parsed
    print(Actions)
    process_command(Actions)
    return {"type":"string","data":"Doing Spotify Action"}

if __name__ == "__main__":
    print(process_input("play song  Dil Ki Tapish by Rahul Deshpande "))