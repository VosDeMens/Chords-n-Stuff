import time
import mido  # type: ignore
from mido import Message  # type: ignore

from src.distribution import Distribution
from src.voicing import Voicing
from src.note import *

DRIVER = "IAC Driver IN"


def panic():
    """Sends note off events for all notes."""
    output_port = mido.open_output(DRIVER)  # type: ignore
    for note in range(0, 90):
        output_port.send(mido.Message("note_off", note=note))  # type: ignore
    output_port.close()  # type: ignore


def play_chord(
    chord: Voicing | Distribution, duration: float = 0.4, wake_up: bool = True
):
    """Sends a chord to the MIDI driver, for its notes to be played simultaneously.

    Parameters
    ----------
    chord : Voicing
        The chord to play.
    duration : float, optional
        The time in seconds  between the note on and note off event, by default 0.4
    wake_up : bool, optional
        Whether to send a dummy note first, to wake up the driver, by default True
    """
    output_port = mido.open_output(DRIVER)  # type: ignore
    if wake_up:
        output_port.send(Message("note_on", note=10, velocity=10))  # type: ignore
        time.sleep(0.2)
    panic()
    for note in chord.notes:
        output_port.send(Message("note_on", note=note.value, velocity=64))  # type: ignore
    time.sleep(duration)
    for note in chord.notes:
        output_port.send(Message("note_off", note=note.value, velocity=64))  # type: ignore
    output_port.close()  # type: ignore


def play_melody(
    notes: list[Note] | Voicing | Distribution,
    durations: list[float] | None = None,
):
    """Sends notes to the MIDI driver, to be played sequentially.

    Parameters
    ----------
    chord : Voicing
        The chord to play.
    durations : list[float], optional
        The time in seconds between the note on and note off events, by default 0.4 per note
    wake_up : bool, optional
        Whether to send a dummy note first, to wake up the driver, by default True
    """
    output_port = mido.open_output(DRIVER)  # type: ignore
    panic()
    if durations is None:
        durations = [0.4] * len(notes)
    for note, duration in zip(notes, durations):
        output_port.send(Message("note_on", note=note.midi_value, velocity=64))  # type: ignore
        time.sleep(duration)
        output_port.send(Message("note_off", note=note.midi_value, velocity=64))  # type: ignore
    output_port.close()  # type: ignore


def peep():
    """Sends a high note (E5) to the driver, lasting 0.3 seconds."""
    output_port = mido.open_output(DRIVER)  # type: ignore
    output_port.send(Message("note_on", note=Ef5.midi_value, velocity=80))  # type: ignore
    time.sleep(0.3)
    output_port.send(Message("note_off", note=Ef5.midi_value, velocity=80))  # type: ignore


def poop():
    """Sends a low note (E2) to the driver, lasting 0.3 seconds."""
    output_port = mido.open_output(DRIVER)  # type: ignore
    output_port.send(Message("note_on", note=Ef2.midi_value, velocity=80))  # type: ignore
    time.sleep(0.3)
    output_port.send(Message("note_off", note=Ef2.midi_value, velocity=80))  # type: ignore
