"""Combination estimators."""

from typing import Callable
from typing import Mapping

from beats.estimators.api import Estimator
from beats.shared_types import SamplingRate
from beats.shared_types import Song
from beats.shared_types import Tempo


SongTransform = Callable[[Song], Song]


class Transformed(Estimator):
    """A decorator estimator that applies a transformation to
    a song's audio input before delegating the tempo estimation to another estimator."""

    def tempo(self, song: Song, fs: SamplingRate) -> Tempo:
        transformed = self._transform(song)
        return self._estimator.tempo(transformed, fs)

    def params(self) -> Mapping[str, str | float | int]:
        params = dict(self._estimator.params())
        assert "transform" not in params
        try:
            params["transform"] = self._transform.__name__
        except AttributeError:
            pass  # TODO: come back to this and solve `partial`
        return params

    def __init__(self, transform: SongTransform, estimator: Estimator) -> None:
        self._transform = transform
        self._estimator = estimator


def cut(song: Song, start_proportion: float = 0.1, end_proportion: float = 0.9) -> Song:
    assert 0 < start_proportion < end_proportion < 1

    n = len(song)
    min_idx, max_idx = int(n * start_proportion), int(n * end_proportion)

    return Song(song[min_idx:max_idx])
