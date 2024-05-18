"""Librosa-based tempo estimators."""

from typing import Mapping

import librosa
import numpy as np
from librosa import onset

from beats.estimators.api import Estimator
from beats.shared_types import SamplingRate
from beats.shared_types import Song
from beats.shared_types import Tempo


class Librosav1(Estimator):
    """Tempo estimator using `librosa.beat.beat_track`."""

    def __init__(self, start_bpm: float = 120.0, max_tempo: float = 350.0):
        self._start_bpm = start_bpm
        self._max_tempo = max_tempo

    def tempo(self, song: Song, fs: SamplingRate) -> Tempo:
        onset_envelope = onset.onset_strength(
            y=song,
            sr=fs,
            hop_length=512,
            aggregate=np.median,
            # constants from librosa.beat.beat_track
        )
        tempo = float(
            librosa.beat.tempo(
                y=song,
                sr=fs,
                start_bpm=self._start_bpm,
                max_tempo=self._max_tempo,
                onset_envelope=onset_envelope,
            )
        )
        return Tempo(float(tempo))

    def params(self) -> Mapping[str, str | float | int]:
        return {
            "start_bpm": self._start_bpm,
            "max_tempo": self._max_tempo,
        }


class Librosav2(Estimator):
    """Tempo estimator using `librosa.beat.beat_track`.
    It takes the initial guess of the tempo and seeds another search with it.
    We retain the higher guess out of the two.

    This approach seems to be surprisingly good at picking out harmonics.
    """

    def __init__(self, start_bpm: float = 120.0, max_tempo: float = 350.0):
        self._start_bpm = start_bpm
        self._max_tempo = max_tempo

    def tempo(self, song: Song, fs: SamplingRate) -> Tempo:
        onset_envelope = onset.onset_strength(
            y=song,
            sr=fs,
            hop_length=512,
            aggregate=np.median,
            # constants from librosa.beat.beat_track
        )
        tempo = float(
            librosa.beat.tempo(
                y=song,
                sr=fs,
                start_bpm=self._start_bpm,
                max_tempo=self._max_tempo,
                onset_envelope=onset_envelope,
            )
        )

        tempo2 = float(
            librosa.beat.tempo(
                y=song,
                sr=fs,
                start_bpm=float(tempo) * 2,
                max_tempo=self._max_tempo,
                onset_envelope=onset_envelope,
            )
        )
        if tempo2 >= 1.8 * tempo:
            return Tempo(tempo2)
        else:
            return Tempo(tempo)

    def params(self) -> Mapping[str, str | float | int]:
        return {
            "start_bpm": self._start_bpm,
            "max_tempo": self._max_tempo,
        }
