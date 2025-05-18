from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH
import torchaudio
import pretty_midi
import os
import torch
from pipelines.musicSeperation import musicSeperationForSheet

def convertToSheet(playlist, song):
    # Create necessary directories
    output_dir = f"/app/playlists/{playlist}/sheets"
    os.makedirs(output_dir, exist_ok=True)
    
    wav_dir = f"/app/playlists/{playlist}/notlofied"
    os.makedirs(wav_dir, exist_ok=True)
    
    wav_path = os.path.join(wav_dir, song)

    # Run music separation and get audio directly
    v_audio, o_audio, sr = musicSeperationForSheet(wav_path, output_dir, song)

    # Ensure both tensors have the same shape
    if v_audio.shape != o_audio.shape:
        # If shapes don't match, pad the shorter one
        max_length = max(v_audio.shape[1], o_audio.shape[1])
        if v_audio.shape[1] < max_length:
            v_audio = torch.nn.functional.pad(v_audio, (0, max_length - v_audio.shape[1]))
        if o_audio.shape[1] < max_length:
            o_audio = torch.nn.functional.pad(o_audio, (0, max_length - o_audio.shape[1]))

    # Mix the audio with proper scaling to prevent clipping
    # Scale each track to 0.7 of its original amplitude to leave headroom
    v_audio = v_audio * 0.7
    o_audio = o_audio * 0.7
    audio = v_audio + o_audio

    # Normalize the mixed audio to prevent clipping
    max_amplitude = torch.max(torch.abs(audio))
    if max_amplitude > 1.0:
        audio = audio / max_amplitude

    # Save the mixed audio to a temporary file
    mixed_audio_path = os.path.join(output_dir, f"mixed_{song}")
    torchaudio.save(mixed_audio_path, audio, sr)

    # Run inference with the correct model path
    model_output, midi_data, note_events = predict(mixed_audio_path, ICASSP_2022_MODEL_PATH)

    # Save the MIDI file
    midi_path = os.path.join(output_dir, song.replace(".wav", ".mid"))
    midi_data.write(midi_path)

    # Clean up the temporary mixed audio file
    os.remove(mixed_audio_path)

    print(f"✅ MIDI saved to {midi_path}")