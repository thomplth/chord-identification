from music21 import converter, stream
import pickle


# I was trying to just inherit music21.stream.base, but
# 1) even stream.base is a module i.e. cannot be extended like class
# 2) I have no idea how to write the parsing result of converter as the object itself
class Piece:
    """
    Piece class represents music piece
    Build on top of music21.stream and generalises some of its functionality

    :param string name: Name of the music piece, without file extension
    :param Stream score: music21 Stream object of the music piece
    """

    def __init__(self, name):
        name = name.split('.')
        self.name = name[0]
        self.score = converter.parse('../data/score/' + self.name + '.mxl')
        # self.len = self.score.duration.quarterLength

    # Not sure if we should use int here, alternatively refer self.len
    def __len__(self):
        return int(self.score.duration.quarterLength)

    def __iter__(self):
        return stream.iterator.StreamIterator(self.score)

    def get_chord_seg_target(self):
        input_path = '../data/data_answer' + '/' + self.name + '.pydata'
        with open(input_path, 'rb') as f:
            return pickle.load(f)

    def get_key_signatures(self):
        keysigs = []
        for item in self.score:
            try:
                if item[1].keySignature:
                    keysigs.append(item[1].keySignature)
            except (IndexError, TypeError):
                pass
        return keysigs

    def write(self, path='../result/'):
        path += self.name + '.mxl'
        self.score.write('mxl', fp=path)

    def show(self):
        self.score.show()


if __name__ == '__main__':
    p = Piece('Twinkle-Twinkle')
    # print(len(p))
    # print(p.len)
    # p.write()
    print(p.get_key_signatures())
