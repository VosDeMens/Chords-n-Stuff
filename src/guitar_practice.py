import asyncio
from sounddevice import play as play_recording  # type: ignore

from src.audio_io import record
from src.audio_to_notes import extract_note_sequence
from src.constants import SAMPLE_RATE
from src.midi_driver_interface import peep, play_melody, poop
from src.metrics.diatonic_local import DiatonicLocal
from src.metrics.internal_interval_range import InternalIntervalRange
from src.metrics.no_combination_reps import NoCombinationReps
from src.metrics.no_dup_notes import NoDupNotes
from src.metrics.legal_ranges import LegalRanges
from src.metrics.legal_patterns import LegalPatterns
from src.pattern import *
from src.stochastic_distribution_engine import StochasticDistributionEngine
from src.metrics.individual_steps import IndividualSteps
from src.distribution import Distribution
from src.pitch_class import *
from src.note import *
from src.shape import *
from src.my_types import *
from IPython.display import display, clear_output  # type: ignore
import ipywidgets as widgets  # type: ignore

DEFAULT_STRING_RANGES = [(G2, G3), (B2, B3), (E3, E4)]
DEFAULT_START = Distribution([C3, F3, A3])


class GuitarPractice:
    """Creates exercises to practise playing by ear.

    Uses a `StochasticDistributionEngine` to generate new `Distribution`s based on some default settings.
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
        self.legal_patterns = LegalPatterns([MARY, MINNY])
        self.internal_interval_range = InternalIntervalRange(3, 5)

        self.start_distribution = DEFAULT_START

        self.engine = StochasticDistributionEngine(
            self.individual_steps,
            [
                self.no_dup_notes,
                self.internal_interval_range,
                self.legal_ranges,
                self.legal_patterns,
                self.no_combination_reps,
                self.diatonic_local,
            ],
            self.start_distribution,
        )

        self.nr_of_chords_per_round: int | None = None
        self.replayable: bool = False

    async def start(
        self,
        nr_of_chords_per_round: int = 2,
        nr_of_rounds: int = 20,
        rec_time_per_chord: float = 2,
        one_go: bool = False,
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
        self.nr_of_chords_per_round = nr_of_chords_per_round
        for _ in range(10):
            self._generate_distributions(nr_of_chords_per_round, nr_of_rounds)
            if self.replayable:
                return await self.restart(rec_time_per_chord)

        print("cul-de-sac")
        return -1

    def _generate_distributions(self, nr_of_chords_per_round: int, nr_of_rounds: int):
        self.engine.reset(self.start_distribution)
        for _ in range(nr_of_rounds):
            for _ in range(nr_of_chords_per_round):
                result = self.engine.get_next()
                if result is None:
                    self.replayable = False
                    return
        self.replayable = True

    async def restart(self, rec_time_per_chord: float = 2) -> float:
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
        if not self.replayable or not self.nr_of_chords_per_round:
            print("Nothing to resart")
            return -1

        history = self.engine.history
        mistakes_total = 0
        nr_of_rounds = 0
        for i in range(
            0,
            len(history) - (self.nr_of_chords_per_round - 1),
            self.nr_of_chords_per_round - 1,
        ):
            distributions = [
                history[i + j] for j in range(0, self.nr_of_chords_per_round)
            ]
            nr_of_mistakes = await self.play_round(distributions, rec_time_per_chord)
            nr_of_rounds += 1
            while nr_of_mistakes:
                mistakes_total += nr_of_mistakes
                nr_of_mistakes = await self.play_round(
                    distributions, rec_time_per_chord
                )
                nr_of_rounds += 1

        optimal = nr_of_rounds * self.nr_of_chords_per_round
        optimal_minus_mistakes = optimal - mistakes_total
        return round(optimal_minus_mistakes / optimal * 100) / 10

    async def play_round(
        self, distributions: list[Distribution], sleep_duration: float
    ) -> int:
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
        distributions : list[Distribution]
            The chords for this round.
        sleep_duration : float
            The time the player gets to play back a chord.
        """
        future: asyncio.Future[int] = asyncio.get_event_loop().create_future()

        for distribution in distributions:
            play_melody(distribution)
        peep()
        recordings: list[floatlist] = []
        for i, distribution in enumerate(distributions):
            recordings.append(record(sleep_duration))
            if i < len(distributions) - 1:
                peep()
        notes_per_recording = [
            extract_note_sequence(recording, len(distribution), self.string_ranges)
            for distribution, recording in zip(distributions, recordings)
        ]

        corrects = [
            distribution.notes == rec_notes
            for distribution, rec_notes in zip(distributions, notes_per_recording)
        ]
        for correct in corrects:
            if correct:
                peep()
            else:
                poop()

        acceptances = corrects.copy()

        def on_accept_click(i: int):
            acceptances[i] = True
            display(widgets.VBox([status_label, button_box, continue_btn]))

        def on_overrule_click(i: int):
            corrects[i] = True
            display(widgets.VBox([status_label, button_box, continue_btn]))

        def on_play_click(i: int):
            play_melody(distributions[i])
            play_recording(recordings[i], SAMPLE_RATE, blocking=True)
            play_melody(notes_per_recording[i])

        def on_continue_click(_):
            nr_of_mistakes = corrects.count(False)
            future.set_result(nr_of_mistakes)

        button_box = widgets.HBox(
            [
                (
                    widgets.VBox(
                        [
                            widgets.Button(description="Play"),
                            widgets.Button(description="Accept"),
                            widgets.Button(description="Overrule"),
                        ]
                    )
                    if not correct and not acceptance
                    else (
                        widgets.Label("Correct")
                        if correct
                        else widgets.Label("Incorrect")
                    )
                )
                for correct, acceptance in zip(corrects, acceptances)
            ]
        )
        continue_btn = widgets.Button(description="Continue")

        for i, vbox in enumerate(button_box.children):
            if not isinstance(vbox, widgets.VBox):
                continue
            children: tuple[widgets.Button] = vbox.children  # type: ignore
            children[0].on_click(lambda _: on_play_click(i))  # type: ignore
            children[1].on_click(lambda _: on_accept_click(i))  # type: ignore
            children[2].on_click(lambda _: on_overrule_click(i))  # type: ignore

        continue_btn.on_click(on_continue_click)

        status_label = widgets.Label()

        display(widgets.VBox([status_label, button_box, continue_btn]))

        result = await future
        return result

    # def play_round_in_one_go(
    #     self, distributions: list[Distribution], sleep_duration: float
    # ) -> None:
    #     """Plays a single round, and replays it if the player didn't play back the chords correctly,
    #     but the player has to play all chords in one go.

    #     Parameters
    #     ----------
    #     distributions : list[Distribution]
    #         The chords for this round.
    #     sleep_duration : float
    #         The time the player gets to play back a single chord.
    #     """
    #     for distribution in distributions:
    #         play_melody(distribution)
    #     peep()
    #     recording = record(len(distributions) * sleep_duration)
    #     rec_notes = extract_note_sequence(
    #         recording,
    #         sum(len(distribution) for distribution in distributions),
    #         self.string_ranges * len(distributions),
    #     )
    #     target_notes = [note for distribution in distributions for note in distribution]

    #     if rec_notes == target_notes:
    #         peep()
    #     else:
    #         poop()
    #         for distribution in distributions:
    #             play_melody(distribution)
    #         play_recording(recording, SAMPLE_RATE, blocking=True)
    #         play_melody(rec_notes)
    #         poop()
    #         sleep(1)
    #         self.play_round_in_one_go(distributions, sleep_duration)

    def study_new(self) -> None: ...

    def study_history(self) -> None:
        """Goes over all the distributions in the history, and plays them back,
        so the player can study them.

        Uses interactive widgets for Jupyter notebook compatibility.
        """
        if not self.engine.history or not self.nr_of_chords_per_round:
            print("No history to study")
            poop()
            return

        self.current_round = 0
        max_rounds = (len(self.engine.history) - 1) // (self.nr_of_chords_per_round - 1)

        def get_current_distributions() -> list[Distribution]:
            assert self.nr_of_chords_per_round, "nr_of_chords_per_round must be set"
            start_index = self.current_round * (self.nr_of_chords_per_round - 1)
            return [
                self.engine.history[j]
                for j in range(start_index, start_index + self.nr_of_chords_per_round)
            ]

        def play_current() -> None:
            distributions = get_current_distributions()
            for distribution in distributions:
                play_melody(distribution)

        def on_previous_click(_):
            if self.current_round > 0:
                self.current_round -= 1
                update_display()
                play_current()
            else:
                poop()

        def on_next_click(_):
            if self.current_round < max_rounds - 1:
                self.current_round += 1
                update_display()
                play_current()
            else:
                poop()

        def on_replay_click(_):
            play_current()

        prev_btn = widgets.Button(description="Previous", button_style="info")
        next_btn = widgets.Button(description="Next", button_style="info")
        replay_btn = widgets.Button(description="Replay", button_style="success")

        prev_btn.on_click(on_previous_click)
        next_btn.on_click(on_next_click)
        replay_btn.on_click(on_replay_click)

        button_box = widgets.HBox([prev_btn, replay_btn, next_btn])
        status_label = widgets.Label()

        def update_display():
            status_label.value = f"Round {self.current_round + 1} of {max_rounds}"

        update_display()
        display(widgets.VBox([status_label, button_box]))

        play_current()
