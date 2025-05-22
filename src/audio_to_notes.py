from typing import cast
import librosa
import numpy as np
from scipy.signal import find_peaks  # type: ignore

from src.constants import SAMPLE_RATE
from src.my_types import *
from src.note import *
from src.visualisation import plot


def extract_note_sequence(
    recording: floatlist,
    nr_of_notes: int,
    ranges_per_note: list[tuple[Note, Note]] | None = None,
) -> list[Note]:
    """Extracts notes from an audio recording.

    Works for melodies, and the notes of the melody can be sustained over onset of new notes.
    Doesn't work for chords, or generally if two notes have an onset too close together in time.

    Parameters
    ----------
    recording : floatlist
        Audio recording as a numpy array of floats.
    nr_of_notes : int
        The number of notes to be detected.
    ranges_per_note : list[tuple[Note, Note]] | None, optional
        The ranges in which to detect the notes, per note, by default (E1, E7) for each note.

    Returns
    -------
    list[Note]
        A list of the detected notes, in order of occurence.
    """
    if ranges_per_note is not None:
        assert len(ranges_per_note) == nr_of_notes
    else:
        ranges_per_note = [(E1, E7) for _ in range(nr_of_notes)]
    n_fft = round(16384 * 2 ** round(log(SAMPLE_RATE / 44100, 2)))
    freqs: floatlist = librosa.fft_frequencies(sr=SAMPLE_RATE, n_fft=n_fft)  # type: ignore
    mask: floatlist = np.linspace(1, 0, len(freqs))

    mask = mask.reshape((mask.shape[0], 1))

    stft_abs: floatlist = np.abs(librosa.stft(recording, n_fft=n_fft, hop_length=512))  # type: ignore

    # Disregard frequencies outside of all notes ranges.
    min_min = min([min(range) for range in ranges_per_note])
    max_max = max([max(range) for range in ranges_per_note])
    min_min_index = round(min_min.freq / freqs[1]) - 4
    max_max_index = round(max_max.freq / freqs[1]) + 4
    stft_abs[:min_min_index] = 0
    stft_abs[max_max_index:] = 0
    stft_masked: floatlist = stft_abs * mask  # type: ignore

    amp_peak_indices = find_amp_peak_indices(stft_abs, nr_of_notes)
    refined_freqs = find_refined_freqs(
        stft_abs, stft_masked, amp_peak_indices, freqs, ranges_per_note
    )
    notes = [Note.from_freq(f) for f in refined_freqs]

    return notes


def find_amp_peak_indices(
    stft_abs: floatlist, nr_of_notes: int, distance: int = 6
) -> list[int]:
    """Detects the onsets of notes by peaks in amplitude.

    Parameters
    ----------
    stft_abs : floatlist
        Absolute values of the STFT spectrogram.
    nr_of_notes : int
        The number of notes to be detected.
    distance : int, optional
        The distance we need to have between peaks, expressed in number of windows, by default 6

    Returns
    -------
    list[int]
        Window indices in the spectrogram for each peak.
    """
    envelope: floatlist = np.sum(stft_abs, axis=0)
    diff_envelope: floatlist = np.concat(([0], np.diff(envelope)))
    diff_peaks, _ = find_peaks(diff_envelope, distance=distance)  # type: ignore
    diff_peaks = cast(intlist, diff_peaks)

    if len(diff_peaks) > nr_of_notes:
        diff_prominences: floatlist = diff_envelope[diff_peaks]
        top_index_indices: intlist = np.argsort(diff_prominences)[-nr_of_notes:]
        diff_peaks = np.sort(diff_peaks[top_index_indices])

    actual_peaks: list[int] = []
    for i_diff_peak in diff_peaks:
        scout = i_diff_peak + 1
        while (
            scout < len(diff_envelope)
            and diff_envelope[scout] > 0
            and diff_envelope[scout] < diff_envelope[scout - 1]
        ):
            scout += 1
        actual_peaks.append(scout - 1)

    if len(actual_peaks) < nr_of_notes:
        print("fewer peaks than expected")
        plot(envelope, green_lines=actual_peaks)
        plot(np.concat(([0], np.diff(envelope))), green_lines=actual_peaks)

    return actual_peaks


def find_refined_freqs(
    stft_abs: floatlist,
    stft_masked: floatlist,
    amp_peak_indices: list[int],
    freqs: floatlist,
    ranges_per_note: list[tuple[Note, Note]],
) -> list[float]:
    """Calculates the true dominant frequency in provided windows of a spectrogram using peak interpolation.

    Parameters
    ----------
    stft_abs : floatlist
        Absolute values of the STFT spectrogram, used for peak interpolation.
    stft_masked : floatlist
        The same spectrogram, but with a mask applied favouring lower frequencies, to prevent overtones
        being detected as the dominant frequency. This masked version is not used in peak interpolation.
    amp_peak_indices : list[int]
        The time indices of the onsets of notes, by peaks in amplitude.
    freqs : floatlist
        The frequencies represented by the bins of the provided spectrogram.
    ranges_per_note : list[tuple[Note, Note]]
        The ranges in which to detect the notes, per note.

    Returns
    -------
    list[float]
        A list of true frequencies per detected note.
    """
    freq_peak_indices: list[int] = []
    for i_amp, (min_note, max_note) in zip(amp_peak_indices, ranges_per_note):
        # From experimentation, it turns out that 4 windows after the peak in amplitude,
        # we get the clearest distribution in frequencies.
        relevant_bit = stft_masked[:, i_amp + 4].copy()

        # By this step, we filter out the frequencies that were already present before.
        if i_amp > 0:
            relevant_bit -= stft_masked[:, i_amp - 4]

        # Disregard the irrelevant frequencies.
        min_note_index = round(min_note.freq / freqs[1]) - 4
        max_note_index = round(max_note.freq / freqs[1]) + 4
        relevant_bit[:min_note_index] = 0
        relevant_bit[max_note_index:] = 0
        freq_peak_indices.append(round(np.argmax(relevant_bit)))

    refined_freqs: list[float] = []
    for i_freq, i_amp in zip(freq_peak_indices, amp_peak_indices):
        if i_freq == 0 or i_freq == len(freqs) - 1:
            refined_freqs.append(freqs[i_freq])

        # Peak interpolation
        left: float = stft_abs[i_freq - 1, i_amp]
        center: float = stft_abs[i_freq, i_amp]
        right: float = stft_abs[i_freq + 1, i_amp]

        a: float = (left + right - 2 * center) / 2
        b: float = (right - left) / 2

        delta: float = -b / (2 * a)
        interpolated_bin: float = i_freq + delta
        refined_freqs.append(float(interpolated_bin * freqs[1]))

    return refined_freqs
