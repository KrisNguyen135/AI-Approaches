import random#; random.seed(0.png)
from tkinter import Tk, Canvas
import platform


class Game:
    class MainWindow:
        def __init__(self, game):
            self.grid_size = 600
            self.cell_size = 40
            self.half_cell = self.cell_size // 2
            self.tiles = self.grid_size // self.cell_size
            self.buffer_height = self.cell_size
            self.WIDTH = self.grid_size
            self.HEIGHT = self.grid_size + self.buffer_height
            self.button_dim = [self.cell_size * 3, self.cell_size // 2]
            self.master = Tk()
            self.canvas = Canvas(self.master,
                                 width=self.WIDTH, height=self.HEIGHT)
            self.count = 0

            self.canvas.bind('<Button-1>', game.callback_left)
            if platform.system() == 'Darwin':
                self.canvas.bind('<Button-2>', game.callback_right)  # OSX
            else:
                self.canvas.bind('<Button-3>', game.callback_right)  # Windows

            self.game = game

        def counter(self):
            """
            This function is called within the event timer. It updates the
            counter, and draws it on the canvas.
            """
            if self.game.gamestate.game_in_prog is False:
                pass
            else:
                self.count += 1

            self.canvas.create_rectangle(250, 0, 350, 40, fill="grey")
            self.canvas.create_text(300, 20, text=str(self.count))

        def event_timer(self):
            """
            This block of code executes once per second.
            """
            self.counter()
            self.canvas.after(1000, self.event_timer)

        def create_buttons(self):
            """
            Generates grid at the beginning of the game
            """
            self.canvas.create_rectangle(
                0, 0, self.button_dim[0], self.button_dim[1], fill="green")
            self.canvas.create_text(
                self.button_dim[0]//2, self.button_dim[1]//2, text="New game")

        def end_graphic(self, cell):
            """
            This code is executed when player selects mine. The locations of
            the mines are displayed to the player with "X"'s in red boxes.
            """
            placement = cell.placement
            self.canvas.create_rectangle(placement[0] * self.cell_size,
                                         placement[1] * self.cell_size,
                                         placement[0] * self.cell_size + self.cell_size,
                                         placement[1] * self.cell_size + self.cell_size,
                                         fill="red")

            self.canvas.create_text(placement[0] * self.cell_size + self.half_cell,
                                    placement[1] * self.cell_size + self.half_cell,
                                    text="X", fill="black")

        def number_graphic(self, cell):
            placement = cell.placement
            mine_count = cell.mine_count
            self.canvas.create_text(placement[0] * self.cell_size + self.half_cell,
                                    placement[1] * self.cell_size + self.half_cell,
                                    text=mine_count, fill="black")

            return mine_count  # to update self.game.board

        def flag_graphic(self, cell):
            placement = cell.placement
            self.canvas.create_text(placement[0] * self.cell_size + self.half_cell,
                                    placement[1] * self.cell_size + self.half_cell,
                                    text="FLAG", fill="black")

        def grey_graphic(self, cell):
            placement = cell.placement
            self.canvas.create_rectangle(placement[0] * self.cell_size,
                                         placement[1] * self.cell_size,
                                         placement[0] * self.cell_size + self.cell_size,
                                         placement[1] * self.cell_size + self.cell_size,
                                         fill="grey")

        def green_graphic(self, cell):
            placement = cell.placement
            self.canvas.create_rectangle(placement[0] * self.cell_size,
                                         placement[1] * self.cell_size,
                                         placement[0] * self.cell_size + self.cell_size,
                                         placement[1] * self.cell_size + self.cell_size,
                                         fill="green")


    class Cell:
        def __init__(self, placement, game):
            self.placement = placement
            self.name = ''
            self.mine_count = 0
            self.adjacent_cells = []
            self.is_mine = False
            self.letters = {
                0: 'A', 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H",
                8: "I", 9: "J", 10: "K", 11: "L", 12: "M", 13: "N", 14: "O",
                15: "P"
            }

            self.game = game

        def find_adjacent_cell(self):
            """
            Takes mouse click cell as input, returns all adjacent cells to self.
            The a1 variable series (a1, a2, etc) represents all adjacent cells.
            """
            self.adjacent_cells = []
            up = -1                                                           #_________________
            down = 1                                                          # a1 |  a2  | a3 |
            left = -1                                                         # a4 | self | a5 |
            right = 1                                                         # a6 |  a7  | a8 |
            same = 0                                                          #=================
            a1 = [self.placement[0] + left, self.placement[1] + up]           # upper left
            a2 = [self.placement[0] + same, self.placement[1] + up]           # upper
            a3 = [self.placement[0] + right, self.placement[1] + up]          # upper right
            a4 = [self.placement[0] + left, self.placement[1] + same]         # left
            a5 = [self.placement[0] + right, self.placement[1] + same]        # right
            a6 = [self.placement[0] + left, self.placement[1] + down]         # lower left
            a7 = [self.placement[0] + same, self.placement[1] + down]         # lower
            a8 = [self.placement[0] + right, self.placement[1] + down]        # lower right
            a_series = [a1, a2, a3, a4, a5, a6, a7, a8]
            for item in a_series:
                if 15 > item[0] >= 0 and 16 > item[1] >= 1:                   #screening out coord not in grid
                    name = self.game.find_name(item)
                    self.adjacent_cells.append(
                        self.game.gamestate.cell_dict[name])
            return self.adjacent_cells

        def mine_probability(self):
            # TODO: change randrange to change mine probability
            a = random.randrange(7)
            if a == 0:
                self.is_mine = True

        def find_adjacent_mines(self):
            for adjacent_cell in self.adjacent_cells:
                if adjacent_cell in self.game.gamestate.mines:
                    self.mine_count += 1

        def create_name(self):
            a = self.letters[self.placement[0]]
            b = self.placement[1]
            self.name = a + str(b)

        def start(self):
            self.create_name()
            self.game.window.grey_graphic(self)

        def select_cell(self):
            self.find_adjacent_cell()
            self.find_adjacent_mines()
            self.game.gamestate.selected_cells.append(self)
            mine_count = self.game.window.number_graphic(self)
            if self.game.auto is not None:
                self.game.board[self.placement[0]][self.placement[1] - 1] \
                    = mine_count
            if self.is_mine:
                self.game.gamestate.trip_mine()


    class GameState:
        def __init__(self, game):
            self.mine_quantity = 35
            self.game_in_prog = True
            self.mines = []
            self.flags = []
            self.selected_tiles = []
            self.cells = []
            self.cell_dict = {}

            self.game = game

        def create_mines(self):
            """
            Randomly generates mines at the beginning of the game.
            """
            for cell in self.cells:
                cell.mine_probability()

        def trip_mine(self):
            """
            Executes if player selects mine
            """
            self.game_in_prog = False
            self.show_mines()

        def show_mines(self):
            """
            This function is called at game over. It visually shows the player
            where the mines are located on the canvas
            """
            for mine in self.mines:
                self.game.window.end_graphic(mine)

        def new_game(self):
            """
            This function re-initializes game state
            """
            self.game.window.count = 0  # in-game counter
            self.game_in_prog = True
            self.flags = []
            self.selected_cells = []
            self.cells = []
            self.mines = []
            self.cell_dict = {}
            self.create_cells()
            self.start_cells()
            self.create_cell_dict()
            self.create_mines()
            self.find_all_mines()
            self.game.window.create_buttons()
            self.find_all_mines()

        def create_cells(self):
            for i in range(self.game.window.tiles):
                for j in range(self.game.window.tiles):
                    placement = [i, j + 1]
                    a_cell = Game.Cell(placement, self.game)
                    self.cells.append(a_cell)

        def create_cell_dict(self):
            for cell in self.cells:
                self.cell_dict[cell.name] = cell

        def start_cells(self):
            for cell in self.cells:
                cell.start()

        def find_all_mines(self):
            for cell in self.cells:
                if cell.is_mine:
                    self.mines.append(cell)


    def __init__(self, auto=None):
        # Objects
        self.window = Game.MainWindow(self)
        self.gamestate = Game.GameState(self)
        self.a_cell = Game.Cell([1, 1], self)

        self.auto = auto
        if self.auto is not None:
            self.board = [['' for _ in range(15)] for __ in range(15)]

    def find_name(self,placement):
        a = self.a_cell.letters[placement[0]]
        b = placement[1]
        name = a + str(b)
        return name


    def detect_button(self, coordinates):
        """
        Determines if player hit "New Game" button, if so start new game
        """
        if coordinates[0] < self.window.button_dim[0] \
                and coordinates[1] < self.window.button_dim[1]:
            self.gamestate.new_game()

    def find_placement(self, coordinates):
        """
        Converts input from mouse measured in pixels --> cell in canvas grid.
        """
        cell_conversion = [0, 0]
        cell_conversion[0] = coordinates[0] // self.window.cell_size
        cell_conversion[1] = coordinates[1] // self.window.cell_size
        return cell_conversion

    def callback_left(self, event):
        """
        Handler for left mouse clicks. This block of code executes every time
        left mouse click event occurs.
        """
        coord = [event.x, event.y]
        self.detect_button(coord)
        if coord[1] < self.window.buffer_height:
            return None
        if self.gamestate.game_in_prog is False:
            return None

        placement = self.find_placement(coord)
        name = self.find_name(placement)
        cell = self.gamestate.cell_dict[name]
        if cell in self.gamestate.selected_cells:
            return None

        cell.select_cell()

    def callback_right(self, event):
        """
        Handler for right mouse clicks. This block of code executes every time
        right mouse click event occurs.
        """
        coord = [event.x, event.y]
        placement = self.find_placement(coord)
        name = self.find_name(placement)
        cell = self.gamestate.cell_dict[name]

        if cell not in self.gamestate.flags:
            self.window.flag_graphic(cell)
            self.gamestate.flags.append(cell)
        else:
            self.window.grey_graphic(cell)
            self.gamestate.flags.remove(cell)

    def auto_solve(self):
        if self.gamestate.game_in_prog:
            to_flag, to_open = self.auto(self.board)

            '''print(to_flag)
            print(to_open)
            print('*' * 40)'''

            for col, row in to_flag:
                self.board[col][row] = 'FLAGGED'

                placement = [col, row + 1]
                name = self.find_name(placement)
                cell = self.gamestate.cell_dict[name]

                if cell not in self.gamestate.flags:
                    self.window.flag_graphic(cell)

            for col, row in to_open:
                placement = [col, row + 1]
                name = self.find_name(placement)
                cell = self.gamestate.cell_dict[name]
                #self.window.grey_graphic(cell)
                if cell not in self.gamestate.selected_cells:
                    cell.select_cell()

            self.window.master.after(1, self.auto_solve)

    def run(self):
        self.gamestate.new_game()
        self.window.event_timer()
        self.window.canvas.pack()
        if self.auto is not None:
            self.window.master.after(1, self.auto_solve)
        self.window.master.mainloop()


if __name__ == '__main__':
    game = Game(auto=1)
    game.run()
