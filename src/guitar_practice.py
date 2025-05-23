from time import sleep
from typing import cast
from sounddevice import play as play_recording  # type: ignore

from src.audio_io import record
from src.audio_to_notes import extract_note_sequence
from src.constants import SAMPLE_RATE
from midi_driver_interface import peep, play_melody, poop
from src.metrics.diatonic_local import DiatonicLocal
from src.metrics.internal_interval_range import InternalIntervalRange
from src.metrics.no_combination_reps import NoCombinationReps
from src.metrics.no_dup_notes import NoDupNotes
from src.metrics.legal_ranges import LegalRanges
from src.metrics.legal_patterns import LegalPatterns
from src.pattern import *
from src.stochastic_voicing_engine import StochasticVoicingEngine
from src.metrics.individual_steps import IndividualSteps
from src.voicing import Voicing
from src.pitch_class import *
from src.note import *
from src.shape import *
from src.my_types import *

DEFAULT_STRING_RANGES = [(G2, G3), (B2, B3), (E3, E4)]
DEFAULT_START = Voicing([C3, F3, A3])


class GuitarPractice:
    """Creates exercises to practise playing by ear.

    Uses a `StochasticVoicingEngine` to generate new `Voicing`s based on some default settings.
    """

    def __init__(self, string_ranges: list[tuple[Note, Note]] | None = None):
        if string_ranges is not None:
            self.string_ranges = string_ranges
        else:
            self.string_ranges = DEFAULT_STRING_RANGES
        self.individual_steps = IndividualSteps(0, 2)
        self.no_dup_notes = NoDupNotes()
        self.no_combination_reps = NoCombinationReps(3, 3)
        self.diatonic_local = DiatonicLocal(2, 2)
        self.legal_ranges = LegalRanges(self.string_ranges)
        self.pattern_rules = LegalPatterns([MARY, MINNY])
        self.internal_interval_range = InternalIntervalRange(3, 5)

        self.start_voicing = DEFAULT_START

        self.engine = StochasticVoicingEngine(
            self.individual_steps,
            [
                self.no_dup_notes,
                self.internal_interval_range,
                self.legal_ranges,
                self.pattern_rules,
                self.no_combination_reps,
                self.diatonic_local,
            ],
            self.start_voicing,
        )

        self.nr_of_chords_per_round: int | None = None

    def start(
        self,
        nr_of_chords_per_round: int = 2,
        nr_of_rounds: int = 20,
        rec_time_per_chord: float = 2,
    ) -> float:
        """Starts a new exercise.

        Every round starts with the last chord of the previous round, and then newly generated chords,
        for a total of `nr_of_chords_per_round`.
        The chords are arpeggiated, and the player has to play them back arpeggiated one by one.
        This function returns a score, based on how many total attempts the player needed.

        Parameters
        ----------
        nr_of_chords_per_round : int, optional
            The number of chords per round, by default 2
        nr_of_rounds : int, optional
            The number of rounds in an exercise, by default 20
        rec_time_per_chord : float, optional
            The number of seconds the player gets to replay a chord, by default 2

        Returns
        -------
        float
            Score, based on how well the player did (between 1 and 10).
        """
        self.engine.reset(self.start_voicing)
        self.nr_of_chords_per_round = nr_of_chords_per_round
        self.attempts_count = 0
        prev = self.start_voicing
        voicings_or_none: list[Voicing | None] = []
        for _ in range(nr_of_rounds):
            if voicings_or_none:
                prev = cast(Voicing, voicings_or_none[-1])
            voicings_or_none = [
                self.engine.get_next() for _ in range(nr_of_chords_per_round - 1)
            ]
            if None in voicings_or_none:
                print("cul-de-sac")
                break
            voicings = cast(list[Voicing], voicings_or_none)
            self.play_round([prev] + voicings, rec_time_per_chord)
        return round(nr_of_rounds / self.attempts_count * 10) / 10

    def restart(self, rec_time_per_chord: float = 2) -> float:
        """Restarts the previous exercise.

        Parameters
        ----------
        rec_time_per_chord : float, optional
            The number of seconds the player gets per chord, by default 2

        Returns
        -------
        float
            Score, based on how well the player did (between 1 and 10).
        """
        if self.nr_of_chords_per_round is None:
            print("Nothing to resart")
            return -1

        history = self.engine.history
        self.attempts_count = 0
        nr_of_rounds = 0
        for i in range(
            0,
            len(history) - (self.nr_of_chords_per_round - 1),
            self.nr_of_chords_per_round - 1,
        ):
            voicings = [history[i + j] for j in range(0, self.nr_of_chords_per_round)]
            self.play_round(voicings, rec_time_per_chord)
            nr_of_rounds += 1
        return round(nr_of_rounds / self.attempts_count * 10) / 10

    def play_round(self, voicings: list[Voicing], sleep_duration: float):
        """Plays a single round, and replays it if the player didn't play back the chords correctly.

        The player will hear:
        - The chords, arpeggiated
        - A high note, followed by silence during which to replay the chord, for every chord
        - A series of high or low notes, indicating which chord were correctly replayed
        - For every incorrectly replayed chord:
            - The correct chord
            - The recording
            - The interpretation of the recording

        Parameters
        ----------
        voicings : list[Voicing]
            The chords for this round.
        sleep_duration : float
            The time the player gets to play back a chord.
        """
        self.attempts_count += 1
        for voicing in voicings:
            play_melody(voicing)
        peep()
        recordings: list[floatlist] = []
        for i, voicing in enumerate(voicings):
            recordings.append(record(sleep_duration))
            if i < len(voicings) - 1:
                peep()
        notes_per_recording = [
            extract_note_sequence(recording, len(voicing), self.string_ranges)
            for voicing, recording in zip(voicings, recordings)
        ]

        corrects = [
            voicing.notes == rec_notes
            for voicing, rec_notes in zip(voicings, notes_per_recording)
        ]
        for correct in corrects:
            if correct:
                peep()
            else:
                poop()
        for voicing, recording, rec_notes, correct in zip(
            voicings, recordings, notes_per_recording, corrects
        ):
            if not correct:
                play_melody(voicing)
                play_recording(recording, SAMPLE_RATE, blocking=True)
                play_melody(rec_notes)
                poop()

        if False in corrects:
            sleep(1)
            self.play_round(voicings, sleep_duration)
