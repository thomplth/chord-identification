from music21 import converter
import pickle


class Piece:
    def __init__(self, name):
        self.name = name
        self.score = converter.parse('../data/score/' + name + '.mxl')

    def get_duration(self):
        return self.score.duration

    def get_cSeg_target(self):
        input_path = '../data/data_answer' + '/' + self.name + '.pydata'
        with open(input_path, 'rb') as f:
            return pickle.load(f)

    def show(self):
        self.score.show()


if __name__ == '__main__':
    p = Piece('Twinkle-Twinkle')
    print(p.get_cSeg_target())
