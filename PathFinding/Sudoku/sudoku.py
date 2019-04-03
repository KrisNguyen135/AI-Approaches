class Game:
    def __init__(self, input_='input/easy.txt', auto=None):
        self.input_ = input_
        self.auto = auto

        with open(self.input_, 'r') as f:
            lines = f.readlines()

        self.board = []
        for line in lines:
            self.board.append(list(map(int, list(line))))

        print(self.board)
