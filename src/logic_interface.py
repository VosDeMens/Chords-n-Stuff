import time
import mido  # type: ignore
from mido import Message  # type: ignore

from src.voicing import Voicing
from src.note import *

DRIVER = "IAC Driver IN"


def panic():
    output_port = mido.open_output(DRIVER)  # type: ignore
    for note in range(0, 90):
        output_port.send(mido.Message("note_off", note=note))  # type: ignore
    output_port.close()  # type: ignore


def play_chord(chord: Voicing, duration: float = 0.4, wake_up: bool = True):
    output_port = mido.open_output(DRIVER)  # type: ignore
    if wake_up:
        output_port.send(Message("note_on", note=0, velocity=1))  # type: ignore
    panic()
    for note in chord.notes:
        output_port.send(Message("note_on", note=note.value, velocity=64))  # type: ignore
    time.sleep(duration)
    for note in chord.notes:
        output_port.send(Message("note_off", note=note.value, velocity=64))  # type: ignore
    output_port.close()  # type: ignore


def play_melody(
    notes: list[Note] | Voicing,
    durations: list[float] | None = None,
    wake_up: bool = True,
):
    output_port = mido.open_output(DRIVER)  # type: ignore
    if wake_up:
        output_port.send(Message("note_on", note=10, velocity=10))  # type: ignore
        time.sleep(0.01)
    panic()
    if durations is None:
        durations = [0.4] * len(notes)
    for note, duration in zip(notes, durations):
        output_port.send(Message("note_on", note=note.value, velocity=64))  # type: ignore
        time.sleep(duration)
        output_port.send(Message("note_off", note=note.value, velocity=64))  # type: ignore
    output_port.close()  # type: ignore


def peep():
    output_port = mido.open_output(DRIVER)  # type: ignore
    output_port.send(Message("note_on", note=E5.value, velocity=80))  # type: ignore
    time.sleep(0.3)
    output_port.send(Message("note_off", note=E5.value, velocity=80))  # type: ignore


def poop():
    output_port = mido.open_output(DRIVER)  # type: ignore
    output_port.send(Message("note_on", note=E2.value, velocity=80))  # type: ignore
    time.sleep(0.3)
    output_port.send(Message("note_off", note=E2.value, velocity=80))  # type: ignore
