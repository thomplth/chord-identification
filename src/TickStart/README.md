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
