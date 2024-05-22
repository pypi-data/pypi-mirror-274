class Chords:
    """
    ref: https://github.com/tidalcycles/Tidal/blob/dev/src/Sound/Tidal/Chords.hs
    """

    # Major chords
    major = [0, 4, 7]
    aug = [0, 4, 8]
    six = [0, 4, 7, 9]
    six_nine = [0, 4, 7, 9, 14]
    major7 = [0, 4, 7, 11]
    major9 = [0, 4, 7, 11, 14]
    add9 = [0, 4, 7, 14]
    major11 = [0, 4, 7, 11, 14, 17]
    add11 = [0, 4, 7, 17]
    major13 = [0, 4, 7, 11, 14, 21]
    add13 = [0, 4, 7, 21]

    # Dominant chords
    dom7 = [0, 4, 7, 10]
    dom9 = [0, 4, 7, 14]
    dom11 = [0, 4, 7, 17]
    dom13 = [0, 4, 7, 21]
    seven_flat5 = [0, 4, 6, 10]
    seven_sharp5 = [0, 4, 8, 10]
    seven_flat9 = [0, 4, 7, 10, 13]
    nine = [0, 4, 7, 10, 14]
    eleven = [0, 4, 7, 10, 14, 17]
    thirteen = [0, 4, 7, 10, 14, 17, 21]

    # Minor chords
    minor = [0, 3, 7]
    diminished = [0, 3, 6]
    minor_sharp5 = [0, 3, 8]
    minor6 = [0, 3, 7, 9]
    minor_six_nine = [0, 3, 9, 7, 14]
    minor7flat5 = [0, 3, 6, 10]
    minor7 = [0, 3, 7, 10]
    minor7sharp5 = [0, 3, 8, 10]
    minor7flat9 = [0, 3, 7, 10, 13]
    minor7sharp9 = [0, 3, 7, 10, 15]
    diminished7 = [0, 3, 6, 9]
    minor9 = [0, 3, 7, 10, 14]
    minor11 = [0, 3, 7, 10, 14, 17]
    minor13 = [0, 3, 7, 10, 14, 17, 21]
    minor_major7 = [0, 3, 7, 11]

    # Other chords
    one = [0]
    five = [0, 7]
    sus2 = [0, 2, 7]
    sus4 = [0, 5, 7]
    seven_sus2 = [0, 2, 7, 10]
    seven_sus4 = [0, 5, 7, 10]
    nine_sus4 = [0, 5, 7, 10, 14]

    # Questionable chords
    seven_flat10 = [0, 4, 7, 10, 15]
    nine_sharp5 = [0, 1, 13]
    minor9sharp5 = [0, 1, 14]
    seven_sharp5flat9 = [0, 4, 8, 10, 13]
    minor7sharp5flat9 = [0, 3, 8, 10, 13]
    eleven_sharp = [0, 4, 7, 10, 14, 18]
    minor11sharp = [0, 3, 7, 10, 14, 18]
