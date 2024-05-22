class Scales:
    """
    ref: https://github.com/tidalcycles/Tidal/blob/dev/src/Sound/Tidal/Scales.hs
    """

    # Five notes scales
    min_pent = [0, 3, 5, 7, 10]
    maj_pent = [0, 2, 4, 7, 9]

    # Another mode of major pentatonic
    ritusen = [0, 2, 5, 7, 9]

    # Another mode of major pentatonic
    egyptian = [0, 2, 5, 7, 10]

    # Other scales
    kumai = [0, 2, 3, 7, 9]
    hirajoshi = [0, 2, 3, 7, 8]
    iwato = [0, 1, 5, 6, 10]
    chinese = [0, 4, 6, 7, 11]
    indian = [0, 4, 5, 7, 10]
    pelog = [0, 1, 3, 7, 8]

    # More scales
    prometheus = [0, 2, 4, 6, 11]
    scriabin = [0, 1, 4, 7, 9]

    # Han Chinese pentatonic scales
    gong = [0, 2, 4, 7, 9]
    shang = [0, 2, 5, 7, 10]
    jiao = [0, 3, 5, 8, 10]
    zhi = [0, 2, 5, 7, 9]
    yu = [0, 3, 5, 7, 10]

    # 6 note scales
    whole = [0, 2, 4, 6, 8, 10]
    augmented = [0, 3, 4, 7, 8, 11]
    augmented2 = [0, 1, 4, 5, 8, 9]

    # Hexatonic modes with no tritone
    hex_major7 = [0, 2, 4, 7, 9, 11]
    hex_dorian = [0, 2, 3, 5, 7, 10]
    hex_phrygian = [0, 1, 3, 5, 8, 10]
    hex_sus = [0, 2, 5, 7, 9, 10]
    hex_major6 = [0, 2, 4, 5, 7, 9]
    hex_aeolian = [0, 3, 5, 7, 8, 10]

    # 7 note scales
    major = [0, 2, 4, 5, 7, 9, 11]
    ionian = [0, 2, 4, 5, 7, 9, 11]
    dorian = [0, 2, 3, 5, 7, 9, 10]
    phrygian = [0, 1, 3, 5, 7, 8, 10]
    lydian = [0, 2, 4, 6, 7, 9, 11]
    mixolydian = [0, 2, 4, 5, 7, 9, 10]
    aeolian = [0, 2, 3, 5, 7, 8, 10]
    minor = [0, 2, 3, 5, 7, 8, 10]
    locrian = [0, 1, 3, 5, 6, 8, 10]
    harmonic_minor = [0, 2, 3, 5, 7, 8, 11]
    harmonic_major = [0, 2, 4, 5, 7, 8, 11]
    melodic_minor = [0, 2, 3, 5, 7, 9, 11]
    melodic_minor_desc = [0, 2, 3, 5, 7, 8, 10]
    melodic_major = [0, 2, 4, 5, 7, 8, 10]
    bartok = melodic_major
    hindu = melodic_major

    # Raga modes
    todi = [0, 1, 3, 6, 7, 8, 11]
    purvi = [0, 1, 4, 6, 7, 8, 11]
    marva = [0, 1, 4, 6, 7, 9, 11]
    bhairav = [0, 1, 4, 5, 7, 8, 11]
    ahirbhairav = [0, 1, 4, 5, 7, 9, 10]

    # More modes
    super_locrian = [0, 1, 3, 4, 6, 8, 10]
    romanian_minor = [0, 2, 3, 6, 7, 9, 10]
    hungarian_minor = [0, 2, 3, 6, 7, 8, 11]
    neapolitan_minor = [0, 1, 3, 5, 7, 8, 11]
    enigmatic = [0, 1, 4, 6, 8, 10, 11]
    spanish = [0, 1, 4, 5, 7, 8, 10]

    # Modes of whole tones with added note ->
    leading_whole = [0, 2, 4, 6, 8, 10, 11]
    lydian_minor = [0, 2, 4, 6, 7, 8, 10]
    neapolitan_major = [0, 1, 3, 5, 7, 9, 11]
    locrian_major = [0, 2, 4, 5, 6, 8, 10]

    # 8 note scales
    diminished = [0, 1, 3, 4, 6, 7, 9, 10]
    diminished2 = [0, 2, 3, 5, 6, 8, 9, 11]

    # Modes of limited transposition
    messiaen1 = whole
    messiaen2 = diminished
    messiaen3 = [0, 2, 3, 4, 6, 7, 8, 10, 11]
    messiaen4 = [0, 1, 2, 5, 6, 7, 8, 11]
    messiaen5 = [0, 1, 5, 6, 7, 11]
    messiaen6 = [0, 2, 4, 5, 6, 8, 10, 11]
    messiaen7 = [0, 1, 2, 3, 5, 6, 7, 8, 9, 11]

    # Arabic maqams taken from SuperCollider's Scale.sc
    bayati = [0, 1.5, 3, 5, 7, 8, 10]
    hijaz = [0, 1, 4, 5, 7, 8.5, 10]
    sikah = [0, 1.5, 3.5, 5.5, 7, 8.5, 10.5]
    rast = [0, 2, 3.5, 5, 7, 9, 10.5]
    iraq = [0, 1.5, 3.5, 5, 6.5, 8.5, 10.5]
    saba = [0, 1.5, 3, 4, 6, 8, 10]

    # 12 note scales
    chromatic = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
