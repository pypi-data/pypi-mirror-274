from .note import Note, PitchClass
from .scales import Scales


class Scale:
    def __init__(self, root: PitchClass, scale: list[int] = Scales.chromatic) -> None:
        self.root = root
        self.scale = scale

    def __map(self, degree: int, octave: int) -> Note:
        octave += degree // len(self.scale)
        degree = degree % len(self.scale)
        note = Note(self.root, octave).transpose(self.scale[degree])
        return note

    def bind(self, degrees: list[int], octave: int = 0) -> list[int]:
        ret = []
        for degree in degrees:
            if degree is None:
                # rest note
                ret.append(None)
            elif not isinstance(degree, list):
                # single note
                ret.append(self.__map(degree=degree, octave=octave).midi_number)
            else:
                # chord
                ret.append(self.bind(degrees=degree, octave=octave))
        return ret
