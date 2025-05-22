import numpy as np
from typing import cast
import sounddevice as sd  # type: ignore

from src.constants import SAMPLE_RATE
from src.my_types import floatlist


NOTE_FADE_DURATION_SEC = 0.025
AUDIO_FADE_DURATION_SEC = 0.15


def record(
    nr_of_seconds: float = 8, sample_rate: int = SAMPLE_RATE, verbose: bool = False
) -> floatlist:
    """Records audio, fit for Jupyter Notebook, not for Streamlit.

    Parameters
    ----------
    nr_of_seconds : int, optional
        Duration to record for, by default 8

    sample_rate : int, optional
        Sample rate of recording, by default SAMPLE_RATE := 44100

    verbose : bool, optional
        Whether to print when recording starts and stops, by default False

    Returns
    -------
    floatlist
        Audio, as a wave.
    """
    recording = sd.rec(  # type: ignore
        (nr_of_seconds * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="float64",
    )
    if verbose:
        print("Recording...")
    sd.wait()
    if verbose:
        print("Recording complete.")
    recording = cast(floatlist, recording)
    recording = recording.reshape((recording.shape[0]))
    recording = fade_in_fade_out(recording)
    return recording


def get_amplitutude_segment(
    length: int,
    fade_duration_sec: float = NOTE_FADE_DURATION_SEC,
    sample_rate: int = SAMPLE_RATE,
) -> floatlist:
    """Generates amplitude values over time for a single note, with a fade in and fade out.

    Parameters
    ----------
    length : int
        Duration of the audio to be generated, in nr of samples.
    fade_duration_sec : float, optional
        Duration of the fade, by default FADE_DURATION_SEC := 0.025
    sample_rate : int, optional
        The sample rate of the audio.

    Returns
    -------
    floatlist
        Amplitude values over time.
    """
    amplitutude_segment: floatlist = np.array(
        [
            *get_attack(fade_duration_sec, sample_rate),
            *np.linspace(1, 1, length - 2 * int(fade_duration_sec * sample_rate)),
            *get_release(fade_duration_sec, sample_rate),
        ]
    )
    return amplitutude_segment


def fade_in_fade_out(
    signal: floatlist,
    fade_duration_sec: float = AUDIO_FADE_DURATION_SEC,
    sample_rate: int = SAMPLE_RATE,
) -> floatlist:
    """Applies fade in and fade out to a wave.

    Parameters
    ----------
    signal : floatlist
        Original wave.
    fade_duration_sec : float, optional
        The duration of a fade in or out, expressed in seconds, by default AUDIO_FADE_DURATION_SEC := 0.15
    sample_rate : int, optional
        The sample rate, by default SAMPLE_RATE := 44100

    Returns
    -------
    floatlist
        Wave with fades.
    """
    assert len(signal.shape) == 1, "signal has to be 1D"
    amplitutude_segment = get_amplitutude_segment(
        len(signal), fade_duration_sec, sample_rate
    )
    return signal * amplitutude_segment


def get_attack(
    attack_duration_sec: float = NOTE_FADE_DURATION_SEC, sample_rate: int = SAMPLE_RATE
) -> floatlist:
    """Creates a smooth fade in envelope, based on cosine.

    Parameters
    ----------
    attack_duration_sec : int, optional
        Duration in seconds, by default NOTE_FADE_DURATION_SEC := 0.025
    sample_rate : int, optional
        The sample rate, by default SAMPLE_RATE := 44100

    Returns
    -------
    floatlist
        Amplitude values
    """
    attack_duration_samples = int(attack_duration_sec * sample_rate)
    cos_input = np.linspace(-np.pi, 0, attack_duration_samples)
    cos_output = np.cos(cos_input)
    moved_up = cos_output + 1
    scaled_down = moved_up / 2
    return scaled_down


def get_release(
    release_duration_sec: float = NOTE_FADE_DURATION_SEC, sample_rate: int = SAMPLE_RATE
) -> floatlist:
    """Creates a smooth fade out envelope, based on cosine.

    Parameters
    ----------
    release_duration_sec : int, optional
        Duration in seconds, by default NOTE_FADE_DURATION_SEC := 0.025
    sample_rate : int, optional
        The sample rate, by default SAMPLE_RATE := 44100

    Returns
    -------
    floatlist
        Amplitude values
    """
    release_duration_samples = int(release_duration_sec * sample_rate)
    cos_input = np.linspace(0, np.pi, release_duration_samples)
    cos_output = np.cos(cos_input)
    moved_up = cos_output + 1
    scaled_down = moved_up / 2
    return scaled_down
