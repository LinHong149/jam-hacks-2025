import os
import subprocess
import torchaudio

def createNotLofiedPlaylist(playlist_url, playlistName):
    project_root = "/app"
    playlist_dir = f"/app/playlists/{playlistName}/notlofied/"
    # venv_spotdl_path = os.path.join(project_root, "venv", "bin", "spotdl")
    spotdl_file_dir = f"/app/playlists/{playlistName}"

    # Ensure directories exist
    os.makedirs(playlist_dir, exist_ok=True)
    os.makedirs(spotdl_file_dir, exist_ok=True)

    print("made directories, getting song")

    subprocess.run([
        "spotdl",
        "sync",
        playlist_url,
        "--save-file", f"{spotdl_file_dir}/playlist.spotdl",
        "--output", f"{playlist_dir}/{{title}}.{{output-ext}}",
        "--format", "mp3"
    ], check=True)
    
    print("songs retrieved")



    for file in os.listdir(playlist_dir):
        if file.endswith(".mp3"):
            mp3Towav(file, playlist_dir)

    print("Converted all files to wav")

def mp3Towav(file, playlist_dir):
    # load paths
    mp3_path = os.path.join(playlist_dir, file)
    wav_path = os.path.join(playlist_dir, file.replace(".mp3", ".wav"))

    # convert to wav and remove mp3
    waveform, sample_rate = torchaudio.load(mp3_path)
    torchaudio.save(wav_path, waveform, sample_rate)
    os.remove(mp3_path)

