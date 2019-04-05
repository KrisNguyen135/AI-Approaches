class Game:
    checkpoints = [0, 3, 6]
    valids = list(range(1, 10))

    def __init__(self, input_='input/easy.txt', auto=None):
        self.input_ = input_
        self.auto = auto

        with open(self.input_, 'r') as f:
            lines = f.readlines()

        self.board = []
        for line in lines:
            self.board.append(list(map(int, list(line[:-1]))))

        self.in_prog = True

    def __str__(self):
        result = ''

        for i, row in enumerate(self.board):
            if i in Game.checkpoints:
                result += '+-------+-------+-------+\n'
            for j, cell in enumerate(row):
                if j in Game.checkpoints:
                    result += '| '
                result += str(self.board[i][j]) + ' '
            result += '|\n'
        result += '+-------+-------+-------+\n'

        return result

    def update(self, row, col, x):
        if self.in_prog and self.board[row][col] == 0:
            temp_row = self.board[row]
            temp_col = [self.board[i][col] for i in range(9)]
            temp_block = [self.board[row // 3 * 3 + i][col // 3 * 3 + j]
                          for i in range(3) for j in range(3)]

            if x in temp_row or x in temp_col or x in temp_block:
                return False

            if x in Game.valids:
                self.board[row][col] = x
                if self.check_complete():
                    self.in_prog = False

        return False

    def check_complete(self):
        for row in self.board:
            if 0 in row:
                return False

        return True
