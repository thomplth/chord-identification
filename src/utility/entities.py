from typing import TypedDict

from preprocess.note import Note
import numpy as np

# note dict: note name -> duration
Note_duration_dict = dict[str, float]


class OffsetChroma(TypedDict):
    chroma: np.ndarray
    offset: float


class OffsetNoteProfile(TypedDict):
    note_profile: Note_duration_dict
    offset: float


Measure_OffsetChroma_dict = dict[int, OffsetChroma]

Pitch_scale = tuple[int, bool]
Notes_frequencies = list[tuple[Note, float]]


class PitchScaleCorrelationValue(TypedDict):
    pitch_scale: Pitch_scale
    corr_val: float


class OffsetPitchScaleCorrelationValues(TypedDict):
    offset: float
    corr_values: list[PitchScaleCorrelationValue]


class ChordSimilarityScore(TypedDict):
    chord: any  # TODO: the type should be Chord only
    similarity_score: float