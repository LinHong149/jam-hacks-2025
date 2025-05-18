import re
import os
import subprocess
import spotdl
from pathlib import Path
from pipelines.musicSeperation import musicSeperation
from pipelines.convertToSheet import convertToSheet

playlists = {}
def create():
    # get playlist name and url list
    playlistName = input("Playlist name: ")
    playlistUrls = []
    while True:
        url = input("Url (x to finish): ")
        if url == "x":
            break
        playlistUrls.append(url)
    
    
    # create not lofied playlist
    for u in playlistUrls:
        spotdl.createNotLofiedPlaylist(u, playlistName)

    playlists.update({playlistName: playlistUrls})
    
def update():
    playlistName = input("Playlist name: ")
    playlistUrls = playlists[playlistName]

    for u in playlistUrls:
        spotdl.createNotLofiedPlaylist(u, playlistName)

def edit():
    # project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # playlists_dir = os.path.join(project_root, f"playlists")
    playlists_dir = "/app/playlists"

    playlistName = input("Playlist to edit: ")
    newName = input("New playlist name: (x to skip): ")
    if newName != "x":
        os.rename(f"{playlists_dir}/{playlistName}", f"{playlists_dir}/{newName}")
        playlistName = newName

def convert():
    playlist = input("Playlists to convert: ") # /a

    # playlists_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "playlists") #/Users/linhong/Documents/Github/Lofied/playlists
    # notlofied_dir = os.path.join(playlists_dir, playlist ,"notlofied") #/Users/linhong/Documents/Github/Lofied/playlists/{playlistName}/notlofied
    # lofied_dir = os.path.join(playlists_dir, playlist, "lofied")
    playlists_dir = "/app/playlists" # Docker /app/playlists
    notlofied_dir = os.path.join(playlists_dir,f"{playlist}/notlofied") # /app/playlists/{playlist}/notlofied
    lofied_dir = os.path.join(playlists_dir,f"{playlist}/lofied")

    print ("Running convert")
    os.makedirs(lofied_dir, exist_ok=True) # Create /lofied if not exist
    

    for song in os.listdir(notlofied_dir):
        if song.endswith('.wav'):  # Only process WAV files
            input_path = os.path.join(notlofied_dir, song)
            output_path = os.path.join(lofied_dir, f"lofied_{song}")
            print(f"Processing {input_path}")
            print(f"Output to {output_path}")
            musicSeperation(input_path, output_path, song)

def sheetMusic():
    print("Generating sheet music")
    playlist = input("Playlist to convert: ")

    playlists_dir = "/app/playlists" # Docker /app/playlists
    notlofied_dir = os.path.join(playlists_dir, f"{playlist}/notlofied") # /app/playlists/{playlist}/lofied

    for song in os.listdir(notlofied_dir):
        if song.endswith('.wav'):
            print(f"Converting {song} to sheet music")
            print(song)
            convertToSheet(playlist, song)