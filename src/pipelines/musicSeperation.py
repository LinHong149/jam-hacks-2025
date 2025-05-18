import os
import torch
import torchaudio
import matplotlib.pyplot as plt
from IPython.display import Audio
from mir_eval import separation
from torchaudio.pipelines import HDEMUCS_HIGH_MUSDB_PLUS
from torchaudio.utils import download_asset
from torchaudio.transforms import Fade
from pipelines.audioTransformation import mergeAudio, drumsTransformation, drumsTransformationLess, bassTransformation, bassTransformationLess, otherTransformation, otherTransformationLess


def musicSeperation(wav_path, output_path,song):
    print("Running music seperation")
    bundle = HDEMUCS_HIGH_MUSDB_PLUS
    bundle = HDEMUCS_HIGH_MUSDB_PLUS
    model = bundle.get_model()
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device)
    sample_rate = bundle.sample_rate
    print(f"Sample rate: {sample_rate}")


    def separate_sources(model, mix, segment=10.0,overlap=0.1, device=None,):
        """
        Apply model to a given mixture. Use fade, and add segments together in order to add model segment by segment.

        Args:
            segment (int): segment length in seconds
            device (torch.device, str, or None): if provided, device on which to
                execute the computation, otherwise `mix.device` is assumed.
                When `device` is different from `mix.device`, only local computations will
                be on `device`, while the entire tracks will be stored on `mix.device`.
        """
        if device is None:
            device = mix.device
        else:
            device = torch.device(device)

        batch, channels, length = mix.shape

        chunk_len = int(sample_rate * segment * (1 + overlap))
        start = 0
        end = chunk_len
        overlap_frames = overlap * sample_rate
        fade = Fade(fade_in_len=0, fade_out_len=int(overlap_frames), fade_shape="linear")

        final = torch.zeros(batch, len(model.sources), channels, length, device=device)

        while start < length - overlap_frames:
            chunk = mix[:, :, start:end]
            with torch.no_grad():
                out = model.forward(chunk)
            out = fade(out)
            final[:, :, :, start:end] += out
            if start == 0:
                fade.fade_in_len = int(overlap_frames)
                start += int(chunk_len - overlap_frames)
            else:
                start += chunk_len
            end += chunk_len
            if end >= length:
                                fade.fade_out_len = 0
        return final

    
    waveform, sample_rate = torchaudio.load(wav_path) 
    waveform = waveform.to(device)
    mixture = waveform

    # parameters
    segment: int = 10
    overlap = 0.1

    print("Separating track")

    ref = waveform.mean(0)
    waveform = (waveform - ref.mean()) / ref.std()  # normalization

    sources = separate_sources(
        model,
        waveform[None],
        device=device,
        segment=segment,
        overlap=overlap,
    )[0]
    sources = sources * ref.std() + ref.mean()

    sources_list = model.sources
    sources = list(sources)

    audios = dict(zip(sources_list, sources))

    print(sample_rate)
    waveformb, sample_rateb = bassTransformation(audios["bass"].cpu(), sample_rate)
    waveformd, sample_rated = drumsTransformation(audios["drums"].cpu(), sample_rate)
    waveformo, sample_rateo = otherTransformation(audios["other"].cpu(), sample_rate)
    merged_waveform, sample_rate = mergeAudio(waveformb, waveformd, waveformo, sample_rateb, sample_rated, sample_rateo)
    print("Sucessfully transformed")
    print(f"Saving to {output_path}")
    torchaudio.save(output_path, merged_waveform, sample_rate)





def musicSeperationForSheet(wav_path, output_path, song):
    print("Running music seperation")
    bundle = HDEMUCS_HIGH_MUSDB_PLUS
    bundle = HDEMUCS_HIGH_MUSDB_PLUS
    model = bundle.get_model()
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device)
    sample_rate = bundle.sample_rate
    print(f"Sample rate: {sample_rate}")

    def separate_sources(model, mix, segment=10.0,overlap=0.1, device=None,):
        """
        Apply model to a given mixture. Use fade, and add segments together in order to add model segment by segment.

        Args:
            segment (int): segment length in seconds
            device (torch.device, str, or None): if provided, device on which to
                execute the computation, otherwise `mix.device` is assumed.
                When `device` is different from `mix.device`, only local computations will
                be on `device`, while the entire tracks will be stored on `mix.device`.
        """
        if device is None:
            device = mix.device
        else:
            device = torch.device(device)

        batch, channels, length = mix.shape

        chunk_len = int(sample_rate * segment * (1 + overlap))
        start = 0
        end = chunk_len
        overlap_frames = overlap * sample_rate
        fade = Fade(fade_in_len=0, fade_out_len=int(overlap_frames), fade_shape="linear")

        final = torch.zeros(batch, len(model.sources), channels, length, device=device)

        while start < length - overlap_frames:
            chunk = mix[:, :, start:end]
            with torch.no_grad():
                out = model.forward(chunk)
            out = fade(out)
            final[:, :, :, start:end] += out
            if start == 0:
                fade.fade_in_len = int(overlap_frames)
                start += int(chunk_len - overlap_frames)
            else:
                start += chunk_len
            end += chunk_len
            if end >= length:
                fade.fade_out_len = 0
        return final

    waveform, sample_rate = torchaudio.load(wav_path) 
    waveform = waveform.to(device)
    mixture = waveform

    # parameters
    segment: int = 10
    overlap = 0.1

    print("Separating track")

    ref = waveform.mean(0)
    waveform = (waveform - ref.mean()) / ref.std()  # normalization

    sources = separate_sources(
        model,
        waveform[None],
        device=device,
        segment=segment,
        overlap=overlap,
    )[0]
    sources = sources * ref.std() + ref.mean()

    sources_list = model.sources
    sources = list(sources)

    audios = dict(zip(sources_list, sources))
    
    # Return the separated audio directly
    return audios["vocals"].cpu(), audios["other"].cpu(), sample_rate



