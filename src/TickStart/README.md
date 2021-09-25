# Terms Explanation

- Note.py (A class to store a note)

  - alphabet : Letter of the note, e.g. the alphabet of "F♯" is "F".
  - accidental : An element of the sharp (♯), flat (♭), double sharp (𝄪) and double flat (𝄫). They are represented by an int value, referring to the number of semitones a note is raised (or lowered if the value is negative), from -2 to 2.
  - interval : The difference between two notes in the format of "X9", where
    - "X": Interval quality. Only terms perfect (P), major (M), minor (m), augmented (A), and diminished (d) are used.
    - "9": Interval number (or "distance" in the program), can be regarded as difference of ascii of alphabets of two notes and then plus 1.
    - We only consider the interval from "P1" to "A7".

- utility.py (helper functions)

  - invert interval : Referring to the new interval where the lower note is transposed (moved) to an octave higher

- scale_generator.py

  - tonic: The first note of a major or a minor scale

- Ref:
  - MAJOR_CHORD_FINDER_DICTIONARY result:
  ```
  ('M3', 'm3') [{'chord': 'I', 'tonic_interval': 'P1'}, {'chord': 'bII', 'tonic_interval': 'm2'}, {'chord': 'IV', 'tonic_interval': 'P4'}, {'chord': 'V', 'tonic_interval': 'P5'}, {'chord': 'bVI', 'tonic_interval': 'm6'}]
  ('m3', 'M3') [{'chord': 'II', 'tonic_interval': 'M2'}, {'chord': 'III', 'tonic_interval': 'M3'}, {'chord': 'VI', 'tonic_interval': 'M6'}]
  ('m3', 'M3', 'm3') [{'chord': 'II7', 'tonic_interval': 'M2'}]
  ('M3', 'm3', 'm3') [{'chord': 'V7', 'tonic_interval': 'P5'}]
  ('M3', 'm3', 'A2') [{'chord': 'GerVI', 'tonic_interval': 'm6'}]
  ('M3', 'M2', 'M3') [{'chord': 'FrVI', 'tonic_interval': 'm6'}]
  ('M3', 'A4') [{'chord': 'ItVI', 'tonic_interval': 'm6'}]
  ('m3', 'm3') [{'chord': 'VIIdim', 'tonic_interval': 'M7'}]
  ('m3', 'm3', 'm3') [{'chord': 'VIIdim7', 'tonic_interval': 'M7'}]
  ```
  - MINOR_CHORD_FINDER_DICTIONARY result:
  ```
  ('m3', 'M3') [{'chord': 'I', 'tonic_interval': 'P1'}, {'chord': 'IV', 'tonic_interval': 'P4'}, {'chord': 'V', 'tonic_interval': 'P5'}]
  ('M3', 'm3') [{'chord': 'I+', 'tonic_interval': 'P1'}, {'chord': 'bII', 'tonic_interval': 'm2'}, {'chord': 'III', 'tonic_interval': 'm3'}, {'chord': 'IV+', 'tonic_interval': 'P4'}, {'chord': 'V+', 'tonic_interval': 'P5'}, {'chord': 'VI', 'tonic_interval': 'm6'}, {'chord': 'VII', 'tonic_interval': 'm7'}]
  ('m3', 'm3') [{'chord': 'IIdim', 'tonic_interval': 'M2'}, {'chord': 'VIIdim', 'tonic_interval': 'M7'}]
  ('m3', 'm3', 'M3') [{'chord': 'II7', 'tonic_interval': 'M2'}]
  ('M3', 'm3', 'm3') [{'chord': 'V7', 'tonic_interval': 'P5'}]
  ('M3', 'm3', 'A2') [{'chord': 'GerVI', 'tonic_interval': 'm6'}]
  ('M3', 'M2', 'M3') [{'chord': 'FrVI', 'tonic_interval': 'm6'}]
  ('M3', 'A4') [{'chord': 'ItVI', 'tonic_interval': 'm6'}]
  ('m3', 'm3', 'm3') [{'chord': 'VIIdim7', 'tonic_interval': 'M7'}]
  ```
