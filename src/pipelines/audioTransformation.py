import torch
import torchaudio
import soundfile as sf
from torchaudio.functional import lowpass_biquad, resample, highpass_biquad
from pedalboard import Pedalboard, Reverb, Gain, Compressor, HighpassFilter, time_stretch,HighShelfFilter, LowShelfFilter
from pedalboard.io import AudioFile
import numpy as np


def mergeAudio(waveformb, waveformd, waveformo, sample_rateb, sample_rated, sample_rateo):
    # Ensure inputs are torch tensors
    if isinstance(waveformb, np.ndarray):
        waveformb = torch.from_numpy(waveformb)
    if isinstance(waveformd, np.ndarray):
        waveformd = torch.from_numpy(waveformd)
    if isinstance(waveformo, np.ndarray):
        waveformo = torch.from_numpy(waveformo)

    # Choose a target sample rate (e.g., the minimum to prevent upsampling artifacts)
    target_sample_rate = min(sample_rateb, sample_rated, sample_rateo)

    # Resample all waveforms to the target sample rate
    if sample_rateb != target_sample_rate:
        waveformb = resample(waveformb, orig_freq=sample_rateb, new_freq=target_sample_rate)
    if sample_rated != target_sample_rate:
        waveformd = resample(waveformd, orig_freq=sample_rated, new_freq=target_sample_rate)
    if sample_rateo != target_sample_rate:
        waveformo = resample(waveformo, orig_freq=sample_rateo, new_freq=target_sample_rate)

    # Match all waveform lengths to the shortest one
    min_len = min(waveformb.shape[-1], waveformd.shape[-1], waveformo.shape[-1])
    waveformb = waveformb[..., :min_len]
    waveformd = waveformd[..., :min_len]
    waveformo = waveformo[..., :min_len]

    # Merge and normalize
    merged_waveform = waveformb + waveformd + waveformo
    max_val = merged_waveform.abs().max()
    if max_val > 1.0:
        merged_waveform = merged_waveform / max_val

    return merged_waveform, target_sample_rate


def drumsTransformation(waveform, sample_rate):
    board = Pedalboard([
        # Gain(gain_db=-1),                   # Slightly lower volume
        # Reverb(room_size=0.5, damping=0.6, wet_level=0.2),    # Soften transients
        HighpassFilter(cutoff_frequency_hz=80),
        Compressor(threshold_db=-30, ratio=3.0),  # Softer
    ])
    
    processed, sample_rate = transformation(waveform, sample_rate, 20000, 600, board)
    return processed, sample_rate



def drumsTransformationLess(waveform, sample_rate):
    board = Pedalboard([
        Gain(gain_db=-1),                   # Slightly lower volume
        Reverb(room_size=0.5, damping=0.6, wet_level=0.2),    # Soften transients
        HighpassFilter(cutoff_frequency_hz=80),
        Compressor(threshold_db=-30, ratio=3.0),  # Softer
    ])
    
    processed = transformation(waveform, sample_rate, 22050, 2500, board)
    return processed



def bassTransformation(waveform, sample_rate):

    waveform = highpass_biquad(waveform, sample_rate=sample_rate, cutoff_freq=100)
    waveform = highpass_biquad(waveform, sample_rate=sample_rate, cutoff_freq=100)

    board = Pedalboard([
        Gain(gain_db=0),                   # Slightly lower volume
        LowShelfFilter(cutoff_frequency_hz=600, gain_db=-16),     # Tame sub-bass rumble
        HighpassFilter(cutoff_frequency_hz=200),  # Remove sub-bass rumble
        HighShelfFilter(cutoff_frequency_hz=2000, gain_db=-6),   # Smooth sharp highs
        Compressor(threshold_db=-22, ratio=3.0, attack_ms=10,release_ms=200),  # Make it punchy
        Reverb(room_size=0.2),              # Add ambient space

    ])
    
    processed, sample_rate = transformation(waveform, sample_rate, 12000, 2000, board)
    return processed, sample_rate


def bassTransformationLess(waveform, sample_rate):
    board = Pedalboard([
        Gain(gain_db=-2),                   # Slightly lower volume
        # Reverb(room_size=0.5, damping=0.6, wet_level=0.2),    # Soften transients
        HighpassFilter(cutoff_frequency_hz=80),
        Compressor(threshold_db=-30, ratio=3.0),  # Softer
    ])
    
    processed = transformation(waveform, sample_rate, 22050, 2500, board)
    return processed



def otherTransformation(waveform, sample_rate):
    board = Pedalboard([
        Gain(gain_db=4),                   # Slightly lower volume
        # Compressor(threshold_db=-32, ratio=4, attack_ms=5, release_ms=100),
        HighpassFilter(cutoff_frequency_hz=150),  # Remove sub-bass rumble
        Compressor(threshold_db=-36, ratio=5, attack_ms=5, release_ms=100),
        Compressor(threshold_db=-25, ratio=3.5, attack_ms=5, release_ms=100),
        Compressor(threshold_db=-12, ratio=2, attack_ms=20, release_ms=250),
        Reverb(room_size=0.5, damping=0.6, wet_level=0.3),              # Add ambient space
    ])
    
    processed, sample_rate = transformation(waveform, sample_rate, 12000, 1400, board)
    return processed, sample_rate



def otherTransformationLess(waveform, sample_rate):
    board = Pedalboard([
        Gain(gain_db=-2),                   # Slightly lower volume
        # Reverb(room_size=0.5, damping=0.6, wet_level=0.2),    # Soften transients
        HighpassFilter(cutoff_frequency_hz=80),
        Compressor(threshold_db=-30, ratio=3.0),  # Softer
    ])
    
    processed = transformation(waveform, sample_rate, 22050, 2500, board)
    return processed



def transformation(waveform, sample_rate, target_sample_rate, lowpass_cutoff_freq, board):
    print(f"Processing waveform at {sample_rate} Hz")

    # --- Low-pass filter ---
    waveform = lowpass_biquad(waveform, sample_rate=sample_rate, cutoff_freq=lowpass_cutoff_freq)
    print("Applied low-pass filter")

    # --- Resample to lower sample rate ---
    if sample_rate != target_sample_rate:
        waveform = resample(waveform, orig_freq=sample_rate, new_freq=target_sample_rate)
        sample_rate = target_sample_rate
        print(f"Resampled to {sample_rate} Hz")

    # --- Convert to numpy for Pedalboard ---
    audio_numpy = waveform.squeeze().cpu().numpy()
    stretched_audio = time_stretch( # Slows down audio
        input_audio = audio_numpy,
        samplerate=sample_rate,
        stretch_factor = 0.9
    )
    
    # --- Apply effects ---
    processed = board(stretched_audio, sample_rate)

    # --- Save to output file ---

    # Ensure stereo (2D) format and float32 dtype
    if processed.ndim == 1:
        processed = np.expand_dims(processed, axis=0)  # [1, time]
    processed = processed.astype(np.float32)

    return processed, sample_rate
    