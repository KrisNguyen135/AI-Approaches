import turtle
from freegames import line

import random
import time


class Game:
    coordinates = [-200.0, -67.0, 66.0]

    def __init__(self, player_first=True, auto=None, show=True):
        self.state = {'player': 0}
        if player_first:
            self.players = [self.drawx, self.drawo]
        else:
            self.players = [self.drawo, self.drawx]
        self.player_turn = player_first

        self.board = [[None for _ in range(3)] for __ in range(3)]
        self.in_prog = False

        self.auto = auto
        self.show = show

    def drawx(self, x, y):
        """Draw X player."""
        coordinate_x = Game.coordinates.index(x)
        coordinate_y = Game.coordinates.index(y)

        if self.board[coordinate_x][coordinate_y] is None:
            if self.show:
                line(x, y, x + 133, y + 133)
                line(x, y + 133, x + 133, y)
            self.board[coordinate_x][coordinate_y] = 'X'
            return True

        return False

    def drawo(self, x, y):
        """Draw O player."""
        coordinate_x = Game.coordinates.index(x)
        coordinate_y = Game.coordinates.index(y)

        if self.board[coordinate_x][coordinate_y] is None:
            if self.show:
                turtle.up()
                turtle.goto(x + 67, y + 5)
                turtle.down()
                turtle.circle(62)
            self.board[coordinate_x][coordinate_y] = 'O'
            return True

        return False

    def check(self):
        # Check for a winner
        rows = [row for row in self.board]
        cols = [[row[i] for row in self.board] for i in range(3)]
        diagonals = [
            [self.board[0][0], self.board[1][1], self.board[2][2]],
            [self.board[0][2], self.board[1][1], self.board[2][0]]
        ]

        for item1, item2, item3 in rows + cols + diagonals:
            if item1 == item2 == item3 and item1 is not None:
                return 1 if item1 == 'X' else -1

        for row in self.board:
            if None in row:
                return False

        return True

    def make_move(self):
        opens = [(i, j) for i in range(3) for j in range(3)
                 if self.board[i][j] is None]

        move = random.choice(opens)
        return move

    def tap(self, x, y):
        """Draw X or O in tapped square."""
        if self.in_prog:
            x = self.floor(x)
            y = self.floor(y)
            player = self.state['player']
            draw = self.players[player]
            draw_result = draw(x, y)
            if self.show:
                turtle.update()

            if draw_result:
                self.state['player'] = not player
                self.player_turn = not self.player_turn

            if self.check():
                self.in_prog = False
            elif not self.player_turn:
                self.auto_update()

    def auto_update(self):
        if self.in_prog:
            time.sleep(0.05)

            if self.player_turn:
                move = self.auto(self.board)
                if self.show:
                    print(f'Player: {move}')
            else:
                move = self.make_move()
                if self.show:
                    print(f'Computer: {move}')

            x = Game.coordinates[move[0]]
            y = Game.coordinates[move[1]]
            self.tap(x, y)

    def run(self):
        self.in_prog = True
        if self.show:
            turtle.setup(420, 420, 370, 0)
            turtle.hideturtle()
            turtle.tracer(False)
            self.grid()
            turtle.update()
            turtle.onscreenclick(self.tap)

        if self.auto is not None:
            while self.in_prog:
                self.auto_update()

        '''finished = self.check()
        while not finished:
            if self.show:
                time.sleep(0.1)

            finished = self.check()'''

        if self.show:
            turtle.done()
            try:
                turtle.bye()
            except turtle.Terminator:
                pass

        return self.check()

    @staticmethod
    def grid():
        """Draw tic-tac-toe grid."""
        line(-67, 200, -67, -200)
        line(67, 200, 67, -200)
        line(-200, -67, 200, -67)
        line(-200, 67, 200, 67)

    @staticmethod
    def floor(value):
        """Round value down to grid with square size 133."""
        return ((value + 200) // 133) * 133 - 200
