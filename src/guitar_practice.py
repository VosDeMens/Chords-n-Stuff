from time import sleep
from typing import cast
from sounddevice import play as play_recording  # type: ignore

from src.audio_io import record
from src.audio_to_notes import extract_note_sequence
from src.constants import SAMPLE_RATE
from src.logic_interface import peep, play_melody, poop
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

    def start(
        self,
        chords_per_round: int = 2,
        nr_of_rounds: int = 20,
        sleep_duration: float = 2,
    ):
        self.engine.reset(self.start_voicing)
        self.attempts_count = 0
        prev = self.start_voicing
        voicings_or_none: list[Voicing | None] = []
        for _ in range(nr_of_rounds):
            if voicings_or_none:
                prev = cast(Voicing, voicings_or_none[-1])
            voicings_or_none = [
                self.engine.get_next() for _ in range(chords_per_round - 1)
            ]
            if None in voicings_or_none:
                print("cul-de-sac")
                break
            voicings = cast(list[Voicing], voicings_or_none)
            self.play_round([prev] + voicings, sleep_duration)
        print(f"{nr_of_rounds / self.attempts_count * 10:.1f}")

    def restart(self, len_sequence: int = 2, sleep_duration: float = 2):
        history = self.engine.history
        self.attempts_count = 0
        nr_of_rounds = 0
        for i in range(0, len(history) - (len_sequence - 1), len_sequence - 1):
            voicings = [history[i + j] for j in range(0, len_sequence)]
            self.play_round(voicings, sleep_duration)
            nr_of_rounds += 1
        print(f"{nr_of_rounds / self.attempts_count * 10:.1f}")

    def play_round(self, voicings: list[Voicing], sleep_duration: float):
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
